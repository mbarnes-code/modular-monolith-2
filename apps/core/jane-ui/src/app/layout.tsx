import type { Metadata, Viewport } from 'next';
import React from 'react';
import ServiceWorkerRegistration from '../components/PWA/ServiceWorkerRegistration';

export const metadata: Metadata = {
  title: {
    default: 'Jane Mental Prosthetic Platform',
    template: '%s | Jane Platform',
  },
  description: 'Executive function support platform consolidating 37 tools for ADHD/autism assistance',
  keywords: ['executive function', 'ADHD', 'autism', 'productivity', 'security', 'mental prosthetic'],
  authors: [{ name: 'Jane Platform Team' }],
  creator: 'Jane Platform',
  publisher: 'Jane Platform',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  // PWA metadata
  manifest: '/manifest.json',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'Jane Platform',
  },
  // Open Graph metadata
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: '/',
    title: 'Jane Mental Prosthetic Platform',
    description: 'Executive function support platform consolidating 37 tools for ADHD/autism assistance',
    siteName: 'Jane Platform',
  },
  // Twitter Card metadata
  twitter: {
    card: 'summary_large_image',
    title: 'Jane Mental Prosthetic Platform',
    description: 'Executive function support platform consolidating 37 tools for ADHD/autism assistance',
  },
  // Icons
  icons: {
    icon: [
      { url: '/icons/icon-192x192.png', sizes: '192x192', type: 'image/png' },
      { url: '/icons/icon-512x512.png', sizes: '512x512', type: 'image/png' },
    ],
    apple: [
      { url: '/icons/icon-180x180.png', sizes: '180x180', type: 'image/png' },
    ],
  },
};

export const viewport: Viewport = {
  themeColor: '#2563eb',
  colorScheme: 'light dark',
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false, // ADHD-friendly: prevent accidental zoom
  viewportFit: 'cover',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        {/* PWA theme color for status bar */}
        <meta name="theme-color" content="#2563eb" />
        <meta name="msapplication-TileColor" content="#2563eb" />
        
        {/* iOS PWA support */}
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="Jane Platform" />
        
        {/* Disable iOS phone number detection (executive function focus) */}
        <meta name="format-detection" content="telephone=no" />
        
        {/* Preconnect to potential external services */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body>
        {children}
        <ServiceWorkerRegistration />
      </body>
    </html>
  );
}
