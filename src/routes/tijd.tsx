import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect, useRef } from "react";
import { Page, Card, EmptyState } from "@/components/dashboard/Page";
import { Play, Square, Trash2 } from "lucide-react";

export const Route = createFileRoute("/tijd")({ component: TijdRoute });

type Entry = { id: string; label: string; order: string; start: number; end: number };
const KEY = "dpv-time";

function TijdRoute() {
  const [entries, setEntries] = useState<Entry[]>([]);
  const [label, setLabel] = useState("");
  const [order, setOrder] = useState("");
  const [running, setRunning] = useState<{ start: number; label: string; order: string } | null>(null);
  const [tick, setTick] = useState(0);
  const ref = useRef<number | null>(null);

  useEffect(() => { try { setEntries(JSON.parse(localStorage.getItem(KEY) ?? "[]")); } catch {} }, []);
  useEffect(() => { localStorage.setItem(KEY, JSON.stringify(entries)); }, [entries]);
  useEffect(() => {
    if (running) { ref.current = window.setInterval(() => setTick((t) => t + 1), 1000); }
    return () => { if (ref.current) clearInterval(ref.current); };
  }, [running]);

  const start = () => { if (!label) return; setRunning({ start: Date.now(), label, order }); };
  const stop = () => {
    if (!running) return;
    setEntries((e) => [{ id: crypto.randomUUID(), label: running.label, order: running.order, start: running.start, end: Date.now() }, ...e]);
    setRunning(null); setLabel(""); setOrder("");
  };

  const today = new Date().toDateString();
  const todays = entries.filter((e) => new Date(e.start).toDateString() === today);
  const totalMs = todays.reduce((s, e) => s + (e.end - e.start), 0);
  const fmt = (ms: number) => {
    const h = Math.floor(ms / 3.6e6); const m = Math.floor((ms % 3.6e6) / 6e4); const s = Math.floor((ms % 6e4) / 1000);
    return `${h.toString().padStart(2,"0")}:${m.toString().padStart(2,"0")}:${s.toString().padStart(2,"0")}`;
  };

  return (
    <Page>
      <Card className="mb-4">
        <div className="p-6 text-center">
          <div className="font-mono text-6xl font-bold text-primary">{running ? fmt(Date.now() - running.start) : "00:00:00"}</div>
          <div className="text-xs text-muted-foreground mt-1">{running ? running.label : "Geen timer actief"}</div>
          <div className="flex justify-center gap-2 mt-4 max-w-md mx-auto">
            <input value={label} onChange={(e) => setLabel(e.target.value)} placeholder="Activiteit" disabled={!!running} className="flex-1 px-3 py-2 bg-muted rounded-md text-sm" />
            <input value={order} onChange={(e) => setOrder(e.target.value)} placeholder="Order #" disabled={!!running} className="w-24 px-3 py-2 bg-muted rounded-md text-sm font-mono" />
            {!running ? (
              <button onClick={start} className="px-4 py-2 bg-[color:var(--success)] text-white rounded-md inline-flex items-center gap-1.5"><Play className="w-4 h-4" /> Start</button>
            ) : (
              <button onClick={stop} className="px-4 py-2 bg-destructive text-destructive-foreground rounded-md inline-flex items-center gap-1.5"><Square className="w-4 h-4" /> Stop</button>
            )}
          </div>
        </div>
      </Card>
      <Card>
        <div className="px-5 py-4 border-b border-border flex items-center justify-between">
          <h2 className="font-display font-bold">Vandaag</h2>
          <div className="text-sm">Totaal: <span className="font-mono font-bold text-primary">{fmt(totalMs)}</span></div>
        </div>
        {todays.length === 0 ? <EmptyState title="Nog geen tijdsregistratie vandaag" /> : (
          <div className="divide-y divide-border">
            {todays.map((e) => (
              <div key={e.id} className="px-5 py-3 flex items-center gap-3">
                <div className="font-mono text-sm w-24">{fmt(e.end - e.start)}</div>
                <div className="flex-1">{e.label}</div>
                <div className="text-xs text-muted-foreground font-mono">{e.order ? `#${e.order}` : ""}</div>
                <button onClick={() => setEntries((es) => es.filter((x) => x.id !== e.id))} className="p-1 hover:bg-muted rounded">
                  <Trash2 className="w-4 h-4 text-muted-foreground" />
                </button>
              </div>
            ))}
          </div>
        )}
      </Card>
    </Page>
  );
}
