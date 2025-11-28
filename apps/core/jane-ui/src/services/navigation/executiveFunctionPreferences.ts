/**
 * Executive Function Navigation Preferences
 * Personalized cognitive load settings and accommodations for individual executive function needs
 */

import { useCallback, useEffect, useState } from 'react';
import { useGlobalStore } from '../../services/store';

export interface ExecutiveFunctionProfile {
  id: string;
  name: string;
  description: string;
  
  // Core executive function areas (0-10 scale, higher = more challenges)
  attentionChallenges: number;        // Difficulty maintaining focus
  workingMemoryChallenges: number;    // Difficulty holding information
  cognitiveFlexibilityChallenges: number; // Difficulty switching contexts
  inhibitoryControlChallenges: number;    // Difficulty ignoring distractions
  planningChallenges: number;         // Difficulty organizing tasks
  
  // ADHD-specific considerations
  hyperactivityLevel: number;         // Need for stimulation/movement
  impulsivityLevel: number;          // Tendency for quick decisions
  hyperfocusPatterns: boolean;       // Tendency to hyperfocus
  
  // Processing preferences
  processingSpeed: 'slow' | 'moderate' | 'fast';
  sensoryPreferences: {
    visualOverload: 'low' | 'moderate' | 'high';
    auditoryOverload: 'low' | 'moderate' | 'high';
    motionSensitivity: 'low' | 'moderate' | 'high';
  };
  
  // Time management preferences
  timePerception: 'underestimate' | 'accurate' | 'overestimate';
  optimalSessionLength: number;      // minutes
  breakFrequency: number;            // minutes between breaks
  transitionTime: number;            // seconds needed between tasks
}

export interface NavigationPreferences {
  // Cognitive load management
  maxCognitiveLoad: number;          // 0-100, personal threshold
  loadWarningThreshold: number;      // 0-100, when to show warnings
  autoLoadReduction: boolean;        // Automatically reduce load when high
  
  // Navigation timing
  minimumSwitchDelay: number;        // seconds between tool switches
  contextPreservationTime: number;   // minutes to preserve context
  cooldownPeriod: number;            // seconds after high-load tasks
  
  // Interface accommodations
  reduceAnimations: boolean;         // Minimize visual motion
  simplifiedInterface: boolean;      // Hide non-essential elements
  highContrastMode: boolean;         // Enhanced visual clarity
  largerClickTargets: boolean;       // Bigger buttons/links
  
  // Focus aids
  enableFocusMode: boolean;          // Allow focus mode activation
  autoFocusMode: boolean;           // Auto-enable for challenging tasks
  focusBreakReminders: boolean;      // Remind to take breaks
  distractionBlocking: boolean;      // Block non-essential notifications
  
  // Tool organization
  preferredGrouping: 'domain' | 'frequency' | 'complexity' | 'workflow' | 'custom';
  maxToolsVisible: number;           // Limit visible tool options
  favoriteToolsFirst: boolean;      // Prioritize frequently used tools
  hideComplexTools: boolean;        // Hide high-complexity tools by default
  
  // Feedback preferences
  provideCognitiveInsights: boolean; // Show load analysis
  celebrateSuccess: boolean;         // Positive reinforcement
  gentleRedirection: boolean;        // Soft guidance vs strict blocking
  progressTracking: boolean;         // Track improvements over time
}

export interface PreferencesTemplate {
  id: string;
  name: string;
  description: string;
  targetConditions: string[];
  profile: ExecutiveFunctionProfile;
  preferences: NavigationPreferences;
}

/**
 * Pre-defined templates for common executive function patterns
 */
