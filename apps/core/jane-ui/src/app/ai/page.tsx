export default function AIPage() {
  return (
    <div className="ai-overview">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">AI Domain Overview</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="tool-card border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <h3 className="font-semibold text-lg mb-2">Goose Agent</h3>
          <p className="text-gray-600 mb-4">AI development agent for code generation and analysis</p>
          <a href="/ai/goose" className="text-blue-600 hover:text-blue-800 font-medium">
            Launch Goose →
          </a>
        </div>
        
        <div className="tool-card border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <h3 className="font-semibold text-lg mb-2">Documentation</h3>
          <p className="text-gray-600 mb-4">AI tool documentation and guides</p>
          <a href="/ai/docs" className="text-blue-600 hover:text-blue-800 font-medium">
            View Docs →
          </a>
        </div>
        
        <div className="tool-card border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <h3 className="font-semibold text-lg mb-2">Firecrawl</h3>
          <p className="text-gray-600 mb-4">Web scraping and data extraction service</p>
          <a href="/ai/firecrawl" className="text-blue-600 hover:text-blue-800 font-medium">
            Launch Firecrawl →
          </a>
        </div>
        
        <div className="tool-card border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <h3 className="font-semibold text-lg mb-2">Monitoring</h3>
          <p className="text-gray-600 mb-4">LLM server monitoring and analytics</p>
          <a href="/ai/monitoring" className="text-blue-600 hover:text-blue-800 font-medium">
            View Monitoring →
          </a>
        </div>
      </div>
      
      <div className="mt-8 p-4 bg-green-50 border border-green-200 rounded-lg">
        <h3 className="font-semibold text-green-900 mb-2">Migration Status - Phase 1 Complete</h3>
        <p className="text-green-700 mb-3">
          ✅ Goose documentation successfully migrated from Docusaurus to Next.js MDX
        </p>
        <div className="space-y-2 text-sm text-green-600">
          <div>• Converted 5+ key documentation pages with enhanced navigation</div>
          <div>• Preserved all content from quickstart, installation, architecture guides</div>
          <div>• Added comprehensive MCP integration documentation</div>
          <div>• Implemented responsive sidebar navigation with dark mode support</div>
        </div>
      </div>
    </div>
  )
}