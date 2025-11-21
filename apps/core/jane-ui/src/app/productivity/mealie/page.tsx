'use client'

import { MealPlan } from '@/components/productivity/mealie/meal-plan'
import { QuickActions } from '@/components/productivity/mealie/quick-actions'
import { RecentRecipes } from '@/components/productivity/mealie/recent-recipes'
import { MealieStats } from '@/components/productivity/mealie/stats'
import { Breadcrumbs } from '@/components/shared/breadcrumbs'
import Link from 'next/link'

const breadcrumbs = [
  { label: 'Productivity', href: '/productivity' },
  { label: 'Mealie', href: '/productivity/mealie' }
]

export default function MealiePage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-lg">
            <span className="text-2xl">🍳</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Mealie</h1>
            <p className="text-gray-600">Recipe management and meal planning platform</p>
          </div>
        </div>
      </div>

      <MealieStats />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-8">
          <RecentRecipes />
          <MealPlan />
        </div>
        
        {/* Sidebar */}
        <div className="space-y-6">
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
            <QuickActions />
          </div>
          
          {/* Recipe Categories */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Popular Categories
            </h3>
            <div className="space-y-3">
              <Link href="/productivity/mealie/recipes?category=breakfast" className="flex items-center justify-between text-sm hover:text-green-600">
                <span>Breakfast</span>
                <span className="text-gray-400">45 recipes</span>
              </Link>
              <Link href="/productivity/mealie/recipes?category=lunch" className="flex items-center justify-between text-sm hover:text-green-600">
                <span>Lunch</span>
                <span className="text-gray-400">62 recipes</span>
              </Link>
              <Link href="/productivity/mealie/recipes?category=dinner" className="flex items-center justify-between text-sm hover:text-green-600">
                <span>Dinner</span>
                <span className="text-gray-400">78 recipes</span>
              </Link>
              <Link href="/productivity/mealie/recipes?category=dessert" className="flex items-center justify-between text-sm hover:text-green-600">
                <span>Desserts</span>
                <span className="text-gray-400">34 recipes</span>
              </Link>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link
          href="/productivity/mealie/recipes"
          className="group p-6 bg-white border border-gray-200 rounded-lg hover:border-green-300 hover:shadow-lg transition-all"
        >
          <div className="flex items-center mb-3">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-3">
              <span className="text-xl">📚</span>
            </div>
            <h3 className="font-semibold text-gray-900">Recipe Collection</h3>
          </div>
          <p className="text-gray-600 text-sm">
            Browse and organize your recipe collection
          </p>
        </Link>

        <Link
          href="/productivity/mealie/meal-plans"
          className="group p-6 bg-white border border-gray-200 rounded-lg hover:border-green-300 hover:shadow-lg transition-all"
        >
          <div className="flex items-center mb-3">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-3">
              <span className="text-xl">📅</span>
            </div>
            <h3 className="font-semibold text-gray-900">Meal Planning</h3>
          </div>
          <p className="text-gray-600 text-sm">
            Plan meals and generate shopping lists
          </p>
        </Link>

        <Link
          href="/productivity/mealie/shopping-lists"
          className="group p-6 bg-white border border-gray-200 rounded-lg hover:border-green-300 hover:shadow-lg transition-all"
        >
          <div className="flex items-center mb-3">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-3">
              <span className="text-xl">🛒</span>
            </div>
            <h3 className="font-semibold text-gray-900">Shopping Lists</h3>
          </div>
          <p className="text-gray-600 text-sm">
            Manage your grocery shopping lists
          </p>
        </Link>
      </div>
    </div>
  )
}