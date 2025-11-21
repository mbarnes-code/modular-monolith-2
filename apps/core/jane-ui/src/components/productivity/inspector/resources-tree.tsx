'use client'

import { useState } from 'react'

export function ResourcesTree() {
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set())
  
  const resources = [
    {
      uri: 'file:///',
      name: 'File System',
      type: 'folder',
      children: [
        { uri: 'file:///documents', name: 'documents', type: 'folder' },
        { uri: 'file:///projects', name: 'projects', type: 'folder' },
        { uri: 'file:///config.json', name: 'config.json', type: 'file' }
      ]
    },
    {
      uri: 'sqlite:///',
      name: 'SQLite Databases',
      type: 'folder',
      children: [
        { uri: 'sqlite:///app.db', name: 'app.db', type: 'database' },
        { uri: 'sqlite:///users.db', name: 'users.db', type: 'database' }
      ]
    },
    {
      uri: 'web:///',
      name: 'Web Resources',
      type: 'folder',
      children: [
        { uri: 'web:///search/results', name: 'Search Results', type: 'resource' },
        { uri: 'web:///cache', name: 'Cache', type: 'resource' }
      ]
    }
  ]
  
  const toggleNode = (uri: string) => {
    const newExpanded = new Set(expandedNodes)
    if (newExpanded.has(uri)) {
      newExpanded.delete(uri)
    } else {
      newExpanded.add(uri)
    }
    setExpandedNodes(newExpanded)
  }
  
  const getIcon = (type: string) => {
    switch (type) {
      case 'folder': return '📁'
      case 'file': return '📄'
      case 'database': return '🗄'
      case 'resource': return '🔗'
      default: return '📄'
    }
  }
  
  return (
    <div className="bg-white border border-gray-200 rounded-lg">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">Resources</h3>
        <p className="text-sm text-gray-600 mt-1">Browse available MCP resources</p>
      </div>
      
      <div className="p-4">
        {resources.map((resource) => (
          <div key={resource.uri} className="mb-2">
            <div
              className="flex items-center cursor-pointer hover:bg-gray-50 p-2 rounded"
              onClick={() => toggleNode(resource.uri)}
            >
              <span className="text-gray-400 mr-2">
                {expandedNodes.has(resource.uri) ? '▼' : '▶'}
              </span>
              <span className="mr-2">{getIcon(resource.type)}</span>
              <span className="text-sm font-medium text-gray-900">
                {resource.name}
              </span>
            </div>
            
            {expandedNodes.has(resource.uri) && resource.children && (
              <div className="ml-6 border-l border-gray-200 pl-4">
                {resource.children.map((child) => (
                  <div
                    key={child.uri}
                    className="flex items-center cursor-pointer hover:bg-gray-50 p-2 rounded"
                  >
                    <span className="mr-2">{getIcon(child.type)}</span>
                    <span className="text-sm text-gray-700">{child.name}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}