'use client'

export function FindingsFilter() {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6">
      <div className="flex flex-wrap items-center gap-4">
        <div>
          <label htmlFor="severity" className="block text-sm font-medium text-gray-700 mb-1">
            Severity
          </label>
          <select
            id="severity"
            className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
          >
            <option value="">All Severities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
            <option value="info">Info</option>
          </select>
        </div>
        
        <div>
          <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
            Category
          </label>
          <select
            id="category"
            className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
          >
            <option value="">All Categories</option>
            <option value="web-application">Web Application</option>
            <option value="network">Network</option>
            <option value="authentication">Authentication</option>
            <option value="authorization">Authorization</option>
            <option value="configuration">Configuration</option>
            <option value="cryptography">Cryptography</option>
          </select>
        </div>

        <div>
          <label htmlFor="cvss-range" className="block text-sm font-medium text-gray-700 mb-1">
            CVSS Score
          </label>
          <select
            id="cvss-range"
            className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
          >
            <option value="">All Scores</option>
            <option value="9.0-10.0">Critical (9.0-10.0)</option>
            <option value="7.0-8.9">High (7.0-8.9)</option>
            <option value="4.0-6.9">Medium (4.0-6.9)</option>
            <option value="0.1-3.9">Low (0.1-3.9)</option>
          </select>
        </div>

        <div>
          <label htmlFor="tags" className="block text-sm font-medium text-gray-700 mb-1">
            Tags
          </label>
          <input
            type="text"
            id="tags"
            placeholder="Filter by tags..."
            className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
          />
        </div>

        <div>
          <label htmlFor="search-findings" className="block text-sm font-medium text-gray-700 mb-1">
            Search
          </label>
          <input
            type="text"
            id="search-findings"
            placeholder="Search findings..."
            className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
          />
        </div>

        <div className="flex-1" />

        <div className="flex gap-2">
          <button className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
            Clear Filters
          </button>
          <button className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 transition-colors">
            Apply Filters
          </button>
        </div>
      </div>
    </div>
  )
}