import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { Page, Card, EmptyState, Badge } from "@/components/dashboard/Page";
import { Plus, Trash2 } from "lucide-react";

export const Route = createFileRoute("/taken")({ component: Taken });

type Task = { id: string; title: string; priority: "urgent" | "hoog" | "normaal" | "laag"; deadline: string; assignee: string; done: boolean };
const KEY = "dpv-tasks";

function Taken() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [show, setShow] = useState(false);
  const [draft, setDraft] = useState<Task>({ id: "", title: "", priority: "normaal", deadline: "", assignee: "", done: false });

  useEffect(() => { try { setTasks(JSON.parse(localStorage.getItem(KEY) ?? "[]")); } catch {} }, []);
  useEffect(() => { localStorage.setItem(KEY, JSON.stringify(tasks)); }, [tasks]);

  const add = () => {
    if (!draft.title) return;
    setTasks((t) => [...t, { ...draft, id: crypto.randomUUID() }]);
    setDraft({ id: "", title: "", priority: "normaal", deadline: "", assignee: "", done: false });
    setShow(false);
  };

  const prioOrder = { urgent: 0, hoog: 1, normaal: 2, laag: 3 };
  const sorted = [...tasks].sort((a, b) => prioOrder[a.priority] - prioOrder[b.priority] || a.deadline.localeCompare(b.deadline));
  const tone = (p: Task["priority"]) => p === "urgent" ? "danger" : p === "hoog" ? "warning" : p === "normaal" ? "success" : "muted";

  return (
    <Page>
      <Card>
        <div className="px-5 py-4 border-b border-border flex items-center justify-between">
          <h2 className="font-display font-bold">Taken</h2>
          <button onClick={() => setShow(!show)} className="px-3 py-1.5 bg-primary text-primary-foreground rounded-md text-sm inline-flex items-center gap-1.5">
            <Plus className="w-4 h-4" /> Nieuwe taak
          </button>
        </div>
        {show && (
          <div className="p-5 bg-muted/30 border-b border-border grid grid-cols-2 md:grid-cols-5 gap-2">
            <input placeholder="Titel" value={draft.title} onChange={(e) => setDraft({ ...draft, title: e.target.value })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm md:col-span-2" />
            <select value={draft.priority} onChange={(e) => setDraft({ ...draft, priority: e.target.value as Task["priority"] })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm">
              <option value="urgent">Urgent</option><option value="hoog">Hoog</option><option value="normaal">Normaal</option><option value="laag">Laag</option>
            </select>
            <input type="date" value={draft.deadline} onChange={(e) => setDraft({ ...draft, deadline: e.target.value })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm" />
            <input placeholder="Medewerker" value={draft.assignee} onChange={(e) => setDraft({ ...draft, assignee: e.target.value })} className="px-3 py-1.5 bg-card border border-border rounded-md text-sm" />
            <button onClick={add} className="md:col-span-5 px-3 py-1.5 bg-primary text-primary-foreground rounded-md text-sm">Toevoegen</button>
          </div>
        )}
        {sorted.length === 0 ? <EmptyState title="Geen taken" hint="Maak je eerste taak aan." /> : (
          <div className="divide-y divide-border">
            {sorted.map((t) => (
              <div key={t.id} className={`px-5 py-3 flex items-center gap-3 ${t.done ? "opacity-50" : ""}`}>
                <input type="checkbox" checked={t.done} onChange={(e) => setTasks((ts) => ts.map((x) => x.id === t.id ? { ...x, done: e.target.checked } : x))} className="w-4 h-4" />
                <Badge tone={tone(t.priority)}>{t.priority}</Badge>
                <div className={`flex-1 ${t.done ? "line-through" : ""}`}>{t.title}</div>
                <div className="text-xs text-muted-foreground font-mono">{t.deadline}</div>
                <div className="text-xs text-muted-foreground">{t.assignee}</div>
                <button onClick={() => setTasks((ts) => ts.filter((x) => x.id !== t.id))} className="p-1 hover:bg-muted rounded">
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
