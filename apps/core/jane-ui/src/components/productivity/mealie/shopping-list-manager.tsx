'use client'

import { useState } from 'react'

export function ShoppingListManager() {
  const [activeList, setActiveList] = useState('weekly')
  
  const shoppingLists = [
    {
      id: 'weekly',
      name: 'Weekly Groceries',
      items: 24,
      completed: 8,
      created: '2 days ago',
      status: 'active'
    },
    {
      id: 'party',
      name: 'Birthday Party',
      items: 15,
      completed: 15,
      created: '1 week ago',
      status: 'completed'
    },
    {
      id: 'special',
      name: 'Special Dinner',
      items: 8,
      completed: 0,
      created: '3 hours ago',
      status: 'active'
    }
  ]
  
  const listItems = {
    weekly: [
      { id: 1, name: 'Chicken Breast', quantity: '2 lbs', category: 'Meat', completed: false, price: '$8.99' },
      { id: 2, name: 'Broccoli', quantity: '1 head', category: 'Vegetables', completed: true, price: '$2.49' },
      { id: 3, name: 'Pasta', quantity: '2 boxes', category: 'Pantry', completed: false, price: '$4.98' },
      { id: 4, name: 'Olive Oil', quantity: '1 bottle', category: 'Pantry', completed: true, price: '$6.99' },
      { id: 5, name: 'Tomatoes', quantity: '6 pieces', category: 'Vegetables', completed: false, price: '$3.24' },
      { id: 6, name: 'Milk', quantity: '1 gallon', category: 'Dairy', completed: true, price: '$3.49' }
    ]
  }
  
  const currentItems = listItems[activeList as keyof typeof listItems] || []
  const completedCount = currentItems.filter(item => item.completed).length
  const totalPrice = currentItems.reduce((sum, item) => sum + parseFloat(item.price.replace('$', '')), 0)

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
      {/* Shopping Lists Sidebar */}
      <div className="lg:col-span-1">
        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
          <div className="px-4 py-3 border-b border-gray-200 bg-gray-50">
            <h3 className="font-medium text-gray-900">Shopping Lists</h3>
          </div>
          <div className="divide-y divide-gray-200">
            {shoppingLists.map((list) => (
              <button
                key={list.id}
                onClick={() => setActiveList(list.id)}
                className={`w-full px-4 py-3 text-left hover:bg-gray-50 transition-colors ${
                  activeList === list.id ? 'bg-green-50 border-r-2 border-green-500' : ''
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-medium text-gray-900">{list.name}</span>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    list.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {list.status}
                  </span>
                </div>
                <div className="text-sm text-gray-600">
                  {list.completed}/{list.items} items • {list.created}
                </div>
              </button>
            ))}
          </div>
          <div className="p-4">
            <button className="w-full px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors">
              New List
            </button>
          </div>
        </div>
      </div>
      
      {/* Active Shopping List */}
      <div className="lg:col-span-3">
        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-medium text-gray-900">
                  {shoppingLists.find(l => l.id === activeList)?.name}
                </h3>
                <p className="text-sm text-gray-600">
                  {completedCount}/{currentItems.length} items completed • 
                  Total: ${totalPrice.toFixed(2)}
                </p>
              </div>
              <div className="flex items-center space-x-2">
                <button className="px-3 py-2 border border-gray-300 rounded text-sm hover:bg-gray-50">
                  Share
                </button>
                <button className="px-3 py-2 border border-gray-300 rounded text-sm hover:bg-gray-50">
                  Export
                </button>
                <button className="px-3 py-2 bg-green-600 text-white rounded text-sm hover:bg-green-700">
                  Add Item
                </button>
              </div>
            </div>
            
            {/* Progress Bar */}
            <div className="mt-4">
              <div className="flex items-center justify-between text-sm text-gray-600 mb-1">
                <span>Progress</span>
                <span>{Math.round((completedCount / currentItems.length) * 100)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-green-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${(completedCount / currentItems.length) * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
          
          {/* Items List */}
          <div className="divide-y divide-gray-200">
            {currentItems.map((item) => (
              <div key={item.id} className={`px-6 py-4 flex items-center space-x-4 ${
                item.completed ? 'bg-gray-50' : 'hover:bg-gray-50'
              }`}>
                <input
                  type="checkbox"
                  checked={item.completed}
                  onChange={() => {}}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <div className="flex-1">
                  <div className={`font-medium ${
                    item.completed ? 'text-gray-500 line-through' : 'text-gray-900'
                  }`}>
                    {item.name}
                  </div>
                  <div className="text-sm text-gray-600">
                    {item.quantity} • {item.category}
                  </div>
                </div>
                <div className={`font-medium ${
                  item.completed ? 'text-gray-500' : 'text-gray-900'
                }`}>
                  {item.price}
                </div>
                <button className="text-gray-400 hover:text-gray-600">
                  <span className="sr-only">Options</span>
                  ⋮
                </button>
              </div>
            ))}
          </div>
          
          {/* Add Item Form */}
          <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
            <div className="flex items-center space-x-3">
              <input
                type="text"
                placeholder="Add new item..."
                className="flex-1 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
              />
              <input
                type="text"
                placeholder="Qty"
                className="w-20 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
              />
              <select className="px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500">
                <option>Category</option>
                <option>Meat</option>
                <option>Vegetables</option>
                <option>Dairy</option>
                <option>Pantry</option>
              </select>
              <button className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                Add
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}