export const EXECUTIVE_FUNCTION_TEMPLATES: PreferencesTemplate[] = [
  {
    id: 'adhd-inattentive',
    name: 'ADHD - Inattentive Type',
    description: 'Optimized for attention maintenance and focus support',
    targetConditions: ['ADHD-I', 'Attention difficulties', 'Focus challenges'],
    profile: {
      id: 'adhd-inattentive',
      name: 'ADHD Inattentive',
      description: 'Primary challenges with sustained attention and focus',
      attentionChallenges: 8,
      workingMemoryChallenges: 6,
      cognitiveFlexibilityChallenges: 4,
      inhibitoryControlChallenges: 3,
      planningChallenges: 6,
      hyperactivityLevel: 2,
      impulsivityLevel: 3,
      hyperfocusPatterns: true,
      processingSpeed: 'moderate',
      sensoryPreferences: {
        visualOverload: 'moderate',
        auditoryOverload: 'high',
        motionSensitivity: 'high'
      },
      timePerception: 'underestimate',
      optimalSessionLength: 25,
      breakFrequency: 25,
      transitionTime: 10
    },
    preferences: {
      maxCognitiveLoad: 70,
      loadWarningThreshold: 60,
      autoLoadReduction: true,
      minimumSwitchDelay: 5,
      contextPreservationTime: 15,
      cooldownPeriod: 30,
      reduceAnimations: true,
      simplifiedInterface: true,
      highContrastMode: false,
      largerClickTargets: true,
      enableFocusMode: true,
      autoFocusMode: true,
      focusBreakReminders: true,
      distractionBlocking: true,
      preferredGrouping: 'frequency',
      maxToolsVisible: 6,
      favoriteToolsFirst: true,
      hideComplexTools: true,
      provideCognitiveInsights: true,
      celebrateSuccess: true,
      gentleRedirection: true,
      progressTracking: true
    }
  },
  
  {
    id: 'adhd-hyperactive',
    name: 'ADHD - Hyperactive/Impulsive Type',
    description: 'Accommodations for hyperactivity and impulse control',
    targetConditions: ['ADHD-H', 'Hyperactivity', 'Impulse control'],
    profile: {
      id: 'adhd-hyperactive',
      name: 'ADHD Hyperactive',
      description: 'Primary challenges with hyperactivity and impulse control',
      attentionChallenges: 5,
      workingMemoryChallenges: 4,
      cognitiveFlexibilityChallenges: 3,
      inhibitoryControlChallenges: 8,
      planningChallenges: 7,
      hyperactivityLevel: 8,
      impulsivityLevel: 8,
      hyperfocusPatterns: false,
      processingSpeed: 'fast',
      sensoryPreferences: {
        visualOverload: 'low',
        auditoryOverload: 'low',
        motionSensitivity: 'low'
      },
      timePerception: 'underestimate',
      optimalSessionLength: 15,
      breakFrequency: 15,
      transitionTime: 5
    },
    preferences: {
      maxCognitiveLoad: 80,
      loadWarningThreshold: 70,
      autoLoadReduction: false,
      minimumSwitchDelay: 3,
      contextPreservationTime: 10,
      cooldownPeriod: 15,
      reduceAnimations: false,
      simplifiedInterface: false,
      highContrastMode: false,
      largerClickTargets: true,
      enableFocusMode: true,
      autoFocusMode: false,
      focusBreakReminders: true,
      distractionBlocking: false,
      preferredGrouping: 'workflow',
      maxToolsVisible: 9,
      favoriteToolsFirst: true,
      hideComplexTools: false,
      provideCognitiveInsights: true,
      celebrateSuccess: true,
      gentleRedirection: false,
      progressTracking: true
    }
  },
  
  {
    id: 'executive-dysfunction',
    name: 'Executive Dysfunction',
    description: 'Support for planning, organization, and task management challenges',
    targetConditions: ['Executive dysfunction', 'Planning difficulties', 'Organization challenges'],
    profile: {
      id: 'executive-dysfunction',
      name: 'Executive Dysfunction',
      description: 'Challenges across multiple executive function domains',
      attentionChallenges: 6,
      workingMemoryChallenges: 7,
      cognitiveFlexibilityChallenges: 8,
      inhibitoryControlChallenges: 5,
      planningChallenges: 9,
      hyperactivityLevel: 3,
      impulsivityLevel: 4,
      hyperfocusPatterns: false,
      processingSpeed: 'slow',
      sensoryPreferences: {
        visualOverload: 'high',
        auditoryOverload: 'high',
        motionSensitivity: 'high'
      },
      timePerception: 'overestimate',
      optimalSessionLength: 45,
      breakFrequency: 30,
      transitionTime: 15
    },
    preferences: {
      maxCognitiveLoad: 60,
      loadWarningThreshold: 50,
      autoLoadReduction: true,
      minimumSwitchDelay: 8,
      contextPreservationTime: 30,
      cooldownPeriod: 60,
      reduceAnimations: true,
      simplifiedInterface: true,
      highContrastMode: true,
      largerClickTargets: true,
      enableFocusMode: true,
      autoFocusMode: true,
      focusBreakReminders: true,
      distractionBlocking: true,
      preferredGrouping: 'domain',
      maxToolsVisible: 4,
      favoriteToolsFirst: true,
      hideComplexTools: true,
      provideCognitiveInsights: true,
      celebrateSuccess: true,
      gentleRedirection: true,
      progressTracking: true
    }
  },
  
  {
    id: 'autistic-profile',
    name: 'Autistic Cognitive Profile',
    description: 'Accommodations for autistic processing differences and sensory needs',
    targetConditions: ['Autism', 'Sensory processing differences', 'Routine preference'],
    profile: {
      id: 'autistic-profile',
      name: 'Autistic Profile',
      description: 'Accommodations for autistic cognitive and sensory differences',
      attentionChallenges: 3,
      workingMemoryChallenges: 4,
      cognitiveFlexibilityChallenges: 9,
      inhibitoryControlChallenges: 2,
      planningChallenges: 5,
      hyperactivityLevel: 2,
      impulsivityLevel: 2,
      hyperfocusPatterns: true,
      processingSpeed: 'moderate',
      sensoryPreferences: {
        visualOverload: 'high',
        auditoryOverload: 'high',
        motionSensitivity: 'high'
      },
      timePerception: 'accurate',
      optimalSessionLength: 60,
      breakFrequency: 45,
      transitionTime: 20
    },
    preferences: {
      maxCognitiveLoad: 65,
      loadWarningThreshold: 55,
      autoLoadReduction: true,
      minimumSwitchDelay: 10,
      contextPreservationTime: 45,
      cooldownPeriod: 120,
      reduceAnimations: true,
      simplifiedInterface: true,
      highContrastMode: true,
      largerClickTargets: false,
      enableFocusMode: true,
      autoFocusMode: false,
      focusBreakReminders: false,
      distractionBlocking: true,
      preferredGrouping: 'domain',
      maxToolsVisible: 5,
      favoriteToolsFirst: false,
      hideComplexTools: false,
      provideCognitiveInsights: true,
      celebrateSuccess: false,
      gentleRedirection: true,
      progressTracking: true
    }
  },
  
  {
    id: 'anxiety-focused',
    name: 'Anxiety-Focused',
    description: 'Reduces cognitive load and provides calming interface elements',
    targetConditions: ['Anxiety', 'Overwhelm', 'Decision paralysis'],
    profile: {
      id: 'anxiety-focused',
      name: 'Anxiety Focused',
      description: 'Accommodations for anxiety and overwhelm management',
      attentionChallenges: 7,
      workingMemoryChallenges: 8,
      cognitiveFlexibilityChallenges: 6,
      inhibitoryControlChallenges: 4,
      planningChallenges: 8,
      hyperactivityLevel: 6,
      impulsivityLevel: 3,
      hyperfocusPatterns: false,
      processingSpeed: 'slow',
      sensoryPreferences: {
        visualOverload: 'high',
        auditoryOverload: 'high',
        motionSensitivity: 'high'
      },
      timePerception: 'overestimate',
      optimalSessionLength: 20,
      breakFrequency: 20,
      transitionTime: 12
    },
    preferences: {
      maxCognitiveLoad: 50,
      loadWarningThreshold: 40,
      autoLoadReduction: true,
      minimumSwitchDelay: 7,
      contextPreservationTime: 20,
      cooldownPeriod: 45,
      reduceAnimations: true,
      simplifiedInterface: true,
      highContrastMode: false,
      largerClickTargets: true,
      enableFocusMode: true,
      autoFocusMode: true,
      focusBreakReminders: true,
      distractionBlocking: true,
      preferredGrouping: 'complexity',
      maxToolsVisible: 3,
      favoriteToolsFirst: true,
      hideComplexTools: true,
      provideCognitiveInsights: false,
      celebrateSuccess: true,
      gentleRedirection: true,
      progressTracking: false
    }
  },
  
  {
    id: 'neurotypical-optimized',
    name: 'Neurotypical Optimized',
    description: 'Standard cognitive load management for typical executive function',
    targetConditions: ['Typical executive function', 'Standard cognitive profile'],
    profile: {
      id: 'neurotypical-optimized',
      name: 'Neurotypical',
      description: 'Standard executive function profile',
      attentionChallenges: 3,
      workingMemoryChallenges: 3,
      cognitiveFlexibilityChallenges: 3,
      inhibitoryControlChallenges: 3,
      planningChallenges: 3,
      hyperactivityLevel: 3,
      impulsivityLevel: 3,
      hyperfocusPatterns: false,
      processingSpeed: 'moderate',
      sensoryPreferences: {
        visualOverload: 'moderate',
        auditoryOverload: 'moderate',
        motionSensitivity: 'moderate'
      },
      timePerception: 'accurate',
      optimalSessionLength: 50,
      breakFrequency: 60,
      transitionTime: 5
    },
    preferences: {
      maxCognitiveLoad: 85,
      loadWarningThreshold: 75,
      autoLoadReduction: false,
      minimumSwitchDelay: 2,
      contextPreservationTime: 10,
      cooldownPeriod: 10,
      reduceAnimations: false,
      simplifiedInterface: false,
      highContrastMode: false,
      largerClickTargets: false,
      enableFocusMode: true,
      autoFocusMode: false,
      focusBreakReminders: false,
      distractionBlocking: false,
      preferredGrouping: 'workflow',
      maxToolsVisible: 12,
      favoriteToolsFirst: false,
      hideComplexTools: false,
      provideCognitiveInsights: true,
      celebrateSuccess: false,
      gentleRedirection: false,
      progressTracking: true
    }
  }
];

