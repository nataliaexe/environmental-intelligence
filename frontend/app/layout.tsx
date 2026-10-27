import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cortex | Inteligência Ambiental",
  description:
    "Monitore a saúde do ecossistema, acompanhe alertas ambientais e explore cenários de resiliência.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="pt-BR" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
