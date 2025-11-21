'use client'

export function ToolsGrid() {
  const tools = [
    {
      name: 'read_file',
      description: 'Read contents of a file',
      server: 'File System Server',
      schema: {
        type: 'object',
        properties: {
          path: { type: 'string', description: 'Path to the file' }
        }
      }
    },
    {
      name: 'write_file',
      description: 'Write content to a file',
      server: 'File System Server',
      schema: {
        type: 'object',
        properties: {
          path: { type: 'string', description: 'Path to the file' },
          content: { type: 'string', description: 'Content to write' }
        }
      }
    },
    {
      name: 'sql_query',
      description: 'Execute SQL query',
      server: 'SQLite Server',
      schema: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'SQL query to execute' }
        }
      }
    },
    {
      name: 'search_web',
      description: 'Search the web',
      server: 'Web Search Server',
      schema: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'Search query' },
          limit: { type: 'number', description: 'Number of results' }
        }
      }
    }
  ]

  return (
    <div className="bg-white border border-gray-200 rounded-lg">
      <div className="p-4 border-b border-gray-200">
        <input
          type="text"
          placeholder="Search tools..."
          className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>
      <div className="divide-y divide-gray-200 max-h-96 overflow-y-auto">
        {tools.map((tool, index) => (
          <div key={index} className="p-4 hover:bg-gray-50 cursor-pointer">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h4 className="text-sm font-medium text-gray-900 mb-1">
                  {tool.name}
                </h4>
                <p className="text-sm text-gray-600 mb-2">
                  {tool.description}
                </p>
                <div className="flex items-center text-xs text-gray-500">
                  <span className="px-2 py-1 bg-gray-100 rounded">{tool.server}</span>
                  <span className="ml-2">
                    {Object.keys(tool.schema.properties || {}).length} parameters
                  </span>
                </div>
              </div>
              <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                Execute
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}