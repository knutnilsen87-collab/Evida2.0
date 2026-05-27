import Link from "next/link";
import { AssistantPanel } from "../../components/assistant-panel";

export default function NewCasePage() {
  return (
    <main className="shell">
      <aside className="sidebar">
        <strong>Advokat AI</strong>
        <nav><Link href="/cases">Tilbake</Link></nav>
      </aside>
      <section className="workspace narrow">
        <header className="topbar">
          <div>
            <p className="eyebrow">Ny sak</p>
            <h1>Start med en enkel arbeidstittel</h1>
          </div>
        </header>
        <form className="form">
          <label>Tittel<input defaultValue="Ny pilotsak" /></label>
          <label>Sakstype<input defaultValue="Sivil sak" /></label>
          <label>Jurisdiksjon<input defaultValue="NO" /></label>
          <label>Beskrivelse<textarea placeholder="Kort notat om saken" /></label>
          <label>Sensitivitet<select defaultValue="standard"><option value="standard">Standard</option><option value="sensitive">Sensitiv</option></select></label>
          <Link className="primary" href="/cases/case-seed">Opprett sak</Link>
        </form>
      </section>
      <AssistantPanel context="Ny sak" prompt="Det holder a fylle inn en enkel arbeidstittel na. Du kan justere detaljene senere." />
    </main>
  );
}
