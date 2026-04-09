import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: process.env.NEXT_PUBLIC_APP_NAME || "DeFi Risk Auditor",
  description: process.env.NEXT_PUBLIC_APP_DESCRIPTION || "TEE-verified DeFi protocol risk analysis with on-chain proof",
  keywords: ["DeFi", "risk analysis", "blockchain", "security", "audit", "OpenGradient", "TEE"],
  authors: [{ name: "DeFi Risk Auditor Team" }],
  openGraph: {
    type: "website",
    title: "DeFi Risk Auditor",
    description: "TEE-verified DeFi protocol risk analysis with on-chain proof",
    siteName: "DeFi Risk Auditor",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen bg-gradient-to-b from-gray-50 to-gray-100`}>
        <div className="flex min-h-screen flex-col">
          <Header />
          <main className="flex-1 container mx-auto px-4 py-8">
            {children}
          </main>
          <Footer />
        </div>
      </body>
    </html>
  );
}