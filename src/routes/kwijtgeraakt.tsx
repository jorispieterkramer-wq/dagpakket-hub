import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { Page, Card, EmptyState } from "@/components/dashboard/Page";
import { Plus, Check } from "lucide-react";

export const Route = createFileRoute("/kwijtgeraakt")({ component: Kwijt });

type Lost = { id: string; product: string; order: string; date: string; note: string; found: boolean };
const KEY = "dpv-lost";

function Kwijt() {
  const [list, setList] = useState<Lost[]>([]);
  const [d, setD] = useState<Lost>({ id: "", product: "", order: "", date: new Date().toISOString().slice(0,10), note: "", found: false });
  useEffect(() => { try { setList(JSON.parse(localStorage.getItem(KEY) ?? "[]")); } catch {} }, []);
  useEffect(() => { localStorage.setItem(KEY, JSON.stringify(list)); }, [list]);
  const add = () => { if (!d.product) return; setList((l) => [{ ...d, id: crypto.randomUUID() }, ...l]); setD({ id: "", product: "", order: "", date: new Date().toISOString().slice(0,10), note: "", found: false }); };

  return (
    <Page>
      <Card>
        <div className="p-5 grid grid-cols-1 md:grid-cols-5 gap-2 border-b border-border bg-muted/30">
          <input placeholder="Product" value={d.product} onChange={(e) => setD({ ...d, product: e.target.value })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm" />
          <input placeholder="Order #" value={d.order} onChange={(e) => setD({ ...d, order: e.target.value })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm font-mono" />
          <input type="date" value={d.date} onChange={(e) => setD({ ...d, date: e.target.value })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm" />
          <input placeholder="Notitie" value={d.note} onChange={(e) => setD({ ...d, note: e.target.value })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm" />
          <button onClick={add} className="px-3 py-1.5 bg-primary text-primary-foreground rounded-md text-sm inline-flex items-center justify-center gap-1.5"><Plus className="w-4 h-4" /> Melden</button>
        </div>
        {list.length === 0 ? <EmptyState title="Geen kwijtgeraakte items" /> : (
          <div className="divide-y divide-border">
            {list.map((l) => (
              <div key={l.id} className={`px-5 py-3 flex items-center gap-3 ${l.found ? "opacity-50" : ""}`}>
                <div className="flex-1">
                  <div className={`font-medium ${l.found ? "line-through" : ""}`}>{l.product}</div>
                  <div className="text-xs text-muted-foreground">#{l.order} · {l.date} · {l.note}</div>
                </div>
                {!l.found && <button onClick={() => setList((ls) => ls.map((x) => x.id === l.id ? { ...x, found: true } : x))} className="px-3 py-1.5 text-sm bg-[color:var(--success)] text-white rounded-md inline-flex items-center gap-1.5"><Check className="w-4 h-4" /> Gevonden</button>}
              </div>
            ))}
          </div>
        )}
      </Card>
    </Page>
  );
}
