/**
 * Task Tracker Component
 * 
 * Visual task progress tracking with executive function support
 * Helps users maintain awareness of task completion and progress
 */

import React, { useState } from 'react';
import { TaskProgress } from './types';

interface TaskTrackerProps {
  /** Array of tasks to track */
  tasks: TaskProgress[];
  /** Whether to show detailed progress */
  showDetails?: boolean;
  /** Whether to show time estimates */
  showTimeEstimates?: boolean;
  /** Whether to show executive function accommodations used */
  showAccommodations?: boolean;
  /** Callback when task is updated */
  onTaskUpdate?: (taskId: string, updates: Partial<TaskProgress>) => void;
  /** Maximum number of tasks to display */
  maxDisplayTasks?: number;
}

export const TaskTracker: React.FC<TaskTrackerProps> = ({
  tasks,
  showDetails = true,
  showTimeEstimates = true,
  showAccommodations = false,
  onTaskUpdate,
  maxDisplayTasks = 10
}) => {
  const [expandedTasks, setExpandedTasks] = useState<Set<string>>(new Set());
  const [sortBy, setSortBy] = useState<'progress' | 'time' | 'activity'>('progress');

  const sortedTasks = [...tasks]
    .sort((a, b) => {
      switch (sortBy) {
        case 'progress':
          return b.completion_percentage - a.completion_percentage;
        case 'time':
          return a.estimated_time_remaining - b.estimated_time_remaining;
        case 'activity':
          return new Date(b.last_activity).getTime() - new Date(a.last_activity).getTime();
        default:
          return 0;
      }
    })
    .slice(0, maxDisplayTasks);

  const toggleExpanded = (taskId: string) => {
    const newExpanded = new Set(expandedTasks);
    if (newExpanded.has(taskId)) {
      newExpanded.delete(taskId);
    } else {
      newExpanded.add(taskId);
    }
    setExpandedTasks(newExpanded);
  };

  const formatTime = (minutes: number): string => {
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };

  const getProgressColor = (percentage: number): string => {
    if (percentage >= 90) return '#22c55e'; // green
    if (percentage >= 70) return '#3b82f6'; // blue
    if (percentage >= 40) return '#f59e0b'; // amber
    return '#ef4444'; // red
  };

  return (
    <div className="mental-prosthetic-task-tracker">
      <div className="task-tracker-header">
        <h3>Task Progress</h3>
        <div className="sort-controls">
          <label htmlFor="sort-select">Sort by:</label>
          <select
            id="sort-select"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as typeof sortBy)}
            className="sort-select"
          >
            <option value="progress">Progress</option>
            <option value="time">Time Remaining</option>
            <option value="activity">Recent Activity</option>
          </select>
        </div>
      </div>

      <div className="task-list">
        {sortedTasks.map((task) => {
          const isExpanded = expandedTasks.has(task.task_id);
          const progressColor = getProgressColor(task.completion_percentage);

          return (
            <div
              key={task.task_id}
              className={`task-item ${isExpanded ? 'expanded' : ''}`}
            >
              <div className="task-summary" onClick={() => toggleExpanded(task.task_id)}>
                <div className="task-info">
                  <h4 className="task-title">{task.task_title}</h4>
                  <div className="task-meta">
                    <span className="completion-percentage">
                      {task.completion_percentage}% complete
                    </span>
                    {showTimeEstimates && task.estimated_time_remaining > 0 && (
                      <span className="time-remaining">
                        {formatTime(task.estimated_time_remaining)} remaining
                      </span>
                    )}
                  </div>
                </div>
                
                <div className="progress-visual">
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{
                        width: `${task.completion_percentage}%`,
                        backgroundColor: progressColor
                      }}
                    />
                  </div>
                  <button
                    className="expand-button"
                    aria-label={isExpanded ? 'Collapse task details' : 'Expand task details'}
                  >
                    {isExpanded ? '▼' : '▶'}
                  </button>
                </div>
              </div>

              {isExpanded && showDetails && (
                <div className="task-details">
                  <div className="subtask-progress">
                    <span>Subtasks: {task.subtasks_completed}/{task.subtasks_total}</span>
                    <div className="subtask-bar">
                      <div
                        className="subtask-fill"
                        style={{
                          width: `${(task.subtasks_completed / task.subtasks_total) * 100}%`,
                          backgroundColor: progressColor
                        }}
                      />
                    </div>
                  </div>

                  <div className="last-activity">
                    <strong>Last activity:</strong> {task.last_activity.toLocaleString()}
                  </div>

                  {showAccommodations && task.executive_function_accommodations_used.length > 0 && (
                    <div className="accommodations-used">
                      <strong>Accommodations used:</strong>
                      <ul>
                        {task.executive_function_accommodations_used.map((accommodation, index) => (
                          <li key={index}>{accommodation}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {onTaskUpdate && (
                    <div className="task-actions">
                      <button
                        onClick={() => onTaskUpdate(task.task_id, {
                          completion_percentage: Math.min(100, task.completion_percentage + 10)
                        })}
                        className="update-progress-btn"
                      >
                        +10% Progress
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {tasks.length > maxDisplayTasks && (
        <div className="task-overflow-notice">
          Showing {maxDisplayTasks} of {tasks.length} tasks
        </div>
      )}

      <style jsx>{`
        .mental-prosthetic-task-tracker {
          border: 1px solid #e2e8f0;
          border-radius: 8px;
          padding: 16px;
          background: white;
          font-family: system-ui, -apple-system, sans-serif;
        }

        .task-tracker-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 16px;
          padding-bottom: 8px;
          border-bottom: 1px solid #e2e8f0;
        }

        .task-tracker-header h3 {
          margin: 0;
          color: #1e293b;
        }

        .sort-controls {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .sort-select {
          padding: 4px 8px;
          border: 1px solid #d1d5db;
          border-radius: 4px;
          font-size: 14px;
        }

        .task-item {
          border: 1px solid #f1f5f9;
          border-radius: 6px;
          margin-bottom: 8px;
          background: #fefefe;
          transition: all 0.15s ease;
        }

        .task-item:hover {
          border-color: #cbd5e1;
          box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .task-summary {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 12px;
          cursor: pointer;
        }

        .task-info {
          flex: 1;
        }

        .task-title {
          margin: 0 0 4px 0;
          font-size: 16px;
          color: #374151;
        }

        .task-meta {
          display: flex;
          gap: 16px;
          font-size: 14px;
          color: #6b7280;
        }

        .progress-visual {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .progress-bar {
          width: 120px;
          height: 8px;
          background: #f1f5f9;
          border-radius: 4px;
          overflow: hidden;
        }

        .progress-fill {
          height: 100%;
          transition: width 0.3s ease;
        }

        .expand-button {
          background: none;
          border: none;
          font-size: 12px;
          color: #6b7280;
          cursor: pointer;
          padding: 4px;
        }

        .task-details {
          padding: 0 12px 12px 12px;
          border-top: 1px solid #f1f5f9;
          background: #f8fafc;
        }

        .subtask-progress {
          margin: 12px 0;
        }

        .subtask-bar {
          width: 100%;
          height: 6px;
          background: #f1f5f9;
          border-radius: 3px;
          margin-top: 4px;
          overflow: hidden;
        }

        .subtask-fill {
          height: 100%;
          transition: width 0.3s ease;
        }

        .last-activity {
          margin: 8px 0;
          font-size: 14px;
          color: #6b7280;
        }

        .accommodations-used {
          margin: 8px 0;
          font-size: 14px;
        }

        .accommodations-used ul {
          margin: 4px 0 0 16px;
        }

        .accommodations-used li {
          margin: 2px 0;
          color: #6b7280;
        }

        .task-actions {
          margin-top: 12px;
          padding-top: 8px;
          border-top: 1px solid #e2e8f0;
        }

        .update-progress-btn {
          background: #3b82f6;
          color: white;
          border: none;
          padding: 6px 12px;
          border-radius: 4px;
          font-size: 14px;
          cursor: pointer;
          transition: background 0.15s ease;
        }

        .update-progress-btn:hover {
          background: #2563eb;
        }

        .task-overflow-notice {
          text-align: center;
          padding: 8px;
          color: #6b7280;
          font-size: 14px;
          font-style: italic;
        }
      `}</style>
    </div>
  );
};