import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState, useMemo } from "react";
import { Page, Card, CardHeader, EmptyState, Loader, Badge } from "@/components/dashboard/Page";
import { supabase, type Booking } from "@/lib/supabase";
import { deliveryTypeLabel, statusLabel } from "@/lib/business";
import { format, parseISO, startOfWeek, endOfWeek, startOfMonth, endOfMonth } from "date-fns";
import { nl } from "date-fns/locale";
import { AlertTriangle, Zap } from "lucide-react";

export const Route = createFileRoute("/boekingen")({ component: Boekingen });

function Boekingen() {
  const [loading, setLoading] = useState(true);
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [period, setPeriod] = useState<"dag" | "week" | "maand" | "alles">("week");
  const [search, setSearch] = useState("");

  useEffect(() => {
    (async () => {
      const { data } = await supabase.from("bookings").select("*").order("event_start_date", { ascending: true });
      setBookings((data ?? []) as Booking[]);
      setLoading(false);
    })();
  }, []);

  const filtered = useMemo(() => {
    const today = new Date();
    let from: Date | null = null, to: Date | null = null;
    if (period === "dag") { from = today; to = today; }
    else if (period === "week") { from = startOfWeek(today, { weekStartsOn: 1 }); to = endOfWeek(today, { weekStartsOn: 1 }); }
    else if (period === "maand") { from = startOfMonth(today); to = endOfMonth(today); }
    return bookings.filter((b) => {
      if (search && !`${b.customer_name ?? ""} ${b.order_id}`.toLowerCase().includes(search.toLowerCase())) return false;
      if (!from || !to) return true;
      if (!b.event_start_date) return false;
      const d = parseISO(b.event_start_date);
      return d >= from && d <= to;
    });
  }, [bookings, period, search]);

  return (
    <Page>
      <Card>
        <div className="px-5 py-4 border-b border-border flex flex-wrap items-center gap-3">
          <div className="flex bg-muted rounded-md p-1">
            {(["dag","week","maand","alles"] as const).map((p) => (
              <button key={p} onClick={() => setPeriod(p)}
                className={`px-3 py-1 text-xs font-medium rounded ${period === p ? "bg-card shadow-sm" : "text-muted-foreground"}`}>
                {p.charAt(0).toUpperCase() + p.slice(1)}
              </button>
            ))}
          </div>
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Zoek op klant of order#"
            className="flex-1 max-w-xs px-3 py-1.5 text-sm bg-muted rounded-md outline-none focus:ring-2 focus:ring-ring"
          />
          <div className="ml-auto text-xs text-muted-foreground">{filtered.length} boekingen</div>
        </div>
        {loading ? <Loader /> : filtered.length === 0 ? <EmptyState title="Geen boekingen in deze periode" /> : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-muted/50 text-xs uppercase text-muted-foreground">
                <tr>
                  <th className="text-left px-5 py-3 font-medium">Order #</th>
                  <th className="text-left px-5 py-3 font-medium">Klant</th>
                  <th className="text-left px-5 py-3 font-medium">Stad</th>
                  <th className="text-left px-5 py-3 font-medium">Evenement</th>
                  <th className="text-left px-5 py-3 font-medium">Bezorging</th>
                  <th className="text-left px-5 py-3 font-medium">Status</th>
                  <th className="text-left px-5 py-3 font-medium">Flags</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {filtered.map((b) => (
                  <tr key={b.id} className="hover:bg-muted/30 transition-colors">
                    <td className="px-5 py-3 font-mono text-xs">#{b.order_id}</td>
                    <td className="px-5 py-3 font-medium">{b.customer_name ?? "—"}</td>
                    <td className="px-5 py-3 text-muted-foreground">{b.city ?? "—"}</td>
                    <td className="px-5 py-3 font-mono text-xs">{b.event_start_date ? format(parseISO(b.event_start_date), "EEE d MMM", { locale: nl }) : "—"}</td>
                    <td className="px-5 py-3"><Badge tone={b.delivery_type === "dhl" ? "warning" : b.delivery_type === "bezorgen" ? "info" : "success"}>{deliveryTypeLabel(b.delivery_type)}</Badge></td>
                    <td className="px-5 py-3"><Badge tone={b.booking_status === "completed" ? "success" : b.booking_status === "cancelled" ? "danger" : "default"}>{statusLabel(b.booking_status)}</Badge></td>
                    <td className="px-5 py-3 flex gap-1.5">
                      {b.is_spoed && <span title="Spoed" className="text-destructive"><Zap className="w-4 h-4" /></span>}
                      {b.is_problem && <span title="Probleem" className="text-[color:var(--warning)]"><AlertTriangle className="w-4 h-4" /></span>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </Page>
  );
}