/**
 * Hook for managing executive function navigation preferences
 */
export function useExecutiveFunctionPreferences() {
  const { userPreferences, updateUserPreferences } = useGlobalStore();
  
  const [currentProfile, setCurrentProfile] = useState<ExecutiveFunctionProfile | null>(null);
  const [currentPrefs, setCurrentPrefs] = useState<NavigationPreferences | null>(null);
  const [isCustomized, setIsCustomized] = useState(false);
  
  // Load preferences on mount
  useEffect(() => {
    const savedProfile = userPreferences?.executiveFunctionProfile;
    const savedPrefs = userPreferences?.navigationPreferences;
    
    if (savedProfile && savedPrefs) {
      setCurrentProfile(savedProfile);
      setCurrentPrefs(savedPrefs);
      setIsCustomized(userPreferences.isCustomProfiler || false);
    } else {
      // Default to neurotypical template
      const defaultTemplate = EXECUTIVE_FUNCTION_TEMPLATES.find(t => t.id === 'neurotypical-optimized')!;
      setCurrentProfile(defaultTemplate.profile);
      setCurrentPrefs(defaultTemplate.preferences);
      setIsCustomized(false);
    }
  }, [userPreferences]);
  
  // Apply template
  const applyTemplate = useCallback((templateId: string) => {
    const template = EXECUTIVE_FUNCTION_TEMPLATES.find(t => t.id === templateId);
    if (!template) return;
    
    setCurrentProfile(template.profile);
    setCurrentPrefs(template.preferences);
    setIsCustomized(false);
    
    // Save to global store
    updateUserPreferences({
      executiveFunctionProfile: template.profile,
      navigationPreferences: template.preferences,
      isCustomProfile: false
    });
  }, [updateUserPreferences]);
  
  // Update profile
  const updateProfile = useCallback((updates: Partial<ExecutiveFunctionProfile>) => {
    if (!currentProfile) return;
    
    const updatedProfile = { ...currentProfile, ...updates };
    setCurrentProfile(updatedProfile);
    setIsCustomized(true);
    
    updateUserPreferences({
      executiveFunctionProfile: updatedProfile,
      isCustomProfile: true
    });
  }, [currentProfile, updateUserPreferences]);
  
  // Update preferences
  const updatePreferences = useCallback((updates: Partial<NavigationPreferences>) => {
    if (!currentPrefs) return;
    
    const updatedPrefs = { ...currentPrefs, ...updates };
    setCurrentPrefs(updatedPrefs);
    setIsCustomized(true);
    
    updateUserPreferences({
      navigationPreferences: updatedPrefs,
      isCustomProfile: true
    });
  }, [currentPrefs, updateUserPreferences]);
  
  // Get cognitive load threshold based on current context
  const getCognitiveLoadThreshold = useCallback((context?: string) => {
    if (!currentPrefs) return 75;
    
    // Adjust threshold based on context
    let threshold = currentPrefs.maxCognitiveLoad;
    
    if (context === 'complex-task') {
      threshold = Math.max(40, threshold - 15);
    } else if (context === 'learning') {
      threshold = Math.max(35, threshold - 20);
    } else if (context === 'routine') {
      threshold = Math.min(95, threshold + 10);
    }
    
    return threshold;
  }, [currentPrefs]);
  
  // Get recommended break time
  const getRecommendedBreakTime = useCallback(() => {
    if (!currentProfile) return 5;
    
    // Calculate break time based on profile
    const baseBreak = 5;
    const attentionMultiplier = currentProfile.attentionChallenges / 10;
    const workingMemoryMultiplier = currentProfile.workingMemoryChallenges / 10;
    
    return Math.round(baseBreak + (attentionMultiplier + workingMemoryMultiplier) * 3);
  }, [currentProfile]);
  
  // Check if tool switch should be delayed
  const shouldDelayToolSwitch = useCallback((fromTool: string, toTool: string, currentLoad: number) => {
    if (!currentPrefs || !currentProfile) return false;
    
    // Always delay if over cognitive load threshold
    if (currentLoad > currentPrefs.loadWarningThreshold) return true;
    
    // Delay based on cognitive flexibility challenges
    const flexibilityPenalty = currentProfile.cognitiveFlexibilityChallenges > 6;
    
    // Delay if switch would be too rapid
    const lastSwitchTime = Date.now() - (userPreferences?.lastToolSwitch || 0);
    const minDelay = currentPrefs.minimumSwitchDelay * 1000;
    
    return flexibilityPenalty || lastSwitchTime < minDelay;
  }, [currentPrefs, currentProfile, userPreferences]);
  
  // Get interface accommodations
  const getInterfaceAccommodations = useCallback(() => {
    if (!currentPrefs) return {};
    
    return {
      reduceAnimations: currentPrefs.reduceAnimations,
      simplifiedInterface: currentPrefs.simplifiedInterface,
      highContrastMode: currentPrefs.highContrastMode,
      largerClickTargets: currentPrefs.largerClickTargets,
      maxVisibleTools: currentPrefs.maxToolsVisible,
      preferredGrouping: currentPrefs.preferredGrouping
    };
  }, [currentPrefs]);
  
  // Generate personalized recommendations
  const getPersonalizedRecommendations = useCallback(() => {
    if (!currentProfile || !currentPrefs) return [];
    
    const recommendations = [];
    
    // Attention-based recommendations
    if (currentProfile.attentionChallenges > 6) {
      recommendations.push({
        type: 'attention',
        message: 'Consider using Focus Mode for complex tasks',
        action: 'enable-focus-mode'
      });
    }
    
    // Working memory recommendations
    if (currentProfile.workingMemoryChallenges > 6) {
      recommendations.push({
        type: 'memory',
        message: 'Keep fewer tools active to reduce memory load',
        action: 'reduce-active-tools'
      });
    }
    
    // Cognitive flexibility recommendations
    if (currentProfile.cognitiveFlexibilityChallenges > 6) {
      recommendations.push({
        type: 'flexibility',
        message: 'Plan task sequences to minimize context switching',
        action: 'group-similar-tasks'
      });
    }
    
    return recommendations;
  }, [currentProfile, currentPrefs]);
  
  return {
    currentProfile,
    currentPreferences: currentPrefs,
    isCustomized,
    templates: EXECUTIVE_FUNCTION_TEMPLATES,
    
    // Actions
    applyTemplate,
    updateProfile,
    updatePreferences,
    
    // Utilities
    getCognitiveLoadThreshold,
    getRecommendedBreakTime,
    shouldDelayToolSwitch,
    getInterfaceAccommodations,
    getPersonalizedRecommendations
  };
}