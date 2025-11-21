import { FindingsFilter } from '@/components/security/ghostwriter/findings-filter'
import { FindingsTable } from '@/components/security/ghostwriter/findings-table'
import { Breadcrumbs } from '@/components/shared/breadcrumbs'

const breadcrumbs = [
  { label: 'Security', href: '/security' },
  { label: 'Ghostwriter', href: '/security/ghostwriter' },
  { label: 'Findings', href: '/security/ghostwriter/findings' }
]

export default function FindingsPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Findings Library</h1>
            <p className="text-gray-600 mt-1">Browse and manage reusable security findings and templates</p>
          </div>
          <button className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors">
            New Finding
          </button>
        </div>
      </div>

      <FindingsFilter />
      <FindingsTable />
    </div>
  )
}