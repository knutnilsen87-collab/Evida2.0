import Link from "next/link";
import { StatusBadge } from "@advokat-ai/ui";

export default function HomePage() {
  return (
    <main className="login">
      <section className="loginPanel">
        <p className="eyebrow">Advokat AI</p>
        <h1>Sikkert juridisk saksrom for dokumentdrevet arbeid.</h1>
        <p>Arbeid med dokumenter, fakta, kilder, utkast og eksport i en kontrollert flyt.</p>
        <div className="row">
          <StatusBadge tone="ready">Pilotklar arbeidsflate</StatusBadge>
          <StatusBadge tone="warning">Menneskelig godkjenning</StatusBadge>
        </div>
        <Link className="primary" href="/cases">Logg inn</Link>
      </section>
    </main>
  );
}
