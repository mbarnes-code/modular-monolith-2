'use client'

import Link from 'next/link'

export function RecentRecipes() {
  const recipes = [
    {
      id: '1',
      name: 'Chicken Alfredo Pasta',
      category: 'Dinner',
      cookTime: '30 minutes',
      rating: 4.8,
      image: '/placeholder-recipe.jpg',
      tags: ['Italian', 'Pasta', 'Chicken'],
      createdAt: '2 days ago'
    },
    {
      id: '2', 
      name: 'Chocolate Chip Cookies',
      category: 'Dessert',
      cookTime: '25 minutes',
      rating: 4.9,
      image: '/placeholder-recipe.jpg',
      tags: ['Baking', 'Cookies', 'Sweet'],
      createdAt: '1 week ago'
    },
    {
      id: '3',
      name: 'Caesar Salad',
      category: 'Lunch',
      cookTime: '15 minutes', 
      rating: 4.5,
      image: '/placeholder-recipe.jpg',
      tags: ['Salad', 'Healthy', 'Quick'],
      createdAt: '3 days ago'
    },
    {
      id: '4',
      name: 'Beef Stir Fry',
      category: 'Dinner',
      cookTime: '20 minutes',
      rating: 4.7,
      image: '/placeholder-recipe.jpg', 
      tags: ['Asian', 'Beef', 'Vegetables'],
      createdAt: '5 days ago'
    }
  ]

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'Breakfast':
        return 'bg-yellow-100 text-yellow-800'
      case 'Lunch':
        return 'bg-green-100 text-green-800'
      case 'Dinner':
        return 'bg-blue-100 text-blue-800'
      case 'Dessert':
        return 'bg-pink-100 text-pink-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-medium text-gray-900">Recent Recipes</h3>
          <Link
            href="/productivity/mealie/recipes"
            className="text-green-600 hover:text-green-700 text-sm font-medium"
          >
            View all
          </Link>
        </div>
      </div>
      <div className="divide-y divide-gray-200">
        {recipes.map((recipe) => (
          <div key={recipe.id} className="px-6 py-4 hover:bg-gray-50">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <div className="w-16 h-16 bg-gray-200 rounded-lg flex items-center justify-center">
                  <span className="text-2xl">🍳</span>
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <Link 
                    href={`/productivity/mealie/recipes/${recipe.id}`}
                    className="text-sm font-medium text-gray-900 hover:text-green-600"
                  >
                    {recipe.name}
                  </Link>
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(recipe.category)}`}
                  >
                    {recipe.category}
                  </span>
                </div>
                <div className="flex items-center gap-4 text-xs text-gray-500 mb-2">
                  <span>🕰️ {recipe.cookTime}</span>
                  <span>⭐ {recipe.rating}</span>
                  <span>Added {recipe.createdAt}</span>
                </div>
                <div className="flex flex-wrap gap-1">
                  {recipe.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}