export default function TCGPage() {
  return (
    <div className="tcg-overview">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">TCG Domain Overview</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="tool-card border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <h3 className="font-semibold text-lg mb-2">Commander Spellbook</h3>
          <p className="text-gray-600 mb-4">Magic: The Gathering combo database and analysis</p>
          <a href="/tcg/commander-spellbook" className="text-yellow-600 hover:text-yellow-800 font-medium">
            Launch Spellbook →
          </a>
        </div>
        
        <div className="tool-card border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
          <h3 className="font-semibold text-lg mb-2">Client Tools</h3>
          <p className="text-gray-600 mb-4">TypeScript libraries and client utilities</p>
          <a href="/tcg/client" className="text-yellow-600 hover:text-yellow-800 font-medium">
            View Tools →
          </a>
        </div>
      </div>
      
      <div className="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <h3 className="font-semibold text-yellow-900 mb-2">Migration Status</h3>
        <p className="text-yellow-700">
          TCG domain has the easiest migration path since Commander Spellbook is already built with Next.js 15.5.2,
          making it fully compatible with the unified App Router architecture.
        </p>
      </div>
    </div>
  )
}