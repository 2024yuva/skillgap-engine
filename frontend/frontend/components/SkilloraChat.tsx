"use client";

import {
  useEffect,
  useRef,
  useState,
  useCallback,
  KeyboardEvent,
} from "react";
import { usePathname } from "next/navigation";
import {
  Bot,
  X,
  Send,
  Loader2,
  Minimize2,
  FileText,
  Brain,
  Briefcase,
  BarChart2,
  DollarSign,
  BookOpen,
  ChevronDown,
} from "lucide-react";
import { api } from "@/lib/api";
import { getSession } from "@/lib/session";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  ts: number;
}

const QUICK_ACTIONS = [
  { icon: FileText,   label: "Improve My Resume",       prompt: "How can I improve my resume?" },
  { icon: Brain,      label: "Analyze My Skills",        prompt: "Analyze my current skills and tell me my strengths and weaknesses." },
  { icon: Briefcase,  label: "Find Suitable Jobs",       prompt: "What jobs are most suitable for me based on my skills?" },
  { icon: BarChart2,  label: "Check My Skill Gap",       prompt: "Show me my skill gap analysis." },
  { icon: DollarSign, label: "Salary Insights",          prompt: "What salary can I expect based on my skills?" },
  { icon: BookOpen,   label: "Recommend Learning Path",  prompt: "Recommend a personalized learning path for me." },
];

const WELCOME: ChatMessage = {
  id: "welcome",
  role: "assistant",
  content:
    "Hi! I'm Skillora AI 👋\n\nI can help you **improve your resume**, identify **skill gaps**, discover **suitable job roles**, explore **salary insights**, and build your **personalized learning path**.\n\nWhat would you like to know?",
  ts: Date.now(),
};

// ---------------------------------------------------------------------------
// Markdown-lite renderer (bold + bullet lists only, no deps)
// ---------------------------------------------------------------------------

