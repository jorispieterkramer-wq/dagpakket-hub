import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Page, Card, CardHeader, Loader, EmptyState, Badge } from "@/components/dashboard/Page";
import { supabase, type Booking } from "@/lib/supabase";
import { deliveryTypeLabel } from "@/lib/business";
import { MapPin, ExternalLink } from "lucide-react";
import { format } from "date-fns";

export const Route = createFileRoute("/bezorging")({ component: Bezorging });

function Bezorging() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [date, setDate] = useState(format(new Date(), "yyyy-MM-dd"));
  const [checked, setChecked] = useState<Record<string, boolean>>({});

  useEffect(() => {
    (async () => {
      const { data } = await supabase.from("bookings").select("*").in("delivery_type", ["bezorgen", "dhl"]);
      setBookings((data ?? []) as Booking[]);
      setLoading(false);
    })();
  }, []);

  const stops = bookings
    .filter((b) => b.packing_date === date)
    .sort((a, b) => (a.postcode ?? "").localeCompare(b.postcode ?? ""));

  const done = stops.filter((s) => checked[s.id]).length;
  const fullRoute = stops.map((s) => encodeURIComponent(`${s.address ?? ""} ${s.postcode ?? ""} ${s.city ?? ""}`)).join("/");
  const mapsUrl = stops.length > 0 ? `https://www.google.com/maps/dir/${fullRoute}` : "#";

  return (
    <Page>
      <Card>
        <div className="px-5 py-4 border-b border-border flex items-center gap-3 flex-wrap">
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} className="px-3 py-1.5 bg-muted rounded-md text-sm" />
          <div className="text-sm text-muted-foreground">{stops.length} stops · {done} klaar</div>
          {stops.length > 0 && (
            <a href={mapsUrl} target="_blank" rel="noreferrer" className="ml-auto inline-flex items-center gap-1.5 px-3 py-1.5 bg-primary text-primary-foreground rounded-md text-sm">
              <MapPin className="w-4 h-4" /> Hele route in Maps
            </a>
          )}
        </div>
        {stops.length > 0 && (
          <div className="px-5 py-3 border-b border-border">
            <div className="h-2 bg-muted rounded-full overflow-hidden">
              <div className="h-full bg-primary transition-all" style={{ width: `${(done / stops.length) * 100}%` }} />
            </div>
          </div>
        )}
        {loading ? <Loader /> : stops.length === 0 ? <EmptyState title="Geen bezorgingen op deze dag" /> : (
          <div className="divide-y divide-border">
            {stops.map((s, i) => (
              <div key={s.id} className="px-5 py-4 flex items-start gap-4">
                <input type="checkbox" checked={!!checked[s.id]} onChange={(e) => setChecked((c) => ({ ...c, [s.id]: e.target.checked }))} className="w-5 h-5 mt-0.5" />
                <div className="font-display font-bold text-2xl text-primary w-10">{i + 1}</div>
                <div className="flex-1 min-w-0">
                  <div className="font-medium">{s.customer_name}</div>
                  <div className="text-sm text-muted-foreground">{s.address}, {s.postcode} {s.city}</div>
                  <div className="text-xs text-muted-foreground mt-1 truncate">{s.product_summary ?? `Order #${s.order_id}`}</div>
                </div>
                <Badge tone={s.delivery_type === "dhl" ? "warning" : "info"}>{deliveryTypeLabel(s.delivery_type)}</Badge>
                <a href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${s.address} ${s.postcode} ${s.city}`)}`} target="_blank" rel="noreferrer"
                  className="p-2 rounded-md hover:bg-muted">
                  <ExternalLink className="w-4 h-4" />
                </a>
              </div>
            ))}
          </div>
        )}
      </Card>
    </Page>
  );
}
