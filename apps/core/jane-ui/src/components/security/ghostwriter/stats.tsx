'use client'

export function GhostwriterStats() {
  const stats = [
    {
      name: 'Active Projects',
      value: '12',
      change: '+3 from last month',
      icon: '🎯',
      color: 'red'
    },
    {
      name: 'Reports Generated',
      value: '45',
      change: '+8 from last month',
      icon: '📊',
      color: 'blue'
    },
    {
      name: 'Findings Library',
      value: '234',
      change: '+12 new this month',
      icon: '🔍',
      color: 'green'
    },
    {
      name: 'Team Members',
      value: '8',
      change: '+2 from last month',
      icon: '👥',
      color: 'purple'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat) => (
        <div
          key={stat.name}
          className="bg-white p-6 rounded-lg border border-gray-200 hover:border-red-200 transition-colors"
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