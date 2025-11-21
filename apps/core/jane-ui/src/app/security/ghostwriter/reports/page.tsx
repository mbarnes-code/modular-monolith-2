import { ReportsFilter } from '@/components/security/ghostwriter/reports-filter'
import { ReportsTable } from '@/components/security/ghostwriter/reports-table'
import { Breadcrumbs } from '@/components/shared/breadcrumbs'

const breadcrumbs = [
  { label: 'Security', href: '/security' },
  { label: 'Ghostwriter', href: '/security/ghostwriter' },
  { label: 'Reports', href: '/security/ghostwriter/reports' }
]

export default function ReportsPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Reports</h1>
            <p className="text-gray-600 mt-1">Generate and collaborate on penetration testing reports</p>
          </div>
          <button className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors">
            New Report
          </button>
        </div>
      </div>

      <ReportsFilter />
      <ReportsTable />
    </div>
  )
}