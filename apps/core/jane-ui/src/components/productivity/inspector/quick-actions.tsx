'use client'

export function QuickActions() {
  const actions = [
    {
      icon: '🖥️',
      title: 'Connect Server',
      description: 'Add a new MCP server connection',
      color: 'blue',
      href: '/productivity/inspector/servers'
    },
    {
      icon: '🛠️',
      title: 'Test Tool',
      description: 'Execute a tool with test parameters',
      color: 'green',
      href: '/productivity/inspector/tools'
    },
    {
      icon: '📂',
      title: 'Browse Resources',
      description: 'Explore available resources',
      color: 'purple',
      href: '/productivity/inspector/resources'
    },
    {
      icon: '📊',
      title: 'Debug Session',
      description: 'Start interactive debugging',
      color: 'orange',
      href: '/productivity/inspector/debug'
    }
  ]

  const getColorClasses = (color: string) => {
    switch (color) {
      case 'blue':
        return 'bg-blue-100 text-blue-600 hover:bg-blue-200'
      case 'green':
        return 'bg-green-100 text-green-600 hover:bg-green-200'
      case 'purple':
        return 'bg-purple-100 text-purple-600 hover:bg-purple-200'
      case 'orange':
        return 'bg-orange-100 text-orange-600 hover:bg-orange-200'
      default:
        return 'bg-gray-100 text-gray-600 hover:bg-gray-200'
    }
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      {actions.map((action, index) => (
        <button
          key={index}
          className="p-4 bg-white border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all text-left"
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