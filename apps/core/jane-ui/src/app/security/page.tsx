export default function SecurityPage() {
  return (
    <div className="security-overview">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Security Domain Overview</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="tool-card border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <h3 className="font-semibold text-lg mb-2">Nemesis</h3>
          <p className="text-gray-600 mb-4">Post-exploitation framework for security analysis</p>
          <a href="/security/nemesis" className="text-red-600 hover:text-red-800 font-medium">
            Launch Nemesis →
          </a>
        </div>
        
        <div className="tool-card border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <h3 className="font-semibold text-lg mb-2">CyberChef</h3>
          <p className="text-gray-600 mb-4">Data analysis and cryptographic operations toolkit</p>
          <a href="/security/cyberchef" className="text-red-600 hover:text-red-800 font-medium">
            Launch CyberChef →
          </a>
        </div>
        
        <div className="tool-card border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <h3 className="font-semibold text-lg mb-2">Dispatch</h3>
          <p className="text-gray-600 mb-4">Incident management and response coordination</p>
          <a href="/security/dispatch" className="text-red-600 hover:text-red-800 font-medium">
            Launch Dispatch →
          </a>
        </div>
      </div>
      
      <div className="mt-8 p-4 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="font-semibold text-red-900 mb-2">Migration Status - Phase 1 Complete</h3>
        <p className="text-red-700 mb-3">
          ✅ Security tools successfully migrated with comprehensive capabilities
        </p>
      </div>
    </div>
  )
}