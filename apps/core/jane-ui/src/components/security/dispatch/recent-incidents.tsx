'use client'

import Link from 'next/link'

export function RecentIncidents() {
  const incidents = [
    {
      id: 'INC-2024-001',
      title: 'Suspicious Network Activity Detected',
      priority: 'High',
      status: 'Active',
      assignee: 'Security Team Alpha',
      created: '2 hours ago',
      description: 'Anomalous traffic patterns detected from external IP ranges'
    },
    {
      id: 'INC-2024-002',
      title: 'Failed Authentication Attempts',
      priority: 'Medium',
      status: 'Investigating',
      assignee: 'John Doe',
      created: '4 hours ago',
      description: 'Multiple failed login attempts from single IP address'
    },
    {
      id: 'INC-2024-003',
      title: 'Malware Detection Alert',
      priority: 'Critical',
      status: 'Resolved',
      assignee: 'Jane Smith',
      created: '6 hours ago',
      description: 'Malicious file detected and quarantined on workstation'
    }
  ]

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'Critical':
        return 'bg-red-100 text-red-800'
      case 'High':
        return 'bg-orange-100 text-orange-800'
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'Low':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Active':
        return 'bg-red-100 text-red-800'
      case 'Investigating':
        return 'bg-blue-100 text-blue-800'
      case 'Resolved':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-medium text-gray-900">Recent Incidents</h3>
          <Link
            href="/security/dispatch/incidents"
            className="text-red-600 hover:text-red-700 text-sm font-medium"
          >
            View all
          </Link>
        </div>
      </div>
      <div className="divide-y divide-gray-200">
        {incidents.map((incident) => (
          <div key={incident.id} className="px-6 py-4 hover:bg-gray-50">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <h4 className="text-sm font-medium text-gray-900">
                    {incident.id}
                  </h4>
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(incident.priority)}`}
                  >
                    {incident.priority}
                  </span>
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(incident.status)}`}
                  >
                    {incident.status}
                  </span>
                </div>
                <h5 className="text-sm font-medium text-gray-900 mb-1">
                  {incident.title}
                </h5>
                <p className="text-xs text-gray-600 mb-2">
                  {incident.description}
                </p>
                <div className="flex items-center gap-4 text-xs text-gray-500">
                  <span>Assignee: {incident.assignee}</span>
                  <span>Created: {incident.created}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}