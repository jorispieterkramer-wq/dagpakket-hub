import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Page, Card, Loader, EmptyState, Badge } from "@/components/dashboard/Page";
import { supabase, type Booking } from "@/lib/supabase";
import { format, parseISO } from "date-fns";
import { nl } from "date-fns/locale";
import { AlertTriangle, Zap, Check } from "lucide-react";

export const Route = createFileRoute("/problemen")({ component: Problemen });

function Problemen() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);
  async function load() {
    setLoading(true);
    const { data } = await supabase.from("bookings").select("*").or("is_problem.eq.true,is_spoed.eq.true").order("event_start_date");
    setBookings((data ?? []) as Booking[]);
    setLoading(false);
  }

  const problems = bookings.filter((b) => b.is_problem);
  const spoed = bookings.filter((b) => !b.is_problem && b.is_spoed);

  async function resolve(id: string) {
    await supabase.from("bookings").update({ is_problem: false, problem_note: null }).eq("id", id);
    load();
  }

  return (
    <Page>
      {loading ? <Loader /> : (
        <div className="space-y-6">
          <Card>
            <div className="px-5 py-4 border-b border-border flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-destructive" />
              <h2 className="font-display font-bold">Problemen ({problems.length})</h2>
            </div>
            {problems.length === 0 ? <EmptyState title="Geen actieve problemen" hint="Alles loopt zoals het hoort." /> : (
              <div className="divide-y divide-border">
                {problems.map((b) => (
                  <div key={b.id} className="px-5 py-4 bg-destructive/5">
                    <div className="flex items-start gap-4">
                      <div className="flex-1">
                        <div className="font-medium">#{b.order_id} · {b.customer_name}</div>
                        <div className="text-xs text-muted-foreground mb-2">{b.event_start_date && format(parseISO(b.event_start_date), "EEEE d MMMM", { locale: nl })}</div>
                        <div className="text-sm bg-card border border-border rounded-md p-3">{b.problem_note ?? "Geen notitie"}</div>
                      </div>
                      <button onClick={() => resolve(b.id)} className="px-3 py-1.5 text-sm bg-[color:var(--success)] text-white rounded-md inline-flex items-center gap-1.5">
                        <Check className="w-4 h-4" /> Opgelost
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          <Card>
            <div className="px-5 py-4 border-b border-border flex items-center gap-2">
              <Zap className="w-4 h-4 text-[color:var(--warning)]" />
              <h2 className="font-display font-bold">Spoedorders ({spoed.length})</h2>
            </div>
            {spoed.length === 0 ? <EmptyState title="Geen spoedorders" /> : (
              <div className="divide-y divide-border">
                {spoed.map((b) => (
                  <div key={b.id} className="px-5 py-3 bg-[color:var(--warning)]/5 flex items-center gap-3">
                    <Badge tone="warning">SPOED</Badge>
                    <div className="font-mono text-xs">#{b.order_id}</div>
                    <div className="flex-1 font-medium">{b.customer_name}</div>
                    <div className="text-xs font-mono">{b.event_start_date && format(parseISO(b.event_start_date), "d MMM", { locale: nl })}</div>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>
      )}
    </Page>
  );
}
