import { CaseFilters } from '@/components/security/dispatch/case-filters'
import { CasesTable } from '@/components/security/dispatch/cases-table'
import { Breadcrumbs } from '@/components/shared/breadcrumbs'

const breadcrumbs = [
  { label: 'Security', href: '/security' },
  { label: 'Dispatch', href: '/security/dispatch' },
  { label: 'Cases', href: '/security/dispatch/cases' }
]

export default function CasesPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Investigation Cases</h1>
            <p className="text-gray-600 mt-1">Track and manage security investigation cases</p>
          </div>
          <button className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors">
            Create Case
          </button>
        </div>
      </div>

      <CaseFilters />
      <CasesTable />
    </div>
  )
}