import { Metadata } from 'next'
import React from 'react'

export const metadata: Metadata = {
  title: 'Goose Documentation',
  description: 'Your local AI agent, automating engineering tasks seamlessly',
}

// @ts-ignore - Temporary fix for React types incompatibility
export default function DocsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex min-h-screen">
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 overflow-y-auto">
        <div className="p-6">
          <h1 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            goose
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
            your local AI agent, automating engineering tasks seamlessly
          </p>
          
          <nav className="space-y-1">
            <a 
              href="/ai/docs" 
              className="block px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"
            >
              Quickstart
            </a>
            <div className="mt-4">
              <h3 className="px-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Getting Started
              </h3>
              <a 
                href="/ai/docs/getting-started" 
                className="block px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"
              >
                Installation
              </a>
              <a 
                href="/ai/docs/getting-started/configuration" 
                className="block px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"
              >
                Configuration
              </a>
            </div>
            
            <div className="mt-4">
              <h3 className="px-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Tutorials
              </h3>
              <a 
                href="/ai/docs/tutorials" 
                className="block px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"
              >
                Basic Tutorial
              </a>
              <a 
                href="/ai/docs/tutorials/advanced" 
                className="block px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"
              >
                Advanced Usage
              </a>
            </div>

            <div className="mt-4">
              <h3 className="px-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Architecture
              </h3>
              <a 
                href="/ai/docs/architecture" 
                className="block px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"
              >
                Overview
              </a>
              <a 
                href="/ai/docs/architecture/toolkits" 
                className="block px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"
              >
                Toolkits
              </a>
            </div>

            <div className="mt-4">
              <h3 className="px-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                MCP Integration
              </h3>
              <a 
                href="/ai/docs/mcp" 
                className="block px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"
              >
                MCP Overview
              </a>
              <a 
                href="/ai/docs/mcp/servers" 
                className="block px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"
              >
                MCP Servers
              </a>
            </div>

            <div className="mt-4">
              <h3 className="px-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Guides
              </h3>
              <a 
                href="/ai/docs/guides" 
                className="block px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"
              >
                Development
              </a>
              <a 
                href="/ai/docs/guides/docker" 
                className="block px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"
              >
                Docker Setup
              </a>
            </div>

            <div className="mt-4">
              <a 
                href="/ai/docs/troubleshooting" 
                className="block px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"
              >
                Troubleshooting
              </a>
            </div>
          </nav>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-6 py-8">
          {children}
        </div>
      </main>
    </div>
  )
}