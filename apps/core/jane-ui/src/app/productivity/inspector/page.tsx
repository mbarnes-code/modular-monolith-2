import Link from 'next/link'
import { Breadcrumbs } from '@/components/shared/breadcrumbs'
import { InspectorStats } from '@/components/productivity/inspector/stats'
import { ServersList } from '@/components/productivity/inspector/servers-list'
import { QuickActions } from '@/components/productivity/inspector/quick-actions'

const breadcrumbs = [
  { label: 'Productivity', href: '/productivity' },
  { label: 'MCP Inspector', href: '/productivity/inspector' }
]

export default function InspectorPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg">
            <span className="text-2xl">🔍</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">MCP Inspector</h1>
            <p className="text-gray-600">Model Context Protocol server inspection and debugging platform</p>
          </div>
        </div>
      </div>

      <InspectorStats />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <QuickActions />
        </div>
        
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Connected Servers</h2>
          <ServersList />
        </div>
      </div>

      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link
          href="/productivity/inspector/servers"
          className="group p-6 bg-white border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-lg transition-all"
        >
          <div className="flex items-center mb-3">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
              <span className="text-xl">🖥️</span>
            </div>
            <h3 className="font-semibold text-gray-900 group-hover:text-blue-600">
              Servers
            </h3>
          </div>
          <p className="text-gray-600 text-sm">
            Connect to and debug MCP servers, inspect capabilities and authentication
          </p>
        </Link>

        <Link
          href="/productivity/inspector/tools"
          className="group p-6 bg-white border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-lg transition-all"
        >
          <div className="flex items-center mb-3">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
              <span className="text-xl">🛠️</span>
            </div>
            <h3 className="font-semibold text-gray-900 group-hover:text-blue-600">
              Tools
            </h3>
          </div>
          <p className="text-gray-600 text-sm">
            Execute and test MCP tools with interactive parameter forms
          </p>
        </Link>

        <Link
          href="/productivity/inspector/resources"
          className="group p-6 bg-white border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-lg transition-all"
        >
          <div className="flex items-center mb-3">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
              <span className="text-xl">📂</span>
            </div>
            <h3 className="font-semibold text-gray-900 group-hover:text-blue-600">
              Resources
            </h3>
          </div>
          <p className="text-gray-600 text-sm">
            Browse and read MCP resources with template support
          </p>
        </Link>
      </div>
    </div>
  )
}