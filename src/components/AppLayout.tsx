import { useState, useEffect, type ReactNode } from "react";
import { Link, useRouterState } from "@tanstack/react-router";
import {
  LayoutDashboard, CalendarDays, CheckSquare, Clock, AlertTriangle,
  ShoppingBag, Users, FileText, Truck, Bell,
  Package, Printer, Boxes, ClipboardCheck, PackageX, BookOpen,
  UserCog, CalendarRange, Car, MapPin,
  Wrench, ShieldCheck, AlertCircle,
  BarChart3, TrendingDown, Tv,
  ChevronLeft, ChevronRight, Sun, Moon, Sparkles, X, Send,
} from "lucide-react";
import { AiChat } from "./AiChat";

type Item = { to: string; label: string; icon: React.ComponentType<{ className?: string }>; };
type Group = { label: string; items: Item[] };

const groups: Group[] = [
  { label: "Operationeel", items: [
    { to: "/", label: "Dashboard", icon: LayoutDashboard },
    { to: "/planning", label: "Planning", icon: CalendarDays },
    { to: "/taken", label: "Taken", icon: CheckSquare },
    { to: "/tijd", label: "Tijdregistratie", icon: Clock },
    { to: "/problemen", label: "Problemen", icon: AlertTriangle },
  ]},
  { label: "Verhuur", items: [
    { to: "/boekingen", label: "Boekingen", icon: ShoppingBag },
    { to: "/klanten", label: "Klanten", icon: Users },
    { to: "/facturen", label: "Facturen & offertes", icon: FileText },
    { to: "/bezorging", label: "Bezorging & routes", icon: Truck },
    { to: "/notificaties", label: "Notificaties", icon: Bell },
  ]},
  { label: "Magazijn", items: [
    { to: "/inpakken", label: "Inpakken", icon: Package },
    { to: "/paklijsten", label: "Paklijsten", icon: Printer },
    { to: "/materialen", label: "Materialen", icon: Boxes },
    { to: "/voorraadtelling", label: "Voorraadtelling", icon: ClipboardCheck },
    { to: "/kwijtgeraakt", label: "Kwijtgeraakt", icon: PackageX },
    { to: "/handleidingen", label: "Handleidingen", icon: BookOpen },
  ]},
  { label: "Personeel", items: [
    { to: "/medewerkers", label: "Medewerkers", icon: UserCog },
    { to: "/personeelsplanner", label: "Personeelsplanner", icon: CalendarRange },
    { to: "/voertuigen", label: "Voertuigen", icon: Car },
    { to: "/gps", label: "GPS tracking", icon: MapPin },
  ]},
  { label: "Onderhoud", items: [
    { to: "/reparaties", label: "Reparaties", icon: Wrench },
    { to: "/keuringen", label: "Keuringen", icon: ShieldCheck },
    { to: "/te-keuren", label: "Te keuren", icon: AlertCircle },
  ]},
  { label: "Inzicht", items: [
    { to: "/statistieken", label: "Statistieken", icon: BarChart3 },
    { to: "/tekorten", label: "Verhuur tekorten", icon: TrendingDown },
    { to: "/tv", label: "TV/Magazijn scherm", icon: Tv },
  ]},
];

