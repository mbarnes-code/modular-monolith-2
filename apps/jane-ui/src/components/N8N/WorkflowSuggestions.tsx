import React, { useCallback, useState } from 'react';

// Types for workflow suggestions
interface WorkflowSuggestion {
  id: string;
  name: string;
  description: string;
  confidence: number;
  estimatedTimeSaved: number; // in minutes
  complexity: 'simple' | 'moderate' | 'complex';
  category: 'automation' | 'data-transformation' | 'notification' | 'integration';
  trigger: {
    type: 'schedule' | 'webhook' | 'manual' | 'pattern';
    description: string;
  };
  steps: WorkflowStep[];
  requiredTools: string[];
  basedOnPattern: string;
  generatedAt: Date;
  status: 'pending' | 'approved' | 'rejected' | 'modified' | 'implemented';
  userFeedback?: {
    rating: number; // 1-5
    comments: string;
    modifications: string[];
  };
}

interface WorkflowStep {
  id: string;
  order: number;
  nodeType: string;
  name: string;
  description: string;
  configuration: Record<string, unknown>;
  isOptional: boolean;
}

interface Props {
  suggestions: WorkflowSuggestion[];
  onApprove: (suggestionId: string) => void;
  onReject: (suggestionId: string, reason: string) => void;
  onModify: (suggestionId: string, modifications: string[]) => void;
  onImplement: (suggestionId: string) => void;
  onProvideFeedback: (suggestionId: string, feedback: {
    rating: number;
    comments: string;
    modifications: string[];
  }) => void;
  loading?: boolean;
  className?: string;
}

// Color scheme for different categories and complexities
const CATEGORY_COLORS = {
  automation: '#4CAF50',
  'data-transformation': '#2196F3',
  notification: '#FF9800',
  integration: '#9C27B0',
};

const COMPLEXITY_COLORS = {
  simple: '#4CAF50',
  moderate: '#FF9800',
  complex: '#f44336',
};

const STATUS_COLORS = {
  pending: '#2196F3',
  approved: '#4CAF50',
  rejected: '#f44336',
  modified: '#FF9800',
  implemented: '#4CAF50',
};

