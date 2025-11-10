'use client';

import { useCallback, useEffect, useState } from 'react';

interface UserPattern {
  id: string;
  type: 'temporal' | 'behavioral' | 'contextual' | 'performance';
  pattern: string;
  frequency: number;
  confidence: number;
  lastOccurrence: Date;
  contexts: string[];
  tools: string[];
}

interface ProactiveReminder {
  id: string;
  type: 'break' | 'context_switch' | 'deadline_warning' | 'focus_maintenance' | 'pattern_detected';
  title: string;
  message: string;
  urgency: 'low' | 'medium' | 'high' | 'critical';
  triggeredBy: UserPattern;
  suggestedAction: string;
  estimatedImpact: 'productivity' | 'focus' | 'wellbeing' | 'accuracy';
  scheduledTime: Date;
  dismissable: boolean;
  executiveFunctionSupport: {
    accommodationType: 'adhd' | 'autism' | 'general';
    supportType: 'time_awareness' | 'task_switching' | 'focus_regulation' | 'memory_aid';
    customization?: Record<string, unknown>;
  };
}

interface PatternRecognitionState {
  patterns: UserPattern[];
  activeReminders: ProactiveReminder[];
  isLearning: boolean;
  confidence: number;
  lastAnalysis: Date | null;
}

class ProactiveReminderService {
  private patterns: Map<string, UserPattern> = new Map();
  private activeReminders: ProactiveReminder[] = [];
  private behaviorHistory: Array<{
    timestamp: Date;
    tool: string;
    action: string;
    context: string[];
    duration?: number;
  }> = [];
  private userPreferences = {
    reminderFrequency: 'moderate' as 'minimal' | 'moderate' | 'frequent',
    breakInterval: 45, // minutes
    focusThreshold: 90, // minutes before focus reminder
    accommodations: ['adhd', 'time_awareness'] as string[]
  };

  /**
   * Record user activity for pattern analysis
   */
  recordActivity(tool: string, action: string, context: string[] = [], duration?: number) {
    this.behaviorHistory.push({
      timestamp: new Date(),
      tool,
      action,
      context,
      duration
    });

    // Keep only last 1000 activities for performance
    if (this.behaviorHistory.length > 1000) {
      this.behaviorHistory = this.behaviorHistory.slice(-1000);
    }

    // Analyze patterns asynchronously
    setTimeout(() => this.analyzePatterns(), 100);
  }

  /**
   * Get current active reminders
   */
  getActiveReminders(): ProactiveReminder[] {
    return this.activeReminders.filter(reminder => 
      reminder.scheduledTime <= new Date()
    );
  }

  /**
   * Get upcoming reminders
   */
  getUpcomingReminders(minutesAhead: number = 30): ProactiveReminder[] {
    const cutoff = new Date(Date.now() + minutesAhead * 60 * 1000);
    return this.activeReminders.filter(reminder => 
      reminder.scheduledTime > new Date() && reminder.scheduledTime <= cutoff
    );
  }

  /**
   * Dismiss a reminder
   */
  dismissReminder(reminderId: string) {
    this.activeReminders = this.activeReminders.filter(r => r.id !== reminderId);
  }

  /**
   * Snooze a reminder
   */
  snoozeReminder(reminderId: string, minutes: number = 10) {
    const reminder = this.activeReminders.find(r => r.id === reminderId);
    if (reminder) {
      reminder.scheduledTime = new Date(Date.now() + minutes * 60 * 1000);
    }
  }

  /**
   * Update user preferences for personalized reminders
   */
  updatePreferences(preferences: Partial<typeof this.userPreferences>) {
    this.userPreferences = { ...this.userPreferences, ...preferences };
    this.reanalyzeAllPatterns();
  }

  private analyzePatterns() {
    this.analyzeTemporalPatterns();
    this.analyzeBehavioralPatterns();
    this.analyzeContextualPatterns();
    this.analyzePerformancePatterns();
    this.generateProactiveReminders();
  }

