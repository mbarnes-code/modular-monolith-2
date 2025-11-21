import { QuickActions } from '@/components/security/dispatch/quick-actions'
import { RecentIncidents } from '@/components/security/dispatch/recent-incidents'
import { DispatchStats } from '@/components/security/dispatch/stats'
import { Breadcrumbs } from '@/components/shared/breadcrumbs'
import Link from 'next/link'

const breadcrumbs = [
  { label: 'Security', href: '/security' },
  { label: 'Dispatch', href: '/security/dispatch' }
]

export default function DispatchPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-red-100 rounded-lg">
            <span className="text-2xl">🚨</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dispatch</h1>
            <p className="text-gray-600">Incident management and response coordination platform</p>
          </div>
        </div>
      </div>

      <DispatchStats />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <QuickActions />
        </div>
        
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Incidents</h2>
          <RecentIncidents />
        </div>
      </div>

      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link
          href="/security/dispatch/incidents"
          className="group p-6 bg-white border border-gray-200 rounded-lg hover:border-red-300 hover:shadow-lg transition-all"
        >
          <div className="flex items-center mb-3">
            <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center mr-3">
              <span className="text-xl">🚨</span>
            </div>
            <h3 className="font-semibold text-gray-900 group-hover:text-red-600">
              Incidents
            </h3>
          </div>
          <p className="text-gray-600 text-sm">
            Manage security incidents, coordinate response teams, and track resolution progress
          </p>
        </Link>

        <Link
          href="/security/dispatch/cases"
          className="group p-6 bg-white border border-gray-200 rounded-lg hover:border-red-300 hover:shadow-lg transition-all"
        >
          <div className="flex items-center mb-3">
            <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center mr-3">
              <span className="text-xl">📁</span>
            </div>
            <h3 className="font-semibold text-gray-900 group-hover:text-red-600">
              Cases
            </h3>
          </div>
          <p className="text-gray-600 text-sm">
            Track investigation cases, collect evidence, and manage case workflows
          </p>
        </Link>

        <Link
          href="/security/dispatch/dashboard"
          className="group p-6 bg-white border border-gray-200 rounded-lg hover:border-red-300 hover:shadow-lg transition-all"
        >
          <div className="flex items-center mb-3">
            <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center mr-3">
              <span className="text-xl">📊</span>
            </div>
            <h3 className="font-semibold text-gray-900 group-hover:text-red-600">
              Analytics
            </h3>
          </div>
          <p className="text-gray-600 text-sm">
            View incident trends, response metrics, and performance analytics
          </p>
        </Link>
      </div>
    </div>
  )
}