'use client'

import Link from 'next/link'

export function ServersList() {
  const servers = [
    {
      id: 1,
      name: 'File System Server',
      status: 'Connected',
      url: 'stdio://path/to/filesystem-server',
      tools: 8,
      resources: 45
    },
    {
      id: 2,
      name: 'SQLite Server',
      status: 'Connected',
      url: 'stdio://path/to/sqlite-server',
      tools: 12,
      resources: 3
    },
    {
      id: 3,
      name: 'Web Search Server',
      status: 'Disconnected',
      url: 'stdio://path/to/search-server',
      tools: 5,
      resources: 0
    }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Connected':
        return 'bg-green-100 text-green-800'
      case 'Disconnected':
        return 'bg-red-100 text-red-800'
      case 'Connecting':
        return 'bg-yellow-100 text-yellow-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-medium text-gray-900">Connected Servers</h3>
          <Link
            href="/productivity/inspector/servers"
            className="text-blue-600 hover:text-blue-700 text-sm font-medium"
          >
            View all
          </Link>
        </div>
      </div>
      <div className="divide-y divide-gray-200">
        {servers.map((server) => (
          <div key={server.id} className="px-6 py-4 hover:bg-gray-50">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <h4 className="text-sm font-medium text-gray-900 mb-1">
                  {server.name}
                </h4>
                <div className="flex items-center gap-3 text-sm text-gray-500 mb-2">
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(server.status)}`}
                  >
                    {server.status}
                  </span>
                  <span>{server.tools} tools</span>
                  <span>{server.resources} resources</span>
                </div>
                <p className="text-xs text-gray-400 font-mono">
                  {server.url}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}