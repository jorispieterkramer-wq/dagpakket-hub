import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { supabase, type Booking, type BookingItem } from "@/lib/supabase";
import { format, parseISO, startOfWeek, endOfWeek } from "date-fns";
import { nl } from "date-fns/locale";
import { deliveryTypeLabel } from "@/lib/business";

export const Route = createFileRoute("/tv")({ component: TV });

function TV() {
  const [now, setNow] = useState(new Date());
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [items, setItems] = useState<BookingItem[]>([]);

  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  useEffect(() => {
    const load = async () => {
      const [b, i] = await Promise.all([
        supabase.from("bookings").select("*"),
        supabase.from("booking_items").select("*"),
      ]);
      setBookings((b.data ?? []) as Booking[]);
      setItems((i.data ?? []) as BookingItem[]);
    };
    load();
    const t = setInterval(load, 60000);
    return () => clearInterval(t);
  }, []);

  const today = format(now, "yyyy-MM-dd");
  const weekStart = startOfWeek(now, { weekStartsOn: 1 });
  const weekEnd = endOfWeek(now, { weekStartsOn: 1 });
  const bookingsWeek = bookings.filter((b) => b.event_start_date && parseISO(b.event_start_date) >= weekStart && parseISO(b.event_start_date) <= weekEnd).length;
  const packToday = bookings.filter((b) => b.packing_date === today);
  const spoed = bookings.filter((b) => b.is_spoed).length;
  const problems = bookings.filter((b) => b.is_problem).length;

  return (
    <div className="min-h-screen bg-[#0a0e1a] text-white p-8">
      <div className="flex items-baseline justify-between mb-8">
        <div>
          <div className="font-mono text-7xl font-bold tracking-tight">{format(now, "HH:mm:ss")}</div>
          <div className="text-xl text-white/60 capitalize mt-1">{format(now, "EEEE d MMMM yyyy", { locale: nl })}</div>
        </div>
        <div className="font-display font-bold text-2xl">DagPakketVerhuur</div>
      </div>
      <div className="grid grid-cols-4 gap-6 mb-8">
        {[
          { label: "Boekingen week", value: bookingsWeek, color: "from-blue-500 to-blue-700" },
          { label: "Inpakken vandaag", value: packToday.length, color: "from-orange-500 to-orange-700" },
          { label: "Spoedorders", value: spoed, color: "from-red-500 to-red-700" },
          { label: "Problemen", value: problems, color: "from-amber-500 to-amber-700" },
        ].map((k) => (
          <div key={k.label} className={`bg-gradient-to-br ${k.color} rounded-2xl p-6`}>
            <div className="text-sm uppercase tracking-wider opacity-80">{k.label}</div>
            <div className="font-display font-bold text-7xl mt-2">{k.value}</div>
          </div>
        ))}
      </div>
      <div className="bg-white/5 rounded-2xl p-6">
        <div className="text-2xl font-display font-bold mb-4">Vandaag inpakken</div>
        <div className="space-y-2 max-h-[40vh] overflow-y-auto scrollbar-thin">
          {packToday.length === 0 ? <div className="text-white/40">Geen inpakwerk vandaag</div> : packToday.map((b) => {
            const its = items.filter((i) => i.order_id === b.order_id);
            return (
              <div key={b.id} className="flex items-center gap-4 bg-white/5 rounded-xl px-4 py-3">
                <div className="font-mono text-lg w-20 text-white/60">#{b.order_id}</div>
                <div className="flex-1">
                  <div className="text-xl font-bold">{b.customer_name}</div>
                  <div className="text-sm text-white/60 truncate">{its.map((i) => `${i.quantity}x ${i.product_name}`).join(" · ") || b.product_summary}</div>
                </div>
                <div className={`px-3 py-1 rounded-md text-sm font-bold uppercase ${b.delivery_type === "dhl" ? "bg-yellow-500/20 text-yellow-300" : b.delivery_type === "bezorgen" ? "bg-orange-500/20 text-orange-300" : "bg-green-500/20 text-green-300"}`}>
                  {deliveryTypeLabel(b.delivery_type)}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
