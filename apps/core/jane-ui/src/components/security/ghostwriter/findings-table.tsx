'use client'

export function FindingsTable() {
  const findings = [
    {
      id: 1,
      title: 'SQL Injection in Login Form',
      severity: 'High',
      category: 'Web Application',
      cvss: 8.1,
      tags: ['SQL Injection', 'Authentication', 'Web'],
      lastModified: '2024-01-05',
      usageCount: 12
    },
    {
      id: 2,
      title: 'Weak Password Policy',
      severity: 'Medium',
      category: 'Authentication',
      cvss: 5.3,
      tags: ['Password', 'Policy', 'Authentication'],
      lastModified: '2024-01-03',
      usageCount: 8
    },
    {
      id: 3,
      title: 'Unencrypted Data Transmission',
      severity: 'High',
      category: 'Network',
      cvss: 7.5,
      tags: ['Encryption', 'Network', 'Data Protection'],
      lastModified: '2023-12-28',
      usageCount: 15
    },
    {
      id: 4,
      title: 'Missing Security Headers',
      severity: 'Low',
      category: 'Web Application',
      cvss: 3.7,
      tags: ['Headers', 'Web', 'Configuration'],
      lastModified: '2023-12-20',
      usageCount: 6
    }
  ]

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'Critical':
        return 'bg-red-100 text-red-800'
      case 'High':
        return 'bg-orange-100 text-orange-800'
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'Low':
        return 'bg-green-100 text-green-800'
      case 'Info':
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getCVSSColor = (cvss: number) => {
    if (cvss >= 9.0) return 'text-red-600 font-bold'
    if (cvss >= 7.0) return 'text-orange-600 font-semibold'
    if (cvss >= 4.0) return 'text-yellow-600 font-medium'
    return 'text-green-600'
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Finding Title
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Severity
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                CVSS Score
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Category
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Tags
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Usage
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Modified
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {findings.map((finding) => (
              <tr key={finding.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">
                    {finding.title}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getSeverityColor(finding.severity)}`}
                  >
                    {finding.severity}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className={`text-sm ${getCVSSColor(finding.cvss)}`}>
                    {finding.cvss}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">{finding.category}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex flex-wrap gap-1">
                    {finding.tags.slice(0, 2).map((tag, index) => (
                      <span
                        key={index}
                        className="inline-flex px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded"
                      >
                        {tag}
                      </span>
                    ))}
                    {finding.tags.length > 2 && (
                      <span className="inline-flex px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded">
                        +{finding.tags.length - 2}
                      </span>
                    )}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">{finding.usageCount}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">{finding.lastModified}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div className="flex gap-2">
                    <button className="text-red-600 hover:text-red-900">Edit</button>
                    <button className="text-blue-600 hover:text-blue-900">View</button>
                    <button className="text-green-600 hover:text-green-900">Clone</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}