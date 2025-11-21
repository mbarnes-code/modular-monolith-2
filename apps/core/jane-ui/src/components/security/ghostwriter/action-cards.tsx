'use client'

export function ActionCards() {
  const actions = [
    {
      icon: '📝',
      title: 'Create Report',
      description: 'Start a new penetration testing report',
      color: 'red',
      href: '/security/ghostwriter/reports/new'
    },
    {
      icon: '🎯',
      title: 'New Project',
      description: 'Set up a new engagement project',
      color: 'blue',
      href: '/security/ghostwriter/projects/new'
    },
    {
      icon: '🔍',
      title: 'Add Finding',
      description: 'Create a reusable security finding',
      color: 'green',
      href: '/security/ghostwriter/findings/new'
    },
    {
      icon: '📊',
      title: 'View Reports',
      description: 'Browse existing reports',
      color: 'purple',
      href: '/security/ghostwriter/reports'
    }
  ]

  const getColorClasses = (color: string) => {
    switch (color) {
      case 'red':
        return 'bg-red-100 text-red-600 hover:bg-red-200'
      case 'blue':
        return 'bg-blue-100 text-blue-600 hover:bg-blue-200'
      case 'green':
        return 'bg-green-100 text-green-600 hover:bg-green-200'
      case 'purple':
        return 'bg-purple-100 text-purple-600 hover:bg-purple-200'
      default:
        return 'bg-gray-100 text-gray-600 hover:bg-gray-200'
    }
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      {actions.map((action, index) => (
        <button
          key={index}
          className="p-4 bg-white border border-gray-200 rounded-lg hover:border-red-300 hover:shadow-md transition-all text-left"
        >
          <div className="flex items-center mb-2">
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center mr-3 ${getColorClasses(action.color)}`}>
              <span className="text-xl">{action.icon}</span>
            </div>
            <h3 className="font-medium text-gray-900">{action.title}</h3>
          </div>
          <p className="text-sm text-gray-600">{action.description}</p>
        </button>
      ))}
    </div>
  )
}