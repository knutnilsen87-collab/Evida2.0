import { AssistantPanel } from "../../../components/assistant-panel";
import { StatusBadge } from "@advokat-ai/ui";

export default function DocumentsPage() {
  return (
    <main className="shell single">
      <section className="workspace">
        <header className="topbar">
          <div><p className="eyebrow">Dokumenter</p><h1>Dokumentgrunnlag</h1></div>
          <button className="primary">Last opp dokument</button>
        </header>
        <article className="panel">
          <h2>Last opp dokumentene saken bygger pa.</h2>
          <p>Nar dokumentene er lest, kan du markere kilder og lage faktapastander.</p>
          <StatusBadge tone="warning">Ma ses over ved usikker tekstlesing</StatusBadge>
        </article>
      </section>
      <AssistantPanel context="Dokumenter" prompt="Jeg kan forklare hva tekstlesing betyr og hvordan dokumentet blir klart som kilde." />
    </main>
  );
}
