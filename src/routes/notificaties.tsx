import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Page, Card, Loader, EmptyState, Badge } from "@/components/dashboard/Page";
import { supabase, type Booking } from "@/lib/supabase";
import { AlertTriangle, Zap, BellRing } from "lucide-react";
import { format, parseISO } from "date-fns";
import { nl } from "date-fns/locale";

export const Route = createFileRoute("/notificaties")({ component: Notificaties });

function Notificaties() {
  const [items, setItems] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [read, setRead] = useState<Set<string>>(new Set());

  useEffect(() => {
    (async () => {
      const { data } = await supabase.from("bookings").select("*").or("is_problem.eq.true,is_spoed.eq.true").order("updated_at", { ascending: false });
      setItems((data ?? []) as Booking[]);
      setLoading(false);
    })();
  }, []);

  return (
    <Page>
      <Card>
        <div className="px-5 py-4 border-b border-border flex items-center gap-3">
          <BellRing className="w-4 h-4" />
          <h2 className="font-display font-bold">Live notificaties</h2>
          <Badge tone="danger">{items.length - read.size} ongelezen</Badge>
          <button onClick={() => setRead(new Set(items.map((i) => i.id)))} className="ml-auto text-sm text-muted-foreground hover:text-foreground">
            Markeer alles gelezen
          </button>
        </div>
        {loading ? <Loader /> : items.length === 0 ? <EmptyState title="Alles rustig" hint="Geen openstaande problemen of spoedorders." /> : (
          <div className="divide-y divide-border">
            {items.map((b) => {
              const isRead = read.has(b.id);
              return (
                <div key={b.id} className={`px-5 py-3 flex items-center gap-3 ${!isRead ? "bg-primary/5" : ""}`} onClick={() => setRead((r) => new Set(r).add(b.id))}>
                  {b.is_problem ? <AlertTriangle className="w-4 h-4 text-destructive" /> : <Zap className="w-4 h-4 text-[color:var(--warning)]" />}
                  <div className="flex-1">
                    <div className="text-sm font-medium">{b.is_problem ? "Probleem" : "Spoedorder"} — #{b.order_id} {b.customer_name}</div>
                    <div className="text-xs text-muted-foreground">{b.problem_note ?? (b.event_start_date && format(parseISO(b.event_start_date), "EEEE d MMM", { locale: nl }))}</div>
                  </div>
                  {!isRead && <span className="w-2 h-2 rounded-full bg-primary" />}
                </div>
              );
            })}
          </div>
        )}
      </Card>
    </Page>
  );
}
