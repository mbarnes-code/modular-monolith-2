'use client'

export function DispatchStats() {
  const stats = [
    {
      name: 'Active Incidents',
      value: '7',
      change: '+2 from last 24h',
      icon: '🚑',
      color: 'red',
      priority: 'high'
    },
    {
      name: 'Open Cases',
      value: '23',
      change: '+5 this week',
      icon: '📁',
      color: 'orange',
      priority: 'medium'
    },
    {
      name: 'Avg Response Time',
      value: '12m',
      change: '-3m from last month',
      icon: '⏱️',
      color: 'green',
      priority: 'good'
    },
    {
      name: 'Team Members',
      value: '15',
      change: '3 on-call now',
      icon: '👥',
      color: 'blue',
      priority: 'info'
    }
  ]

  const getColorClasses = (color: string, priority: string) => {
    if (priority === 'high') return 'bg-red-50 border-red-200'
    if (priority === 'medium') return 'bg-orange-50 border-orange-200'
    if (priority === 'good') return 'bg-green-50 border-green-200'
    return 'bg-blue-50 border-blue-200'
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat) => (
        <div
          key={stat.name}
          className={`p-6 rounded-lg border hover:shadow-lg transition-colors ${getColorClasses(stat.color, stat.priority)}`}
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