'use client'

export function ProjectsFilter() {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6">
      <div className="flex flex-wrap items-center gap-4">
        <div>
          <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">
            Status
          </label>
          <select
            id="status"
            className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
          >
            <option value="">All Statuses</option>
            <option value="planning">Planning</option>
            <option value="in-progress">In Progress</option>
            <option value="reporting">Reporting</option>
            <option value="completed">Completed</option>
          </select>
        </div>
        
        <div>
          <label htmlFor="team" className="block text-sm font-medium text-gray-700 mb-1">
            Team Member
          </label>
          <select
            id="team"
            className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
          >
            <option value="">All Team Members</option>
            <option value="john-doe">John Doe</option>
            <option value="jane-smith">Jane Smith</option>
            <option value="mike-johnson">Mike Johnson</option>
            <option value="sarah-wilson">Sarah Wilson</option>
          </select>
        </div>

        <div>
          <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
            Search
          </label>
          <input
            type="text"
            id="search"
            placeholder="Search projects..."
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