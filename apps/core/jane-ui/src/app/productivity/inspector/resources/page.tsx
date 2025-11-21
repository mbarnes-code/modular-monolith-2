import { Breadcrumbs } from '@/components/shared/breadcrumbs'
import { ResourcesTree } from '@/components/productivity/inspector/resources-tree'
import { ResourceViewer } from '@/components/productivity/inspector/resource-viewer'

const breadcrumbs = [
  { label: 'Productivity', href: '/productivity' },
  { label: 'MCP Inspector', href: '/productivity/inspector' },
  { label: 'Resources', href: '/productivity/inspector/resources' }
]

export default function ResourcesPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">MCP Resources</h1>
            <p className="text-gray-600 mt-1">Browse and read Model Context Protocol resources</p>
          </div>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
            Refresh Resources
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Resource Tree</h2>
          <ResourcesTree />
        </div>
        <div className="lg:col-span-2">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Resource Content</h2>
          <ResourceViewer />
        </div>
      </div>
    </div>
  )
}