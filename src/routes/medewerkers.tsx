import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { Page, Card, EmptyState } from "@/components/dashboard/Page";
import { Plus, Trash2 } from "lucide-react";

export const Route = createFileRoute("/medewerkers")({ component: Medewerkers });

type Emp = { id: string; name: string; role: "inpakker" | "bezorger" | "beide" | "beheerder"; phone: string; email: string };
const KEY = "dpv-employees";

function Medewerkers() {
  const [list, setList] = useState<Emp[]>([]);
  const [draft, setDraft] = useState<Emp>({ id: "", name: "", role: "inpakker", phone: "", email: "" });

  useEffect(() => { try { setList(JSON.parse(localStorage.getItem(KEY) ?? "[]")); } catch {} }, []);
  useEffect(() => { localStorage.setItem(KEY, JSON.stringify(list)); }, [list]);

  const add = () => { if (!draft.name) return; setList((l) => [...l, { ...draft, id: crypto.randomUUID() }]); setDraft({ id: "", name: "", role: "inpakker", phone: "", email: "" }); };

  return (
    <Page>
      <Card>
        <div className="p-5 grid grid-cols-1 md:grid-cols-5 gap-2 border-b border-border bg-muted/30">
          <input placeholder="Naam" value={draft.name} onChange={(e) => setDraft({ ...draft, name: e.target.value })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm" />
          <select value={draft.role} onChange={(e) => setDraft({ ...draft, role: e.target.value as Emp["role"] })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm">
            <option value="inpakker">Inpakker</option><option value="bezorger">Bezorger</option><option value="beide">Beide</option><option value="beheerder">Beheerder</option>
          </select>
          <input placeholder="Telefoon" value={draft.phone} onChange={(e) => setDraft({ ...draft, phone: e.target.value })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm" />
          <input placeholder="Email" value={draft.email} onChange={(e) => setDraft({ ...draft, email: e.target.value })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm" />
          <button onClick={add} className="px-3 py-1.5 bg-primary text-primary-foreground rounded-md text-sm inline-flex items-center justify-center gap-1.5"><Plus className="w-4 h-4" /> Toevoegen</button>
        </div>
        {list.length === 0 ? <EmptyState title="Nog geen medewerkers" /> : (
          <table className="w-full text-sm">
            <thead className="bg-muted/50 text-xs uppercase text-muted-foreground">
              <tr><th className="text-left px-5 py-3">Naam</th><th className="text-left px-5 py-3">Rol</th><th className="text-left px-5 py-3">Telefoon</th><th className="text-left px-5 py-3">Email</th><th /></tr>
            </thead>
            <tbody className="divide-y divide-border">
              {list.map((e) => (
                <tr key={e.id}><td className="px-5 py-3 font-medium">{e.name}</td><td className="px-5 py-3 capitalize">{e.role}</td><td className="px-5 py-3 font-mono text-xs">{e.phone}</td><td className="px-5 py-3 text-muted-foreground">{e.email}</td><td className="px-5 py-3"><button onClick={() => setList((ls) => ls.filter((x) => x.id !== e.id))}><Trash2 className="w-4 h-4 text-muted-foreground" /></button></td></tr>
              ))}
            </tbody>
          </table>
        )}
      </Card>
    </Page>
  );
}