export function AppLayout({ children }: { children: ReactNode }) {
  const [expanded, setExpanded] = useState(false);
  const [dark, setDark] = useState(false);
  const [aiOpen, setAiOpen] = useState(false);
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  useEffect(() => {
    const saved = localStorage.getItem("dpv-dark");
    if (saved === "1") { document.documentElement.classList.add("dark"); setDark(true); }
  }, []);

  // TV scherm = volledig scherm zonder layout
  if (pathname === "/tv") return <>{children}</>;

  const toggleDark = () => {
    const next = !dark;
    setDark(next);
    document.documentElement.classList.toggle("dark", next);
    localStorage.setItem("dpv-dark", next ? "1" : "0");
  };

  const currentTitle = (() => {
    for (const g of groups) for (const i of g.items) if (i.to === pathname) return i.label;
    return "DagPakketVerhuur";
  })();

  const today = new Date().toLocaleDateString("nl-NL", { weekday: "long", day: "numeric", month: "long", year: "numeric" });

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      <aside
        className={`${expanded ? "w-[220px]" : "w-[64px]"} transition-all duration-200 bg-sidebar border-r border-sidebar-border flex flex-col`}
        onMouseEnter={() => setExpanded(true)}
        onMouseLeave={() => setExpanded(false)}
      >
        <div className="h-[58px] flex items-center px-4 border-b border-sidebar-border shrink-0">
          <div className="w-8 h-8 rounded-md bg-primary flex items-center justify-center text-primary-foreground font-display font-bold text-sm shrink-0">D</div>
          {expanded && <span className="ml-3 font-display font-bold text-sm tracking-tight whitespace-nowrap">DagPakketVerhuur</span>}
        </div>
        <nav className="flex-1 overflow-y-auto py-3 scrollbar-thin">
          {groups.map((g) => (
            <div key={g.label} className="mb-3">
              {expanded && <div className="px-4 py-1 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">{g.label}</div>}
              {g.items.map((it) => {
                const active = pathname === it.to;
                const Icon = it.icon;
                return (
                  <Link
                    key={it.to}
                    to={it.to}
                    className={`flex items-center h-9 px-4 text-sm relative transition-colors ${
                      active ? "text-primary font-medium bg-sidebar-hover" : "text-foreground hover:bg-sidebar-hover"
                    }`}
                    title={!expanded ? it.label : undefined}
                  >
                    {active && <span className="absolute left-0 top-1.5 bottom-1.5 w-[3px] rounded-r bg-primary" />}
                    <Icon className="w-4 h-4 shrink-0" />
                    {expanded && <span className="ml-3 truncate">{it.label}</span>}
                  </Link>
                );
              })}
            </div>
          ))}
        </nav>
        <div className="p-2 border-t border-sidebar-border">
          <button
            onClick={() => setExpanded((e) => !e)}
            className="w-full flex items-center justify-center h-8 rounded-md hover:bg-sidebar-hover text-muted-foreground"
            aria-label="Toggle sidebar"
          >
            {expanded ? <ChevronLeft className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
          </button>
        </div>
      </aside>

      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="h-[58px] shrink-0 bg-card border-b border-border flex items-center px-6 gap-4">
          <h1 className="font-display font-bold text-base">{currentTitle}</h1>
          <div className="ml-auto flex items-center gap-3 text-sm">
            <span className="text-muted-foreground hidden md:inline capitalize">{today}</span>
            <button onClick={toggleDark} className="w-8 h-8 rounded-md hover:bg-muted flex items-center justify-center" aria-label="Toggle dark mode">
              {dark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
            <Link to="/notificaties" className="w-8 h-8 rounded-md hover:bg-muted flex items-center justify-center relative">
              <Bell className="w-4 h-4" />
            </Link>
            <div className="flex items-center gap-2 pl-3 border-l border-border">
              <div className="w-7 h-7 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xs font-semibold">J</div>
              <span className="font-medium hidden md:inline">Joris</span>
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-auto scrollbar-thin">
          {children}
        </main>
      </div>

      {/* Floating AI button */}
      <button
        onClick={() => setAiOpen(true)}
        className="fixed bottom-6 right-6 w-[52px] h-[52px] rounded-full bg-gradient-to-br from-primary to-accent text-primary-foreground shadow-lg flex items-center justify-center animate-soft-pulse z-40"
        aria-label="AI Manager"
      >
        <Sparkles className="w-5 h-5" />
      </button>
      {aiOpen && <AiChat onClose={() => setAiOpen(false)} />}
    </div>
  );
}
