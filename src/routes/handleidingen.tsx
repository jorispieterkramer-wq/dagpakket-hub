import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { Page, Card } from "@/components/dashboard/Page";

export const Route = createFileRoute("/handleidingen")({ component: Handleidingen });

const MANUALS = [
  { id: "lxl", cat: "Lasergame", name: "Lasergame XL", content: "1. Pak de set uit en controleer alle 4 wapens.\n2. Plaats 4x AA batterijen per wapen.\n3. Synchroniseer wapens via de hoofdknop (3s ingedrukt).\n4. Stel team A en team B in.\n\nTip: laad de wapens 's avonds van tevoren op." },
  { id: "lc", cat: "Lasergame", name: "Lasergame Compact", content: "1. Plaats 3x AAA batterijen per wapen.\n2. Druk lang op trigger om te starten.\n\nTip: ideaal binnen-spel." },
  { id: "gb", cat: "Gelblaster", name: "Gelblaster", content: "1. Week de gel-balletjes minstens 4 uur in water.\n2. Plaats 6x AA batterijen.\n3. Vul de magazijntrechter.\n4. Bril verplicht!" },
  { id: "tv", cat: "Lasergame", name: "Target vest", content: "1. Plaats 3x AAA batterijen.\n2. Vest aan, sensor naar voren.\n3. Synchroniseer met wapen." },
  { id: "pt", cat: "Partytent", name: "Partytent", content: "1. Leg het frame uit op de grond.\n2. Klik elke hoek vast.\n3. Trek het dak strak.\n4. Veranker met haringen of gewichten.\n\nTip: niet opzetten bij windkracht 6 of meer." },
  { id: "pc", cat: "Keukenapparatuur", name: "Popcornmachine", content: "1. Steek de stekker in.\n2. Voeg olie en mais toe in de ketel.\n3. Wacht tot popcorn klaar is, schep eruit.\n\nVeiligheid: pan blijft heet." },
  { id: "ss", cat: "Keukenapparatuur", name: "Suikerspinmachine", content: "1. Apparaat op een stevige tafel.\n2. Suiker in de kop.\n3. Aanzetten, 1 minuut opwarmen.\n4. Stokje rond de kop bewegen." },
];

function Handleidingen() {
  const [sel, setSel] = useState(MANUALS[0]);
  const [q, setQ] = useState("");
  const list = MANUALS.filter((m) => m.name.toLowerCase().includes(q.toLowerCase()) || m.cat.toLowerCase().includes(q.toLowerCase()));

  return (
    <Page>
      <div className="grid grid-cols-1 md:grid-cols-[280px_1fr] gap-4">
        <Card>
          <div className="p-3 border-b border-border">
            <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Zoek handleiding" className="w-full px-3 py-1.5 bg-muted rounded-md text-sm outline-none" />
          </div>
          <div className="divide-y divide-border max-h-[600px] overflow-y-auto scrollbar-thin">
            {list.map((m) => (
              <button key={m.id} onClick={() => setSel(m)} className={`w-full px-4 py-3 text-left hover:bg-muted/40 ${sel.id === m.id ? "bg-primary/5 border-l-2 border-primary" : ""}`}>
                <div className="text-sm font-medium">{m.name}</div>
                <div className="text-xs text-muted-foreground">{m.cat}</div>
              </button>
            ))}
          </div>
        </Card>
        <Card>
          <div className="px-6 py-5 border-b border-border">
            <div className="text-xs uppercase text-muted-foreground tracking-wider">{sel.cat}</div>
            <h2 className="font-display font-bold text-xl mt-1">{sel.name}</h2>
          </div>
          <div className="p-6 whitespace-pre-line leading-relaxed text-sm">{sel.content}</div>
        </Card>
      </div>
    </Page>
  );
}
