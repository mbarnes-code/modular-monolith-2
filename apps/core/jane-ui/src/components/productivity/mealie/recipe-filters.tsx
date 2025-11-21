'use client'

import { useState } from 'react'

export function RecipeFilters() {
  const [searchQuery, setSearchQuery] = useState('')
  const [category, setCategory] = useState('all')
  const [difficulty, setDifficulty] = useState('all')
  const [cookTime, setCookTime] = useState('all')

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Search Recipes
          </label>
          <input
            type="text"
            placeholder="Search by name, ingredient..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Category
          </label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="all">All Categories</option>
            <option value="breakfast">Breakfast</option>
            <option value="lunch">Lunch</option>
            <option value="dinner">Dinner</option>
            <option value="dessert">Dessert</option>
            <option value="snack">Snack</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Difficulty
          </label>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="all">All Levels</option>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Cook Time
          </label>
          <select
            value={cookTime}
            onChange={(e) => setCookTime(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="all">Any Duration</option>
            <option value="under15">Under 15 min</option>
            <option value="15to30">15-30 min</option>
            <option value="30to60">30-60 min</option>
            <option value="over60">Over 60 min</option>
          </select>
        </div>
      </div>
      
      <div className="mt-4 flex items-center justify-between">
        <div className="text-sm text-gray-600">
          Showing 234 recipes
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-700">Sort by:</span>
          <select className="px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-green-500">
            <option value="name">Name</option>
            <option value="rating">Rating</option>
            <option value="cookTime">Cook Time</option>
            <option value="difficulty">Difficulty</option>
            <option value="recent">Recently Added</option>
          </select>
        </div>
      </div>
    </div>
  )
}