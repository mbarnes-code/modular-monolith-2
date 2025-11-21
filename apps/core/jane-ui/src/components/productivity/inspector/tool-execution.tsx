'use client'

import { useState } from 'react'

export function ToolExecution() {
  const [selectedTool, setSelectedTool] = useState('read_file')
  const [executing, setExecuting] = useState(false)
  const [result, setResult] = useState<any>(null)
  
  const tools = {
    read_file: {
      name: 'read_file',
      description: 'Read contents of a file',
      parameters: [
        { name: 'path', type: 'string', description: 'Path to the file', required: true }
      ]
    },
    write_file: {
      name: 'write_file',
      description: 'Write content to a file',
      parameters: [
        { name: 'path', type: 'string', description: 'Path to the file', required: true },
        { name: 'content', type: 'string', description: 'Content to write', required: true }
      ]
    }
  }
  
  const currentTool = tools[selectedTool as keyof typeof tools]
  
  const handleExecute = async () => {
    setExecuting(true)
    // Simulate API call
    setTimeout(() => {
      setResult({
        success: true,
        output: 'Tool executed successfully',
        timestamp: new Date().toISOString()
      })
      setExecuting(false)
    }, 2000)
  }
  
  return (
    <div className="bg-white border border-gray-200 rounded-lg">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">Tool Execution</h3>
        <p className="text-sm text-gray-600 mt-1">Execute MCP tools with custom parameters</p>
      </div>
      
      <div className="p-4 space-y-4">
        <div>
          <label htmlFor="tool-select" className="block text-sm font-medium text-gray-700 mb-1">
            Select Tool
          </label>
          <select
            id="tool-select"
            value={selectedTool}
            onChange={(e) => setSelectedTool(e.target.value)}
            className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            {Object.entries(tools).map(([key, tool]) => (
              <option key={key} value={key}>
                {tool.name} - {tool.description}
              </option>
            ))}
          </select>
        </div>
        
        {currentTool && (
          <div className="space-y-3">
            <h4 className="font-medium text-gray-900">Parameters</h4>
            {currentTool.parameters.map((param) => (
              <div key={param.name}>
                <label htmlFor={param.name} className="block text-sm font-medium text-gray-700 mb-1">
                  {param.name} {param.required && <span className="text-red-500">*</span>}
                </label>
                <input
                  type="text"
                  id={param.name}
                  placeholder={param.description}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <p className="text-xs text-gray-500 mt-1">{param.description}</p>
              </div>
            ))}
          </div>
        )}
        
        <button
          onClick={handleExecute}
          disabled={executing}
          className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {executing ? 'Executing...' : 'Execute Tool'}
        </button>
        
        {result && (
          <div className="mt-4 p-3 bg-gray-50 rounded-md">
            <h5 className="font-medium text-gray-900 mb-2">Result</h5>
            <pre className="text-sm text-gray-700 overflow-auto">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  )
}