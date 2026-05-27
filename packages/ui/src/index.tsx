import type { ReactNode } from "react";

type Tone = "ready" | "warning" | "blocked";

const colors: Record<Tone, { bg: string; fg: string; bd: string }> = {
  ready: { bg: "#e8f5f1", fg: "#0f766e", bd: "#9ed6cc" },
  warning: { bg: "#fff7dd", fg: "#9a6700", bd: "#f0d177" },
  blocked: { bg: "#fff0ed", fg: "#b42318", bd: "#f3b0a8" }
};

export function StatusBadge({ tone, children }: { tone: Tone; children: ReactNode }) {
  const c = colors[tone];
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        minHeight: 28,
        borderRadius: 999,
        border: `1px solid ${c.bd}`,
        background: c.bg,
        color: c.fg,
        padding: "0 10px",
        fontSize: 13,
        fontWeight: 700
      }}
    >
      {children}
    </span>
  );
}
