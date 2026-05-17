import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState, useMemo } from "react";
import { Page, Card, CardHeader, Loader, Badge, EmptyState } from "@/components/dashboard/Page";
import { supabase, type Booking, type BookingItem } from "@/lib/supabase";
import { accessoriesFor, deliveryTypeLabel } from "@/lib/business";
import { format, parseISO, addDays, startOfWeek } from "date-fns";
import { nl } from "date-fns/locale";
import { X } from "lucide-react";

export const Route = createFileRoute("/inpakken")({ component: Inpakken });

function Inpakken() {
  const [tab, setTab] = useState<"kalender" | "lijst">("kalender");
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [items, setItems] = useState<BookingItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Booking | null>(null);

  useEffect(() => {
    (async () => {
      const [b, i] = await Promise.all([
        supabase.from("bookings").select("*"),
        supabase.from("booking_items").select("*"),
      ]);
      setBookings((b.data ?? []) as Booking[]);
      setItems((i.data ?? []) as BookingItem[]);
      setLoading(false);
    })();
  }, []);

  const weekStart = startOfWeek(new Date(), { weekStartsOn: 1 });
  const days = Array.from({ length: 28 }, (_, i) => addDays(weekStart, i));

  const byDay = useMemo(() => {
    const m: Record<string, Booking[]> = {};
    bookings.forEach((b) => {
      if (!b.packing_date) return;
      (m[b.packing_date] ??= []).push(b);
    });
    return m;
  }, [bookings]);

  const selectedItems = selected ? items.filter((i) => i.order_id === selected.order_id) : [];

  if (loading) return <Page><Loader /></Page>;

  return (
    <Page>
      <div className="flex gap-2 mb-4">
        {(["kalender","lijst"] as const).map((t) => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm rounded-md font-medium ${tab === t ? "bg-primary text-primary-foreground" : "bg-card border border-border"}`}>
            {t === "kalender" ? "Kalender (4 weken)" : "Lijstweergave"}
          </button>
        ))}
      </div>

      {tab === "kalender" ? (
        <Card>
          <div className="grid grid-cols-7 border-b border-border bg-muted/30">
            {["Ma","Di","Wo","Do","Vr","Za","Zo"].map((d) => (
              <div key={d} className="px-3 py-2 text-xs font-semibold text-muted-foreground text-center">{d}</div>
            ))}
          </div>
          <div className="grid grid-cols-7">
            {days.map((d) => {
              const key = format(d, "yyyy-MM-dd");
              const list = byDay[key] ?? [];
              const isToday = key === format(new Date(), "yyyy-MM-dd");
              return (
                <div key={key} className={`min-h-[120px] p-2 border-b border-r border-border ${isToday ? "bg-primary/5" : ""}`}>
                  <div className={`text-xs font-mono mb-1.5 ${isToday ? "text-primary font-bold" : "text-muted-foreground"}`}>{format(d, "d MMM", { locale: nl })}</div>
                  <div className="space-y-1">
                    {list.map((b) => {
                      const tone = b.delivery_type === "dhl" ? "bg-[color:var(--warning)]/15 text-[color:var(--warning)]" :
                                   b.delivery_type === "bezorgen" ? "bg-[color:var(--warning)]/25 text-[color:var(--warning)]" :
                                   "bg-[color:var(--success)]/15 text-[color:var(--success)]";
                      return (
                        <button key={b.id} onClick={() => setSelected(b)}
                          className={`block w-full text-left text-[11px] px-2 py-1 rounded ${tone} truncate hover:opacity-80`}>
                          #{b.order_id} {b.customer_name}
                        </button>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </Card>
      ) : (
        <Card>
          <CardHeader title="Te pakken boekingen" subtitle="Gesorteerd op inpakdatum" />
          <div className="divide-y divide-border">
            {bookings.filter((b) => b.packing_date).sort((a,b) => (a.packing_date ?? "").localeCompare(b.packing_date ?? "")).map((b) => (
              <button key={b.id} onClick={() => setSelected(b)} className="w-full px-5 py-3 flex items-center gap-4 hover:bg-muted/30 text-left">
                <div className="font-mono text-xs w-20">{b.packing_date ? format(parseISO(b.packing_date), "d MMM", { locale: nl }) : "—"}</div>
                <div className="font-mono text-xs text-muted-foreground w-16">#{b.order_id}</div>
                <div className="flex-1 text-sm font-medium">{b.customer_name}</div>
                <Badge tone={b.delivery_type === "dhl" ? "warning" : "info"}>{deliveryTypeLabel(b.delivery_type)}</Badge>
              </button>
            ))}
          </div>
        </Card>
      )}

      {selected && (
        <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4" onClick={() => setSelected(null)}>
          <div className="bg-card rounded-xl w-full max-w-2xl max-h-[85vh] overflow-auto" onClick={(e) => e.stopPropagation()}>
            <div className="px-6 py-4 border-b border-border flex items-center justify-between">
              <div>
                <h3 className="font-display font-bold text-lg">Paklijst #{selected.order_id}</h3>
                <p className="text-sm text-muted-foreground">{selected.customer_name} · {selected.city}</p>
              </div>
              <button onClick={() => setSelected(null)} className="p-2 rounded hover:bg-muted"><X className="w-4 h-4" /></button>
            </div>
            <div className="p-6">
              <div className="text-xs text-muted-foreground mb-2">Evenement: {selected.event_start_date && format(parseISO(selected.event_start_date), "EEEE d MMMM yyyy", { locale: nl })}</div>
              <div className="space-y-2">
                {selectedItems.length === 0 ? <EmptyState title="Geen items gekoppeld" /> : selectedItems.map((item) => (
                  <div key={item.id}>
                    <div className="flex items-center gap-3 p-3 bg-muted rounded-lg">
                      <input type="checkbox" className="w-4 h-4" />
                      <div className="font-mono text-xs text-muted-foreground w-10">{item.quantity}x</div>
                      <div className="flex-1 font-medium">{item.product_name}</div>
                    </div>
                    {accessoriesFor(item.product_name).map((acc, j) => (
                      <div key={j} className={`ml-10 mt-1 flex items-center gap-3 p-2 rounded text-sm ${acc.type === "manual" ? "bg-[color:var(--success)]/10 text-[color:var(--success)]" : "bg-[color:var(--warning)]/10 text-[color:var(--warning)]"}`}>
                        <input type="checkbox" className="w-3.5 h-3.5" />
                        <span>+ {acc.name}</span>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </Page>
  );
}
