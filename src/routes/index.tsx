import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Page, Card, CardHeader, EmptyState, Loader, Badge } from "@/components/dashboard/Page";
import { supabase, type Booking } from "@/lib/supabase";
import { deliveryTypeLabel, statusLabel } from "@/lib/business";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { format, parseISO, startOfWeek, endOfWeek, startOfYear } from "date-fns";
import { nl } from "date-fns/locale";

export const Route = createFileRoute("/")({ component: Dashboard });

const MONTHS = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"];

function Kpi({ label, value, tone, pulse }: { label: string; value: number | string; tone: "primary" | "warning" | "danger"; pulse?: boolean }) {
  const tones = {
    primary: "before:bg-primary",
    warning: "before:bg-[color:var(--warning)]",
    danger: "before:bg-destructive",
  } as const;
  return (
    <div className={`relative bg-card border border-border rounded-xl p-5 overflow-hidden before:absolute before:top-0 before:left-0 before:right-0 before:h-[3px] ${tones[tone]} ${pulse ? "animate-soft-pulse" : ""}`}>
      <div className="text-xs text-muted-foreground uppercase tracking-wider font-medium">{label}</div>
      <div className="font-display font-bold text-[44px] leading-tight mt-2">{value}</div>
    </div>
  );
}

function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [recent, setRecent] = useState<Booking[]>([]);

  useEffect(() => {
    (async () => {
      try {
        const yearStart = format(startOfYear(new Date()), "yyyy-MM-dd");
        const [all, rec] = await Promise.all([
          supabase.from("bookings").select("*").gte("event_start_date", yearStart),
          supabase.from("bookings").select("*").order("updated_at", { ascending: false }).limit(10),
        ]);
        setBookings((all.data ?? []) as Booking[]);
        setRecent((rec.data ?? []) as Booking[]);
      } finally { setLoading(false); }
    })();
  }, []);

  const today = new Date();
  const weekStart = startOfWeek(today, { weekStartsOn: 1 });
  const weekEnd = endOfWeek(today, { weekStartsOn: 1 });

  const bookingsThisWeek = bookings.filter((b) => {
    if (!b.event_start_date) return false;
    const d = parseISO(b.event_start_date);
    return d >= weekStart && d <= weekEnd;
  }).length;

  const packToday = bookings.filter((b) => b.packing_date === format(today, "yyyy-MM-dd")).length;
  const spoed = bookings.filter((b) => b.is_spoed).length;
  const problems = bookings.filter((b) => b.is_problem).length;

  const byMonth = new Array(12).fill(0);
  bookings.forEach((b) => {
    if (!b.event_start_date) return;
    const m = parseISO(b.event_start_date).getMonth();
    byMonth[m]++;
  });
  const chartData = MONTHS.map((m, i) => ({ month: m, value: byMonth[i] }));
  const currentMonth = today.getMonth();

  return (
    <Page>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <Kpi label="Boekingen deze week" value={bookingsThisWeek} tone="primary" />
        <Kpi label="Inpakken vandaag" value={packToday} tone="warning" />
        <Kpi label="Spoedorders" value={spoed} tone="danger" pulse={spoed > 0} />
        <Kpi label="Actieve problemen" value={problems} tone="danger" pulse={problems > 0} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <Card className="lg:col-span-2">
          <CardHeader title="Boekingen per maand" subtitle={`${today.getFullYear()}`} />
          <div className="p-5 h-[280px]">
            {loading ? <Loader /> : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" vertical={false} />
                  <XAxis dataKey="month" stroke="var(--color-muted-foreground)" fontSize={11} tickLine={false} axisLine={false} />
                  <YAxis stroke="var(--color-muted-foreground)" fontSize={11} tickLine={false} axisLine={false} />
                  <Tooltip contentStyle={{ background: "var(--color-card)", border: "1px solid var(--color-border)", borderRadius: 8, fontSize: 12 }} />
                  <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                    {chartData.map((_, i) => (
                      <Cell key={i} fill={i === currentMonth ? "var(--color-primary)" : "var(--color-border)"} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </Card>

        <Card>
          <CardHeader title="Recente boekingen" subtitle="Laatst bijgewerkt" />
          <div className="divide-y divide-border">
            {loading ? <Loader /> : recent.length === 0 ? <EmptyState title="Nog geen boekingen" hint="Boekingen verschijnen hier zodra ze in Supabase staan." /> : recent.slice(0, 8).map((b) => (
              <div key={b.id} className="px-5 py-3 flex items-center gap-3">
                <div className="font-mono text-xs text-muted-foreground w-12 shrink-0">#{b.order_id}</div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium truncate">{b.customer_name ?? "—"}</div>
                  <div className="text-xs text-muted-foreground">{b.event_start_date ? format(parseISO(b.event_start_date), "d MMM", { locale: nl }) : "—"}</div>
                </div>
                <Badge tone={b.booking_status === "completed" ? "success" : b.booking_status === "cancelled" ? "danger" : "info"}>{statusLabel(b.booking_status)}</Badge>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </Page>
  );
}
