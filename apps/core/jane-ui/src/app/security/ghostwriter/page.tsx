import { ActionCards } from '@/components/security/ghostwriter/action-cards'
import { RecentProjects } from '@/components/security/ghostwriter/recent-projects'
import { GhostwriterStats } from '@/components/security/ghostwriter/stats'
import { Breadcrumbs } from '@/components/shared/breadcrumbs'
import Link from 'next/link'

const breadcrumbs = [
  { label: 'Security', href: '/security' },
  { label: 'Ghostwriter', href: '/security/ghostwriter' }
]

export default function GhostwriterPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-red-100 rounded-lg">
            <span className="text-2xl">📝</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Ghostwriter</h1>
            <p className="text-gray-600">Penetration testing report generation and collaboration platform</p>
          </div>
        </div>
      </div>

      <GhostwriterStats />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <ActionCards />
        </div>
        
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Projects</h2>
          <RecentProjects />
        </div>
      </div>

      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link
          href="/security/ghostwriter/projects"
          className="group p-6 bg-white border border-gray-200 rounded-lg hover:border-red-300 hover:shadow-lg transition-all"
        >
          <div className="flex items-center mb-3">
            <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center mr-3">
              <span className="text-xl">🎯</span>
            </div>
            <h3 className="font-semibold text-gray-900 group-hover:text-red-600">
              Projects
            </h3>
          </div>
          <p className="text-gray-600 text-sm">
            Manage penetration testing projects, scopes, and team assignments
          </p>
        </Link>

        <Link
          href="/security/ghostwriter/reports"
          className="group p-6 bg-white border border-gray-200 rounded-lg hover:border-red-300 hover:shadow-lg transition-all"
        >
          <div className="flex items-center mb-3">
            <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center mr-3">
              <span className="text-xl">📊</span>
            </div>
            <h3 className="font-semibold text-gray-900 group-hover:text-red-600">
              Reports
            </h3>
          </div>
          <p className="text-gray-600 text-sm">
            Generate and collaborate on penetration testing reports
          </p>
        </Link>

        <Link
          href="/security/ghostwriter/findings"
          className="group p-6 bg-white border border-gray-200 rounded-lg hover:border-red-300 hover:shadow-lg transition-all"
        >
          <div className="flex items-center mb-3">
            <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center mr-3">
              <span className="text-xl">🔍</span>
            </div>
            <h3 className="font-semibold text-gray-900 group-hover:text-red-600">
              Findings Library
            </h3>
          </div>
          <p className="text-gray-600 text-sm">
            Browse and manage reusable security findings and templates
          </p>
        </Link>
      </div>
    </div>
  )
}