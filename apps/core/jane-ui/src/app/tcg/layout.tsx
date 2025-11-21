import { Metadata } from 'next'
import { ReactNode } from 'react'

export const metadata: Metadata = {
  title: 'TCG Tools - Jane Platform',
  description: 'Trading Card Game analysis and deck building tools',
}

interface TCGLayoutProps {
  children: ReactNode
}

export default function TCGLayout({ children }: TCGLayoutProps) {
  return (
    <div className="tcg-domain">
      <nav className="domain-nav bg-yellow-50 border-b border-yellow-200 p-4">
        <h2 className="text-lg font-semibold text-yellow-900 mb-2">🟡 TCG Domain</h2>
        <div className="flex gap-4 text-sm">
          <a href="/tcg/commander-spellbook" className="text-yellow-700 hover:text-yellow-900">Commander Spellbook</a>
          <a href="/tcg/client" className="text-yellow-700 hover:text-yellow-900">Client Tools</a>
        </div>
      </nav>
      <main className="tcg-content p-6">
        {children}
      </main>
    </div>
  )
}