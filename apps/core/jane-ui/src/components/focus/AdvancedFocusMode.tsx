/**
 * Advanced Focus Mode Component
 * Executive function support with deep work capabilities and distraction blocking
 */

import React, { useState, useEffect, useRef } from 'react';
import { useSharedContext } from '../../services/state/optimizedStateManager';
import { usePerformanceMonitor } from '../../services/performance/performanceMonitor';

interface FocusSession {
  id: string;
  type: 'focus' | 'deep-work' | 'flow-state';
  duration: number; // in minutes
  tool?: string;
  startTime: number;
  endTime?: number;
  breaks: { start: number; end: number; type: 'micro' | 'short' | 'long' }[];
  productivity: number; // 0-100 score
  distractions: number;
  completed: boolean;
}

interface FocusModeProps {
  className?: string;
  onModeChange?: (mode: 'normal' | 'focus' | 'deep-work', active: boolean) => void;
}

const FOCUS_PRESETS = {
  'pomodoro': { duration: 25, break: 5, type: 'focus' as const },
  'deep-work': { duration: 90, break: 15, type: 'deep-work' as const },
  'flow-state': { duration: 120, break: 20, type: 'flow-state' as const },
  'micro-focus': { duration: 15, break: 3, type: 'focus' as const }
};

export function AdvancedFocusMode({ className = '', onModeChange }: FocusModeProps) {
  const sharedContext = useSharedContext();
  const { enableFocusMode, disableFocusMode, markUIInteraction } = usePerformanceMonitor();
  
  const [isActive, setIsActive] = useState(false);
  const [currentSession, setCurrentSession] = useState<FocusSession | null>(null);
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [selectedPreset, setSelectedPreset] = useState<keyof typeof FOCUS_PRESETS>('pomodoro');
  const [customDuration, setCustomDuration] = useState(25);
  const [inBreak, setInBreak] = useState(false);
  const [distractionCount, setDistractionCount] = useState(0);
  const [showStats, setShowStats] = useState(false);
  const [sessions, setSessions] = useState<FocusSession[]>([]);
  
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Load focus mode state from shared context
  useEffect(() => {
    const focusState = sharedContext.userFocus;
    if (focusState.mode !== 'normal' && focusState.timeRemaining) {
      setIsActive(true);
      setTimeRemaining(focusState.timeRemaining);
    }
  }, [sharedContext.userFocus]);

  // Timer logic
  useEffect(() => {
    if (isActive && timeRemaining > 0) {
      timerRef.current = setInterval(() => {
        setTimeRemaining(prev => {
          const newTime = prev - 1;
          
          // Update shared context
          sharedContext.setFocusMode(
            currentSession?.type || 'focus',
            sharedContext.userFocus.currentTool,
            newTime
          );
          
          if (newTime <= 0) {
            handleSessionEnd();
            return 0;
          }
          return newTime;
        });
      }, 1000);
    } else if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    };
  }, [isActive, timeRemaining]);

  // Initialize audio for notifications
  useEffect(() => {
    if (typeof window !== 'undefined') {
      audioRef.current = new Audio();
      // Use a simple beep sound or notification sound
      audioRef.current.src = 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmMABji8xP'; // Basic beep
    }
  }, []);

  const startFocusSession = (preset: keyof typeof FOCUS_PRESETS) => {
    markUIInteraction('focus-session-start');
    
    const config = FOCUS_PRESETS[preset];
    const duration = preset === 'custom' ? customDuration : config.duration;
    
    const session: FocusSession = {
      id: `session-${Date.now()}`,
      type: config.type,
      duration,
      tool: sharedContext.userFocus.currentTool,
      startTime: Date.now(),
      breaks: [],
      productivity: 0,
      distractions: 0,
      completed: false
    };

    setCurrentSession(session);
    setTimeRemaining(duration * 60); // Convert to seconds
    setIsActive(true);
    setInBreak(false);
    setDistractionCount(0);

    // Enable focus mode in performance monitor
    enableFocusMode();
    
    // Update shared context
    sharedContext.setFocusMode(config.type, sharedContext.userFocus.currentTool, duration * 60);
    
    // Notify parent component
    onModeChange?.(config.type, true);

    // Apply focus styling
    document.body.classList.add('focus-mode-active');
    
    // Optional: Play start sound
    playNotification('start');
  };

  const handleSessionEnd = () => {
    if (!currentSession) return;

    const endTime = Date.now();
    const actualDuration = (endTime - currentSession.startTime) / (1000 * 60); // minutes
    const productivity = calculateProductivity(currentSession, actualDuration);

    const completedSession: FocusSession = {
      ...currentSession,
      endTime,
      productivity,
      distractions: distractionCount,
      completed: true
    };

    // Add to sessions history
    setSessions(prev => [completedSession, ...prev.slice(0, 9)]); // Keep last 10 sessions

    // Reset state
    setIsActive(false);
    setCurrentSession(null);
    setTimeRemaining(0);
    setInBreak(false);
    
    // Disable focus mode
    disableFocusMode();
    sharedContext.setFocusMode('normal');
    
    // Notify parent component
    onModeChange?.('normal', false);
    
    // Remove focus styling
    document.body.classList.remove('focus-mode-active');
    
    // Play completion sound
    playNotification('complete');
    
    // Show session summary
    setTimeout(() => setShowStats(true), 500);
  };

  const pauseSession = () => {
    setIsActive(false);
    markUIInteraction('focus-session-pause');
  };

  const resumeSession = () => {
    setIsActive(true);
    markUIInteraction('focus-session-resume');
  };

  const cancelSession = () => {
    if (currentSession) {
      const canceledSession: FocusSession = {
        ...currentSession,
        endTime: Date.now(),
        productivity: 0,
        distractions: distractionCount,
        completed: false
      };
      setSessions(prev => [canceledSession, ...prev.slice(0, 9)]);
    }

    setIsActive(false);
    setCurrentSession(null);
    setTimeRemaining(0);
    setInBreak(false);
    
    disableFocusMode();
    sharedContext.setFocusMode('normal');
    onModeChange?.('normal', false);
    document.body.classList.remove('focus-mode-active');
    
    markUIInteraction('focus-session-cancel');
  };

  const takeBreak = (type: 'micro' | 'short' | 'long') => {
    if (!currentSession) return;
    
    const breakDuration = type === 'micro' ? 2 : type === 'short' ? 5 : 15; // minutes
    setInBreak(true);
    setTimeRemaining(breakDuration * 60);
    
    currentSession.breaks.push({
      start: Date.now(),
      end: Date.now() + (breakDuration * 60 * 1000),
      type
    });
    
    markUIInteraction(`focus-break-${type}`);
  };

  const calculateProductivity = (session: FocusSession, actualDuration: number): number => {
    const plannedDuration = session.duration;
    const completionRate = Math.min(actualDuration / plannedDuration, 1) * 100;
    const distractionPenalty = Math.min(session.distractions * 5, 50);
    return Math.max(0, completionRate - distractionPenalty);
  };

  const playNotification = (type: 'start' | 'complete' | 'break') => {
    if (audioRef.current && 'Notification' in window) {
      audioRef.current.play().catch(() => {
        // Fallback to system notification
        new Notification(`Focus Session ${type === 'start' ? 'Started' : type === 'complete' ? 'Completed' : 'Break Time'}!`);
      });
    }
  };

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getSessionStats = () => {
    if (sessions.length === 0) return null;
    
    const completedSessions = sessions.filter(s => s.completed);
    const totalSessions = sessions.length;
    const avgProductivity = completedSessions.reduce((sum, s) => sum + s.productivity, 0) / Math.max(completedSessions.length, 1);
    const totalFocusTime = completedSessions.reduce((sum, s) => sum + s.duration, 0);
    
    return {
      totalSessions,
      completedSessions: completedSessions.length,
      avgProductivity: Math.round(avgProductivity),
      totalFocusTime: Math.round(totalFocusTime)
    };
  };

  if (isActive && currentSession) {
    return (
      <div className={`advanced-focus-mode ${className}`}>
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-900 rounded-2xl p-8 max-w-md w-full mx-4 border border-gray-200 dark:border-gray-700">
            {/* Session Type Header */}
            <div className="text-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                {inBreak ? '☕ Break Time' : 
                 currentSession.type === 'deep-work' ? '🧠 Deep Work' :
                 currentSession.type === 'flow-state' ? '🌊 Flow State' : '🎯 Focus Mode'}
              </h2>
              <p className="text-gray-600 dark:text-gray-400">
                {inBreak ? 'Take a moment to recharge' : `Working on ${currentSession.tool || 'current task'}`}
              </p>
            </div>

            {/* Timer Display */}
            <div className="text-center mb-8">
              <div className="text-6xl font-mono font-bold text-blue-600 dark:text-blue-400 mb-4">
                {formatTime(timeRemaining)}
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-1000"
                  style={{
                    width: `${((currentSession.duration * 60 - timeRemaining) / (currentSession.duration * 60)) * 100}%`
                  }}
                />
              </div>
            </div>

            {/* Session Info */}
            <div className="grid grid-cols-2 gap-4 mb-6 text-center">
              <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-3">
                <div className="text-sm text-gray-600 dark:text-gray-400">Duration</div>
                <div className="font-semibold text-gray-900 dark:text-white">
                  {currentSession.duration}min
                </div>
              </div>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-3">
                <div className="text-sm text-gray-600 dark:text-gray-400">Distractions</div>
                <div className="font-semibold text-gray-900 dark:text-white">
                  {distractionCount}
                </div>
              </div>
            </div>

            {/* Control Buttons */}
            <div className="flex gap-3">
              {!inBreak && (
                <>
                  <button
                    onClick={isActive ? pauseSession : resumeSession}
                    className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    {isActive ? 'Pause' : 'Resume'}
                  </button>
                  <button
                    onClick={() => takeBreak('micro')}
                    className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                    title="2 min break"
                  >
                    ☕
                  </button>
                </>
              )}
              <button
                onClick={cancelSession}
                className="px-4 py-2 border border-red-300 text-red-600 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
              >
                End Session
              </button>
            </div>

            {/* Distraction Counter */}
            <div className="mt-4 text-center">
              <button
                onClick={() => setDistractionCount(prev => prev + 1)}
                className="text-sm text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
              >
                Mark distraction (+1)
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`advanced-focus-mode ${className}`}>
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Focus Mode
        </h3>

        {/* Preset Options */}
        <div className="grid grid-cols-2 gap-3 mb-6">
          {Object.entries(FOCUS_PRESETS).map(([key, config]) => (
            <button
              key={key}
              onClick={() => startFocusSession(key as keyof typeof FOCUS_PRESETS)}
              className={`p-3 border rounded-lg text-left hover:shadow-md transition-shadow ${
                selectedPreset === key
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                  : 'border-gray-200 dark:border-gray-600'
              }`}
            >
              <div className="font-medium text-gray-900 dark:text-white capitalize">
                {key.replace('-', ' ')}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                {config.duration} min • {config.break} min break
              </div>
            </button>
          ))}
        </div>

        {/* Custom Duration */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Custom Duration (minutes)
          </label>
          <div className="flex gap-3">
            <input
              type="number"
              min="5"
              max="180"
              value={customDuration}
              onChange={(e) => setCustomDuration(Number(e.target.value))}
              className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
            <button
              onClick={() => {
                const customPreset = { duration: customDuration, break: 5, type: 'focus' as const };
                startFocusSession('pomodoro'); // Use pomodoro as base, but with custom duration
              }}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
            >
              Start Custom
            </button>
          </div>
        </div>

        {/* Session Statistics */}
        {sessions.length > 0 && (
          <div className="border-t border-gray-200 dark:border-gray-600 pt-4">
            <div className="flex items-center justify-between mb-3">
              <h4 className="font-medium text-gray-900 dark:text-white">
                Session Statistics
              </h4>
              <button
                onClick={() => setShowStats(!showStats)}
                className="text-sm text-blue-600 hover:text-blue-700"
              >
                {showStats ? 'Hide' : 'Show'} Details
              </button>
            </div>
            
            {showStats && (
              <div className="grid grid-cols-2 gap-4 text-sm">
                {(() => {
                  const stats = getSessionStats();
                  if (!stats) return null;
                  
                  return (
                    <>
                      <div>
                        <span className="text-gray-600 dark:text-gray-400">Completed:</span>
                        <span className="ml-2 font-medium text-gray-900 dark:text-white">
                          {stats.completedSessions}/{stats.totalSessions}
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-600 dark:text-gray-400">Avg Productivity:</span>
                        <span className="ml-2 font-medium text-gray-900 dark:text-white">
                          {stats.avgProductivity}%
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-600 dark:text-gray-400">Total Focus:</span>
                        <span className="ml-2 font-medium text-gray-900 dark:text-white">
                          {stats.totalFocusTime}min
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-600 dark:text-gray-400">This Week:</span>
                        <span className="ml-2 font-medium text-gray-900 dark:text-white">
                          {sessions.filter(s => {
                            const sessionDate = new Date(s.startTime);
                            const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
                            return sessionDate > weekAgo;
                          }).length} sessions
                        </span>
                      </div>
                    </>
                  );
                })()}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}