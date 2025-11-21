'use client'

import { useState } from 'react'

export function ResourceViewer() {
  const [selectedResource, setSelectedResource] = useState<string | null>(null)
  const [content, setContent] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  
  const sampleResources = [
    {
      uri: 'file:///config.json',
      name: 'config.json',
      type: 'application/json',
      content: {
        "app_name": "MCP Inspector",
        "version": "1.0.0",
        "settings": {
          "debug": true,
          "log_level": "info"
        }
      }
    },
    {
      uri: 'file:///readme.md',
      name: 'readme.md',
      type: 'text/markdown',
      content: "# MCP Inspector\n\nA tool for inspecting Model Context Protocol servers.\n\n## Features\n\n- Server connection management\n- Tool execution\n- Resource browsing\n- Real-time debugging"
    }
  ]
  
  const loadResource = async (uri: string) => {
    setLoading(true)
    setSelectedResource(uri)
    
    // Simulate API call
    setTimeout(() => {
      const resource = sampleResources.find(r => r.uri === uri)
      setContent(resource || null)
      setLoading(false)
    }, 1000)
  }
  
  const formatContent = (content: any, type: string) => {
    if (type === 'application/json') {
      return JSON.stringify(content, null, 2)
    }
    return content
  }
  
  return (
    <div className="bg-white border border-gray-200 rounded-lg">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-medium text-gray-900">Resource Content</h3>
            <p className="text-sm text-gray-600 mt-1">
              {selectedResource ? selectedResource : 'Select a resource to view its content'}
            </p>
          </div>
          {selectedResource && (
            <div className="flex gap-2">
              <button className="text-sm px-3 py-1 border border-gray-300 rounded hover:bg-gray-50">
                Download
              </button>
              <button className="text-sm px-3 py-1 border border-gray-300 rounded hover:bg-gray-50">
                Refresh
              </button>
            </div>
          )}
        </div>
      </div>
      
      <div className="p-4">
        {!selectedResource ? (
          <div className="space-y-2">
            <p className="text-sm text-gray-600 mb-4">Available resources:</p>
            {sampleResources.map((resource) => (
              <button
                key={resource.uri}
                onClick={() => loadResource(resource.uri)}
                className="block w-full text-left p-3 border border-gray-200 rounded hover:border-blue-300 hover:shadow-sm transition-all"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-gray-900">{resource.name}</div>
                    <div className="text-sm text-gray-500">{resource.uri}</div>
                  </div>
                  <span className="text-xs px-2 py-1 bg-gray-100 rounded">
                    {resource.type}
                  </span>
                </div>
              </button>
            ))}
          </div>
        ) : loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="text-gray-500">Loading resource content...</div>
          </div>
        ) : content ? (
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-900">{content.name}</span>
                <span className="text-xs px-2 py-1 bg-gray-100 rounded">{content.type}</span>
              </div>
              <button
                onClick={() => setSelectedResource(null)}
                className="text-sm text-gray-500 hover:text-gray-700"
              >
                ← Back to resources
              </button>
            </div>
            <div className="border border-gray-200 rounded">
              <pre className="p-4 text-sm overflow-auto max-h-96 bg-gray-50">
                {formatContent(content.content, content.type)}
              </pre>
            </div>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            Resource not found or failed to load
          </div>
        )}
      </div>
    </div>
  )
}