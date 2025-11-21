'use client'

import Link from 'next/link'

export function RecipesGrid() {
  const recipes = [
    {
      id: '1',
      name: 'Chicken Alfredo Pasta',
      category: 'Dinner',
      cookTime: '30 min',
      servings: 4,
      rating: 4.8,
      difficulty: 'Easy',
      image: '/placeholder-recipe.jpg',
      tags: ['Italian', 'Pasta', 'Chicken']
    },
    {
      id: '2',
      name: 'Chocolate Chip Cookies',
      category: 'Dessert',
      cookTime: '25 min',
      servings: 24,
      rating: 4.9,
      difficulty: 'Easy',
      image: '/placeholder-recipe.jpg',
      tags: ['Baking', 'Cookies', 'Sweet']
    },
    {
      id: '3',
      name: 'Caesar Salad',
      category: 'Lunch',
      cookTime: '15 min',
      servings: 2,
      rating: 4.5,
      difficulty: 'Easy',
      image: '/placeholder-recipe.jpg',
      tags: ['Salad', 'Healthy', 'Quick']
    },
    {
      id: '4',
      name: 'Beef Stir Fry',
      category: 'Dinner',
      cookTime: '20 min',
      servings: 4,
      rating: 4.7,
      difficulty: 'Medium',
      image: '/placeholder-recipe.jpg',
      tags: ['Asian', 'Beef', 'Vegetables']
    },
    {
      id: '5',
      name: 'Blueberry Pancakes',
      category: 'Breakfast',
      cookTime: '20 min',
      servings: 4,
      rating: 4.6,
      difficulty: 'Easy',
      image: '/placeholder-recipe.jpg',
      tags: ['Breakfast', 'Pancakes', 'Berries']
    },
    {
      id: '6',
      name: 'Vegetable Curry',
      category: 'Dinner',
      cookTime: '45 min',
      servings: 6,
      rating: 4.4,
      difficulty: 'Medium',
      image: '/placeholder-recipe.jpg',
      tags: ['Indian', 'Vegetarian', 'Spicy']
    }
  ]

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Easy':
        return 'bg-green-100 text-green-800'
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'Hard':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {recipes.map((recipe) => (
        <div key={recipe.id} className="bg-white border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
          <div className="aspect-w-16 aspect-h-9 bg-gray-200 flex items-center justify-center">
            <span className="text-4xl">🍳</span>
          </div>
          
          <div className="p-4">
            <div className="flex items-start justify-between mb-2">
              <Link 
                href={`/productivity/mealie/recipes/${recipe.id}`}
                className="text-lg font-semibold text-gray-900 hover:text-green-600 line-clamp-2"
              >
                {recipe.name}
              </Link>
            </div>
            
            <div className="flex items-center gap-2 mb-3">
              <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                {recipe.category}
              </span>
              <span className={`px-2 py-1 text-xs rounded-full ${getDifficultyColor(recipe.difficulty)}`}>
                {recipe.difficulty}
              </span>
            </div>
            
            <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
              <span className="flex items-center gap-1">
                <span>🕰️</span>
                {recipe.cookTime}
              </span>
              <span className="flex items-center gap-1">
                <span>🍽️</span>
                {recipe.servings} servings
              </span>
              <span className="flex items-center gap-1">
                <span>⭐</span>
                {recipe.rating}
              </span>
            </div>
            
            <div className="flex flex-wrap gap-1 mb-4">
              {recipe.tags.slice(0, 3).map((tag, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded"
                >
                  {tag}
                </span>
              ))}
              {recipe.tags.length > 3 && (
                <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                  +{recipe.tags.length - 3}
                </span>
              )}
            </div>
            
            <div className="flex gap-2">
              <Link
                href={`/productivity/mealie/recipes/${recipe.id}`}
                className="flex-1 bg-green-600 text-white text-center py-2 px-3 rounded text-sm hover:bg-green-700 transition-colors"
              >
                View Recipe
              </Link>
              <button className="px-3 py-2 border border-gray-300 rounded text-sm hover:bg-gray-50 transition-colors">
                ❤️
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}