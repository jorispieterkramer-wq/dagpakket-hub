import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState, useMemo } from "react";
import { Page, Card, CardHeader, Loader, EmptyState } from "@/components/dashboard/Page";
import { supabase, type Product, type BookingItem } from "@/lib/supabase";
import { addDays, parseISO } from "date-fns";

export const Route = createFileRoute("/tekorten")({ component: Tekorten });

function Tekorten() {
  const [products, setProducts] = useState<Product[]>([]);
  const [items, setItems] = useState<BookingItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState<"week" | "maand" | "kwartaal">("week");

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

  const tekorten = useMemo(() => {
    const days = period === "week" ? 7 : period === "maand" ? 30 : 90;
    const limit = addDays(new Date(), days);
    const usage: Record<string, number> = {};
    items.forEach((it) => {
      if (!it.event_start_date) return;
      const d = parseISO(it.event_start_date);
      if (d <= limit && d >= new Date()) {
        const k = it.product_id ?? it.product_name;
        usage[k] = (usage[k] ?? 0) + (it.quantity ?? 1);
      }
    });
    return products.map((p) => {
      const demand = usage[p.product_id] ?? usage[p.name] ?? 0;
      const shortage = demand - (p.stock_total ?? 0);
      return { ...p, demand, shortage };
    }).filter((p) => p.shortage > 0).sort((a, b) => b.shortage - a.shortage);
  }, [products, items, period]);

  if (loading) return <Page><Loader /></Page>;
  return (
    <Page>
      <Card>
        <div className="px-5 py-4 border-b border-border flex gap-2 items-center">
          {(["week","maand","kwartaal"] as const).map((p) => (
            <button key={p} onClick={() => setPeriod(p)} className={`px-3 py-1.5 text-xs rounded-md ${period === p ? "bg-primary text-primary-foreground" : "bg-muted"}`}>{p}</button>
          ))}
          <div className="ml-auto text-xs text-muted-foreground">{tekorten.length} tekorten</div>
        </div>
        {tekorten.length > 0 && (
          <div className="px-5 py-3 bg-destructive/10 border-b border-destructive/20 text-sm text-destructive font-medium">
            ⚠ Er zijn {tekorten.length} producten met een tekort in deze periode.
          </div>
        )}
        {tekorten.length === 0 ? <EmptyState title="Geen tekorten" hint="Alle producten zijn voldoende beschikbaar." /> : (
          <table className="w-full text-sm">
            <thead className="bg-muted/50 text-xs uppercase text-muted-foreground">
              <tr><th className="text-left px-5 py-3">Product</th><th className="text-right px-5 py-3">Vraag</th><th className="text-right px-5 py-3">Voorraad</th><th className="text-right px-5 py-3">Tekort</th></tr>
            </thead>
            <tbody className="divide-y divide-border">
              {tekorten.map((p) => (
                <tr key={p.id}><td className="px-5 py-3 font-medium">{p.name}</td><td className="px-5 py-3 text-right font-mono">{p.demand}</td><td className="px-5 py-3 text-right font-mono">{p.stock_total ?? 0}</td><td className="px-5 py-3 text-right font-mono font-bold text-destructive">-{p.shortage}</td></tr>
              ))}
            </tbody>
          </table>
        )}
      </Card>
    </Page>
  );
}
