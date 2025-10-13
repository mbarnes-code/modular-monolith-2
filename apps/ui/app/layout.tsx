import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Jane Monorepo UI',
  description: 'Next.js 15 + React 19 UI',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
