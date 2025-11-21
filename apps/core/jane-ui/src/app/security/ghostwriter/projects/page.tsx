import { ProjectsFilter } from '@/components/security/ghostwriter/projects-filter'
import { ProjectsTable } from '@/components/security/ghostwriter/projects-table'
import { Breadcrumbs } from '@/components/shared/breadcrumbs'

const breadcrumbs = [
  { label: 'Security', href: '/security' },
  { label: 'Ghostwriter', href: '/security/ghostwriter' },
  { label: 'Projects', href: '/security/ghostwriter/projects' }
]

export default function ProjectsPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
            <p className="text-gray-600 mt-1">Manage penetration testing projects and engagements</p>
          </div>
          <button className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors">
            New Project
          </button>
        </div>
      </div>

      <ProjectsFilter />
      <ProjectsTable />
    </div>
  )
}