'use client'

export function MealieStats() {
  const stats = [
    {
      name: 'Total Recipes',
      value: '234',
      change: '+12 this month',
      icon: '📚',
      color: 'green',
      priority: 'info'
    },
    {
      name: 'Meal Plans',
      value: '8',
      change: 'This week planned',
      icon: '📅',
      color: 'blue',
      priority: 'info'
    },
    {
      name: 'Shopping Lists',
      value: '3',
      change: '2 active lists',
      icon: '🛒',
      color: 'orange',
      priority: 'info'
    },
    {
      name: 'Favorite Recipes',
      value: '47',
      change: '+3 this week',
      icon: '❤️',
      color: 'red',
      priority: 'info'
    }
  ]

  const getColorClasses = (color: string) => {
    switch (color) {
      case 'green':
        return 'bg-green-50 border-green-200'
      case 'blue':
        return 'bg-blue-50 border-blue-200'
      case 'orange':
        return 'bg-orange-50 border-orange-200'
      case 'red':
        return 'bg-red-50 border-red-200'
      default:
        return 'bg-gray-50 border-gray-200'
    }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat) => (
        <div
          key={stat.name}
          className={`p-6 rounded-lg border hover:shadow-lg transition-colors ${getColorClasses(stat.color)}`}
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