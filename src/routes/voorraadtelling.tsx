import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Page, Card, Loader, EmptyState } from "@/components/dashboard/Page";
import { supabase, type Product } from "@/lib/supabase";
import { Save } from "lucide-react";

export const Route = createFileRoute("/voorraadtelling")({ component: Voorraad });

function Voorraad() {
  const [products, setProducts] = useState<Product[]>([]);
  const [counts, setCounts] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const { data } = await supabase.from("products").select("*").order("name");
      setProducts((data ?? []) as Product[]);
      setLoading(false);
    })();
  }, []);

  const save = () => {
    const key = `dpv-count-${new Date().toISOString().slice(0,10)}`;
    localStorage.setItem(key, JSON.stringify(counts));
    alert("Telling opgeslagen.");
  };

  if (loading) return <Page><Loader /></Page>;
  return (
    <Page>
      <Card>
        <div className="px-5 py-4 border-b border-border flex items-center justify-between">
          <h2 className="font-display font-bold">Voorraadtelling — {new Date().toLocaleDateString("nl-NL")}</h2>
          <button onClick={save} className="px-3 py-1.5 bg-primary text-primary-foreground rounded-md text-sm inline-flex items-center gap-1.5"><Save className="w-4 h-4" /> Opslaan</button>
        </div>
        {products.length === 0 ? <EmptyState title="Geen producten" /> : (
          <table className="w-full text-sm">
            <thead className="bg-muted/50 text-xs uppercase text-muted-foreground">
              <tr><th className="text-left px-5 py-3">Product</th><th className="text-right px-5 py-3">Systeem</th><th className="text-right px-5 py-3 w-32">Geteld</th><th className="text-right px-5 py-3">Verschil</th></tr>
            </thead>
            <tbody className="divide-y divide-border">
              {products.map((p) => {
                const c = counts[p.id];
                const diff = c === undefined ? null : c - (p.stock_total ?? 0);
                return (
                  <tr key={p.id}>
                    <td className="px-5 py-3 font-medium">{p.name}</td>
                    <td className="px-5 py-3 text-right font-mono">{p.stock_total ?? 0}</td>
                    <td className="px-5 py-3">
                      <input type="number" value={c ?? ""} onChange={(e) => setCounts((cs) => ({ ...cs, [p.id]: parseInt(e.target.value) }))} className="w-24 px-2 py-1 bg-muted rounded text-right font-mono text-sm" />
                    </td>
                    <td className={`px-5 py-3 text-right font-mono font-bold ${diff === null ? "" : diff < 0 ? "text-destructive" : diff > 0 ? "text-[color:var(--success)]" : "text-muted-foreground"}`}>
                      {diff === null ? "—" : diff > 0 ? `+${diff}` : diff}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </Card>
    </Page>
  );
}
