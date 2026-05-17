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
