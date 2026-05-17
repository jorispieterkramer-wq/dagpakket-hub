import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState, useMemo } from "react";
import { Page, Card, CardHeader, Loader, EmptyState } from "@/components/dashboard/Page";
import { supabase, type Product, type BookingItem } from "@/lib/supabase";
import { parseISO } from "date-fns";

export const Route = createFileRoute("/materialen")({ component: Materialen });

function Materialen() {
  const [products, setProducts] = useState<Product[]>([]);
  const [items, setItems] = useState<BookingItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const [search, setSearch] = useState("");

  useEffect(() => {
    (async () => {
      const [p, i] = await Promise.all([
        supabase.from("products").select("*"),
        supabase.from("booking_items").select("*"),
      ]);
      setProducts((p.data ?? []) as Product[]);
      setItems((i.data ?? []) as BookingItem[]);
      setLoading(false);
    })();
  }, []);

  const usage = useMemo(() => {
    if (!from || !to) return {};
    const f = parseISO(from), t = parseISO(to);
    const map: Record<string, number> = {};
    items.forEach((it) => {
      if (!it.event_start_date) return;
      const d = parseISO(it.event_start_date);
      if (d >= f && d <= t) {
        const k = it.product_id ?? it.product_name;
        map[k] = (map[k] ?? 0) + (it.quantity ?? 1);
      }
    });
    return map;
  }, [items, from, to]);

  const list = products
    .filter((p) => !search || p.name.toLowerCase().includes(search.toLowerCase()) || (p.sku ?? "").toLowerCase().includes(search.toLowerCase()))
    .map((p) => {
      const booked = usage[p.product_id] ?? usage[p.name] ?? 0;
      return { ...p, booked, free: (p.stock_total ?? 0) - booked };
    })
    .sort((a, b) => a.free - b.free);

  return (
    <Page>
      <Card className="mb-4">
        <CardHeader title="Beschikbaarheidscheck" subtitle="Selecteer een periode om geboekt vs vrij te zien" />
        <div className="p-5 flex gap-3 flex-wrap">
          <div>
            <label className="block text-xs text-muted-foreground mb-1">Van</label>
            <input type="date" value={from} onChange={(e) => setFrom(e.target.value)} className="px-3 py-1.5 bg-muted rounded-md text-sm" />
          </div>
          <div>
            <label className="block text-xs text-muted-foreground mb-1">Tot</label>
            <input type="date" value={to} onChange={(e) => setTo(e.target.value)} className="px-3 py-1.5 bg-muted rounded-md text-sm" />
          </div>
        </div>
      </Card>

      <Card>
        <div className="px-5 py-4 border-b border-border flex items-center gap-3">
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Zoek product, SKU of barcode"
            className="flex-1 max-w-md px-3 py-1.5 text-sm bg-muted rounded-md outline-none focus:ring-2 focus:ring-ring"
          />
          <div className="ml-auto text-xs text-muted-foreground">{list.length} producten</div>
        </div>
        {loading ? <Loader /> : list.length === 0 ? <EmptyState title="Nog geen producten" hint="Voeg producten toe in Supabase." /> : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-muted/50 text-xs uppercase text-muted-foreground">
                <tr>
                  <th className="text-left px-5 py-3 font-medium">Naam</th>
                  <th className="text-left px-5 py-3 font-medium">SKU</th>
                  <th className="text-left px-5 py-3 font-medium">Categorie</th>
                  <th className="text-right px-5 py-3 font-medium">Totaal</th>
                  <th className="text-right px-5 py-3 font-medium">Geboekt</th>
                  <th className="text-right px-5 py-3 font-medium">Vrij</th>
                  <th className="text-left px-5 py-3 font-medium w-40">Beschikbaar</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {list.map((p) => {
                  const total = p.stock_total || 1;
                  const pct = Math.max(0, Math.min(100, (p.free / total) * 100));
                  const tone = pct < 20 ? "bg-destructive" : pct < 50 ? "bg-[color:var(--warning)]" : "bg-[color:var(--success)]";
                  return (
                    <tr key={p.id} className="hover:bg-muted/30">
                      <td className="px-5 py-3 font-medium">{p.name}</td>
                      <td className="px-5 py-3 font-mono text-xs text-muted-foreground">{p.sku ?? "—"}</td>
                      <td className="px-5 py-3 text-muted-foreground">{p.category ?? "—"}</td>
                      <td className="px-5 py-3 text-right font-mono">{p.stock_total ?? 0}</td>
                      <td className="px-5 py-3 text-right font-mono">{p.booked}</td>
                      <td className={`px-5 py-3 text-right font-mono font-bold ${p.free < 0 ? "text-destructive" : ""}`}>{p.free}</td>
                      <td className="px-5 py-3">
                        <div className="h-2 bg-muted rounded-full overflow-hidden">
                          <div className={`h-full ${tone}`} style={{ width: `${pct}%` }} />
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </Page>
  );
}
