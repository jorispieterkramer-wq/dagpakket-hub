import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState, useMemo } from "react";
import { Page, Card, CardHeader, Loader, EmptyState } from "@/components/dashboard/Page";
import { supabase, type Customer } from "@/lib/supabase";
import { format, parseISO } from "date-fns";
import { nl } from "date-fns/locale";
import { Link } from "@tanstack/react-router";

export const Route = createFileRoute("/klanten")({ component: Klanten });

function Klanten() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    (async () => {
      const { data, error } = await supabase
        .from("customers")
        .select("*")
        .order("last_seen_at", { ascending: false, nullsFirst: false });
      if (error) console.error(error);
      setCustomers((data ?? []) as Customer[]);
      setLoading(false);
    })();
  }, []);

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return customers;
    return customers.filter((c) =>
      (c.name ?? "").toLowerCase().includes(q) ||
      (c.email ?? "").toLowerCase().includes(q) ||
      (c.city ?? "").toLowerCase().includes(q),
    );
  }, [customers, search]);

  return (
    <Page>
      <Card>
        <div className="px-5 py-4 border-b border-border flex items-center gap-3">
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Zoek klant…" className="flex-1 max-w-md px-3 py-1.5 text-sm bg-muted rounded-md outline-none focus:ring-2 focus:ring-ring" />
          <div className="ml-auto text-xs text-muted-foreground">{filtered.length} klanten</div>
        </div>
        {loading ? <Loader /> : filtered.length === 0 ? <EmptyState title="Nog geen klanten" hint="Run eerst de Fase 1 migratie in Supabase, dan worden klanten gebackfilled vanuit boekingen." /> : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-muted/50 text-xs uppercase text-muted-foreground">
                <tr>
                  <th className="text-left px-5 py-3 font-medium">Naam</th>
                  <th className="text-left px-5 py-3 font-medium">Email</th>
                  <th className="text-left px-5 py-3 font-medium">Telefoon</th>
                  <th className="text-left px-5 py-3 font-medium">Stad</th>
                  <th className="text-right px-5 py-3 font-medium">Orders</th>
                  <th className="text-left px-5 py-3 font-medium">Laatste</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {filtered.map((c) => (
                  <tr key={c.id} className="hover:bg-muted/30 cursor-pointer">
                    <td className="px-5 py-3 font-medium">
                      <Link to="/klanten/$id" params={{ id: c.id }} className="hover:underline">
                        {c.name || "—"}
                      </Link>
                    </td>
                    <td className="px-5 py-3 text-muted-foreground">{c.email || "—"}</td>
                    <td className="px-5 py-3 font-mono text-xs">{c.phone || "—"}</td>
                    <td className="px-5 py-3 text-muted-foreground">{c.city || "—"}</td>
                    <td className="px-5 py-3 text-right font-mono font-semibold">{c.total_orders}</td>
                    <td className="px-5 py-3 font-mono text-xs">{c.last_seen_at ? format(parseISO(c.last_seen_at), "d MMM yyyy", { locale: nl }) : "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </Page>
  );
}