function renderMarkdown(text: string) {
  const lines = text.split("\n");
  const elements: React.ReactNode[] = [];
  let listItems: string[] = [];

  function flushList(key: string) {
    if (listItems.length === 0) return;
    elements.push(
      <ul key={key} className="list-none space-y-1 my-1.5">
        {listItems.map((item, i) => (
          <li key={i} className="flex items-start gap-1.5 text-[13px] leading-relaxed">
            <span className="text-indigo-400 mt-[3px] shrink-0">•</span>
            <span>{inlineBold(item)}</span>
          </li>
        ))}
      </ul>
    );
    listItems = [];
  }

  lines.forEach((line, idx) => {
    const trimmed = line.trim();
    if (trimmed.startsWith("- ") || trimmed.startsWith("• ") || trimmed.match(/^\d+\.\s/)) {
      listItems.push(trimmed.replace(/^[-•]\s|^\d+\.\s/, ""));
    } else {
      flushList(`list-${idx}`);
      if (trimmed === "") {
        elements.push(<div key={`br-${idx}`} className="h-1" />);
      } else if (trimmed.startsWith("###") || trimmed.startsWith("**") && trimmed.endsWith("**") && !trimmed.slice(2, -2).includes("**")) {
        const heading = trimmed.replace(/^#+\s*/, "").replace(/^\*\*|\*\*$/g, "");
        elements.push(
          <p key={idx} className="font-semibold text-slate-800 text-[13px] mt-2 mb-0.5">
            {heading}
          </p>
        );
      } else {
        elements.push(
          <p key={idx} className="text-[13px] leading-relaxed">
            {inlineBold(trimmed)}
          </p>
        );
      }
    }
  });
  flushList("list-end");
  return <>{elements}</>;
}

function inlineBold(text: string): React.ReactNode {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return (
    <>
      {parts.map((part, i) =>
        part.startsWith("**") && part.endsWith("**") ? (
          <strong key={i} className="font-semibold text-slate-800">
            {part.slice(2, -2)}
          </strong>
        ) : (
          <span key={i}>{part}</span>
        )
      )}
    </>
  );
}

// ---------------------------------------------------------------------------
// ChatMessage bubble
// ---------------------------------------------------------------------------

function MessageBubble({ msg }: { msg: ChatMessage }) {
  const isUser = msg.role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} gap-2`}>
      {!isUser && (
        <div className="w-7 h-7 rounded-full bg-indigo-600 flex items-center justify-center shrink-0 mt-0.5">
          <Bot size={13} className="text-white" />
        </div>
      )}
      <div
        className={`max-w-[85%] px-3.5 py-2.5 rounded-2xl text-slate-700 shadow-sm ${
          isUser
            ? "bg-indigo-600 text-white rounded-br-sm"
            : "bg-white border border-slate-100 rounded-bl-sm"
        }`}
      >
        {isUser ? (
          <p className="text-[13px] leading-relaxed text-white">{msg.content}</p>
        ) : (
          <div className="text-slate-700">{renderMarkdown(msg.content)}</div>
        )}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Typing indicator
// ---------------------------------------------------------------------------

function TypingIndicator() {
  return (
    <div className="flex justify-start gap-2">
      <div className="w-7 h-7 rounded-full bg-indigo-600 flex items-center justify-center shrink-0">
        <Bot size={13} className="text-white" />
      </div>
      <div className="bg-white border border-slate-100 rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm">
        <div className="flex gap-1 items-center h-4">
          {[0, 1, 2].map((i) => (
            <span
              key={i}
              className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-bounce"
              style={{ animationDelay: `${i * 0.15}s` }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Quick action chips
// ---------------------------------------------------------------------------

function QuickActions({ onSelect }: { onSelect: (prompt: string) => void }) {
  return (
    <div className="flex flex-wrap gap-1.5 px-4 py-2">
      {QUICK_ACTIONS.map(({ icon: Icon, label, prompt }) => (
        <button
          key={label}
          onClick={() => onSelect(prompt)}
          className="flex items-center gap-1.5 text-[11px] font-medium px-2.5 py-1.5 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 hover:bg-indigo-100 transition-colors no-ripple"
        >
          <Icon size={11} />
          {label}
        </button>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Chat input bar
// ---------------------------------------------------------------------------

function ChatInput({
  onSend,
  disabled,
}: {
  onSend: (text: string) => void;
  disabled: boolean;
}) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  function submit() {
    const text = value.trim();
    if (!text || disabled) return;
    onSend(text);
    setValue("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
  }

  function onKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  function onInput() {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 120)}px`;
  }

  return (
    <div className="flex items-end gap-2 px-3 py-3 border-t border-slate-100 bg-white rounded-b-2xl">
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={onKeyDown}
        onInput={onInput}
        disabled={disabled}
        rows={1}
        placeholder="Ask me anything about your career…"
        className="flex-1 resize-none text-[13px] text-slate-700 placeholder-slate-400 border border-slate-200 rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-300 disabled:opacity-50 custom-scrollbar"
        style={{ minHeight: "38px", maxHeight: "120px" }}
      />
      <button
        onClick={submit}
        disabled={disabled || !value.trim()}
        className="w-9 h-9 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 flex items-center justify-center text-white shrink-0 transition-all no-ripple"
        aria-label="Send message"
      >
        {disabled ? (
          <Loader2 size={15} className="animate-spin" />
        ) : (
          <Send size={15} />
        )}
      </button>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main chatbot component (button + window)
// ---------------------------------------------------------------------------

export default function SkilloraChat() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [minimized, setMinimized] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME]);
  const [loading, setLoading] = useState(false);
  const [unread, setUnread] = useState(0);
  const [showQuickActions, setShowQuickActions] = useState(true);
  const bottomRef = useRef<HTMLDivElement>(null);
  const session = typeof window !== "undefined" ? getSession() : null;

  // Scroll to bottom on new messages
  useEffect(() => {
    if (open && !minimized) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, loading, open, minimized]);

  // Track unread count when closed
  useEffect(() => {
    if (!open) {
      const assistantCount = messages.filter((m) => m.role === "assistant").length - 1;
      setUnread(Math.max(0, assistantCount));
    } else {
      setUnread(0);
    }
  }, [open, messages]);

  const sendMessage = useCallback(
    async (text: string) => {
      if (!text.trim() || loading) return;

      setShowQuickActions(false);

      const userMsg: ChatMessage = {
        id: `u-${Date.now()}`,
        role: "user",
        content: text,
        ts: Date.now(),
      };
      setMessages((prev) => [...prev, userMsg]);
      setLoading(true);

      // Build history from existing messages (exclude welcome)
      const history = messages
        .filter((m) => m.id !== "welcome")
        .map((m) => ({ role: m.role, content: m.content }));

      try {
        const { reply } = await api.skillora.chat({
          user_id: session?.id ?? undefined,
          message: text,
          history,
          page_context: pathname ?? "",
        });

        const botMsg: ChatMessage = {
          id: `a-${Date.now()}`,
          role: "assistant",
          content: reply,
          ts: Date.now(),
        };
        setMessages((prev) => [...prev, botMsg]);
      } catch (e) {
        const errMsg: ChatMessage = {
          id: `err-${Date.now()}`,
          role: "assistant",
          content:
            "Sorry, I couldn't reach the server. Please make sure the backend is running and try again.",
          ts: Date.now(),
        };
        setMessages((prev) => [...prev, errMsg]);
      } finally {
        setLoading(false);
      }
    },
    [loading, messages, session, pathname]
  );

  function handleOpen() {
    setOpen(true);
    setMinimized(false);
    setUnread(0);
  }

  // Page-level context label for display
  const pageLabel = pathname?.replace("/", "") || "home";

  return (
    <>
      {/* ── Floating button ─────────────────────────────────────────────── */}
      {!open && (
        <button
          onClick={handleOpen}
          aria-label="Open Skillora AI Assistant"
          className="
            fixed bottom-6 right-6 z-50
            w-14 h-14 rounded-full
            bg-indigo-600 hover:bg-indigo-500
            shadow-lg hover:shadow-indigo-300/50 hover:shadow-xl
            flex items-center justify-center
            transition-all duration-200 hover:scale-105
            no-ripple
          "
        >
          <Bot size={24} className="text-white" />
          {unread > 0 && (
            <span className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-red-500 text-white text-[10px] font-bold flex items-center justify-center">
              {unread}
            </span>
          )}
        </button>
      )}

      {/* ── Chat window ──────────────────────────────────────────────────── */}
      {open && (
        <div
          className={`
            fixed bottom-6 right-6 z-50
            w-[370px] max-w-[calc(100vw-2rem)]
            bg-[#f8fafc] rounded-2xl shadow-2xl border border-slate-200
            flex flex-col overflow-hidden
            transition-all duration-300
            ${minimized ? "h-14" : "h-[580px] max-h-[calc(100vh-6rem)]"}
          `}
          role="dialog"
          aria-label="Skillora AI Assistant"
        >
          {/* ── Header ── */}
          <div className="flex items-center gap-2.5 px-4 py-3 bg-indigo-600 shrink-0">
            <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center shrink-0">
              <Bot size={16} className="text-white" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-bold text-white leading-none">Skillora AI Assistant</p>
              <p className="text-[10px] text-indigo-200 mt-0.5 leading-none">
                Your Personal Career &amp; Skill Guide
              </p>
            </div>
            <button
              onClick={() => setMinimized((m) => !m)}
              className="text-white/70 hover:text-white transition-colors p-1 no-ripple"
              aria-label={minimized ? "Expand chat" : "Minimize chat"}
            >
              {minimized ? (
                <ChevronDown size={16} className="rotate-180" />
              ) : (
                <Minimize2 size={15} />
              )}
            </button>
            <button
              onClick={() => setOpen(false)}
              className="text-white/70 hover:text-white transition-colors p-1 no-ripple"
              aria-label="Close chat"
            >
              <X size={16} />
            </button>
          </div>

          {!minimized && (
            <>
              {/* ── Messages ── */}
              <div className="flex-1 overflow-y-auto px-4 py-4 space-y-3 custom-scrollbar">
                {messages.map((msg) => (
                  <MessageBubble key={msg.id} msg={msg} />
                ))}
                {loading && <TypingIndicator />}
                <div ref={bottomRef} />
              </div>

              {/* ── Quick actions (only shown until user sends first message) ── */}
              {showQuickActions && (
                <QuickActions onSelect={sendMessage} />
              )}

              {/* ── Input ── */}
              <ChatInput onSend={sendMessage} disabled={loading} />
            </>
          )}
        </div>
      )}
    </>
  );
}
