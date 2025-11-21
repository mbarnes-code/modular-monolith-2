import { Metadata } from 'next'
import { ReactNode } from 'react'

export const metadata: Metadata = {
  title: 'Productivity Tools - Jane Platform',
  description: 'Workflow automation and personal productivity applications',
}

interface ProductivityLayoutProps {
  children: ReactNode
}

export default function ProductivityLayout({ children }: ProductivityLayoutProps) {
  return (
    <div className="productivity-domain">
      <nav className="domain-nav bg-green-50 border-b border-green-200 p-4">
        <h2 className="text-lg font-semibold text-green-900 mb-2">🟢 Productivity Domain</h2>
        <div className="flex gap-4 text-sm">
          <a href="/productivity/actual" className="text-green-700 hover:text-green-900">Actual Budget</a>
          <a href="/productivity/n8n" className="text-green-700 hover:text-green-900">n8n</a>
          <a href="/productivity/mealie" className="text-green-700 hover:text-green-900">Mealie</a>
          <a href="/productivity/inspector" className="text-green-700 hover:text-green-900">Inspector</a>
          <a href="/productivity/onex" className="text-green-700 hover:text-green-900">OneX</a>
          <a href="/productivity/dashboard" className="text-green-700 hover:text-green-900">Dashboard</a>
        </div>
      </nav>
      <main className="productivity-content p-6">
        {children}
      </main>
    </div>
  )
}