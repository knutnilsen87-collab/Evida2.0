import Link from "next/link";
import { AssistantPanel } from "../../../../components/assistant-panel";
import { StatusBadge } from "@advokat-ai/ui";

export default function DraftEditorPage() {
  return (
    <main className="shell">
      <section className="workspace editor">
        <header className="topbar">
          <div><p className="eyebrow">Utkast</p><h1>Prosesskriv</h1></div>
          <Link className="primary" href="/cases/case-seed/export-preview">Se hva som mangler</Link>
        </header>
        <div className="draft">
          <aside className="gutter"><StatusBadge tone="blocked">Mangler kilde</StatusBadge></aside>
          <article className="paper">
            <h2>Faktum</h2>
            <p>Dette avsnittet mangler kilde.</p>
            <p>Marker dokumentgrunnlag for a gjore avsnittet klart.</p>
          </article>
        </div>
      </section>
      <AssistantPanel context="Utkastredigering" prompt="Jeg kan sjekke arbeidet og ga gjennom manglende kilder med deg." />
    </main>
  );
}
