import { useState } from "react";
import { X, Send, Sparkles } from "lucide-react";

type Msg = { role: "user" | "assistant"; text: string };

export function AiChat({ onClose }: { onClose: () => void }) {
  const [messages, setMessages] = useState<Msg[]>([
    { role: "assistant", text: "Hoi Joris! Ik ben je AI operationeel manager. Stel me een vraag over je boekingen, voorraad of planning." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const send = async (text: string) => {
    if (!text.trim()) return;
    setMessages((m) => [...m, { role: "user", text }]);
    setInput("");
    setLoading(true);
    // Placeholder — Anthropic API key niet ingesteld. Toon nette mock.
    setTimeout(() => {
      setMessages((m) => [...m, { role: "assistant", text: "Ik kan helpen zodra de Anthropic API-koppeling is geconfigureerd in de instellingen. Stuur je vraag, dan zet ik het in de wachtrij." }]);
      setLoading(false);
    }, 600);
  };

  const suggestions = ["Hoeveel boekingen deze week?", "Wat moet ik morgen inpakken?", "Zijn er spoedorders?"];

  return (
    <div className="fixed bottom-24 right-6 w-[380px] h-[540px] bg-card border border-border rounded-xl shadow-2xl flex flex-col z-50 overflow-hidden">
      <div className="bg-primary text-primary-foreground px-4 py-3 flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-white/15 flex items-center justify-center">
          <Sparkles className="w-4 h-4" />
        </div>
        <div className="flex-1">
          <div className="text-sm font-display font-bold">AI Manager</div>
          <div className="text-[11px] opacity-70">Live operationeel inzicht</div>
        </div>
        <button onClick={onClose} className="p-1 rounded hover:bg-white/10"><X className="w-4 h-4" /></button>
      </div>
      <div className="flex-1 overflow-auto p-4 space-y-3 scrollbar-thin">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-[85%] text-sm px-3 py-2 rounded-lg ${
              m.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted"
            }`}>{m.text}</div>
          </div>
        ))}
        {loading && <div className="text-xs text-muted-foreground">Aan het nadenken…</div>}
        {messages.length <= 1 && (
          <div className="flex flex-wrap gap-2 pt-2">
            {suggestions.map((s) => (
              <button key={s} onClick={() => send(s)} className="text-xs px-3 py-1.5 rounded-full bg-muted hover:bg-border transition">{s}</button>
            ))}
          </div>
        )}
      </div>
      <div className="p-3 border-t border-border flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send(input)}
          placeholder="Vraag iets…"
          className="flex-1 px-3 py-2 text-sm bg-muted rounded-md outline-none focus:ring-2 focus:ring-ring"
        />
        <button onClick={() => send(input)} className="w-9 h-9 rounded-md bg-primary text-primary-foreground flex items-center justify-center hover:opacity-90">
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
