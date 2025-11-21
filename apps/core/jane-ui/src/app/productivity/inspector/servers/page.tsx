import { Breadcrumbs } from '@/components/shared/breadcrumbs'
import { ServersTable } from '@/components/productivity/inspector/servers-table'
import { ServerConnection } from '@/components/productivity/inspector/server-connection'

const breadcrumbs = [
  { label: 'Productivity', href: '/productivity' },
  { label: 'MCP Inspector', href: '/productivity/inspector' },
  { label: 'Servers', href: '/productivity/inspector/servers' }
]

export default function ServersPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">MCP Servers</h1>
            <p className="text-gray-600 mt-1">Connect to and manage Model Context Protocol servers</p>
          </div>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
            Connect Server
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1">
          <ServerConnection />
        </div>
        <div className="lg:col-span-2">
          <ServersTable />
        </div>
      </div>
    </div>
  )
}