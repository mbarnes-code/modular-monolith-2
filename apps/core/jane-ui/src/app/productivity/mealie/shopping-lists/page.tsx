'use client'

import { ShoppingListManager } from '@/components/productivity/mealie/shopping-list-manager'
import { Breadcrumbs } from '@/components/shared/breadcrumbs'

const breadcrumbs = [
  { label: 'Productivity', href: '/productivity' },
  { label: 'Mealie', href: '/productivity/mealie' },
  { label: 'Shopping Lists', href: '/productivity/mealie/shopping-lists' }
]

export default function ShoppingListsPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Shopping Lists</h1>
            <p className="text-gray-600 mt-1">Manage your grocery shopping lists and ingredients</p>
          </div>
          <div className="flex items-center space-x-4">
            <button className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
              Export List
            </button>
            <button className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors">
              New List
            </button>
          </div>
        </div>
      </div>

      <ShoppingListManager />
    </div>
  )
}