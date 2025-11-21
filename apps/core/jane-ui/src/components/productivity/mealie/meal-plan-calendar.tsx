'use client'

import { useState } from 'react'

export function MealPlanCalendar() {
  const [selectedWeek, setSelectedWeek] = useState(0)
  
  const weekDays = [
    { name: 'Monday', date: '15' },
    { name: 'Tuesday', date: '16' },
    { name: 'Wednesday', date: '17' },
    { name: 'Thursday', date: '18' },
    { name: 'Friday', date: '19' },
    { name: 'Saturday', date: '20' },
    { name: 'Sunday', date: '21' }
  ]
  
  const mealPlan = {
    'Monday': {
      breakfast: 'Oatmeal with Berries',
      lunch: 'Caesar Salad',
      dinner: 'Chicken Alfredo Pasta'
    },
    'Tuesday': {
      breakfast: 'Greek Yogurt Parfait',
      lunch: 'Turkey Sandwich', 
      dinner: 'Beef Stir Fry'
    },
    'Wednesday': {
      breakfast: 'Scrambled Eggs',
      lunch: 'Quinoa Bowl',
      dinner: 'Salmon with Rice'
    },
    'Thursday': {
      breakfast: 'Smoothie Bowl',
      lunch: 'Chicken Wrap',
      dinner: 'Pasta Primavera'
    },
    'Friday': {
      breakfast: 'Pancakes',
      lunch: 'Soup & Salad',
      dinner: 'Pizza Night'
    },
    'Saturday': {
      breakfast: 'French Toast',
      lunch: 'Leftover Pizza',
      dinner: 'Grilled Chicken'
    },
    'Sunday': {
      breakfast: 'Breakfast Burrito',
      lunch: 'Sandwich',
      dinner: 'Meal Prep'
    }
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-medium text-gray-900">
            Week of December 15-21, 2024
          </h3>
          <div className="flex items-center space-x-2">
            <button className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50">
              Copy to Next Week
            </button>
            <button className="px-3 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700">
              Auto-Plan
            </button>
          </div>
        </div>
      </div>
      
      <div className="p-6">
        <div className="grid grid-cols-1 lg:grid-cols-7 gap-4">
          {weekDays.map((day) => {
            const meals = mealPlan[day.name as keyof typeof mealPlan]
            return (
              <div key={day.name} className="border border-gray-200 rounded-lg overflow-hidden">
                <div className="bg-gray-50 px-3 py-2 border-b border-gray-200">
                  <div className="text-center">
                    <h4 className="font-medium text-gray-900">{day.name}</h4>
                    <div className="text-sm text-gray-500">Dec {day.date}</div>
                  </div>
                </div>
                
                <div className="p-3 space-y-3">
                  {/* Breakfast */}
                  <div className="p-2 bg-yellow-50 border border-yellow-200 rounded">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-medium text-yellow-800">Breakfast</span>
                      <button className="text-xs text-yellow-600 hover:text-yellow-800">+</button>
                    </div>
                    {meals?.breakfast ? (
                      <div className="text-xs text-yellow-700 cursor-pointer hover:text-yellow-900">
                        {meals.breakfast}
                      </div>
                    ) : (
                      <div className="text-xs text-yellow-500 italic">Click to add</div>
                    )}
                  </div>
                  
                  {/* Lunch */}
                  <div className="p-2 bg-green-50 border border-green-200 rounded">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-medium text-green-800">Lunch</span>
                      <button className="text-xs text-green-600 hover:text-green-800">+</button>
                    </div>
                    {meals?.lunch ? (
                      <div className="text-xs text-green-700 cursor-pointer hover:text-green-900">
                        {meals.lunch}
                      </div>
                    ) : (
                      <div className="text-xs text-green-500 italic">Click to add</div>
                    )}
                  </div>
                  
                  {/* Dinner */}
                  <div className="p-2 bg-blue-50 border border-blue-200 rounded">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-medium text-blue-800">Dinner</span>
                      <button className="text-xs text-blue-600 hover:text-blue-800">+</button>
                    </div>
                    {meals?.dinner ? (
                      <div className="text-xs text-blue-700 cursor-pointer hover:text-blue-900">
                        {meals.dinner}
                      </div>
                    ) : (
                      <div className="text-xs text-blue-500 italic">Click to add</div>
                    )}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
        
        <div className="mt-8 p-4 bg-gray-50 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-gray-900">Weekly Summary</h4>
              <p className="text-sm text-gray-600">21 meals planned • 5 recipes repeated • Estimated prep time: 6 hours</p>
            </div>
            <div className="flex items-center space-x-3">
              <button className="px-4 py-2 border border-gray-300 rounded text-sm hover:bg-white">
                View Shopping List
              </button>
              <button className="px-4 py-2 bg-green-600 text-white rounded text-sm hover:bg-green-700">
                Generate Shopping List
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MealPlanCalendar