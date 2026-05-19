import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Page, Card, CardHeader, Loader, EmptyState } from "@/components/dashboard/Page";
import {
  supabase,
  type Customer,
  type CustomerNote,
  type CustomerTag,
  type Booking,
} from "@/lib/supabase";
import { fmtEUR, logAction } from "@/lib/audit";
import { format, parseISO } from "date-fns";
import { nl } from "date-fns/locale";
import { ArrowLeft, Pin, Trash2, Plus } from "lucide-react";

export const Route = createFileRoute("/klanten/$id")({ component: CustomerDetail });

function CustomerDetail() {
  const { id } = Route.useParams();
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [notes, setNotes] = useState<CustomerNote[]>([]);
  const [tags, setTags] = useState<CustomerTag[]>([]);
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [newNote, setNewNote] = useState("");
  const [newTag, setNewTag] = useState("");

  const reload = async () => {
    const { data: c } = await supabase.from("customers").select("*").eq("id", id).single();
    if (!c) {
      setLoading(false);
      return;
    }
    setCustomer(c as Customer);
    const [n, t, b] = await Promise.all([
      supabase.from("customer_notes").select("*").eq("customer_id", id).order("pinned", { ascending: false }).order("created_at", { ascending: false }),
      supabase.from("customer_tags").select("*").eq("customer_id", id),
      c.email
        ? supabase.from("bookings").select("*").ilike("email", c.email).order("event_start_date", { ascending: false })
        : Promise.resolve({ data: [] as Booking[] }),
    ]);
    setNotes((n.data ?? []) as CustomerNote[]);
    setTags((t.data ?? []) as CustomerTag[]);
    setBookings((b.data ?? []) as Booking[]);
    setLoading(false);
  };

  useEffect(() => { reload(); }, [id]);

  const addNote = async () => {
    const body = newNote.trim();
    if (!body) return;
    const { data, error } = await supabase.from("customer_notes").insert({ customer_id: id, body }).select().single();
    if (!error && data) {
      setNotes([data as CustomerNote, ...notes]);
      setNewNote("");
      logAction({ entity_type: "customers", entity_id: id, action: "note_added", meta: { note_id: data.id } });
    }
  };

  const togglePin = async (n: CustomerNote) => {
    await supabase.from("customer_notes").update({ pinned: !n.pinned }).eq("id", n.id);
    reload();
  };
  const deleteNote = async (n: CustomerNote) => {
    await supabase.from("customer_notes").delete().eq("id", n.id);
    setNotes(notes.filter((x) => x.id !== n.id));
    logAction({ entity_type: "customers", entity_id: id, action: "note_deleted" });
  };

  const addTag = async () => {
    const tag = newTag.trim();
    if (!tag) return;
    const { data, error } = await supabase.from("customer_tags").insert({ customer_id: id, tag }).select().single();
    if (!error && data) {
      setTags([...tags, data as CustomerTag]);
      setNewTag("");
    }
  };
  const removeTag = async (t: CustomerTag) => {
    await supabase.from("customer_tags").delete().eq("id", t.id);
    setTags(tags.filter((x) => x.id !== t.id));
  };

  if (loading) return <Page><Loader /></Page>;
  if (!customer) return <Page><EmptyState title="Klant niet gevonden" /></Page>;

  return (
    <Page>
      <Link to="/klanten" className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground mb-4">
        <ArrowLeft className="size-4" /> Alle klanten
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Linkerkolom — info */}
        <div className="lg:col-span-1 space-y-4">
          <Card>
            <div className="p-5">
              <h1 className="font-display text-2xl font-bold">{customer.name || "—"}</h1>
              <div className="text-sm text-muted-foreground mt-1">{customer.email || "—"}</div>
              <dl className="mt-4 space-y-2 text-sm">
                <div className="flex justify-between"><dt className="text-muted-foreground">Telefoon</dt><dd className="font-mono">{customer.phone || "—"}</dd></div>
                <div className="flex justify-between"><dt className="text-muted-foreground">Adres</dt><dd className="text-right">{customer.address || "—"}</dd></div>
                <div className="flex justify-between"><dt className="text-muted-foreground">Plaats</dt><dd>{customer.postcode} {customer.city}</dd></div>
                <div className="flex justify-between"><dt className="text-muted-foreground">Eerste boeking</dt><dd className="font-mono text-xs">{format(parseISO(customer.first_seen_at), "d MMM yyyy", { locale: nl })}</dd></div>
              </dl>
              <div className="grid grid-cols-2 gap-3 mt-5 pt-5 border-t border-border">
                <div>
                  <div className="text-xs uppercase text-muted-foreground">Orders</div>
                  <div className="font-display text-3xl font-bold">{customer.total_orders}</div>
                </div>
                <div>
                  <div className="text-xs uppercase text-muted-foreground">Omzet</div>
                  <div className="font-display text-3xl font-bold">{fmtEUR(customer.total_revenue_cents)}</div>
                </div>
              </div>
            </div>
          </Card>

          <Card>
            <CardHeader title="Tags" />
            <div className="p-5">
              <div className="flex flex-wrap gap-2 mb-3">
                {tags.length === 0 && <span className="text-xs text-muted-foreground">Nog geen tags</span>}
                {tags.map((t) => (
                  <span key={t.id} className="inline-flex items-center gap-1 px-2 py-1 rounded-md text-xs font-medium" style={{ background: `${t.color}20`, color: t.color ?? undefined }}>
                    {t.tag}
                    <button onClick={() => removeTag(t)} className="opacity-60 hover:opacity-100">×</button>
                  </span>
                ))}
              </div>
              <div className="flex gap-2">
                <input value={newTag} onChange={(e) => setNewTag(e.target.value)} onKeyDown={(e) => e.key === "Enter" && addTag()} placeholder="Nieuwe tag…" className="flex-1 px-2 py-1.5 text-xs bg-muted rounded-md outline-none" />
                <button onClick={addTag} className="px-2 py-1.5 bg-primary text-primary-foreground rounded-md text-xs"><Plus className="size-3.5" /></button>
              </div>
            </div>
          </Card>
        </div>

        {/* Rechterkolom — notities + boekingen */}
        <div className="lg:col-span-2 space-y-4">
          <Card>
            <CardHeader title={`Notities (${notes.length})`} />
            <div className="p-5 space-y-3">
              <div className="flex gap-2">
                <textarea value={newNote} onChange={(e) => setNewNote(e.target.value)} placeholder="Notitie toevoegen…" rows={2} className="flex-1 px-3 py-2 text-sm bg-muted rounded-md outline-none focus:ring-2 focus:ring-ring resize-none" />
                <button onClick={addNote} className="px-3 py-2 bg-primary text-primary-foreground rounded-md text-sm self-start">Voeg toe</button>
              </div>
              {notes.length === 0 ? <div className="text-sm text-muted-foreground text-center py-4">Nog geen notities</div> : (
                <div className="space-y-2">
                  {notes.map((n) => (
                    <div key={n.id} className={`p-3 rounded-md border ${n.pinned ? "border-accent bg-accent/5" : "border-border"}`}>
                      <div className="flex items-start gap-2">
                        <div className="flex-1 text-sm whitespace-pre-wrap">{n.body}</div>
                        <button onClick={() => togglePin(n)} className={`p-1 rounded ${n.pinned ? "text-accent" : "text-muted-foreground hover:text-foreground"}`}><Pin className="size-3.5" /></button>
                        <button onClick={() => deleteNote(n)} className="p-1 rounded text-muted-foreground hover:text-destructive"><Trash2 className="size-3.5" /></button>
                      </div>
                      <div className="text-xs text-muted-foreground mt-1 font-mono">{format(parseISO(n.created_at), "d MMM yyyy HH:mm", { locale: nl })}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </Card>

          <Card>
            <CardHeader title={`Boekingen (${bookings.length})`} />
            {bookings.length === 0 ? <EmptyState title="Geen boekingen gevonden" /> : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-muted/50 text-xs uppercase text-muted-foreground">
                    <tr>
                      <th className="text-left px-5 py-2.5 font-medium">Order</th>
                      <th className="text-left px-5 py-2.5 font-medium">Datum</th>
                      <th className="text-left px-5 py-2.5 font-medium">Bezorging</th>
                      <th className="text-left px-5 py-2.5 font-medium">Status</th>
                      <th className="text-left px-5 py-2.5 font-medium">Producten</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border">
                    {bookings.map((b) => (
                      <tr key={b.id} className="hover:bg-muted/30">
                        <td className="px-5 py-2.5 font-mono text-xs">#{b.order_id}</td>
                        <td className="px-5 py-2.5 font-mono text-xs">{b.event_start_date ? format(parseISO(b.event_start_date), "d MMM yyyy", { locale: nl }) : "—"}</td>
                        <td className="px-5 py-2.5">{b.delivery_type ?? "—"}</td>
                        <td className="px-5 py-2.5">{b.booking_status ?? "—"}</td>
                        <td className="px-5 py-2.5 text-muted-foreground truncate max-w-xs">{b.product_summary ?? "—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </Card>
        </div>
      </div>
    </Page>
  );
}