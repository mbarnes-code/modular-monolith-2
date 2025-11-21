'use client'

import { RecipeFilters } from '@/components/productivity/mealie/recipe-filters'
import { RecipesGrid } from '@/components/productivity/mealie/recipes-grid'
import { Breadcrumbs } from '@/components/shared/breadcrumbs'
import Link from 'next/link'

const breadcrumbs = [
  { label: 'Productivity', href: '/productivity' },
  { label: 'Mealie', href: '/productivity/mealie' },
  { label: 'Recipes', href: '/productivity/mealie/recipes' }
]

export default function RecipesPage() {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <Breadcrumbs items={breadcrumbs} />
      
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Recipe Collection</h1>
            <p className="text-gray-600 mt-1">Discover and manage your favorite recipes</p>
          </div>
          <div className="flex items-center space-x-4">
            <button className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
              Import Recipe
            </button>
            <Link
              href="/productivity/mealie/recipes/new"
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
            >
              Add Recipe
            </Link>
          </div>
        </div>
      </div>

      <RecipeFilters />
      <RecipesGrid />
    </div>
  )
}