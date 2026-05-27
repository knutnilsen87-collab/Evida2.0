import { AssistantPanel } from "../../../components/assistant-panel";
import { StatusBadge } from "@advokat-ai/ui";

export default function ExportPreviewPage() {
  return (
    <main className="shell single">
      <section className="workspace">
        <header className="topbar">
          <div><p className="eyebrow">Eksportkontroll</p><h1>Eksport er stoppet</h1></div>
          <StatusBadge tone="blocked">Stoppet</StatusBadge>
        </header>
        <article className="panel">
          <h2>Dette ma ryddes forst</h2>
          <p>Et avsnitt mangler kilde. Koble avsnittet til dokument, side eller tekstutdrag.</p>
          <button>Ga til forste problem</button>
        </article>
      </section>
      <AssistantPanel context="Eksportkontroll" prompt="Jeg kan forklare hvorfor eksport er stoppet og ga gjennom punktene med deg." />
    </main>
  );
}
