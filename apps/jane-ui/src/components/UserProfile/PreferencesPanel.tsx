import React, { useEffect, useState } from 'react';

// Global type declarations for Node.js environment
declare global {
    function setTimeout(callback: () => void, ms: number): number;
    function clearTimeout(id: number): void;
}

// Core preference types for executive function accommodations
interface ADHDAccommodations {
    ui_animations: boolean;
    focus_mode: boolean;
    time_awareness: boolean;
    progress_indicators: boolean;
    interrupt_protection: boolean;
    consistent_navigation: boolean;
    context_preservation: boolean;
    task_breakdown: boolean;
}

interface AutismAccommodations {
    predictable_patterns: boolean;
    sensory_considerations: boolean;
    clear_structure: boolean;
    routine_support: boolean;
    change_warnings: boolean;
    detailed_feedback: boolean;
    preference_stability: boolean;
    cognitive_load_reduction: boolean;
}

interface UIPreferences {
    theme: 'light' | 'dark' | 'auto';
    font_size: 'small' | 'medium' | 'large';
    animation_speed: 'none' | 'reduced' | 'normal';
    density: 'compact' | 'comfortable' | 'spacious';
    color_coding: boolean;
}

interface PerformancePreferences {
    response_time_target: number;
    preload_frequent_tools: boolean;
    cache_aggressively: boolean;
    offline_support: boolean;
    background_sync: boolean;
}

interface AccessibilityPreferences {
    screen_reader: boolean;
    high_contrast: boolean;
    large_text: boolean;
    keyboard_navigation: boolean;
    focus_indicators: boolean;
    reduced_motion: boolean;
    color_blind_support: boolean;
}

interface UserPreferences {
    adhd_accommodations: ADHDAccommodations;
    autism_accommodations: AutismAccommodations;
    ui_preferences: UIPreferences;
    performance_preferences: PerformancePreferences;
    accessibility_preferences: AccessibilityPreferences;
}

interface PreferencesPanelProps {
    userId: string;
    onPreferencesChange?: (preferences: UserPreferences) => void;
    className?: string;
}

