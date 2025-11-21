export default function ProductivityPage() {
  return (
    <div className="productivity-overview">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Productivity Domain Overview</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="tool-card border border-green-200 bg-green-50 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <div className="flex items-center mb-2">
            <h3 className="font-semibold text-lg">💰 Actual Budget</h3>
            <span className="ml-2 px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">✅ Migrated</span>
          </div>
          <p className="text-gray-600 mb-4">Local-first personal finance and budgeting application</p>
          <a href="/productivity/actual" className="text-green-600 hover:text-green-800 font-medium">
            Launch Actual →
          </a>
        </div>
        
        <div className="tool-card border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <h3 className="font-semibold text-lg mb-2">n8n</h3>
          <p className="text-gray-600 mb-4">Workflow automation and no-code platform</p>
          <a href="/productivity/n8n" className="text-green-600 hover:text-green-800 font-medium">
            Launch n8n →
          </a>
        </div>
        
        <div className="tool-card border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <h3 className="font-semibold text-lg mb-2">Mealie</h3>
          <p className="text-gray-600 mb-4">Recipe management and meal planning</p>
          <a href="/productivity/mealie" className="text-green-600 hover:text-green-800 font-medium">
            Launch Mealie →
          </a>
        </div>
        
        <div className="tool-card border border-green-200 bg-green-50 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <div className="flex items-center mb-2">
            <h3 className="font-semibold text-lg">🔍 MCP Inspector</h3>
            <span className="ml-2 px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">✅ Migrated</span>
          </div>
          <p className="text-gray-600 mb-4">Model Context Protocol server inspection and debugging platform</p>
          <a href="/productivity/inspector" className="text-green-600 hover:text-green-800 font-medium">
            Launch Inspector →
          </a>
        </div>
        
        <div className="tool-card border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <h3 className="font-semibold text-lg mb-2">OneX</h3>
          <p className="text-gray-600 mb-4">Security toolkit and utilities</p>
          <a href="/productivity/onex" className="text-green-600 hover:text-green-800 font-medium">
            Launch OneX →
          </a>
        </div>
        
        <div className="tool-card border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <h3 className="font-semibold text-lg mb-2">Dashboard</h3>
          <p className="text-gray-600 mb-4">Unified productivity dashboard</p>
          <a href="/productivity/dashboard" className="text-green-600 hover:text-green-800 font-medium">
            Launch Dashboard →
          </a>
        </div>
      </div>
      
      <div className="mt-8 p-4 bg-green-50 border border-green-200 rounded-lg">
        <h3 className="font-semibold text-green-900 mb-2">Migration Status - Phase 1 Complete</h3>
        <p className="text-green-700 mb-3">
          ✅ Actual Budget & MCP Inspector React applications successfully migrated with full functionality preserved
        </p>
        <div className="space-y-2 text-sm text-green-600">
          <div>• Actual Budget: React 19.2.0 personal finance app with local-first architecture</div>
          <div>• MCP Inspector: React 18.3.1 debugging platform with Radix UI components</div>
          <div>• Server management, tool execution, and resource browsing capabilities preserved</div>
          <div>• Unified jane-ui navigation and theming integration across both applications</div>
        </div>
        <p className="text-green-700 mt-3">
          Next: Vue.js framework conversions (dispatch, n8n, mealie) to complete productivity domain migration.
        </p>
      </div>
    </div>
  )
}