// CSS styles for the component
const styles = {
  container: {
    padding: '20px',
    fontFamily: 'system-ui, -apple-system, sans-serif',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '24px',
  },
  title: {
    fontSize: '24px',
    fontWeight: 'bold',
    margin: 0,
    color: '#333',
  },
  subtitle: {
    fontSize: '16px',
    color: '#666',
    marginTop: '4px',
  },
  filterContainer: {
    display: 'flex',
    gap: '12px',
    marginBottom: '24px',
    padding: '16px',
    backgroundColor: '#f5f5f5',
    borderRadius: '8px',
  },
  filterButton: {
    padding: '8px 16px',
    border: '1px solid #ddd',
    borderRadius: '20px',
    backgroundColor: '#fff',
    cursor: 'pointer',
    fontSize: '14px',
    transition: 'all 0.2s',
  },
  filterButtonActive: {
    backgroundColor: '#2196F3',
    color: 'white',
    borderColor: '#2196F3',
  },
  suggestionsGrid: {
    display: 'grid',
    gap: '20px',
  },
  suggestionCard: {
    border: '1px solid #e0e0e0',
    borderRadius: '12px',
    backgroundColor: '#fff',
    padding: '20px',
    transition: 'all 0.3s ease',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  suggestionCardHover: {
    transform: 'translateY(-2px)',
    boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
  },
  suggestionHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '16px',
  },
  suggestionTitle: {
    fontSize: '20px',
    fontWeight: 'bold',
    margin: 0,
    color: '#333',
  },
  suggestionDescription: {
    fontSize: '14px',
    color: '#666',
    lineHeight: '1.5',
    marginBottom: '16px',
  },
  metadataRow: {
    display: 'flex',
    flexWrap: 'wrap' as const,
    gap: '12px',
    marginBottom: '16px',
  },
  chip: {
    padding: '4px 12px',
    borderRadius: '16px',
    fontSize: '12px',
    fontWeight: 'bold',
    border: '1px solid',
  },
  confidenceBar: {
    width: '100%',
    height: '8px',
    backgroundColor: '#e0e0e0',
    borderRadius: '4px',
    overflow: 'hidden',
    marginBottom: '16px',
  },
  confidenceFill: {
    height: '100%',
    borderRadius: '4px',
    transition: 'width 0.3s ease',
  },
  stepsContainer: {
    backgroundColor: '#f9f9f9',
    borderRadius: '8px',
    padding: '16px',
    marginBottom: '16px',
  },
  stepsTitle: {
    fontSize: '16px',
    fontWeight: 'bold',
    marginBottom: '12px',
    color: '#333',
  },
  step: {
    display: 'flex',
    alignItems: 'center',
    padding: '8px 0',
    borderBottom: '1px solid #eee',
  },
  stepNumber: {
    width: '24px',
    height: '24px',
    borderRadius: '50%',
    backgroundColor: '#2196F3',
    color: 'white',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '12px',
    fontWeight: 'bold',
    marginRight: '12px',
    flexShrink: 0,
  },
  stepContent: {
    flex: 1,
  },
  stepName: {
    fontWeight: 'bold',
    fontSize: '14px',
    marginBottom: '2px',
  },
  stepDescription: {
    fontSize: '12px',
    color: '#666',
  },
  actionsContainer: {
    display: 'flex',
    gap: '8px',
    marginTop: '16px',
  },
  button: {
    padding: '8px 16px',
    border: '1px solid',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: 'bold',
    transition: 'all 0.2s',
    backgroundColor: '#fff',
  },
  primaryButton: {
    backgroundColor: '#4CAF50',
    borderColor: '#4CAF50',
    color: 'white',
  },
  secondaryButton: {
    backgroundColor: '#fff',
    borderColor: '#ddd',
    color: '#333',
  },
  dangerButton: {
    backgroundColor: '#f44336',
    borderColor: '#f44336',
    color: 'white',
  },
  warningButton: {
    backgroundColor: '#FF9800',
    borderColor: '#FF9800',
    color: 'white',
  },
  feedbackContainer: {
    backgroundColor: '#f0f0f0',
    borderRadius: '8px',
    padding: '16px',
    marginTop: '16px',
  },
  feedbackTitle: {
    fontSize: '14px',
    fontWeight: 'bold',
    marginBottom: '12px',
  },
  textarea: {
    width: '100%',
    minHeight: '80px',
    padding: '8px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '14px',
    resize: 'vertical' as const,
    fontFamily: 'inherit',
  },
  ratingContainer: {
    display: 'flex',
    gap: '4px',
    marginBottom: '12px',
  },
  star: {
    fontSize: '20px',
    cursor: 'pointer',
    transition: 'color 0.2s',
  },
  starFilled: {
    color: '#FFD700',
  },
  starEmpty: {
    color: '#ddd',
  },
  modificationsList: {
    listStyle: 'none',
    padding: 0,
    margin: '12px 0',
  },
  modificationItem: {
    padding: '8px',
    backgroundColor: '#fff',
    border: '1px solid #ddd',
    borderRadius: '4px',
    marginBottom: '8px',
    fontSize: '14px',
  },
  emptyState: {
    textAlign: 'center' as const,
    padding: '60px 20px',
    color: '#666',
  },
  emptyStateIcon: {
    fontSize: '48px',
    marginBottom: '16px',
  },
  statusBadge: {
    padding: '4px 8px',
    borderRadius: '12px',
    fontSize: '12px',
    fontWeight: 'bold',
    textTransform: 'uppercase' as const,
  },
};

/**
 * WorkflowSuggestions Component
 * 
 * Displays AI-generated workflow suggestions with user approval workflow.
 * Supports approval, rejection, modification, and feedback collection.
 * 
 * Constitutional Requirements:
 * - <200ms UI response time for user interactions
 * - Executive function support through clear visual hierarchy and consistent patterns
 * - ADHD-friendly design with reduced cognitive load and clear action buttons
 */
