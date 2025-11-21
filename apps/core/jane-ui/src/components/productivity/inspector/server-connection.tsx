'use client'

import { useState } from 'react'

export function ServerConnection() {
  const [connectionType, setConnectionType] = useState('stdio')
  
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Connect New Server</h3>
      
      <form className="space-y-4">
        <div>
          <label htmlFor="server-name" className="block text-sm font-medium text-gray-700 mb-1">
            Server Name
          </label>
          <input
            type="text"
            id="server-name"
            placeholder="e.g., File System Server"
            className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        
        <div>
          <label htmlFor="connection-type" className="block text-sm font-medium text-gray-700 mb-1">
            Connection Type
          </label>
          <select
            id="connection-type"
            value={connectionType}
            onChange={(e) => setConnectionType(e.target.value)}
            className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="stdio">Standard I/O</option>
            <option value="http">HTTP</option>
            <option value="websocket">WebSocket</option>
          </select>
        </div>
        
        {connectionType === 'stdio' ? (
          <div>
            <label htmlFor="command" className="block text-sm font-medium text-gray-700 mb-1">
              Command
            </label>
            <input
              type="text"
              id="command"
              placeholder="path/to/server-executable"
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        ) : (
          <div>
            <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-1">
              URL
            </label>
            <input
              type="url"
              id="url"
              placeholder="http://localhost:3000/mcp"
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        )}
        
        <div>
          <label htmlFor="args" className="block text-sm font-medium text-gray-700 mb-1">
            Arguments (optional)
          </label>
          <input
            type="text"
            id="args"
            placeholder="--arg1 value1 --arg2 value2"
            className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        
        <div>
          <label className="flex items-center">
            <input
              type="checkbox"
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="ml-2 text-sm text-gray-700">Auto-reconnect on disconnect</span>
          </label>
        </div>
        
        <div className="flex gap-2">
          <button
            type="submit"
            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
          >
            Connect
          </button>
          <button
            type="button"
            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Test
          </button>
        </div>
      </form>
    </div>
  )
}