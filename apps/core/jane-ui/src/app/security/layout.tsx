import { Metadata } from 'next'
import { ReactNode } from 'react'

export const metadata: Metadata = {
  title: 'Security Tools - Jane Platform',
  description: 'Cybersecurity analysis and incident management tools',
}

interface SecurityLayoutProps {
  children: ReactNode
}

export default function SecurityLayout({ children }: SecurityLayoutProps) {
  return (
    <div className="security-domain">
      <nav className="domain-nav bg-red-50 border-b border-red-200 p-4">
        <h2 className="text-lg font-semibold text-red-900 mb-2">🔴 Security Domain</h2>
        <div className="flex gap-4 text-sm">
          <a href="/security/nemesis" className="text-red-700 hover:text-red-900 font-medium">🛡️ Nemesis</a>
          <a href="/security/cyberchef" className="text-red-700 hover:text-red-900">CyberChef</a>
          <a href="/security/dispatch" className="text-red-700 hover:text-red-900">Dispatch</a>
          <a href="/security/vnc" className="text-red-700 hover:text-red-900">VNC</a>
          <a href="/security/ghostwriter" className="text-red-700 hover:text-red-900">Ghostwriter</a>
          <a href="/security/misp" className="text-red-700 hover:text-red-900">MISP</a>
          <a href="/security/maltrail" className="text-red-700 hover:text-red-900">Maltrail</a>
        </div>
      </nav>
      <main className="security-content p-6">
        {children}
      </main>
    </div>
  )
}