  private analyzeTemporalPatterns() {
    // Analyze work session durations
    const sessions = this.groupActivitiesBySession();
    
    sessions.forEach(session => {
      const duration = session.endTime.getTime() - session.startTime.getTime();
      const durationMinutes = duration / (1000 * 60);
      
      if (durationMinutes > this.userPreferences.focusThreshold) {
        this.updatePattern({
          id: 'long-focus-session',
          type: 'temporal',
          pattern: 'extended_focus_session',
          frequency: this.getPatternFrequency('extended_focus_session'),
          confidence: 0.8,
          lastOccurrence: session.endTime,
          contexts: session.contexts,
          tools: session.tools
        });
      }
    });

    // Analyze break patterns
    const breakIntervals = this.calculateBreakIntervals();
    if (breakIntervals.average > this.userPreferences.breakInterval * 1.5) {
      this.updatePattern({
        id: 'infrequent-breaks',
        type: 'temporal',
        pattern: 'skipping_breaks',
        frequency: this.getPatternFrequency('skipping_breaks'),
        confidence: 0.9,
        lastOccurrence: new Date(),
        contexts: [],
        tools: []
      });
    }
  }

  private analyzeBehavioralPatterns() {
    const recentActivities = this.behaviorHistory.slice(-50);
    
    // Tool switching frequency
    const toolSwitches = this.countToolSwitches(recentActivities);
    if (toolSwitches > 10) {
      this.updatePattern({
        id: 'frequent-tool-switching',
        type: 'behavioral',
        pattern: 'context_switching',
        frequency: toolSwitches,
        confidence: 0.85,
        lastOccurrence: new Date(),
        contexts: ['productivity'],
        tools: [...new Set(recentActivities.map(a => a.tool))]
      });
    }

    // Repetitive action patterns
    const actionCounts = recentActivities.reduce((acc, activity) => {
      acc[activity.action] = (acc[activity.action] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    Object.entries(actionCounts).forEach(([action, count]) => {
      if (count > 5) {
        this.updatePattern({
          id: `repetitive-${action}`,
          type: 'behavioral',
          pattern: 'repetitive_action',
          frequency: count,
          confidence: 0.7,
          lastOccurrence: new Date(),
          contexts: ['automation_opportunity'],
          tools: []
        });
      }
    });
  }

  private analyzeContextualPatterns() {
    const contextSwitches = this.behaviorHistory
      .slice(-20)
      .reduce((switches, activity, index, arr) => {
        if (index > 0 && arr[index - 1].context.join() !== activity.context.join()) {
          switches++;
        }
        return switches;
      }, 0);

    if (contextSwitches > 8) {
      this.updatePattern({
        id: 'frequent-context-switching',
        type: 'contextual',
        pattern: 'context_fragmentation',
        frequency: contextSwitches,
        confidence: 0.8,
        lastOccurrence: new Date(),
        contexts: ['executive_function'],
        tools: []
      });
    }
  }

  private analyzePerformancePatterns() {
    // Analyze response times and error patterns
    const performanceMetrics = this.calculatePerformanceMetrics();
    
    if (performanceMetrics.averageResponseTime > 2000) {
      this.updatePattern({
        id: 'degraded-performance',
        type: 'performance',
        pattern: 'performance_degradation',
        frequency: 1,
        confidence: 0.9,
        lastOccurrence: new Date(),
        contexts: ['performance'],
        tools: []
      });
    }
  }

  private generateProactiveReminders() {
    this.patterns.forEach(pattern => {
      const reminders = this.generateRemindersForPattern(pattern);
      this.activeReminders.push(...reminders);
    });

    // Remove duplicate reminders
    this.activeReminders = this.activeReminders.filter((reminder, index, self) =>
      index === self.findIndex(r => r.id === reminder.id)
    );
  }

  private generateRemindersForPattern(pattern: UserPattern): ProactiveReminder[] {
    const reminders: ProactiveReminder[] = [];
    const now = new Date();

    switch (pattern.pattern) {
      case 'extended_focus_session':
        if (pattern.confidence > 0.7) {
          reminders.push({
            id: `break-reminder-${Date.now()}`,
            type: 'break',
            title: 'Take a Focus Break',
            message: 'You\'ve been focusing for a while. A 5-minute break will help maintain your cognitive performance.',
            urgency: 'medium',
            triggeredBy: pattern,
            suggestedAction: 'Take a 5-minute break away from screens',
            estimatedImpact: 'focus',
            scheduledTime: new Date(now.getTime() + 5 * 60 * 1000),
            dismissable: true,
            executiveFunctionSupport: {
              accommodationType: 'adhd',
              supportType: 'focus_regulation'
            }
          });
        }
        break;

      case 'skipping_breaks':
        reminders.push({
          id: `break-pattern-${Date.now()}`,
          type: 'break',
          title: 'Break Pattern Detected',
          message: 'You\'ve been skipping breaks lately. Regular breaks are crucial for sustained attention.',
          urgency: 'high',
          triggeredBy: pattern,
          suggestedAction: 'Set up automatic break reminders',
          estimatedImpact: 'wellbeing',
          scheduledTime: now,
          dismissable: true,
          executiveFunctionSupport: {
            accommodationType: 'adhd',
            supportType: 'time_awareness'
          }
        });
        break;

      case 'context_switching':
        if (pattern.frequency > 15) {
          reminders.push({
            id: `context-switching-${Date.now()}`,
            type: 'context_switch',
            title: 'High Context Switching Detected',
            message: 'Frequent tool switching can impact focus. Consider batching similar tasks.',
            urgency: 'medium',
            triggeredBy: pattern,
            suggestedAction: 'Group similar tasks together or use focus mode',
            estimatedImpact: 'productivity',
            scheduledTime: new Date(now.getTime() + 2 * 60 * 1000),
            dismissable: true,
            executiveFunctionSupport: {
              accommodationType: 'adhd',
              supportType: 'task_switching'
            }
          });
        }
        break;

      case 'repetitive_action':
        reminders.push({
          id: `automation-${Date.now()}`,
          type: 'pattern_detected',
          title: 'Automation Opportunity',
          message: 'You\'ve been repeating similar actions. Consider creating a workflow to automate this.',
          urgency: 'low',
          triggeredBy: pattern,
          suggestedAction: 'Create an n8n workflow for this repetitive task',
          estimatedImpact: 'productivity',
          scheduledTime: new Date(now.getTime() + 10 * 60 * 1000),
          dismissable: true,
          executiveFunctionSupport: {
            accommodationType: 'general',
            supportType: 'memory_aid'
          }
        });
        break;

      case 'performance_degradation':
        reminders.push({
          id: `performance-${Date.now()}`,
          type: 'focus_maintenance',
          title: 'Performance Decline Detected',
          message: 'System performance has declined. This might affect your cognitive load.',
          urgency: 'high',
          triggeredBy: pattern,
          suggestedAction: 'Check system resources or switch to lighter tools',
          estimatedImpact: 'accuracy',
          scheduledTime: now,
          dismissable: false,
          executiveFunctionSupport: {
            accommodationType: 'autism',
            supportType: 'focus_regulation'
          }
        });
        break;
    }

    return reminders;
  }

  private updatePattern(pattern: UserPattern) {
    this.patterns.set(pattern.id, pattern);
  }

  private getPatternFrequency(patternType: string): number {
    return this.behaviorHistory.filter(activity => 
      activity.action.includes(patternType) || 
      activity.context.some(ctx => ctx.includes(patternType))
    ).length;
  }

  private groupActivitiesBySession() {
    const sessions: Array<{
      startTime: Date;
      endTime: Date;
      tools: string[];
      contexts: string[];
    }> = [];

    let currentSession: {
      startTime: Date;
      endTime: Date;
      tools: Set<string>;
      contexts: Set<string>;
    } | null = null;

    this.behaviorHistory.forEach(activity => {
      if (!currentSession || 
          activity.timestamp.getTime() - currentSession.endTime.getTime() > 15 * 60 * 1000) {
        // New session (15+ minute gap)
        if (currentSession) {
          sessions.push({
            startTime: currentSession.startTime,
            endTime: currentSession.endTime,
            tools: Array.from(currentSession.tools),
            contexts: Array.from(currentSession.contexts)
          });
        }
        
        currentSession = {
          startTime: activity.timestamp,
          endTime: activity.timestamp,
          tools: new Set([activity.tool]),
          contexts: new Set(activity.context)
        };
      } else {
        // Continue current session
        currentSession.endTime = activity.timestamp;
        currentSession.tools.add(activity.tool);
        activity.context.forEach(ctx => currentSession!.contexts.add(ctx));
      }
    });

    if (currentSession) {
      sessions.push({
        startTime: currentSession.startTime,
        endTime: currentSession.endTime,
        tools: Array.from(currentSession.tools),
        contexts: Array.from(currentSession.contexts)
      });
    }

    return sessions;
  }

  private calculateBreakIntervals(): { average: number; median: number } {
    const intervals: number[] = [];
    const sessions = this.groupActivitiesBySession();

    for (let i = 1; i < sessions.length; i++) {
      const breakDuration = sessions[i].startTime.getTime() - sessions[i - 1].endTime.getTime();
      const breakMinutes = breakDuration / (1000 * 60);
      if (breakMinutes > 0 && breakMinutes < 480) { // Ignore breaks longer than 8 hours
        intervals.push(breakMinutes);
      }
    }

    const average = intervals.length > 0 ? intervals.reduce((a, b) => a + b, 0) / intervals.length : 0;
    const median = intervals.length > 0 ? intervals.sort((a, b) => a - b)[Math.floor(intervals.length / 2)] : 0;

    return { average, median };
  }

  private countToolSwitches(activities: typeof this.behaviorHistory): number {
    let switches = 0;
    for (let i = 1; i < activities.length; i++) {
      if (activities[i].tool !== activities[i - 1].tool) {
        switches++;
      }
    }
    return switches;
  }

  private calculatePerformanceMetrics(): { averageResponseTime: number; errorRate: number } {
    // Mock performance calculation
    return {
      averageResponseTime: Math.random() * 3000,
      errorRate: Math.random() * 0.1
    };
  }

  private reanalyzeAllPatterns() {
    this.patterns.clear();
    this.analyzePatterns();
  }
}

// Create singleton instance
export const proactiveReminderService = new ProactiveReminderService();

// React hook for using the proactive reminder system
export function useProactiveReminders() {
  const [state, setState] = useState<PatternRecognitionState>({
    patterns: [],
    activeReminders: [],
    isLearning: false,
    confidence: 0,
    lastAnalysis: null
  });

  // Record user activity
  const recordActivity = useCallback((tool: string, action: string, context: string[] = [], duration?: number) => {
    proactiveReminderService.recordActivity(tool, action, context, duration);
    refreshState();
  }, []);

  // Get active reminders
  const getActiveReminders = useCallback(() => {
    return proactiveReminderService.getActiveReminders();
  }, []);

  // Get upcoming reminders
  const getUpcomingReminders = useCallback((minutesAhead?: number) => {
    return proactiveReminderService.getUpcomingReminders(minutesAhead);
  }, []);

  // Dismiss reminder
  const dismissReminder = useCallback((reminderId: string) => {
    proactiveReminderService.dismissReminder(reminderId);
    refreshState();
  }, []);

  // Snooze reminder
  const snoozeReminder = useCallback((reminderId: string, minutes?: number) => {
    proactiveReminderService.snoozeReminder(reminderId, minutes);
    refreshState();
  }, []);

  // Update preferences
  const updatePreferences = useCallback((preferences: Record<string, unknown>) => {
    proactiveReminderService.updatePreferences(preferences);
    refreshState();
  }, []);

  // Refresh state from service
  const refreshState = useCallback(() => {
    setState({
      patterns: Array.from((proactiveReminderService as any).patterns.values()),
      activeReminders: proactiveReminderService.getActiveReminders(),
      isLearning: true,
      confidence: 0.8,
      lastAnalysis: new Date()
    });
  }, []);

  // Auto-refresh state periodically
  useEffect(() => {
    refreshState();
    
    const interval = setInterval(refreshState, 10000); // Every 10 seconds
    return () => clearInterval(interval);
  }, [refreshState]);

  return {
    ...state,
    recordActivity,
    getActiveReminders,
    getUpcomingReminders,
    dismissReminder,
    snoozeReminder,
    updatePreferences,
    refreshState
  };
}

export type { PatternRecognitionState, ProactiveReminder, UserPattern };
