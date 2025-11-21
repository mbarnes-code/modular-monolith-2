'use client'

import Link from 'next/link'

export function MealPlan() {
  const weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  
  const mealPlan = {
    'Mon': {
      breakfast: 'Oatmeal with Berries',
      lunch: 'Caesar Salad',
      dinner: 'Chicken Alfredo Pasta'
    },
    'Tue': {
      breakfast: 'Greek Yogurt Parfait',
      lunch: 'Turkey Sandwich', 
      dinner: 'Beef Stir Fry'
    },
    'Wed': {
      breakfast: 'Scrambled Eggs',
      lunch: 'Quinoa Bowl',
      dinner: 'Salmon with Rice'
    },
    'Thu': {
      breakfast: 'Smoothie Bowl',
      lunch: 'Chicken Wrap',
      dinner: 'Pasta Primavera'
    },
    'Fri': {
      breakfast: 'Pancakes',
      lunch: 'Soup & Salad',
      dinner: 'Pizza Night'
    },
    'Sat': {
      breakfast: 'French Toast',
      lunch: 'Leftover Pizza',
      dinner: 'Grilled Chicken'
    },
    'Sun': {
      breakfast: 'Breakfast Burrito',
      lunch: 'Sandwich',
      dinner: 'Meal Prep'
    }
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-medium text-gray-900">This Week's Meal Plan</h3>
          <Link
            href="/productivity/mealie/meal-plans"
            className="text-green-600 hover:text-green-700 text-sm font-medium"
          >
            Edit plan
          </Link>
        </div>
      </div>
      
      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-7 gap-4">
          {weekDays.map((day) => {
            const meals = mealPlan[day as keyof typeof mealPlan]
            return (
              <div key={day} className="space-y-3">
                <div className="text-center">
                  <h4 className="font-medium text-gray-900">{day}</h4>
                  <div className="text-xs text-gray-500">Dec {15 + weekDays.indexOf(day)}</div>
                </div>
                
                <div className="space-y-2">
                  <div className="p-2 bg-yellow-50 border border-yellow-200 rounded text-xs">
                    <div className="font-medium text-yellow-800">Breakfast</div>
                    <div className="text-yellow-700">{meals?.breakfast || 'Not planned'}</div>
                  </div>
                  
                  <div className="p-2 bg-green-50 border border-green-200 rounded text-xs">
                    <div className="font-medium text-green-800">Lunch</div>
                    <div className="text-green-700">{meals?.lunch || 'Not planned'}</div>
                  </div>
                  
                  <div className="p-2 bg-blue-50 border border-blue-200 rounded text-xs">
                    <div className="font-medium text-blue-800">Dinner</div>
                    <div className="text-blue-700">{meals?.dinner || 'Not planned'}</div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
        
        <div className="mt-6 text-center">
          <Link
            href="/productivity/mealie/shopping-lists"
            className="inline-flex items-center px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-md hover:bg-green-700 transition-colors"
          >
            <span className="mr-2">🛒</span>
            Generate Shopping List
          </Link>
        </div>
      </div>
    </div>
  )
}

export default MealPlan