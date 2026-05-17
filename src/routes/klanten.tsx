import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState, useMemo } from "react";
import { Page, Card, CardHeader, Loader, EmptyState } from "@/components/dashboard/Page";
import { supabase, type Booking } from "@/lib/supabase";
import { format, parseISO } from "date-fns";
import { nl } from "date-fns/locale";

export const Route = createFileRoute("/klanten")({ component: Klanten });

function Klanten() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    (async () => {
      const { data } = await supabase.from("bookings").select("*");
      setBookings((data ?? []) as Booking[]);
      setLoading(false);
    })();
  }, []);

  const customers = useMemo(() => {
    const map: Record<string, { name: string; email: string; phone: string; city: string; count: number; last: string }> = {};
    bookings.forEach((b) => {
      const key = (b.email ?? `${b.customer_name}-${b.phone}`).toLowerCase();
      if (!map[key]) map[key] = { name: b.customer_name ?? "—", email: b.email ?? "", phone: b.phone ?? "", city: b.city ?? "", count: 0, last: "" };
      map[key].count++;
      const d = b.event_start_date ?? "";
      if (d > map[key].last) map[key].last = d;
    });
    return Object.values(map).filter((c) => !search || c.name.toLowerCase().includes(search.toLowerCase()) || c.email.toLowerCase().includes(search.toLowerCase()));
  }, [bookings, search]);

  return (
    <Page>
      <Card>
        <div className="px-5 py-4 border-b border-border flex items-center gap-3">
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Zoek klant…" className="flex-1 max-w-md px-3 py-1.5 text-sm bg-muted rounded-md outline-none focus:ring-2 focus:ring-ring" />
          <div className="ml-auto text-xs text-muted-foreground">{customers.length} klanten</div>
        </div>
        {loading ? <Loader /> : customers.length === 0 ? <EmptyState title="Nog geen klanten" /> : (
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
                {customers.map((c, i) => (
                  <tr key={i} className="hover:bg-muted/30">
                    <td className="px-5 py-3 font-medium">{c.name}</td>
                    <td className="px-5 py-3 text-muted-foreground">{c.email || "—"}</td>
                    <td className="px-5 py-3 font-mono text-xs">{c.phone || "—"}</td>
                    <td className="px-5 py-3 text-muted-foreground">{c.city || "—"}</td>
                    <td className="px-5 py-3 text-right font-mono font-semibold">{c.count}</td>
                    <td className="px-5 py-3 font-mono text-xs">{c.last ? format(parseISO(c.last), "d MMM yyyy", { locale: nl }) : "—"}</td>
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
