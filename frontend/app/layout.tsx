import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "ContractShield AI — Know What You're Signing",
  description:
    "AI-powered contract risk analysis. Upload your NDA or contract and get instant risk flagging, severity scoring, and safer clause suggestions — in under 60 seconds.",
  keywords: [
    "contract analysis",
    "NDA review",
    "legal risk",
    "AI contract review",
    "clause library",
    "ContractShield",
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${jetbrainsMono.variable} h-full antialiased dark`}
    >
      <body className="min-h-full flex flex-col bg-[#0a0a0a] text-[#ededed] font-sans">
        {children}
      </body>
    </html>
  );
}
