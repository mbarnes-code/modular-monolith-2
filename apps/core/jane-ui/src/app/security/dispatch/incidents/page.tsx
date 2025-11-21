import { IncidentFilters } from '@/components/security/dispatch/incident-filters'
import { IncidentsTable } from '@/components/security/dispatch/incidents-table'
import { Breadcrumbs } from '@/components/shared/breadcrumbs'

const breadcrumbs = [
  { label: 'Security', href: '/security' },
  { label: 'Dispatch', href: '/security/dispatch' },
  { label: 'Incidents', href: '/security/dispatch/incidents' }
]

export default function IncidentsPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Security Incidents</h1>
            <p className="text-gray-600 mt-1">Manage and coordinate security incident response</p>
          </div>
          <button className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors">
            Create Incident
          </button>
        </div>
      </div>

      <IncidentFilters />
      <IncidentsTable />
    </div>
  )
}