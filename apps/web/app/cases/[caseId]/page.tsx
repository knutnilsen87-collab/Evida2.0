import Link from "next/link";
import { AssistantPanel } from "../../components/assistant-panel";
import { StatusBadge } from "@advokat-ai/ui";

const cards = [
  ["Dokumentgrunnlag", "Last opp dokumentene saken bygger pa.", "Last opp dokumenter"],
  ["Fakta og kilder", "Bygg pastander som kan spores til dokumenter.", "Fiks manglende kilder"],
  ["Kronologi", "Samle hendelser i riktig rekkefolge.", "Ny hendelse"],
  ["Risiko", "Se svake punkter rolig og konkret.", "Se risiko"],
  ["Utkast", "Skriv med kildekontroll i margen.", "Fortsett pa utkast"],
  ["Eksportstatus", "Eksport krever kontroll og godkjenning.", "Se hva som stopper eksport"]
];

export default function CaseOverview() {
  return (
    <main className="shell">
      <aside className="sidebar">
        <strong>Advokat AI</strong>
        <nav>
          <Link href="/cases">Saker</Link>
          <Link href="/cases/case-seed/documents">Dokumenter</Link>
          <Link href="/cases/case-seed/facts">Fakta</Link>
          <Link href="/cases/case-seed/drafts">Utkast</Link>
          <Link href="/cases/case-seed/audit">Audit</Link>
        </nav>
      </aside>
      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Saksrom</p>
            <h1>Pilot sak</h1>
          </div>
          <StatusBadge tone="warning">Neste steg: Last opp dokumenter</StatusBadge>
        </header>
        <div className="grid">
          {cards.map(([title, body, action]) => (
            <article className="panel" key={title}>
              <h2>{title}</h2>
              <p>{body}</p>
              <button>{action}</button>
            </article>
          ))}
        </div>
        <footer className="bottomStatus">Lagret lokalt. Kildedekning mangler for nye utkast. Eksport er ikke klar.</footer>
      </section>
      <AssistantPanel context="Saksoversikt" prompt="Spor meg om hva du bor gjore videre i saken." />
    </main>
  );
}
