-- =====================================================================
-- DagPakketVerhuur — Fase 1: CRM + audit log + product stats
-- Run dit in de Supabase SQL editor van project snjkmikrlkyalvjaadia
-- Alles is idempotent (IF NOT EXISTS) — herhaaldelijk runnen is veilig.
-- =====================================================================

-- 1) Enum voor rollen (admin / magazijn / chauffeur / finance)
do $$ begin
  if not exists (select 1 from pg_type where typname = 'app_role') then
    create type public.app_role as enum ('admin', 'magazijn', 'chauffeur', 'finance');
  end if;
end $$;

-- 2) user_roles tabel (NOOIT rol op profiles/users zetten — security)
create table if not exists public.user_roles (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  role public.app_role not null,
  created_at timestamptz not null default now(),
  unique (user_id, role)
);
alter table public.user_roles enable row level security;

-- security definer helper om recursie in RLS te voorkomen
create or replace function public.has_role(_user_id uuid, _role public.app_role)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.user_roles
    where user_id = _user_id and role = _role
  )
$$;

drop policy if exists "user_roles_select_own_or_admin" on public.user_roles;
create policy "user_roles_select_own_or_admin" on public.user_roles
  for select to authenticated
  using (auth.uid() = user_id or public.has_role(auth.uid(), 'admin'));

drop policy if exists "user_roles_admin_write" on public.user_roles;
create policy "user_roles_admin_write" on public.user_roles
  for all to authenticated
  using (public.has_role(auth.uid(), 'admin'))
  with check (public.has_role(auth.uid(), 'admin'));

-- 3) customers tabel — eigen master, los van bookings
create table if not exists public.customers (
  id uuid primary key default gen_random_uuid(),
  email text unique,
  name text,
  phone text,
  address text,
  postcode text,
  city text,
  country text default 'NL',
  woo_customer_id bigint,
  first_seen_at timestamptz not null default now(),
  last_seen_at timestamptz,
  total_orders int not null default 0,
  total_revenue_cents bigint not null default 0,
  notes_count int not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_customers_email on public.customers (lower(email));
create index if not exists idx_customers_woo on public.customers (woo_customer_id);

alter table public.customers enable row level security;
drop policy if exists "customers_authenticated_all" on public.customers;
create policy "customers_authenticated_all" on public.customers
  for all to authenticated using (true) with check (true);

-- 4) customer_notes — vrije notities per klant
create table if not exists public.customer_notes (
  id uuid primary key default gen_random_uuid(),
  customer_id uuid not null references public.customers(id) on delete cascade,
  author text,
  body text not null,
  pinned boolean not null default false,
  created_at timestamptz not null default now()
);
create index if not exists idx_customer_notes_customer on public.customer_notes (customer_id, created_at desc);
alter table public.customer_notes enable row level security;
drop policy if exists "customer_notes_authenticated_all" on public.customer_notes;
create policy "customer_notes_authenticated_all" on public.customer_notes
  for all to authenticated using (true) with check (true);

-- 5) customer_tags — losse labels (VIP, school, herhaling, no-show, ...)
create table if not exists public.customer_tags (
  id uuid primary key default gen_random_uuid(),
  customer_id uuid not null references public.customers(id) on delete cascade,
  tag text not null,
  color text default '#567c8d',
  created_at timestamptz not null default now(),
  unique (customer_id, tag)
);
create index if not exists idx_customer_tags_customer on public.customer_tags (customer_id);
alter table public.customer_tags enable row level security;
drop policy if exists "customer_tags_authenticated_all" on public.customer_tags;
create policy "customer_tags_authenticated_all" on public.customer_tags
  for all to authenticated using (true) with check (true);

-- 6) audit_log — generieke log van wijzigingen
create table if not exists public.audit_log (
  id bigserial primary key,
  actor text,                 -- email of "system"
  entity_type text not null,  -- bookings / customers / payments / ...
  entity_id text not null,    -- pk als text
  action text not null,       -- create / update / delete / status_change / ...
  meta jsonb,
  created_at timestamptz not null default now()
);
create index if not exists idx_audit_log_entity on public.audit_log (entity_type, entity_id, created_at desc);
create index if not exists idx_audit_log_created on public.audit_log (created_at desc);
alter table public.audit_log enable row level security;
drop policy if exists "audit_log_authenticated_read" on public.audit_log;
create policy "audit_log_authenticated_read" on public.audit_log
  for select to authenticated using (true);
drop policy if exists "audit_log_authenticated_insert" on public.audit_log;
create policy "audit_log_authenticated_insert" on public.audit_log
  for insert to authenticated with check (true);

-- 7) product_stats — view die per product totaal aantal verhuurd + omzet aggregeert
--    Werkt op bestaande booking_items + bookings. Omzet wordt geschat op basis
--    van line_total_cents als die kolom bestaat, anders 0.
do $$
declare
  has_line_total boolean;
begin
  select exists (
    select 1 from information_schema.columns
    where table_schema = 'public' and table_name = 'booking_items'
      and column_name = 'line_total_cents'
  ) into has_line_total;

  execute 'drop view if exists public.product_stats cascade';

  if has_line_total then
    execute $v$
      create view public.product_stats as
      select
        coalesce(bi.product_id, bi.product_name) as product_key,
        bi.product_name,
        count(distinct bi.order_id)              as rental_count,
        coalesce(sum(bi.quantity), 0)            as units_rented,
        coalesce(sum(bi.line_total_cents), 0)    as revenue_cents,
        max(bi.event_start_date)                 as last_rented_at
      from public.booking_items bi
      left join public.bookings b on b.order_id = bi.order_id
      where coalesce(b.booking_status, 'processing') not in ('cancelled', 'refunded')
      group by 1, 2
    $v$;
  else
    execute $v$
      create view public.product_stats as
      select
        coalesce(bi.product_id, bi.product_name) as product_key,
        bi.product_name,
        count(distinct bi.order_id)              as rental_count,
        coalesce(sum(bi.quantity), 0)            as units_rented,
        0::bigint                                as revenue_cents,
        max(bi.event_start_date)                 as last_rented_at
      from public.booking_items bi
      left join public.bookings b on b.order_id = bi.order_id
      where coalesce(b.booking_status, 'processing') not in ('cancelled', 'refunded')
      group by 1, 2
    $v$;
  end if;
end $$;

grant select on public.product_stats to authenticated, anon;

-- 8) Trigger: keep customers.updated_at fresh
create or replace function public.touch_updated_at()
returns trigger language plpgsql as $$
begin new.updated_at = now(); return new; end $$;

drop trigger if exists trg_customers_touch on public.customers;
create trigger trg_customers_touch before update on public.customers
for each row execute function public.touch_updated_at();

-- 9) Backfill customers vanuit bestaande bookings (1x veilig te draaien)
insert into public.customers (email, name, phone, address, postcode, city, first_seen_at, last_seen_at, total_orders)
select
  lower(b.email),
  max(b.customer_name),
  max(b.phone),
  max(b.address),
  max(b.postcode),
  max(b.city),
  min(coalesce(b.event_start_date::timestamptz, now())),
  max(coalesce(b.event_start_date::timestamptz, now())),
  count(*)
from public.bookings b
where b.email is not null and b.email <> ''
group by lower(b.email)
on conflict (email) do update
  set name = excluded.name,
      phone = excluded.phone,
      address = excluded.address,
      postcode = excluded.postcode,
      city = excluded.city,
      last_seen_at = greatest(public.customers.last_seen_at, excluded.last_seen_at),
      total_orders = excluded.total_orders;

-- Done.