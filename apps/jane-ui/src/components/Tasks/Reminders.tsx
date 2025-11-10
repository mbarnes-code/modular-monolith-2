'use client';

import { useEffect, useState } from 'react';

interface Reminder {
  id: string;
  title: string;
  description: string;
  type: 'deadline' | 'follow_up' | 'break' | 'review' | 'focus';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  scheduledTime: Date;
  isActive: boolean;
  relatedTools?: string[];
  context?: string[];
  executiveFunctionType: 'time_management' | 'task_switching' | 'focus_maintenance' | 'memory_support';
}

interface RemindersProps {
  className?: string;
  onReminderAction?: (reminderId: string, action: 'snooze' | 'complete' | 'dismiss') => void;
  onCreateReminder?: (reminder: Partial<Reminder>) => void;
}

export function Reminders({
  className = '',
  onReminderAction,
  onCreateReminder
}: RemindersProps) {
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newReminder, setNewReminder] = useState<Partial<Reminder>>({
    type: 'deadline',
    priority: 'medium',
    executiveFunctionType: 'time_management'
  });
  const [filter, setFilter] = useState<'all' | 'active' | 'upcoming' | 'overdue'>('active');

  // Load and update reminders
  useEffect(() => {
    loadReminders();
    
    // Set up periodic reminder checking
    const interval = setInterval(() => {
      checkForActiveReminders();
    }, 30000); // Check every 30 seconds
    
    return () => clearInterval(interval);
  }, []);

  const loadReminders = () => {
    // Mock reminders with executive function focus
    const mockReminders: Reminder[] = [
      {
        id: 'rem-1',
        title: 'Take Focus Break',
        description: 'You\'ve been working for 45 minutes. Time for a 5-minute break to maintain cognitive performance.',
        type: 'break',
        priority: 'medium',
        scheduledTime: new Date(Date.now() + 5 * 60 * 1000), // 5 minutes from now
        isActive: true,
        executiveFunctionType: 'focus_maintenance',
        context: ['productivity', 'executive-function']
      },
      {
        id: 'rem-2',
        title: 'Security Review Deadline',
        description: 'MISP threat intelligence review due in 30 minutes.',
        type: 'deadline',
        priority: 'high',
        scheduledTime: new Date(Date.now() + 30 * 60 * 1000), // 30 minutes from now
        isActive: true,
        relatedTools: ['MISP', 'HELK'],
        executiveFunctionType: 'time_management',
        context: ['security', 'threat-intelligence']
      },
      {
        id: 'rem-3',
        title: 'Task Context Switch',
        description: 'Remember to save your current work before switching to the MTG deck analysis task.',
        type: 'follow_up',
        priority: 'medium',
        scheduledTime: new Date(Date.now() + 10 * 60 * 1000), // 10 minutes from now
        isActive: false,
        relatedTools: ['Commander Spellbook'],
        executiveFunctionType: 'task_switching',
        context: ['mtg', 'deck-analysis']
      }
    ];
    
    setReminders(mockReminders);
  };

  const checkForActiveReminders = () => {
    const now = new Date();
    setReminders(prev => prev.map(reminder => ({
      ...reminder,
      isActive: reminder.scheduledTime <= now && !reminder.isActive
    })));
  };

  const handleReminderAction = (reminderId: string, action: 'snooze' | 'complete' | 'dismiss') => {
    setReminders(prev => prev.map(reminder => {
      if (reminder.id === reminderId) {
        switch (action) {
          case 'snooze':
            return {
              ...reminder,
              scheduledTime: new Date(Date.now() + 10 * 60 * 1000), // Snooze for 10 minutes
              isActive: false
            };
          case 'complete':
          case 'dismiss':
            return {
              ...reminder,
              isActive: false
            };
          default:
            return reminder;
        }
      }
      return reminder;
    }));
    
    if (onReminderAction) {
      onReminderAction(reminderId, action);
    }
  };

  const handleCreateReminder = () => {
    if (!newReminder.title || !newReminder.scheduledTime) return;
    
    const reminder: Reminder = {
      id: `rem-${Date.now()}`,
      title: newReminder.title,
      description: newReminder.description || '',
      type: newReminder.type || 'deadline',
      priority: newReminder.priority || 'medium',
      scheduledTime: newReminder.scheduledTime,
      isActive: false,
      relatedTools: newReminder.relatedTools || [],
      context: newReminder.context || [],
      executiveFunctionType: newReminder.executiveFunctionType || 'time_management'
    };
    
    setReminders(prev => [...prev, reminder]);
    setNewReminder({
      type: 'deadline',
      priority: 'medium',
      executiveFunctionType: 'time_management'
    });
    setShowCreateForm(false);
    
    if (onCreateReminder) {
      onCreateReminder(reminder);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'border-red-500 bg-red-100 text-red-800';
      case 'high': return 'border-orange-400 bg-orange-100 text-orange-800';
      case 'medium': return 'border-yellow-400 bg-yellow-100 text-yellow-800';
      case 'low': return 'border-gray-400 bg-gray-100 text-gray-800';
      default: return 'border-gray-400 bg-gray-100 text-gray-800';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'deadline': return '⏰';
      case 'follow_up': return '🔄';
      case 'break': return '☕';
      case 'review': return '📋';
      case 'focus': return '🎯';
      default: return '📝';
    }
  };

  const getExecutiveFunctionLabel = (type: string) => {
    switch (type) {
      case 'time_management': return 'Time Management';
      case 'task_switching': return 'Task Switching';
      case 'focus_maintenance': return 'Focus Support';
      case 'memory_support': return 'Memory Aid';
      default: return 'Executive Function';
    }
  };

  const filteredReminders = reminders.filter(reminder => {
    const now = new Date();
    switch (filter) {
      case 'active':
        return reminder.isActive;
      case 'upcoming':
        return reminder.scheduledTime > now && !reminder.isActive;
      case 'overdue':
        return reminder.scheduledTime < now && !reminder.isActive;
      default:
        return true;
    }
  });

  const activeReminders = reminders.filter(r => r.isActive);

  return (
    <div className={`bg-white border rounded-lg shadow-sm ${className}`}>
      {/* Header */}
      <div className="border-b p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <h3 className="font-semibold text-gray-900">Smart Reminders</h3>
            {activeReminders.length > 0 && (
              <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full">
                {activeReminders.length}
              </span>
            )}
          </div>
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            + Add Reminder
          </button>
        </div>
        
        {/* Filter tabs */}
        <div className="mt-3 flex gap-1">
          {(['all', 'active', 'upcoming', 'overdue'] as const).map((filterType) => (
            <button
              key={filterType}
              onClick={() => setFilter(filterType)}
              className={`px-3 py-1 text-xs rounded-full capitalize ${
                filter === filterType
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              {filterType}
            </button>
          ))}
        </div>
      </div>

      {/* Active reminder alerts - Executive function accommodation */}
      {activeReminders.length > 0 && (
        <div className="bg-red-50 border-b border-red-200 p-4">
          <h4 className="font-medium text-red-800 mb-2">Active Reminders</h4>
          {activeReminders.map((reminder) => (
            <div key={reminder.id} className="bg-red-100 border border-red-300 rounded-lg p-3 mb-2 last:mb-0">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-lg">{getTypeIcon(reminder.type)}</span>
                    <h5 className="font-medium text-red-900">{reminder.title}</h5>
                  </div>
                  <p className="text-sm text-red-800">{reminder.description}</p>
                  
                  {/* Executive function context */}
                  <div className="mt-2 flex items-center gap-2">
                    <span className="text-xs bg-red-200 text-red-700 px-2 py-1 rounded">
                      {getExecutiveFunctionLabel(reminder.executiveFunctionType)}
                    </span>
                    {reminder.relatedTools && reminder.relatedTools.map((tool, index) => (
                      <span key={index} className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                        {tool}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div className="flex gap-2 ml-4">
                  <button
                    onClick={() => handleReminderAction(reminder.id, 'snooze')}
                    className="text-xs bg-yellow-600 text-white px-2 py-1 rounded hover:bg-yellow-700"
                  >
                    Snooze
                  </button>
                  <button
                    onClick={() => handleReminderAction(reminder.id, 'complete')}
                    className="text-xs bg-green-600 text-white px-2 py-1 rounded hover:bg-green-700"
                  >
                    Done
                  </button>
                  <button
                    onClick={() => handleReminderAction(reminder.id, 'dismiss')}
                    className="text-xs bg-gray-600 text-white px-2 py-1 rounded hover:bg-gray-700"
                  >
                    Dismiss
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create reminder form */}
      {showCreateForm && (
        <div className="border-b bg-gray-50 p-4">
          <h4 className="font-medium text-gray-900 mb-3">Create New Reminder</h4>
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
              <input
                type="text"
                value={newReminder.title || ''}
                onChange={(e) => setNewReminder(prev => ({ ...prev, title: e.target.value }))}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                placeholder="Reminder title..."
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea
                value={newReminder.description || ''}
                onChange={(e) => setNewReminder(prev => ({ ...prev, description: e.target.value }))}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500 resize-none"
                rows={2}
                placeholder="Additional details..."
              />
            </div>
            
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
                <select
                  value={newReminder.type || 'deadline'}
                  onChange={(e) => setNewReminder(prev => ({ ...prev, type: e.target.value as any }))}
                  className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                >
                  <option value="deadline">Deadline</option>
                  <option value="follow_up">Follow Up</option>
                  <option value="break">Break</option>
                  <option value="review">Review</option>
                  <option value="focus">Focus</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
                <select
                  value={newReminder.priority || 'medium'}
                  onChange={(e) => setNewReminder(prev => ({ ...prev, priority: e.target.value as any }))}
                  className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Executive Function Type</label>
              <select
                value={newReminder.executiveFunctionType || 'time_management'}
                onChange={(e) => setNewReminder(prev => ({ ...prev, executiveFunctionType: e.target.value as any }))}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
              >
                <option value="time_management">Time Management</option>
                <option value="task_switching">Task Switching</option>
                <option value="focus_maintenance">Focus Maintenance</option>
                <option value="memory_support">Memory Support</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Scheduled Time</label>
              <input
                type="datetime-local"
                value={newReminder.scheduledTime ? new Date(newReminder.scheduledTime.getTime() - newReminder.scheduledTime.getTimezoneOffset() * 60000).toISOString().slice(0, 16) : ''}
                onChange={(e) => setNewReminder(prev => ({ ...prev, scheduledTime: new Date(e.target.value) }))}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
              />
            </div>
            
            <div className="flex gap-2">
              <button
                onClick={handleCreateReminder}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700"
              >
                Create Reminder
              </button>
              <button
                onClick={() => setShowCreateForm(false)}
                className="bg-gray-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-700"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Reminders list */}
      <div className="p-4">
        {filteredReminders.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🔔</span>
            </div>
            <p className="text-sm mb-2">No {filter === 'all' ? '' : filter} reminders</p>
            <p className="text-xs">
              Smart reminders help you maintain focus and manage tasks effectively
            </p>
          </div>
        )}
        
        <div className="space-y-3">
          {filteredReminders.map((reminder) => (
            <div
              key={reminder.id}
              className={`border rounded-lg p-3 ${
                reminder.isActive ? 'border-red-300 bg-red-50' : 'border-gray-200'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm">{getTypeIcon(reminder.type)}</span>
                    <h5 className="font-medium text-gray-900">{reminder.title}</h5>
                    <span className={`text-xs px-2 py-1 rounded ${getPriorityColor(reminder.priority)}`}>
                      {reminder.priority}
                    </span>
                  </div>
                  
                  <p className="text-sm text-gray-600 mb-2">{reminder.description}</p>
                  
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <div className="flex items-center gap-2">
                      <span>{getExecutiveFunctionLabel(reminder.executiveFunctionType)}</span>
                      <span>•</span>
                      <span>{reminder.scheduledTime.toLocaleString()}</span>
                    </div>
                    
                    {reminder.relatedTools && reminder.relatedTools.length > 0 && (
                      <div className="flex gap-1">
                        {reminder.relatedTools.map((tool, index) => (
                          <span key={index} className="bg-blue-100 text-blue-700 px-2 py-1 rounded">
                            {tool}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
                
                {!reminder.isActive && (
                  <button
                    onClick={() => handleReminderAction(reminder.id, 'dismiss')}
                    className="ml-3 text-gray-400 hover:text-gray-600"
                  >
                    ✕
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Reminders;