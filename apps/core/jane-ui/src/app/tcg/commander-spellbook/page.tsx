export default function CommanderSpellbookPage() {
  return (
    <div className="commander-spellbook-integration">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Commander Spellbook</h1>
      
      <div className="integration-status mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <h3 className="font-semibold text-yellow-900 mb-2">Migration Status: Ready for Integration</h3>
        <p className="text-yellow-700 mb-2">
          Commander Spellbook is already built with Next.js 15.5.2 and React 19, making it fully compatible.
        </p>
      </div>
      
      <div className="integration-options grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="option-card border border-gray-200 rounded-lg p-4">
          <h3 className="font-semibold text-lg mb-2">🔗 Direct Link Integration</h3>
          <p className="text-gray-600 mb-4">
            Access the Commander Spellbook application in a new tab.
          </p>
          <a 
            href="http://localhost:3000" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-block bg-yellow-600 text-white px-4 py-2 rounded hover:bg-yellow-700 transition-colors"
          >
            Open Commander Spellbook →
          </a>
        </div>
        
        <div className="option-card border border-gray-200 rounded-lg p-4">
          <h3 className="font-semibold text-lg mb-2">🔄 Component Migration</h3>
          <p className="text-gray-600 mb-4">
            Migrate React components to App Router structure.
          </p>
          <button 
            className="inline-block bg-gray-300 text-gray-600 px-4 py-2 rounded cursor-not-allowed"
            disabled
          >
            Coming Soon
          </button>
        </div>
      </div>
    </div>
  )
}