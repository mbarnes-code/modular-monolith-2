import { IncidentMetrics } from '@/components/security/dispatch/incident-metrics'
import { ResponseTimes } from '@/components/security/dispatch/response-times'
import { TeamPerformance } from '@/components/security/dispatch/team-performance'
import { Breadcrumbs } from '@/components/shared/breadcrumbs'

const breadcrumbs = [
  { label: 'Security', href: '/security' },
  { label: 'Dispatch', href: '/security/dispatch' },
  { label: 'Analytics', href: '/security/dispatch/dashboard' }
]

export default function DashboardPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Incident Analytics</h1>
            <p className="text-gray-600 mt-1">Performance metrics and incident trends analysis</p>
          </div>
          <button className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors">
            Export Report
          </button>
        </div>
      </div>

      <div className="space-y-8">
        <IncidentMetrics />
        <ResponseTimes />
        <TeamPerformance />
      </div>
    </div>
  )
}