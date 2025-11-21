'use client'

import Link from 'next/link'
import { useState } from 'react'

interface Case {
  id: string
  title: string
  type: 'Investigation' | 'Forensic' | 'Compliance' | 'Incident Response'
  status: 'Open' | 'In Progress' | 'Under Review' | 'Closed'
  lead: string
  priority: 'Critical' | 'High' | 'Medium' | 'Low'
  created: string
  dueDate: string
  evidence: number
  relatedIncidents: string[]
}

export function CasesTable() {
  const [filterStatus, setFilterStatus] = useState<string>('all')
  const [filterType, setFilterType] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')

  const cases: Case[] = [
    {
      id: 'CASE-2024-001',
      title: 'Advanced Persistent Threat Investigation',
      type: 'Investigation',
      status: 'In Progress',
      lead: 'Security Team Alpha',
      priority: 'Critical',
      created: '2024-01-10',
      dueDate: '2024-01-25',
      evidence: 15,
      relatedIncidents: ['INC-2024-001', 'INC-2024-003']
    },
    {
      id: 'CASE-2024-002',
      title: 'Data Breach Forensic Analysis',
      type: 'Forensic',
      status: 'Under Review',
      lead: 'Jane Smith',
      priority: 'High',
      created: '2024-01-12',
      dueDate: '2024-01-20',
      evidence: 8,
      relatedIncidents: ['INC-2024-005']
    },
    {
      id: 'CASE-2024-003',
      title: 'Compliance Audit Follow-up',
      type: 'Compliance',
      status: 'Open',
      lead: 'Bob Johnson',
      priority: 'Medium',
      created: '2024-01-14',
      dueDate: '2024-02-01',
      evidence: 3,
      relatedIncidents: []
    },
    {
      id: 'CASE-2024-004',
      title: 'Phishing Campaign Analysis',
      type: 'Incident Response',
      status: 'Closed',
      lead: 'Security Team Beta',
      priority: 'High',
      created: '2024-01-08',
      dueDate: '2024-01-18',
      evidence: 22,
      relatedIncidents: ['INC-2024-002', 'INC-2024-004']
    }
  ]

  const filteredCases = cases.filter(caseItem => {
    const matchesStatus = filterStatus === 'all' || caseItem.status === filterStatus
    const matchesType = filterType === 'all' || caseItem.type === filterType
    const matchesSearch = searchQuery === '' || 
      caseItem.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      caseItem.id.toLowerCase().includes(searchQuery.toLowerCase())
    
    return matchesStatus && matchesType && matchesSearch
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Open':
        return 'bg-blue-100 text-blue-800'
      case 'In Progress':
        return 'bg-yellow-100 text-yellow-800'
      case 'Under Review':
        return 'bg-purple-100 text-purple-800'
      case 'Closed':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

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

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'Investigation':
        return 'bg-blue-100 text-blue-800'
      case 'Forensic':
        return 'bg-purple-100 text-purple-800'
      case 'Compliance':
        return 'bg-green-100 text-green-800'
      case 'Incident Response':
        return 'bg-red-100 text-red-800'
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
              placeholder="Search cases..."
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
              <option value="Open">Open</option>
              <option value="In Progress">In Progress</option>
              <option value="Under Review">Under Review</option>
              <option value="Closed">Closed</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Type
            </label>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
            >
              <option value="all">All Types</option>
              <option value="Investigation">Investigation</option>
              <option value="Forensic">Forensic</option>
              <option value="Compliance">Compliance</option>
              <option value="Incident Response">Incident Response</option>
            </select>
          </div>
          <div className="flex items-end">
            <Link
              href="/security/dispatch/cases/new"
              className="w-full bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors text-center"
            >
              New Case
            </Link>
          </div>
        </div>
      </div>

      {/* Results Count */}
      <div className="text-sm text-gray-600">
        Showing {filteredCases.length} of {cases.length} cases
      </div>

      {/* Cases Table */}
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Case ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Title
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Lead
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Due Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Evidence
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredCases.map((caseItem) => (
                <tr key={caseItem.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <Link
                      href={`/security/dispatch/cases/${caseItem.id}`}
                      className="text-red-600 hover:text-red-700 font-medium"
                    >
                      {caseItem.id}
                    </Link>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-gray-900">{caseItem.title}</div>
                    <div className="flex items-center gap-1 mt-1">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-medium border ${getPriorityColor(caseItem.priority)}`}
                      >
                        {caseItem.priority}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(caseItem.type)}`}
                    >
                      {caseItem.type}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(caseItem.status)}`}
                    >
                      {caseItem.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {caseItem.lead}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {caseItem.dueDate}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <span className="text-sm text-gray-900">{caseItem.evidence}</span>
                      <span className="text-xs text-gray-500 ml-1">items</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <Link
                      href={`/security/dispatch/cases/${caseItem.id}`}
                      className="text-red-600 hover:text-red-700"
                    >
                      View
                    </Link>
                    <Link
                      href={`/security/dispatch/cases/${caseItem.id}/edit`}
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