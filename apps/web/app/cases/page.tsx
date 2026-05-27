import Link from "next/link";
import { AssistantPanel } from "../components/assistant-panel";
import { StatusBadge } from "@advokat-ai/ui";

const cases = [
  {
    id: "case-seed",
    title: "Pilot sak",
    status: "Aktiv",
    documents: 0,
    missingSources: 0,
    risks: 0,
    nextAction: "Last opp dokumenter"
  }
];

export default function CasesPage() {
  return (
    <main className="shell">
      <aside className="sidebar">
        <strong>Advokat AI</strong>
        <nav>
          <Link href="/cases">Saker</Link>
          <Link href="/settings">Innstillinger</Link>
        </nav>
      </aside>
      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Saker</p>
            <h1>Velg sak</h1>
          </div>
          <Link className="primary" href="/cases/new">Ny sak</Link>
        </header>
        <div className="toolbar">
          <input aria-label="Sok etter sak" placeholder="Sok etter sak" />
          <StatusBadge tone="ready">Kun saker du har tilgang til</StatusBadge>
        </div>
        <div className="caseList">
          {cases.map((item) => (
            <Link className="caseCard" href={`/cases/${item.id}`} key={item.id}>
              <div>
                <h2>{item.title}</h2>
                <p>Neste steg: {item.nextAction}</p>
              </div>
              <div className="metrics">
                <span>{item.documents} dokumenter</span>
                <span>{item.missingSources} mangler kilde</span>
                <span>{item.risks} risiko</span>
              </div>
            </Link>
          ))}
        </div>
      </section>
      <AssistantPanel context="Saksliste" prompt="Jeg kan forklare hvordan en sak bygges opp her." />
    </main>
  );
}
