'use client'

export function QuickActions() {
  const actions = [
    {
      icon: '🚑',
      title: 'Report Incident',
      description: 'Create a new security incident',
      color: 'red',
      href: '/security/dispatch/incidents/new',
      urgent: true
    },
    {
      icon: '🔍',
      title: 'Start Investigation',
      description: 'Open a new investigation case',
      color: 'orange',
      href: '/security/dispatch/cases/new',
      urgent: false
    },
    {
      icon: '📊',
      title: 'View Analytics',
      description: 'Check incident trends and metrics',
      color: 'blue',
      href: '/security/dispatch/dashboard',
      urgent: false
    },
    {
      icon: '👥',
      title: 'Team Status',
      description: 'Check on-call team availability',
      color: 'green',
      href: '/security/dispatch/team',
      urgent: false
    }
  ]

  const getColorClasses = (color: string, urgent: boolean) => {
    const baseClasses = urgent ? 'ring-2 ring-offset-2' : ''
    switch (color) {
      case 'red':
        return `bg-red-100 text-red-600 hover:bg-red-200 ${urgent ? 'ring-red-500' : ''} ${baseClasses}`
      case 'orange':
        return `bg-orange-100 text-orange-600 hover:bg-orange-200 ${baseClasses}`
      case 'blue':
        return `bg-blue-100 text-blue-600 hover:bg-blue-200 ${baseClasses}`
      case 'green':
        return `bg-green-100 text-green-600 hover:bg-green-200 ${baseClasses}`
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
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center mr-3 ${getColorClasses(action.color, action.urgent)}`}>
              <span className="text-xl">{action.icon}</span>
            </div>
            <div className="flex-1">
              <h3 className="font-medium text-gray-900">{action.title}</h3>
              {action.urgent && (
                <span className="text-xs text-red-600 font-medium">URGENT</span>
              )}
            </div>
          </div>
          <p className="text-sm text-gray-600">{action.description}</p>
        </button>
      ))}
    </div>
  )
}