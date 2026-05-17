import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState, useMemo } from "react";
import { Page, Card, CardHeader, Loader } from "@/components/dashboard/Page";
import { supabase, type Booking, type BookingItem } from "@/lib/supabase";
import { BarChart, Bar, PieChart, Pie, Cell, ResponsiveContainer, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from "recharts";
import { parseISO, startOfYear } from "date-fns";

export const Route = createFileRoute("/statistieken")({ component: Stats });

const MONTHS = ["jan","feb","mrt","apr","mei","jun","jul","aug","sep","okt","nov","dec"];
const COLORS = ["var(--color-primary)", "var(--color-accent)", "var(--color-warning)", "var(--color-success)", "var(--color-info)"];

function Stats() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [items, setItems] = useState<BookingItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const [b, i] = await Promise.all([
        supabase.from("bookings").select("*").gte("event_start_date", startOfYear(new Date()).toISOString().slice(0, 10)),
        supabase.from("booking_items").select("*"),
      ]);
      setBookings((b.data ?? []) as Booking[]);
      setItems((i.data ?? []) as BookingItem[]);
      setLoading(false);
    })();
  }, []);

  const byMonth = useMemo(() => {
    const arr = new Array(12).fill(0);
    bookings.forEach((b) => { if (b.event_start_date) arr[parseISO(b.event_start_date).getMonth()]++; });
    return arr.map((v, i) => ({ month: MONTHS[i], value: v }));
  }, [bookings]);

  const byType = useMemo(() => {
    const m: Record<string, number> = {};
    bookings.forEach((b) => { const k = b.delivery_type ?? "onbekend"; m[k] = (m[k] ?? 0) + 1; });
    return Object.entries(m).map(([name, value]) => ({ name, value }));
  }, [bookings]);

  const topProducts = useMemo(() => {
    const m: Record<string, number> = {};
    items.forEach((it) => { m[it.product_name] = (m[it.product_name] ?? 0) + (it.quantity ?? 1); });
    return Object.entries(m).sort((a, b) => b[1] - a[1]).slice(0, 10).map(([name, value]) => ({ name, value }));
  }, [items]);

  if (loading) return <Page><Loader /></Page>;
  return (
    <Page>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card>
          <CardHeader title="Boekingen per maand" />
          <div className="p-5 h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={byMonth}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" vertical={false} />
                <XAxis dataKey="month" fontSize={11} stroke="var(--color-muted-foreground)" axisLine={false} tickLine={false} />
                <YAxis fontSize={11} stroke="var(--color-muted-foreground)" axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: "var(--color-card)", border: "1px solid var(--color-border)", borderRadius: 8 }} />
                <Bar dataKey="value" fill="var(--color-primary)" radius={[6,6,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
        <Card>
          <CardHeader title="Bezorgtype verdeling" />
          <div className="p-5 h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={byType} dataKey="value" nameKey="name" outerRadius={90} label>
                  {byType.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Legend />
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>
        <Card className="lg:col-span-2">
          <CardHeader title="Top 10 producten" />
          <div className="p-5 h-[360px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topProducts} layout="vertical" margin={{ left: 100 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" horizontal={false} />
                <XAxis type="number" fontSize={11} stroke="var(--color-muted-foreground)" axisLine={false} tickLine={false} />
                <YAxis dataKey="name" type="category" fontSize={11} stroke="var(--color-muted-foreground)" axisLine={false} tickLine={false} width={150} />
                <Tooltip contentStyle={{ background: "var(--color-card)", border: "1px solid var(--color-border)", borderRadius: 8 }} />
                <Bar dataKey="value" fill="var(--color-accent)" radius={[0,6,6,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </Page>
  );
}
