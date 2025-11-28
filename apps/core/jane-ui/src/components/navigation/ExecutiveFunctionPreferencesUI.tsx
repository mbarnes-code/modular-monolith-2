/**
 * Executive Function Preferences UI
 * Interface for configuring personalized cognitive load settings and accommodations
 */

import { motion } from 'framer-motion';
import {
    AlertCircle,
    BarChart3,
    Brain,
    Check,
    Eye,
    Lightbulb,
    MousePointer,
    RotateCcw,
    Target,
    User
} from 'lucide-react';
import { useEffect, useState } from 'react';
import {
    EXECUTIVE_FUNCTION_TEMPLATES,
    useExecutiveFunctionPreferences,
    type ExecutiveFunctionProfile,
    type NavigationPreferences
} from '../../services/navigation/executiveFunctionPreferences';

interface ExecutiveFunctionPreferencesUIProps {
  isOpen: boolean;
  onClose: () => void;
  className?: string;
}

type ConfigSection = 'profile' | 'navigation' | 'interface' | 'focus' | 'organization';

export function ExecutiveFunctionPreferencesUI({ 
  isOpen, 
  onClose, 
  className = '' 
}: ExecutiveFunctionPreferencesUIProps) {
  const {
    currentProfile,
    currentPreferences,
    isCustomized,
    templates,
    applyTemplate,
    updateProfile,
    updatePreferences,
    getPersonalizedRecommendations
  } = useExecutiveFunctionPreferences();

  const [activeSection, setActiveSection] = useState<ConfigSection>('profile');
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
  const [pendingChanges, setPendingChanges] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  const recommendations = getPersonalizedRecommendations();

  // Track changes
  useEffect(() => {
    setPendingChanges(isCustomized);
  }, [isCustomized]);

  const handleTemplateSelect = (templateId: string) => {
    setSelectedTemplate(templateId);
    applyTemplate(templateId);
    setPendingChanges(false);
  };

  const handleProfileUpdate = (field: keyof ExecutiveFunctionProfile, value: any) => {
    if (!currentProfile) return;
    updateProfile({ [field]: value });
    setPendingChanges(true);
  };

  const handlePreferencesUpdate = (field: keyof NavigationPreferences, value: any) => {
    if (!currentPreferences) return;
    updatePreferences({ [field]: value });
    setPendingChanges(true);
  };

  const renderSlider = (
    label: string,
    value: number,
    onChange: (value: number) => void,
    min: number = 0,
    max: number = 10,
    description?: string
  ) => (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <label className="text-sm font-medium text-gray-700">{label}</label>
        <span className="text-sm text-gray-500">{value}/{max}</span>
      </div>
      {description && (
        <p className="text-xs text-gray-500">{description}</p>
      )}
      <div className="relative">
        <input
          type="range"
          min={min}
          max={max}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
        />
        <div className="flex justify-between text-xs text-gray-400 mt-1">
          <span>Low</span>
          <span>High</span>
        </div>
      </div>
    </div>
  );

  const renderToggle = (
    label: string,
    value: boolean,
    onChange: (value: boolean) => void,
    description?: string
  ) => (
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <label className="text-sm font-medium text-gray-700">{label}</label>
        {description && (
          <p className="text-xs text-gray-500 mt-1">{description}</p>
        )}
      </div>
      <button
        onClick={() => onChange(!value)}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
          value ? 'bg-blue-600' : 'bg-gray-200'
        }`}
      >
        <span
          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
            value ? 'translate-x-6' : 'translate-x-1'
          }`}
        />
      </button>
    </div>
  );

  const renderSelect = (
    label: string,
    value: string,
    options: Array<{ value: string; label: string }>,
    onChange: (value: string) => void,
    description?: string
  ) => (
    <div className="space-y-2">
      <label className="text-sm font-medium text-gray-700">{label}</label>
      {description && (
        <p className="text-xs text-gray-500">{description}</p>
      )}
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full p-2 border border-gray-300 rounded text-sm"
      >
        {options.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );

  if (!isOpen) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <Brain className="w-6 h-6 text-blue-600" />
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                Executive Function Preferences
              </h2>
              <p className="text-sm text-gray-600">
                Personalize your cognitive load management and interface accommodations
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            {pendingChanges && (
              <span className="px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded">
                Unsaved Changes
              </span>
            )}
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-gray-600 rounded"
            >
              ×
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex h-full">
          {/* Sidebar Navigation */}
          <div className="w-64 bg-gray-50 border-r border-gray-200 p-4">
            <div className="space-y-1">
              {[
                { id: 'profile' as const, label: 'Cognitive Profile', icon: User },
                { id: 'navigation' as const, label: 'Navigation Settings', icon: MousePointer },
                { id: 'interface' as const, label: 'Interface Accommodations', icon: Eye },
                { id: 'focus' as const, label: 'Focus & Attention', icon: Target },
                { id: 'organization' as const, label: 'Tool Organization', icon: BarChart3 }
              ].map(section => (
                <button
                  key={section.id}
                  onClick={() => setActiveSection(section.id)}
                  className={`w-full flex items-center gap-3 px-3 py-2 text-left rounded text-sm ${
                    activeSection === section.id
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <section.icon className="w-4 h-4" />
                  {section.label}
                </button>
              ))}
            </div>

            {/* Template Selection */}
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h4 className="text-sm font-medium text-gray-900 mb-3">Quick Templates</h4>
              <div className="space-y-1">
                {templates.slice(0, 3).map(template => (
                  <button
                    key={template.id}
                    onClick={() => handleTemplateSelect(template.id)}
                    className={`w-full text-left px-3 py-2 text-xs rounded ${
                      selectedTemplate === template.id
                        ? 'bg-green-100 text-green-700'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    {template.name}
                  </button>
                ))}
              </div>
            </div>

            {/* Recommendations */}
            {recommendations.length > 0 && (
              <div className="mt-6 pt-6 border-t border-gray-200">
                <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center gap-2">
                  <Lightbulb className="w-4 h-4 text-yellow-500" />
                  Recommendations
                </h4>
                <div className="space-y-2">
                  {recommendations.slice(0, 2).map((rec, index) => (
                    <div key={index} className="p-2 bg-yellow-50 rounded text-xs text-yellow-800">
                      {rec.message}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Main Content */}
          <div className="flex-1 overflow-auto">
            <div className="p-6">
              {/* Cognitive Profile Section */}
              {activeSection === 'profile' && currentProfile && (
                <div className="space-y-6">
                  <h3 className="text-lg font-medium text-gray-900">Cognitive Profile</h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {renderSlider(
                      'Attention Challenges',
                      currentProfile.attentionChallenges,
                      (value) => handleProfileUpdate('attentionChallenges', value),
                      0, 10,
                      'Difficulty maintaining focus on tasks'
                    )}
                    
                    {renderSlider(
                      'Working Memory Challenges',
                      currentProfile.workingMemoryChallenges,
                      (value) => handleProfileUpdate('workingMemoryChallenges', value),
                      0, 10,
                      'Difficulty holding information in mind'
                    )}
                    
                    {renderSlider(
                      'Cognitive Flexibility Challenges',
                      currentProfile.cognitiveFlexibilityChallenges,
                      (value) => handleProfileUpdate('cognitiveFlexibilityChallenges', value),
                      0, 10,
                      'Difficulty switching between tasks or perspectives'
                    )}
                    
                    {renderSlider(
                      'Inhibitory Control Challenges',
                      currentProfile.inhibitoryControlChallenges,
                      (value) => handleProfileUpdate('inhibitoryControlChallenges', value),
                      0, 10,
                      'Difficulty ignoring distractions or impulses'
                    )}
                    
                    {renderSlider(
                      'Planning Challenges',
                      currentProfile.planningChallenges,
                      (value) => handleProfileUpdate('planningChallenges', value),
                      0, 10,
                      'Difficulty organizing and sequencing tasks'
                    )}
                    
                    {renderSlider(
                      'Hyperactivity Level',
                      currentProfile.hyperactivityLevel,
                      (value) => handleProfileUpdate('hyperactivityLevel', value),
                      0, 10,
                      'Need for movement and stimulation'
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {renderSelect(
                      'Processing Speed',
                      currentProfile.processingSpeed,
                      [
                        { value: 'slow', label: 'Slow - Need more time' },
                        { value: 'moderate', label: 'Moderate - Typical pace' },
                        { value: 'fast', label: 'Fast - Quick processing' }
                      ],
                      (value) => handleProfileUpdate('processingSpeed', value as any),
                      'How quickly you typically process information'
                    )}
                    
                    {renderSelect(
                      'Time Perception',
                      currentProfile.timePerception,
                      [
                        { value: 'underestimate', label: 'Underestimate - Time flies' },
                        { value: 'accurate', label: 'Accurate - Good time sense' },
                        { value: 'overestimate', label: 'Overestimate - Time drags' }
                      ],
                      (value) => handleProfileUpdate('timePerception', value as any),
                      'How you typically perceive the passage of time'
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {renderSlider(
                      'Optimal Session Length (min)',
                      currentProfile.optimalSessionLength,
                      (value) => handleProfileUpdate('optimalSessionLength', value),
                      5, 120,
                      'How long you can focus comfortably'
                    )}
                    
                    {renderSlider(
                      'Break Frequency (min)',
                      currentProfile.breakFrequency,
                      (value) => handleProfileUpdate('breakFrequency', value),
                      5, 120,
                      'How often you need breaks'
                    )}
                    
                    {renderSlider(
                      'Transition Time (sec)',
                      currentProfile.transitionTime,
                      (value) => handleProfileUpdate('transitionTime', value),
                      1, 60,
                      'Time needed to switch between tasks'
                    )}
                  </div>
                </div>
              )}

              {/* Navigation Settings Section */}
              {activeSection === 'navigation' && currentPreferences && (
                <div className="space-y-6">
                  <h3 className="text-lg font-medium text-gray-900">Navigation Settings</h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {renderSlider(
                      'Maximum Cognitive Load (%)',
                      currentPreferences.maxCognitiveLoad,
                      (value) => handlePreferencesUpdate('maxCognitiveLoad', value),
                      30, 100,
                      'Your personal cognitive load limit'
                    )}
                    
                    {renderSlider(
                      'Warning Threshold (%)',
                      currentPreferences.loadWarningThreshold,
                      (value) => handlePreferencesUpdate('loadWarningThreshold', value),
                      20, 90,
                      'When to show cognitive load warnings'
                    )}
                    
                    {renderSlider(
                      'Minimum Switch Delay (sec)',
                      currentPreferences.minimumSwitchDelay,
                      (value) => handlePreferencesUpdate('minimumSwitchDelay', value),
                      0, 15,
                      'Enforced delay between tool switches'
                    )}
                    
                    {renderSlider(
                      'Context Preservation (min)',
                      currentPreferences.contextPreservationTime,
                      (value) => handlePreferencesUpdate('contextPreservationTime', value),
                      5, 60,
                      'How long to keep tool context active'
                    )}
                  </div>

                  <div className="space-y-4">
                    {renderToggle(
                      'Auto Load Reduction',
                      currentPreferences.autoLoadReduction,
                      (value) => handlePreferencesUpdate('autoLoadReduction', value),
                      'Automatically reduce cognitive load when it gets too high'
                    )}
                    
                    {renderToggle(
                      'Gentle Redirection',
                      currentPreferences.gentleRedirection,
                      (value) => handlePreferencesUpdate('gentleRedirection', value),
                      'Use soft guidance instead of strict blocking'
                    )}
                  </div>
                </div>
              )}

              {/* Interface Accommodations Section */}
              {activeSection === 'interface' && currentPreferences && (
                <div className="space-y-6">
                  <h3 className="text-lg font-medium text-gray-900">Interface Accommodations</h3>
                  
                  <div className="space-y-4">
                    {renderToggle(
                      'Reduce Animations',
                      currentPreferences.reduceAnimations,
                      (value) => handlePreferencesUpdate('reduceAnimations', value),
                      'Minimize visual motion and transitions'
                    )}
                    
                    {renderToggle(
                      'Simplified Interface',
                      currentPreferences.simplifiedInterface,
                      (value) => handlePreferencesUpdate('simplifiedInterface', value),
                      'Hide non-essential interface elements'
                    )}
                    
                    {renderToggle(
                      'High Contrast Mode',
                      currentPreferences.highContrastMode,
                      (value) => handlePreferencesUpdate('highContrastMode', value),
                      'Enhanced visual clarity and contrast'
                    )}
                    
                    {renderToggle(
                      'Larger Click Targets',
                      currentPreferences.largerClickTargets,
                      (value) => handlePreferencesUpdate('largerClickTargets', value),
                      'Bigger buttons and interactive elements'
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {renderSlider(
                      'Maximum Visible Tools',
                      currentPreferences.maxToolsVisible,
                      (value) => handlePreferencesUpdate('maxToolsVisible', value),
                      3, 15,
                      'Limit the number of tools shown at once'
                    )}
                  </div>
                </div>
              )}

              {/* Focus & Attention Section */}
              {activeSection === 'focus' && currentPreferences && (
                <div className="space-y-6">
                  <h3 className="text-lg font-medium text-gray-900">Focus & Attention</h3>
                  
                  <div className="space-y-4">
                    {renderToggle(
                      'Enable Focus Mode',
                      currentPreferences.enableFocusMode,
                      (value) => handlePreferencesUpdate('enableFocusMode', value),
                      'Allow focus mode activation for distraction-free work'
                    )}
                    
                    {renderToggle(
                      'Auto Focus Mode',
                      currentPreferences.autoFocusMode,
                      (value) => handlePreferencesUpdate('autoFocusMode', value),
                      'Automatically enable focus mode for challenging tasks'
                    )}
                    
                    {renderToggle(
                      'Focus Break Reminders',
                      currentPreferences.focusBreakReminders,
                      (value) => handlePreferencesUpdate('focusBreakReminders', value),
                      'Remind you to take breaks during focused work'
                    )}
                    
                    {renderToggle(
                      'Distraction Blocking',
                      currentPreferences.distractionBlocking,
                      (value) => handlePreferencesUpdate('distractionBlocking', value),
                      'Block non-essential notifications and distractions'
                    )}
                  </div>
                </div>
              )}

              {/* Tool Organization Section */}
              {activeSection === 'organization' && currentPreferences && (
                <div className="space-y-6">
                  <h3 className="text-lg font-medium text-gray-900">Tool Organization</h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {renderSelect(
                      'Preferred Grouping',
                      currentPreferences.preferredGrouping,
                      [
                        { value: 'domain', label: 'By Domain' },
                        { value: 'frequency', label: 'By Usage Frequency' },
                        { value: 'complexity', label: 'By Complexity' },
                        { value: 'workflow', label: 'By Workflow' },
                        { value: 'custom', label: 'Custom Groups' }
                      ],
                      (value) => handlePreferencesUpdate('preferredGrouping', value as any),
                      'How tools should be organized and grouped'
                    )}
                  </div>

                  <div className="space-y-4">
                    {renderToggle(
                      'Favorite Tools First',
                      currentPreferences.favoriteToolsFirst,
                      (value) => handlePreferencesUpdate('favoriteToolsFirst', value),
                      'Show frequently used tools at the top'
                    )}
                    
                    {renderToggle(
                      'Hide Complex Tools',
                      currentPreferences.hideComplexTools,
                      (value) => handlePreferencesUpdate('hideComplexTools', value),
                      'Hide high-complexity tools by default'
                    )}
                    
                    {renderToggle(
                      'Provide Cognitive Insights',
                      currentPreferences.provideCognitiveInsights,
                      (value) => handlePreferencesUpdate('provideCognitiveInsights', value),
                      'Show cognitive load analysis and insights'
                    )}
                    
                    {renderToggle(
                      'Progress Tracking',
                      currentPreferences.progressTracking,
                      (value) => handlePreferencesUpdate('progressTracking', value),
                      'Track and show improvement over time'
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            {isCustomized && (
              <>
                <AlertCircle className="w-4 h-4 text-orange-500" />
                Custom profile - changes saved automatically
              </>
            )}
          </div>
          
          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                const defaultTemplate = EXECUTIVE_FUNCTION_TEMPLATES.find(t => t.id === 'neurotypical-optimized');
                if (defaultTemplate) handleTemplateSelect(defaultTemplate.id);
              }}
              className="px-4 py-2 text-gray-600 hover:text-gray-800 flex items-center gap-2"
            >
              <RotateCcw className="w-4 h-4" />
              Reset to Default
            </button>
            
            <button
              onClick={onClose}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 flex items-center gap-2"
            >
              <Check className="w-4 h-4" />
              Done
            </button>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}