import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SkillGap Engine",
  description:
    "Competency-based skill gap analysis and personalised course recommendations",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 text-slate-900">
        {children}
      </body>
    </html>
  );
}
