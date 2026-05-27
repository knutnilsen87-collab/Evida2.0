import { AssistantPanel } from "../../../components/assistant-panel";
import { StatusBadge } from "@advokat-ai/ui";

export default function FactsPage() {
  return (
    <main className="shell single">
      <section className="workspace">
        <header className="topbar">
          <div><p className="eyebrow">Fakta</p><h1>Fakta og kilder</h1></div>
          <button className="primary">Ny faktapastand</button>
        </header>
        <article className="panel">
          <h2>Avtalen ble signert.</h2>
          <p>Koble pastanden til riktig dokument, side eller tekstutdrag.</p>
          <StatusBadge tone="blocked">Mangler kilde</StatusBadge>
        </article>
      </section>
      <AssistantPanel context="Fakta" prompt="Jeg kan forklare forskjellen pa dokumentert, antatt og omtvistet." />
    </main>
  );
}
