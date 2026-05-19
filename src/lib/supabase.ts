import { createClient } from "@supabase/supabase-js";

const url = "https://snjkmikrlkyalvjaadia.supabase.co";
const key = "sb_publishable_koLey6P5yenCno24IUCJQw_Z95gwsL0";

export const supabase = createClient(url, key, {
  auth: { persistSession: true, autoRefreshToken: true },
});

export type Booking = {
  id: string;
  order_id: number;
  customer_name: string | null;
  email: string | null;
  phone: string | null;
  address: string | null;
  city: string | null;
  postcode: string | null;
  event_start_date: string | null;
  event_end_date: string | null;
  delivery_type: "bezorgen" | "ophalen" | "dhl" | null;
  booking_status: "processing" | "completed" | "cancelled" | "refunded" | "new" | "packed" | null;
  packing_date: string | null;
  is_problem: boolean | null;
  is_spoed: boolean | null;
  problem_note: string | null;
  product_summary: string | null;
  updated_at: string | null;
};

export type BookingItem = {
  id: string;
  order_id: number;
  product_id: string | null;
  product_name: string;
  quantity: number;
  event_start_date: string | null;
  event_end_date: string | null;
  delivery_type: string | null;
};

export type Product = {
  id: string;
  product_id: string;
  name: string;
  sku: string | null;
  barcode: string | null;
  category: string | null;
  stock_total: number;
  stock_available: number;
};

export type Customer = {
  id: string;
  email: string | null;
  name: string | null;
  phone: string | null;
  address: string | null;
  postcode: string | null;
  city: string | null;
  country: string | null;
  woo_customer_id: number | null;
  first_seen_at: string;
  last_seen_at: string | null;
  total_orders: number;
  total_revenue_cents: number;
  notes_count: number;
  created_at: string;
  updated_at: string;
};

export type CustomerNote = {
  id: string;
  customer_id: string;
  author: string | null;
  body: string;
  pinned: boolean;
  created_at: string;
};

export type CustomerTag = {
  id: string;
  customer_id: string;
  tag: string;
  color: string | null;
  created_at: string;
};

export type ProductStat = {
  product_key: string;
  product_name: string;
  rental_count: number;
  units_rented: number;
  revenue_cents: number;
  last_rented_at: string | null;
};

export type AuditLog = {
  id: number;
  actor: string | null;
  entity_type: string;
  entity_id: string;
  action: string;
  meta: Record<string, unknown> | null;
  created_at: string;
};
