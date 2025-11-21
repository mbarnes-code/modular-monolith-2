'use client'

import { MealPlanCalendar } from '@/components/productivity/mealie/meal-plan-calendar'
import { Breadcrumbs } from '@/components/shared/breadcrumbs'
import Link from 'next/link'

const breadcrumbs = [
  { label: 'Productivity', href: '/productivity' },
  { label: 'Mealie', href: '/productivity/mealie' },
  { label: 'Meal Plans', href: '/productivity/mealie/meal-plans' }
]

export default function MealPlansPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Meal Planning</h1>
            <p className="text-gray-600 mt-1">Plan your weekly meals and generate shopping lists</p>
          </div>
          <div className="flex items-center space-x-4">
            <button className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
              Previous Week
            </button>
            <button className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
              Next Week
            </button>
            <Link
              href="/productivity/mealie/shopping-lists"
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
            >
              Generate Shopping List
            </Link>
          </div>
        </div>
      </div>

      <MealPlanCalendar />
    </div>
  )
}