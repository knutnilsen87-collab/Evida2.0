import type { Metadata } from "next";
import "./styles.css";

export const metadata: Metadata = {
  title: "Advokat AI",
  description: "Sikkert juridisk saksrom for dokumentdrevet arbeid."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="nb">
      <body>{children}</body>
    </html>
  );
}
