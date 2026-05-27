import Link from "next/link";
import { AssistantPanel } from "../../../components/assistant-panel";
import { StatusBadge } from "@advokat-ai/ui";

export default function DraftsPage() {
  return (
    <main className="shell single">
      <section className="workspace">
        <header className="topbar">
          <div><p className="eyebrow">Utkast</p><h1>Juridiske utkast</h1></div>
          <Link className="primary" href="/cases/case-seed/drafts/draft-seed">Nytt utkast</Link>
        </header>
        <article className="panel">
          <h2>Prosesskriv</h2>
          <p>Kildedekning ma kontrolleres for eksport.</p>
          <StatusBadge tone="warning">Krever gjennomgang</StatusBadge>
        </article>
      </section>
      <AssistantPanel context="Utkast" prompt="Jeg kan sjekke arbeidet og vise hva som mangler for eksport." />
    </main>
  );
}
