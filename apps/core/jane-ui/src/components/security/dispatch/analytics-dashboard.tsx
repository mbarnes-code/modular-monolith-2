'use client'

import { useState } from 'react'

export function AnalyticsDashboard() {
  const [timeRange, setTimeRange] = useState('7d')

  const metrics = {
    totalIncidents: 45,
    resolvedIncidents: 38,
    avgResponseTime: '14 minutes',
    mttr: '2.5 hours', // Mean Time to Resolution
    activeCases: 12,
    escalatedIncidents: 3
  }

  const trendData = [
    { period: 'Mon', incidents: 3, resolved: 2 },
    { period: 'Tue', incidents: 7, resolved: 6 },
    { period: 'Wed', incidents: 5, resolved: 4 },
    { period: 'Thu', incidents: 8, resolved: 7 },
    { period: 'Fri', incidents: 12, resolved: 9 },
    { period: 'Sat', incidents: 6, resolved: 5 },
    { period: 'Sun', incidents: 4, resolved: 5 }
  ]

  const categoryBreakdown = [
    { category: 'Network Security', count: 15, percentage: 33 },
    { category: 'Malware', count: 12, percentage: 27 },
    { category: 'Access Control', count: 8, percentage: 18 },
    { category: 'Data Security', count: 6, percentage: 13 },
    { category: 'Other', count: 4, percentage: 9 }
  ]

  const priorityDistribution = [
    { priority: 'Critical', count: 5, color: 'bg-red-500' },
    { priority: 'High', count: 12, color: 'bg-orange-500' },
    { priority: 'Medium', count: 18, color: 'bg-yellow-500' },
    { priority: 'Low', count: 10, color: 'bg-green-500' }
  ]

  return (
    <div className="space-y-8">
      {/* Time Range Filter */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Security Analytics</h2>
        <div className="flex space-x-2">
          {['24h', '7d', '30d', '90d'].map((range) => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`px-3 py-1 text-sm rounded-md ${
                timeRange === range
                  ? 'bg-red-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {range}
            </button>
          ))}
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-500">Total Incidents</h3>
          <p className="text-2xl font-bold text-gray-900">{metrics.totalIncidents}</p>
          <p className="text-sm text-green-600">+12% vs last period</p>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-500">Resolved</h3>
          <p className="text-2xl font-bold text-green-600">{metrics.resolvedIncidents}</p>
          <p className="text-sm text-gray-500">{Math.round((metrics.resolvedIncidents / metrics.totalIncidents) * 100)}% resolution rate</p>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-500">Avg Response</h3>
          <p className="text-2xl font-bold text-blue-600">{metrics.avgResponseTime}</p>
          <p className="text-sm text-green-600">-3 min improvement</p>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-500">MTTR</h3>
          <p className="text-2xl font-bold text-purple-600">{metrics.mttr}</p>
          <p className="text-sm text-red-600">+0.2h vs target</p>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-500">Active Cases</h3>
          <p className="text-2xl font-bold text-orange-600">{metrics.activeCases}</p>
          <p className="text-sm text-gray-500">Investigation ongoing</p>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-500">Escalated</h3>
          <p className="text-2xl font-bold text-red-600">{metrics.escalatedIncidents}</p>
          <p className="text-sm text-yellow-600">Requires attention</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Incident Trends */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Incident Trends</h3>
          <div className="space-y-3">
            {trendData.map((data, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-sm text-gray-600 w-12">{data.period}</span>
                <div className="flex-1 mx-4">
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-red-500 h-2 rounded-full"
                        style={{ width: `${(data.incidents / 12) * 100}%` }}
                      ></div>
                    </div>
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-green-500 h-2 rounded-full"
                        style={{ width: `${(data.resolved / 12) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
                <div className="flex space-x-4 text-sm">
                  <span className="text-red-600">{data.incidents} new</span>
                  <span className="text-green-600">{data.resolved} resolved</span>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className="flex justify-center space-x-6 text-sm">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
                <span>New Incidents</span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <span>Resolved</span>
              </div>
            </div>
          </div>
        </div>

        {/* Category Breakdown */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Incident Categories</h3>
          <div className="space-y-4">
            {categoryBreakdown.map((category, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium text-gray-900">{category.category}</span>
                    <span className="text-sm text-gray-500">{category.count} incidents</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-red-500 h-2 rounded-full"
                      style={{ width: `${category.percentage}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Priority Distribution */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Priority Distribution</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {priorityDistribution.map((priority, index) => (
            <div key={index} className="text-center">
              <div className={`w-16 h-16 ${priority.color} rounded-full mx-auto mb-2 flex items-center justify-center`}>
                <span className="text-white font-bold text-lg">{priority.count}</span>
              </div>
              <p className="text-sm font-medium text-gray-900">{priority.priority}</p>
              <p className="text-xs text-gray-500">{Math.round((priority.count / metrics.totalIncidents) * 100)}%</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}