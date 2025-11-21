'use client'

export function QuickActions() {
  const actions = [
    {
      icon: '🍳',
      title: 'Add Recipe',
      description: 'Create a new recipe',
      color: 'green',
      href: '/productivity/mealie/recipes/new',
      urgent: false
    },
    {
      icon: '📅',
      title: 'Plan Meals',
      description: 'Schedule this week\'s meals',
      color: 'blue',
      href: '/productivity/mealie/meal-plans',
      urgent: false
    },
    {
      icon: '🛒',
      title: 'Shopping List',
      description: 'Create grocery list',
      color: 'orange',
      href: '/productivity/mealie/shopping-lists',
      urgent: false
    },
    {
      icon: '🔍',
      title: 'Find Recipe',
      description: 'Search recipe collection',
      color: 'purple',
      href: '/productivity/mealie/recipes',
      urgent: false
    }
  ]

  const getColorClasses = (color: string) => {
    switch (color) {
      case 'green':
        return 'bg-green-100 text-green-600 hover:bg-green-200'
      case 'blue':
        return 'bg-blue-100 text-blue-600 hover:bg-blue-200'
      case 'orange':
        return 'bg-orange-100 text-orange-600 hover:bg-orange-200'
      case 'purple':
        return 'bg-purple-100 text-purple-600 hover:bg-purple-200'
      default:
        return 'bg-gray-100 text-gray-600 hover:bg-gray-200'
    }
  }

  return (
    <div className="grid grid-cols-1 gap-3">
      {actions.map((action, index) => (
        <button
          key={index}
          className="p-4 bg-white border border-gray-200 rounded-lg hover:border-green-300 hover:shadow-md transition-all text-left w-full"
        >
          <div className="flex items-center mb-2">
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center mr-3 ${getColorClasses(action.color)}`}>
              <span className="text-xl">{action.icon}</span>
            </div>
            <div className="flex-1">
              <h3 className="font-medium text-gray-900">{action.title}</h3>
            </div>
          </div>
          <p className="text-sm text-gray-600 ml-13">{action.description}</p>
        </button>
      ))}
    </div>
  )
}

export default QuickActions