const PreferencesPanel: React.FC<PreferencesPanelProps> = ({ 
    userId, 
    onPreferencesChange, 
    className 
}) => {
    const [preferences, setPreferences] = useState<UserPreferences | null>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [activeTab, setActiveTab] = useState('adhd');
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    // Load user preferences on component mount
    useEffect(() => {
        loadPreferences();
    }, [userId]);

    const loadPreferences = async () => {
        try {
            setLoading(true);
            setError(null);
            
            // Default preferences for constitutional compliance
            const defaultPreferences: UserPreferences = {
                adhd_accommodations: {
                    ui_animations: false,
                    focus_mode: true,
                    time_awareness: true,
                    progress_indicators: true,
                    interrupt_protection: true,
                    consistent_navigation: true,
                    context_preservation: true,
                    task_breakdown: true
                },
                autism_accommodations: {
                    predictable_patterns: true,
                    sensory_considerations: true,
                    clear_structure: true,
                    routine_support: true,
                    change_warnings: true,
                    detailed_feedback: true,
                    preference_stability: true,
                    cognitive_load_reduction: true
                },
                ui_preferences: {
                    theme: 'light',
                    font_size: 'medium',
                    animation_speed: 'reduced',
                    density: 'comfortable',
                    color_coding: true
                },
                performance_preferences: {
                    response_time_target: 200,
                    preload_frequent_tools: true,
                    cache_aggressively: true,
                    offline_support: true,
                    background_sync: true
                },
                accessibility_preferences: {
                    screen_reader: false,
                    high_contrast: false,
                    large_text: false,
                    keyboard_navigation: true,
                    focus_indicators: true,
                    reduced_motion: false,
                    color_blind_support: false
                }
            };

            setPreferences(defaultPreferences);
        } finally {
            setLoading(false);
        }
    };

    const updatePreferences = async (
        category: keyof UserPreferences,
        updates: Partial<UserPreferences[keyof UserPreferences]>
    ) => {
        if (!preferences) return;

        try {
            setSaving(true);
            setError(null);

            const updatedPreferences = {
                ...preferences,
                [category]: {
                    ...preferences[category],
                    ...updates
                }
            };

            setPreferences(updatedPreferences);
            onPreferencesChange?.(updatedPreferences);
            setSuccess('Preferences updated successfully');
        } catch {
            setError('Failed to update preferences. Please try again.');
        } finally {
            setSaving(false);
        }
    };

    const resetToDefaults = async () => {
        try {
            setSaving(true);
            setError(null);
            
            await loadPreferences();
            
            setSuccess('Preferences reset to constitutional defaults');
        } catch {
            setError('Failed to reset preferences. Please try again.');
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className={`preferences-panel ${className || ''}`} style={{ padding: '2rem' }}>
                <div style={{ textAlign: 'center' }}>
                    <div style={{ marginBottom: '1rem' }}>⟳</div>
                    <span>Loading preferences...</span>
                </div>
            </div>
        );
    }

    if (!preferences) {
        return (
            <div className={`preferences-panel ${className || ''}`} style={{ padding: '2rem' }}>
                <div style={{ padding: '1rem', backgroundColor: '#fee', border: '1px solid #fcc', borderRadius: '4px' }}>
                    <p>Unable to load preferences. Please refresh the page.</p>
                </div>
            </div>
        );
    }

    const tabStyle = {
        padding: '0.5rem 1rem',
        border: 'none',
        backgroundColor: 'transparent',
        cursor: 'pointer',
        borderBottom: '2px solid transparent'
    };

    const activeTabStyle = {
        ...tabStyle,
        borderBottomColor: '#3b82f6',
        color: '#3b82f6'
    };

    const checkboxStyle = {
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        marginBottom: '0.5rem',
        padding: '0.5rem'
    };

    return (
        <div className={`preferences-panel ${className || ''}`} style={{ padding: '1rem' }}>
            {error && (
                <div style={{ 
                    padding: '1rem', 
                    backgroundColor: '#fee', 
                    border: '1px solid #fcc', 
                    borderRadius: '4px',
                    marginBottom: '1rem' 
                }}>
                    <p style={{ margin: 0, color: '#c53030' }}>{error}</p>
                </div>
            )}
            
            {success && (
                <div style={{ 
                    padding: '1rem', 
                    backgroundColor: '#f0fff4', 
                    border: '1px solid #9ae6b4', 
                    borderRadius: '4px',
                    marginBottom: '1rem' 
                }}>
                    <p style={{ margin: 0, color: '#38a169' }}>{success}</p>
                </div>
            )}

            <div style={{ border: '1px solid #d1d5db', borderRadius: '8px', overflow: 'hidden' }}>
                <div style={{ padding: '1.5rem', borderBottom: '1px solid #d1d5db' }}>
                    <h2 style={{ margin: '0 0 0.5rem 0', fontSize: '1.25rem', fontWeight: 'bold' }}>
                        Executive Function Preferences
                    </h2>
                    <p style={{ margin: 0, color: '#6b7280' }}>
                        Customize your experience for ADHD/autism accommodations and personal preferences.
                    </p>
                </div>

                <div style={{ padding: '1.5rem' }}>
                    {/* Tab Navigation */}
                    <div style={{ display: 'flex', borderBottom: '1px solid #d1d5db', marginBottom: '1.5rem' }}>
                        <button
                            onClick={() => setActiveTab('adhd')}
                            style={activeTab === 'adhd' ? activeTabStyle : tabStyle}
                        >
                            ADHD
                        </button>
                        <button
                            onClick={() => setActiveTab('autism')}
                            style={activeTab === 'autism' ? activeTabStyle : tabStyle}
                        >
                            Autism
                        </button>
                        <button
                            onClick={() => setActiveTab('ui')}
                            style={activeTab === 'ui' ? activeTabStyle : tabStyle}
                        >
                            UI
                        </button>
                        <button
                            onClick={() => setActiveTab('performance')}
                            style={activeTab === 'performance' ? activeTabStyle : tabStyle}
                        >
                            Performance
                        </button>
                        <button
                            onClick={() => setActiveTab('accessibility')}
                            style={activeTab === 'accessibility' ? activeTabStyle : tabStyle}
                        >
                            Accessibility
                        </button>
                    </div>

                    {/* Tab Content */}
                    <div style={{ minHeight: '300px' }}>
                        {activeTab === 'adhd' && (
                            <div>
                                <h3 style={{ marginBottom: '1rem' }}>ADHD Accommodations</h3>
                                <div>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.adhd_accommodations.ui_animations}
                                            onChange={(e) => updatePreferences('adhd_accommodations', { ui_animations: e.target.checked })}
                                            disabled={saving}
                                        />
                                        Enable UI animations
                                    </label>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.adhd_accommodations.focus_mode}
                                            onChange={(e) => updatePreferences('adhd_accommodations', { focus_mode: e.target.checked })}
                                            disabled={saving}
                                        />
                                        Focus mode
                                    </label>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.adhd_accommodations.time_awareness}
                                            onChange={(e) => updatePreferences('adhd_accommodations', { time_awareness: e.target.checked })}
                                            disabled={saving}
                                        />
                                        Time awareness indicators
                                    </label>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.adhd_accommodations.progress_indicators}
                                            onChange={(e) => updatePreferences('adhd_accommodations', { progress_indicators: e.target.checked })}
                                            disabled={saving}
                                        />
                                        Progress indicators
                                    </label>
                                </div>
                            </div>
                        )}

                        {activeTab === 'autism' && (
                            <div>
                                <h3 style={{ marginBottom: '1rem' }}>Autism Accommodations</h3>
                                <div>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.autism_accommodations.predictable_patterns}
                                            onChange={(e) => updatePreferences('autism_accommodations', { predictable_patterns: e.target.checked })}
                                            disabled={saving}
                                        />
                                        Predictable patterns
                                    </label>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.autism_accommodations.sensory_considerations}
                                            onChange={(e) => updatePreferences('autism_accommodations', { sensory_considerations: e.target.checked })}
                                            disabled={saving}
                                        />
                                        Sensory considerations
                                    </label>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.autism_accommodations.clear_structure}
                                            onChange={(e) => updatePreferences('autism_accommodations', { clear_structure: e.target.checked })}
                                            disabled={saving}
                                        />
                                        Clear structure
                                    </label>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.autism_accommodations.routine_support}
                                            onChange={(e) => updatePreferences('autism_accommodations', { routine_support: e.target.checked })}
                                            disabled={saving}
                                        />
                                        Routine support
                                    </label>
                                </div>
                            </div>
                        )}

                        {activeTab === 'ui' && (
                            <div>
                                <h3 style={{ marginBottom: '1rem' }}>UI Preferences</h3>
                                <div>
                                    <div style={{ marginBottom: '1rem' }}>
                                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>
                                            Theme:
                                        </label>
                                        <select
                                            value={preferences.ui_preferences.theme}
                                            onChange={(e) => updatePreferences('ui_preferences', { theme: e.target.value as 'light' | 'dark' | 'auto' })}
                                            disabled={saving}
                                            style={{ padding: '0.5rem', border: '1px solid #d1d5db', borderRadius: '4px' }}
                                        >
                                            <option value="light">Light</option>
                                            <option value="dark">Dark</option>
                                            <option value="auto">Auto</option>
                                        </select>
                                    </div>
                                    <div style={{ marginBottom: '1rem' }}>
                                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>
                                            Font Size:
                                        </label>
                                        <select
                                            value={preferences.ui_preferences.font_size}
                                            onChange={(e) => updatePreferences('ui_preferences', { font_size: e.target.value as 'small' | 'medium' | 'large' })}
                                            disabled={saving}
                                            style={{ padding: '0.5rem', border: '1px solid #d1d5db', borderRadius: '4px' }}
                                        >
                                            <option value="small">Small</option>
                                            <option value="medium">Medium</option>
                                            <option value="large">Large</option>
                                        </select>
                                    </div>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.ui_preferences.color_coding}
                                            onChange={(e) => updatePreferences('ui_preferences', { color_coding: e.target.checked })}
                                            disabled={saving}
                                        />
                                        Color coding
                                    </label>
                                </div>
                            </div>
                        )}

                        {activeTab === 'performance' && (
                            <div>
                                <h3 style={{ marginBottom: '1rem' }}>Performance Preferences</h3>
                                <div>
                                    <div style={{ marginBottom: '1rem' }}>
                                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>
                                            Response Time Target (ms):
                                        </label>
                                        <input
                                            type="number"
                                            min="100"
                                            max="5000"
                                            value={preferences.performance_preferences.response_time_target}
                                            onChange={(e) => updatePreferences('performance_preferences', { response_time_target: parseInt(e.target.value) })}
                                            disabled={saving}
                                            style={{ padding: '0.5rem', border: '1px solid #d1d5db', borderRadius: '4px' }}
                                        />
                                    </div>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.performance_preferences.preload_frequent_tools}
                                            onChange={(e) => updatePreferences('performance_preferences', { preload_frequent_tools: e.target.checked })}
                                            disabled={saving}
                                        />
                                        Preload frequent tools
                                    </label>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.performance_preferences.cache_aggressively}
                                            onChange={(e) => updatePreferences('performance_preferences', { cache_aggressively: e.target.checked })}
                                            disabled={saving}
                                        />
                                        Aggressive caching
                                    </label>
                                </div>
                            </div>
                        )}

                        {activeTab === 'accessibility' && (
                            <div>
                                <h3 style={{ marginBottom: '1rem' }}>Accessibility Preferences</h3>
                                <div>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.accessibility_preferences.high_contrast}
                                            onChange={(e) => updatePreferences('accessibility_preferences', { high_contrast: e.target.checked })}
                                            disabled={saving}
                                        />
                                        High contrast
                                    </label>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.accessibility_preferences.large_text}
                                            onChange={(e) => updatePreferences('accessibility_preferences', { large_text: e.target.checked })}
                                            disabled={saving}
                                        />
                                        Large text
                                    </label>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.accessibility_preferences.keyboard_navigation}
                                            onChange={(e) => updatePreferences('accessibility_preferences', { keyboard_navigation: e.target.checked })}
                                            disabled={saving}
                                        />
                                        Keyboard navigation
                                    </label>
                                    <label style={checkboxStyle}>
                                        <input
                                            type="checkbox"
                                            checked={preferences.accessibility_preferences.reduced_motion}
                                            onChange={(e) => updatePreferences('accessibility_preferences', { reduced_motion: e.target.checked })}
                                            disabled={saving}
                                        />
                                        Reduced motion
                                    </label>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Action Buttons */}
                    <div style={{ 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        alignItems: 'center',
                        paddingTop: '1.5rem',
                        borderTop: '1px solid #d1d5db'
                    }}>
                        <button
                            onClick={resetToDefaults}
                            disabled={saving}
                            style={{
                                padding: '0.5rem 1rem',
                                border: '1px solid #d1d5db',
                                backgroundColor: 'white',
                                borderRadius: '4px',
                                cursor: saving ? 'not-allowed' : 'pointer',
                                opacity: saving ? 0.6 : 1
                            }}
                        >
                            Reset to Constitutional Defaults
                        </button>
                        
                        {saving && (
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#6b7280' }}>
                                <span>⟳</span>
                                <span>Saving...</span>
                            </div>
                        )}
                        
                        {!saving && (
                            <span style={{ color: '#6b7280', fontSize: '0.875rem' }}>
                                Auto-save enabled
                            </span>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PreferencesPanel;