import { addDays, differenceInDays, isSunday, parseISO } from "date-fns";

export function computePackingDate(eventStart: string | null, deliveryType: string | null): Date | null {
  if (!eventStart) return null;
  const d = parseISO(eventStart);
  const offset = deliveryType === "dhl" ? 7 : 2;
  let pack = addDays(d, -offset);
  if (isSunday(pack)) pack = addDays(pack, -1);
  return pack;
}

export function isSpoed(eventStart: string | null, status: string | null): boolean {
  if (!eventStart || status === "cancelled" || status === "refunded") return false;
  const diff = differenceInDays(parseISO(eventStart), new Date());
  return diff >= 0 && diff <= 3;
}

export const accessoriesFor = (productName: string): { name: string; type: "manual" | "battery" }[] => {
  const acc: { name: string; type: "manual" | "battery" }[] = [
    { name: "Handleiding", type: "manual" },
  ];
  const n = productName.toLowerCase();
  if (n.includes("lasergame xl")) acc.push({ name: "4x AA batterijen", type: "battery" });
  else if (n.includes("lasergame compact")) acc.push({ name: "3x AAA batterijen", type: "battery" });
  else if (n.includes("gelblaster")) acc.push({ name: "6x AA batterijen", type: "battery" });
  else if (n.includes("target vest") || n.includes("targetvest")) acc.push({ name: "3x AAA batterijen", type: "battery" });
  return acc;
};

const LOW_VAT_KEYWORDS = ["popcorn", "suikerspin", "frisdrank", "drank", "snoep", "ingredi"];
export function vatRateFor(productName: string): number {
  const n = productName.toLowerCase();
  return LOW_VAT_KEYWORDS.some((k) => n.includes(k)) ? 0.09 : 0.21;
}

export const deliveryTypeLabel = (t: string | null) => {
  if (t === "bezorgen") return "Bezorgen";
  if (t === "ophalen") return "Ophalen";
  if (t === "dhl") return "DHL";
  return "Onbekend";
};

export const statusLabel = (s: string | null) => {
  const map: Record<string, string> = {
    new: "Nieuw", processing: "In behandeling", completed: "Afgerond",
    cancelled: "Geannuleerd", refunded: "Terugbetaald", packed: "Ingepakt",
  };
  return s ? map[s] ?? s : "—";
};