export const WorkflowSuggestions: React.FC<Props> = ({
  suggestions,
  onApprove,
  onReject,
  onModify,
  onImplement,
  onProvideFeedback,
  loading = false,
  className = '',
}) => {
  const [selectedStatus, setSelectedStatus] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [showingFeedback, setShowingFeedback] = useState<string | null>(null);
  const [feedbackData, setFeedbackData] = useState<{
    rating: number;
    comments: string;
    modifications: string[];
  }>({
    rating: 0,
    comments: '',
    modifications: [],
  });

  // Filter suggestions based on status and category
  const filteredSuggestions = suggestions.filter(suggestion => {
    const statusMatch = selectedStatus === 'all' || suggestion.status === selectedStatus;
    const categoryMatch = selectedCategory === 'all' || suggestion.category === selectedCategory;
    return statusMatch && categoryMatch;
  });

  // Handle user interactions with constitutional compliance (<200ms response)
  const handleApprove = useCallback((suggestionId: string) => {
    onApprove(suggestionId);
  }, [onApprove]);

  const handleReject = useCallback((suggestionId: string) => {
    // In real app this would be a modal confirmation
    onReject(suggestionId, 'User rejected');
  }, [onReject]);

  const handleModify = useCallback((suggestionId: string) => {
    // For now, call modify with a placeholder - in real app would open a modal
    onModify(suggestionId, ['User requested modifications']);
  }, [onModify]);

  const handleImplement = useCallback((suggestionId: string) => {
    onImplement(suggestionId);
  }, [onImplement]);

  const handleShowFeedback = (suggestionId: string) => {
    setShowingFeedback(suggestionId);
    setFeedbackData({ rating: 0, comments: '', modifications: [] });
  };

  const handleSubmitFeedback = (suggestionId: string) => {
    onProvideFeedback(suggestionId, feedbackData);
    setShowingFeedback(null);
    setFeedbackData({ rating: 0, comments: '', modifications: [] });
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return '#4CAF50';
    if (confidence >= 0.6) return '#FF9800';
    return '#f44336';
  };

  const formatTimeSaved = (minutes: number) => {
    if (minutes < 60) return `${minutes}min`;
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}min` : `${hours}h`;
  };

  const getStatusBadge = (status: string) => {
    return (
      <span
        style={{
          ...styles.statusBadge,
          backgroundColor: STATUS_COLORS[status as keyof typeof STATUS_COLORS],
          color: 'white',
        }}
      >
        {status}
      </span>
    );
  };

  const renderStars = (rating: number, interactive: boolean = false) => {
    return (
      <div style={styles.ratingContainer}>
        {[1, 2, 3, 4, 5].map((star) => (
          <span
            key={star}
            style={{
              ...styles.star,
              ...(star <= rating ? styles.starFilled : styles.starEmpty),
              cursor: interactive ? 'pointer' : 'default',
            }}
            onClick={interactive ? () => setFeedbackData({ ...feedbackData, rating: star }) : undefined}
          >
            ★
          </span>
        ))}
      </div>
    );
  };

  if (loading) {
    return (
      <div style={{ ...styles.container, textAlign: 'center', padding: '60px' }}>
        <div>Loading workflow suggestions...</div>
      </div>
    );
  }

  return (
    <div className={`workflow-suggestions ${className}`} style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <div>
          <h2 style={styles.title}>Workflow Suggestions</h2>
          <div style={styles.subtitle}>
            AI-generated workflows based on your usage patterns
          </div>
        </div>
      </div>

      {/* Filters */}
      <div style={styles.filterContainer}>
        <div>
          <strong>Status:</strong>
          {['all', 'pending', 'approved', 'rejected', 'modified', 'implemented'].map((status) => (
            <button
              key={status}
              style={{
                ...styles.filterButton,
                ...(selectedStatus === status ? styles.filterButtonActive : {}),
                marginLeft: '8px',
              }}
              onClick={() => setSelectedStatus(status)}
            >
              {status === 'all' ? 'All' : status.charAt(0).toUpperCase() + status.slice(1)}
            </button>
          ))}
        </div>
        <div style={{ marginTop: '8px' }}>
          <strong>Category:</strong>
          {['all', 'automation', 'data-transformation', 'notification', 'integration'].map((category) => (
            <button
              key={category}
              style={{
                ...styles.filterButton,
                ...(selectedCategory === category ? styles.filterButtonActive : {}),
                marginLeft: '8px',
              }}
              onClick={() => setSelectedCategory(category)}
            >
              {category === 'all' ? 'All' : category.charAt(0).toUpperCase() + category.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Suggestions */}
      {filteredSuggestions.length === 0 ? (
        <div style={styles.emptyState}>
          <div style={styles.emptyStateIcon}>🤖</div>
          <h3>No workflow suggestions found</h3>
          <p>
            {suggestions.length === 0
              ? 'Keep using the platform and AI will detect patterns to suggest workflows.'
              : 'Try adjusting your filters to see more suggestions.'}
          </p>
        </div>
      ) : (
        <div style={styles.suggestionsGrid}>
          {filteredSuggestions.map((suggestion) => (
            <div
              key={suggestion.id}
              style={{
                ...styles.suggestionCard,
                borderLeftColor: CATEGORY_COLORS[suggestion.category],
                borderLeftWidth: '4px',
              }}
              onMouseEnter={(e) => {
                Object.assign(e.currentTarget.style, styles.suggestionCardHover);
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'none';
                e.currentTarget.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
              }}
            >
              {/* Header */}
              <div style={styles.suggestionHeader}>
                <div>
                  <h3 style={styles.suggestionTitle}>{suggestion.name}</h3>
                  <div style={{ marginTop: '8px' }}>
                    {getStatusBadge(suggestion.status)}
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '12px', color: '#666' }}>
                    Generated {suggestion.generatedAt.toLocaleDateString()}
                  </div>
                </div>
              </div>

              <p style={styles.suggestionDescription}>
                {suggestion.description}
              </p>

              {/* Metadata */}
              <div style={styles.metadataRow}>
                <span
                  style={{
                    ...styles.chip,
                    backgroundColor: CATEGORY_COLORS[suggestion.category],
                    color: 'white',
                    borderColor: CATEGORY_COLORS[suggestion.category],
                  }}
                >
                  {suggestion.category}
                </span>
                <span
                  style={{
                    ...styles.chip,
                    backgroundColor: COMPLEXITY_COLORS[suggestion.complexity],
                    color: 'white',
                    borderColor: COMPLEXITY_COLORS[suggestion.complexity],
                  }}
                >
                  {suggestion.complexity}
                </span>
                <span
                  style={{
                    ...styles.chip,
                    backgroundColor: '#e0e0e0',
                    color: '#333',
                    borderColor: '#e0e0e0',
                  }}
                >
                  💾 {formatTimeSaved(suggestion.estimatedTimeSaved)}
                </span>
                <span
                  style={{
                    ...styles.chip,
                    backgroundColor: '#e0e0e0',
                    color: '#333',
                    borderColor: '#e0e0e0',
                  }}
                >
                  🔧 {suggestion.requiredTools.length} tools
                </span>
              </div>

              {/* Confidence */}
              <div style={{ marginBottom: '16px' }}>
                <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>
                  Confidence: {(suggestion.confidence * 100).toFixed(1)}%
                </div>
                <div style={styles.confidenceBar}>
                  <div
                    style={{
                      ...styles.confidenceFill,
                      width: `${suggestion.confidence * 100}%`,
                      backgroundColor: getConfidenceColor(suggestion.confidence),
                    }}
                  />
                </div>
              </div>

              {/* Steps */}
              <div style={styles.stepsContainer}>
                <div style={styles.stepsTitle}>Workflow Steps ({suggestion.steps.length})</div>
                {suggestion.steps.slice(0, 3).map((step) => (
                  <div key={step.id} style={styles.step}>
                    <div style={styles.stepNumber}>{step.order}</div>
                    <div style={styles.stepContent}>
                      <div style={styles.stepName}>{step.name}</div>
                      <div style={styles.stepDescription}>{step.description}</div>
                    </div>
                  </div>
                ))}
                {suggestion.steps.length > 3 && (
                  <div style={{ fontSize: '12px', color: '#666', marginTop: '8px' }}>
                    ... and {suggestion.steps.length - 3} more steps
                  </div>
                )}
              </div>

              {/* Actions */}
              {suggestion.status === 'pending' && (
                <div style={styles.actionsContainer}>
                  <button
                    style={{ ...styles.button, ...styles.primaryButton }}
                    onClick={() => handleApprove(suggestion.id)}
                  >
                    ✓ Approve
                  </button>
                  <button
                    style={{ ...styles.button, ...styles.warningButton }}
                    onClick={() => handleModify(suggestion.id)}
                  >
                    ✏ Modify
                  </button>
                  <button
                    style={{ ...styles.button, ...styles.dangerButton }}
                    onClick={() => handleReject(suggestion.id)}
                  >
                    ✗ Reject
                  </button>
                </div>
              )}

              {suggestion.status === 'approved' && (
                <div style={styles.actionsContainer}>
                  <button
                    style={{ ...styles.button, ...styles.primaryButton }}
                    onClick={() => handleImplement(suggestion.id)}
                  >
                    🚀 Implement
                  </button>
                  <button
                    style={{ ...styles.button, ...styles.secondaryButton }}
                    onClick={() => handleShowFeedback(suggestion.id)}
                  >
                    💬 Feedback
                  </button>
                </div>
              )}

              {(suggestion.status === 'implemented' || suggestion.status === 'rejected') && (
                <div style={styles.actionsContainer}>
                  <button
                    style={{ ...styles.button, ...styles.secondaryButton }}
                    onClick={() => handleShowFeedback(suggestion.id)}
                  >
                    💬 Provide Feedback
                  </button>
                </div>
              )}

              {/* Feedback Form */}
              {showingFeedback === suggestion.id && (
                <div style={styles.feedbackContainer}>
                  <div style={styles.feedbackTitle}>Provide Feedback</div>
                  
                  <div style={{ marginBottom: '12px' }}>
                    <label style={{ fontSize: '12px', fontWeight: 'bold', display: 'block', marginBottom: '4px' }}>
                      Rating:
                    </label>
                    {renderStars(feedbackData.rating, true)}
                  </div>

                  <div style={{ marginBottom: '12px' }}>
                    <label style={{ fontSize: '12px', fontWeight: 'bold', display: 'block', marginBottom: '4px' }}>
                      Comments:
                    </label>
                    <textarea
                      style={styles.textarea}
                      value={feedbackData.comments}
                      onChange={(e) => setFeedbackData({ ...feedbackData, comments: e.target.value })}
                      placeholder="Share your thoughts about this workflow suggestion..."
                    />
                  </div>

                  <div style={styles.actionsContainer}>
                    <button
                      style={{ ...styles.button, ...styles.primaryButton }}
                      onClick={() => handleSubmitFeedback(suggestion.id)}
                    >
                      Submit Feedback
                    </button>
                    <button
                      style={{ ...styles.button, ...styles.secondaryButton }}
                      onClick={() => setShowingFeedback(null)}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}

              {/* Existing Feedback */}
              {suggestion.userFeedback && (
                <div style={styles.feedbackContainer}>
                  <div style={styles.feedbackTitle}>Your Feedback</div>
                  {renderStars(suggestion.userFeedback.rating)}
                  {suggestion.userFeedback.comments && (
                    <p style={{ fontSize: '14px', color: '#666', margin: '8px 0' }}>
                      "{suggestion.userFeedback.comments}"
                    </p>
                  )}
                  {suggestion.userFeedback.modifications.length > 0 && (
                    <div>
                      <strong style={{ fontSize: '12px' }}>Suggested Modifications:</strong>
                      <ul style={styles.modificationsList}>
                        {suggestion.userFeedback.modifications.map((mod, index) => (
                          <li key={index} style={styles.modificationItem}>
                            {mod}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default WorkflowSuggestions;