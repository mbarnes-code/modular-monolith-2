import { Metadata } from 'next'
import { ReactNode } from 'react'

export const metadata: Metadata = {
  title: 'AI Tools - Jane Platform',
  description: 'Artificial intelligence and development agent tools',
}

interface AILayoutProps {
  children: ReactNode
}

export default function AILayout({ children }: AILayoutProps) {
  return (
    <div className="ai-domain">
      <nav className="domain-nav bg-blue-50 border-b border-blue-200 p-4">
        <h2 className="text-lg font-semibold text-blue-900 mb-2">🔵 AI Domain</h2>
        <div className="flex gap-4 text-sm">
          <a href="/ai/goose" className="text-blue-700 hover:text-blue-900">Goose Agent</a>
          <a href="/ai/docs" className="text-blue-700 hover:text-blue-900">Documentation</a>
          <a href="/ai/firecrawl" className="text-blue-700 hover:text-blue-900">Firecrawl</a>
          <a href="/ai/monitoring" className="text-blue-700 hover:text-blue-900">Monitoring</a>
        </div>
      </nav>
      <main className="ai-content p-6">
        {children}
      </main>
    </div>
  )
}