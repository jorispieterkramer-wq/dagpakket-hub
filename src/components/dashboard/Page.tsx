import type { ReactNode } from "react";

export function Page({ children, actions }: { children: ReactNode; actions?: ReactNode }) {
  return (
    <div className="p-6 max-w-[1600px] mx-auto">
      {actions && <div className="flex justify-end mb-4">{actions}</div>}
      {children}
    </div>
  );
}

export function Card({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <div className={`bg-card border border-border rounded-xl ${className}`}>{children}</div>;
}

export function CardHeader({ title, subtitle, action }: { title: string; subtitle?: string; action?: ReactNode }) {
  return (
    <div className="px-5 py-4 border-b border-border flex items-center justify-between">
      <div>
        <h2 className="font-display font-bold text-base">{title}</h2>
        {subtitle && <p className="text-xs text-muted-foreground mt-0.5">{subtitle}</p>}
      </div>
      {action}
    </div>
  );
}

export function EmptyState({ title, hint }: { title: string; hint?: string }) {
  return (
    <div className="py-16 text-center">
      <div className="text-sm font-medium text-foreground">{title}</div>
      {hint && <div className="text-xs text-muted-foreground mt-1">{hint}</div>}
    </div>
  );
}

export function Loader() {
  return (
    <div className="py-16 flex items-center justify-center">
      <div className="w-6 h-6 border-2 border-muted border-t-primary rounded-full animate-spin" />
    </div>
  );
}

export function Badge({ children, tone = "default" }: { children: ReactNode; tone?: "default" | "success" | "warning" | "danger" | "info" | "muted" }) {
  const tones: Record<string, string> = {
    default: "bg-muted text-foreground",
    success: "bg-[color:var(--success)]/15 text-[color:var(--success)]",
    warning: "bg-[color:var(--warning)]/15 text-[color:var(--warning)]",
    danger: "bg-destructive/15 text-destructive",
    info: "bg-[color:var(--info)]/15 text-[color:var(--info)]",
    muted: "bg-muted text-muted-foreground",
  };
  return <span className={`inline-flex items-center px-2 py-0.5 rounded-md text-[11px] font-medium ${tones[tone]}`}>{children}</span>;
}

export function PageStub({ title, description }: { title: string; description: string }) {
  return (
    <Page>
      <Card>
        <div className="p-10 text-center">
          <h2 className="font-display font-bold text-lg mb-2">{title}</h2>
          <p className="text-sm text-muted-foreground max-w-md mx-auto">{description}</p>
          <p className="text-xs text-muted-foreground mt-4">Deze module wordt in een volgende iteratie volledig uitgebouwd.</p>
        </div>
      </Card>
    </Page>
  );
}
