'use client'

import Link from 'next/link'

export function RecentProjects() {
  const projects = [
    {
      id: 1,
      name: 'Acme Corp Pentest',
      status: 'In Progress',
      dueDate: '2024-01-15',
      progress: 65
    },
    {
      id: 2,
      name: 'Beta Inc Web App Assessment',
      status: 'Planning',
      dueDate: '2024-01-22',
      progress: 25
    },
    {
      id: 3,
      name: 'Gamma LLC Infrastructure Review',
      status: 'Reporting',
      dueDate: '2024-01-08',
      progress: 90
    }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'In Progress':
        return 'bg-blue-100 text-blue-800'
      case 'Planning':
        return 'bg-yellow-100 text-yellow-800'
      case 'Reporting':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-medium text-gray-900">Recent Projects</h3>
          <Link
            href="/security/ghostwriter/projects"
            className="text-red-600 hover:text-red-700 text-sm font-medium"
          >
            View all
          </Link>
        </div>
      </div>
      <div className="divide-y divide-gray-200">
        {projects.map((project) => (
          <div key={project.id} className="px-6 py-4 hover:bg-gray-50">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <h4 className="text-sm font-medium text-gray-900 mb-1">
                  {project.name}
                </h4>
                <div className="flex items-center gap-3 text-sm text-gray-500">
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}
                  >
                    {project.status}
                  </span>
                  <span>Due: {project.dueDate}</span>
                </div>
                <div className="mt-2">
                  <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span>Progress</span>
                    <span>{project.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-red-600 h-2 rounded-full transition-all"
                      style={{ width: `${project.progress}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}