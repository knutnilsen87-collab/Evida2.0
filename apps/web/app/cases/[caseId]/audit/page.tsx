import { StatusBadge } from "@advokat-ai/ui";

export default function AuditPage() {
  return (
    <main className="shell single">
      <section className="workspace">
        <header className="topbar">
          <div><p className="eyebrow">Audit</p><h1>Sporbarhet</h1></div>
          <StatusBadge tone="ready">Kun autoriserte roller</StatusBadge>
        </header>
        <table>
          <thead><tr><th>Handling</th><th>Objekt</th><th>Tid</th></tr></thead>
          <tbody><tr><td>Sak apnet</td><td>Case</td><td>Na</td></tr></tbody>
        </table>
      </section>
    </main>
  );
}
