import { Breadcrumbs } from '@/components/shared/breadcrumbs'
import { ToolsGrid } from '@/components/productivity/inspector/tools-grid'
import { ToolExecution } from '@/components/productivity/inspector/tool-execution'

const breadcrumbs = [
  { label: 'Productivity', href: '/productivity' },
  { label: 'MCP Inspector', href: '/productivity/inspector' },
  { label: 'Tools', href: '/productivity/inspector/tools' }
]

export default function ToolsPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">MCP Tools</h1>
            <p className="text-gray-600 mt-1">Execute and test Model Context Protocol tools</p>
          </div>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
            Refresh Tools
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Available Tools</h2>
          <ToolsGrid />
        </div>
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Tool Execution</h2>
          <ToolExecution />
        </div>
      </div>
    </div>
  )
}