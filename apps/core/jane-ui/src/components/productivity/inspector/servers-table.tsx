'use client'

export function ServersTable() {
  const servers = [
    {
      id: 1,
      name: 'File System Server',
      status: 'Connected',
      type: 'stdio',
      url: 'stdio://path/to/filesystem-server',
      version: '1.0.0',
      tools: 8,
      resources: 45,
      lastPing: '2 seconds ago'
    },
    {
      id: 2,
      name: 'SQLite Server',
      status: 'Connected',
      type: 'stdio',
      url: 'stdio://path/to/sqlite-server',
      version: '1.2.1',
      tools: 12,
      resources: 3,
      lastPing: '1 minute ago'
    },
    {
      id: 3,
      name: 'Web Search Server',
      status: 'Disconnected',
      type: 'http',
      url: 'http://localhost:3001/mcp',
      version: '0.9.5',
      tools: 5,
      resources: 0,
      lastPing: '5 minutes ago'
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
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Server
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Capabilities
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Last Ping
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {servers.map((server) => (
              <tr key={server.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div>
                    <div className="text-sm font-medium text-gray-900">
                      {server.name}
                    </div>
                    <div className="text-sm text-gray-500">{server.version}</div>
                    <div className="text-xs text-gray-400 font-mono">
                      {server.url}
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(server.status)}`}
                  >
                    {server.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">
                    {server.tools} tools, {server.resources} resources
                  </div>
                  <div className="text-xs text-gray-500">
                    Type: {server.type}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">{server.lastPing}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div className="flex gap-2">
                    <button className="text-blue-600 hover:text-blue-900">Inspect</button>
                    <button className="text-green-600 hover:text-green-900">Ping</button>
                    <button className="text-red-600 hover:text-red-900">Disconnect</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}