'use client'

export function InspectorStats() {
  const stats = [
    {
      name: 'Connected Servers',
      value: '4',
      change: '+2 from last session',
      icon: '🖥️',
      color: 'blue'
    },
    {
      name: 'Available Tools',
      value: '23',
      change: '+5 new capabilities',
      icon: '🛠️',
      color: 'green'
    },
    {
      name: 'Resources Loaded',
      value: '156',
      change: '+34 from cache',
      icon: '📂',
      color: 'purple'
    },
    {
      name: 'Active Sessions',
      value: '2',
      change: 'Real-time monitoring',
      icon: '📊',
      color: 'orange'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat) => (
        <div
          key={stat.name}
          className="bg-white p-6 rounded-lg border border-gray-200 hover:border-blue-200 transition-colors"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <span className="text-2xl">{stat.icon}</span>
            </div>
            <div className="ml-4 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  {stat.name}
                </dt>
                <dd className="flex items-baseline">
                  <div className="text-2xl font-semibold text-gray-900">
                    {stat.value}
                  </div>
                </dd>
                <dd className="text-sm text-gray-600 mt-1">
                  {stat.change}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}