import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SmartShelf",
  description: "Computer vision powered smart inventory tracking.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}