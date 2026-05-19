import { supabase } from "./supabase";

export async function logAction(params: {
  entity_type: string;
  entity_id: string | number;
  action: string;
  actor?: string;
  meta?: Record<string, unknown>;
}) {
  try {
    await supabase.from("audit_log").insert({
      entity_type: params.entity_type,
      entity_id: String(params.entity_id),
      action: params.action,
      actor: params.actor ?? "dashboard",
      meta: params.meta ?? null,
    });
  } catch (e) {
    console.warn("audit log failed", e);
  }
}

export const fmtEUR = (cents: number) =>
  new Intl.NumberFormat("nl-NL", { style: "currency", currency: "EUR" }).format((cents ?? 0) / 100);