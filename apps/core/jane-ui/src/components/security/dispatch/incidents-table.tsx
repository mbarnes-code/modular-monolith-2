'use client'

import Link from 'next/link'
import { useState } from 'react'

interface Incident {
  id: string
  title: string
  priority: 'Critical' | 'High' | 'Medium' | 'Low'
  status: 'Active' | 'Investigating' | 'Resolved' | 'Closed'
  assignee: string
  created: string
  updated: string
  category: string
}

export function IncidentsTable() {
  const [filterStatus, setFilterStatus] = useState<string>('all')
  const [filterPriority, setFilterPriority] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')

  const incidents: Incident[] = [
    {
      id: 'INC-2024-001',
      title: 'Suspicious Network Activity Detected',
      priority: 'High',
      status: 'Active',
      assignee: 'Security Team Alpha',
      created: '2024-01-15 14:30',
      updated: '2024-01-15 16:45',
      category: 'Network Security'
    },
    {
      id: 'INC-2024-002',
      title: 'Failed Authentication Attempts',
      priority: 'Medium',
      status: 'Investigating',
      assignee: 'John Doe',
      created: '2024-01-15 10:15',
      updated: '2024-01-15 15:20',
      category: 'Authentication'
    },
    {
      id: 'INC-2024-003',
      title: 'Malware Detection Alert',
      priority: 'Critical',
      status: 'Resolved',
      assignee: 'Jane Smith',
      created: '2024-01-15 08:00',
      updated: '2024-01-15 12:30',
      category: 'Malware'
    },
    {
      id: 'INC-2024-004',
      title: 'Unauthorized Access Attempt',
      priority: 'High',
      status: 'Active',
      assignee: 'Bob Johnson',
      created: '2024-01-14 22:45',
      updated: '2024-01-15 09:15',
      category: 'Access Control'
    },
    {
      id: 'INC-2024-005',
      title: 'Data Exfiltration Suspected',
      priority: 'Critical',
      status: 'Investigating',
      assignee: 'Security Team Beta',
      created: '2024-01-14 18:20',
      updated: '2024-01-15 11:00',
      category: 'Data Security'
    }
  ]

  const filteredIncidents = incidents.filter(incident => {
    const matchesStatus = filterStatus === 'all' || incident.status === filterStatus
    const matchesPriority = filterPriority === 'all' || incident.priority === filterPriority
    const matchesSearch = searchQuery === '' || 
      incident.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      incident.id.toLowerCase().includes(searchQuery.toLowerCase())
    
    return matchesStatus && matchesPriority && matchesSearch
  })

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'Critical':
        return 'bg-red-100 text-red-800 border-red-200'
      case 'High':
        return 'bg-orange-100 text-orange-800 border-orange-200'
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'Low':
        return 'bg-green-100 text-green-800 border-green-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
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
      case 'Closed':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-6">
      {/* Filters and Search */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Search
            </label>
            <input
              type="text"
              placeholder="Search incidents..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
            >
              <option value="all">All Statuses</option>
              <option value="Active">Active</option>
              <option value="Investigating">Investigating</option>
              <option value="Resolved">Resolved</option>
              <option value="Closed">Closed</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Priority
            </label>
            <select
              value={filterPriority}
              onChange={(e) => setFilterPriority(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
            >
              <option value="all">All Priorities</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>
          <div className="flex items-end">
            <Link
              href="/security/dispatch/incidents/new"
              className="w-full bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors text-center"
            >
              New Incident
            </Link>
          </div>
        </div>
      </div>

      {/* Results Count */}
      <div className="text-sm text-gray-600">
        Showing {filteredIncidents.length} of {incidents.length} incidents
      </div>

      {/* Incidents Table */}
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Incident ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Title
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Priority
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Assignee
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Created
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredIncidents.map((incident) => (
                <tr key={incident.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <Link
                      href={`/security/dispatch/incidents/${incident.id}`}
                      className="text-red-600 hover:text-red-700 font-medium"
                    >
                      {incident.id}
                    </Link>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-gray-900">{incident.title}</div>
                    <div className="text-sm text-gray-500">{incident.category}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium border ${getPriorityColor(incident.priority)}`}
                    >
                      {incident.priority}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(incident.status)}`}
                    >
                      {incident.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {incident.assignee}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {incident.created}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <Link
                      href={`/security/dispatch/incidents/${incident.id}`}
                      className="text-red-600 hover:text-red-700"
                    >
                      View
                    </Link>
                    <Link
                      href={`/security/dispatch/incidents/${incident.id}/edit`}
                      className="text-blue-600 hover:text-blue-700"
                    >
                      Edit
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}