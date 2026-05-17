import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { Page, Card, EmptyState } from "@/components/dashboard/Page";
import { Plus, Trash2 } from "lucide-react";

export const Route = createFileRoute("/voertuigen")({ component: Voertuigen });
type V = { id: string; name: string; plate: string; type: string };
const KEY = "dpv-vehicles";

function Voertuigen() {
  const [list, setList] = useState<V[]>([]);
  const [draft, setDraft] = useState<V>({ id: "", name: "", plate: "", type: "Bus" });
  useEffect(() => { try { setList(JSON.parse(localStorage.getItem(KEY) ?? "[]")); } catch {} }, []);
  useEffect(() => { localStorage.setItem(KEY, JSON.stringify(list)); }, [list]);
  const add = () => { if (!draft.name) return; setList((l) => [...l, { ...draft, id: crypto.randomUUID() }]); setDraft({ id: "", name: "", plate: "", type: "Bus" }); };

  return (
    <Page>
      <Card>
        <div className="p-5 grid grid-cols-1 md:grid-cols-4 gap-2 border-b border-border bg-muted/30">
          <input placeholder="Naam" value={draft.name} onChange={(e) => setDraft({ ...draft, name: e.target.value })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm" />
          <input placeholder="Kenteken" value={draft.plate} onChange={(e) => setDraft({ ...draft, plate: e.target.value })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm font-mono uppercase" />
          <input placeholder="Type" value={draft.type} onChange={(e) => setDraft({ ...draft, type: e.target.value })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm" />
          <button onClick={add} className="px-3 py-1.5 bg-primary text-primary-foreground rounded-md text-sm inline-flex items-center justify-center gap-1.5"><Plus className="w-4 h-4" /> Toevoegen</button>
        </div>
        {list.length === 0 ? <EmptyState title="Nog geen voertuigen" /> : (
          <table className="w-full text-sm">
            <thead className="bg-muted/50 text-xs uppercase text-muted-foreground"><tr><th className="text-left px-5 py-3">Naam</th><th className="text-left px-5 py-3">Kenteken</th><th className="text-left px-5 py-3">Type</th><th /></tr></thead>
            <tbody className="divide-y divide-border">{list.map((v) => (
              <tr key={v.id}><td className="px-5 py-3 font-medium">{v.name}</td><td className="px-5 py-3 font-mono">{v.plate}</td><td className="px-5 py-3">{v.type}</td><td className="px-5 py-3"><button onClick={() => setList((ls) => ls.filter((x) => x.id !== v.id))}><Trash2 className="w-4 h-4 text-muted-foreground" /></button></td></tr>
            ))}</tbody>
          </table>
        )}
      </Card>
    </Page>
  );
}
