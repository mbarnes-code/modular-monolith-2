import React, { ChangeEvent, useMemo, useState } from 'react';

// Types for pattern detection data
interface WorkflowPattern {
  id: string;
  name: string;
  description: string;
  occurrences: number;
  confidence: number;
  lastDetected: Date;
  similarity: number;
  category: 'automation' | 'data-transformation' | 'notification' | 'integration';
  status: 'active' | 'inactive' | 'learning';
  tools: string[];
  avgExecutionTime: number;
  successRate: number;
  userApprovalRate: number;
}

interface PatternMetrics {
  totalPatterns: number;
  activePatterns: number;
  averageConfidence: number;
  patternsByCategory: Record<string, number>;
  recentActivity: Array<{
    date: string;
    patternsDetected: number;
    workflowsGenerated: number;
  }>;
  topPerformingPatterns: WorkflowPattern[];
}

interface Props {
  patterns: WorkflowPattern[];
  metrics: PatternMetrics;
  onPatternSelect: (pattern: WorkflowPattern) => void;
  onRefresh: () => void;
  loading?: boolean;
  className?: string;
}

// Color scheme for different categories and statuses
const CATEGORY_COLORS = {
  automation: '#4CAF50',
  'data-transformation': '#2196F3',
  notification: '#FF9800',
  integration: '#9C27B0',
};

const STATUS_COLORS = {
  active: '#4CAF50',
  inactive: '#757575',
  learning: '#FF9800',
};

// CSS styles object for the component
const styles = {
  container: {
    padding: '20px',
    fontFamily: 'system-ui, -apple-system, sans-serif',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px',
  },
  title: {
    fontSize: '24px',
    fontWeight: 'bold',
    margin: 0,
  },
  buttonGroup: {
    display: 'flex',
    gap: '10px',
  },
  button: {
    padding: '8px 16px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    backgroundColor: '#fff',
    cursor: 'pointer',
    fontSize: '14px',
  },
  metricsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '16px',
    marginBottom: '24px',
  },
  metricCard: {
    padding: '16px',
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    backgroundColor: '#fff',
  },
  metricTitle: {
    fontSize: '14px',
    color: '#666',
    marginBottom: '8px',
  },
  metricValue: {
    fontSize: '32px',
    fontWeight: 'bold',
    margin: 0,
  },
  filtersCard: {
    padding: '16px',
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    backgroundColor: '#fff',
    marginBottom: '20px',
  },
  filtersRow: {
    display: 'flex',
    gap: '16px',
    flexWrap: 'wrap' as const,
    alignItems: 'center',
  },
  input: {
    padding: '8px 12px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontSize: '14px',
    minWidth: '120px',
  },
  patternsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '16px',
  },
  patternCard: {
    padding: '16px',
    border: '1px solid #e0e0e0',  
    borderRadius: '8px',
    backgroundColor: '#fff',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  patternCardHover: {
    transform: 'translateY(-2px)',
    boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
  },
  patternHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '12px',
  },
  patternTitle: {
    fontSize: '18px',
    fontWeight: 'bold',
    margin: 0,
  },
  patternDescription: {
    fontSize: '14px',
    color: '#666',
    marginBottom: '12px',
  },
  chipContainer: {
    display: 'flex',
    gap: '8px',
    marginBottom: '12px',
  },
  chip: {
    padding: '4px 8px',
    borderRadius: '12px',
    fontSize: '12px',
    fontWeight: 'bold',
  },
  progressContainer: {
    marginBottom: '8px',
  },
  progressLabel: {
    fontSize: '12px',
    color: '#666',
    marginBottom: '4px',
  },
  progressBar: {
    width: '100%',
    height: '8px',
    backgroundColor: '#e0e0e0',
    borderRadius: '4px',
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: '4px',
    transition: 'width 0.3s ease',
  },
  statusIcon: {
    width: '20px',
    height: '20px',
    borderRadius: '50%',
  },
  alert: {
    padding: '12px',
    backgroundColor: '#e3f2fd',
    border: '1px solid #2196f3',
    borderRadius: '4px',
    color: '#1976d2',
  },
  loading: {
    padding: '20px',
    textAlign: 'center' as const,
    color: '#666',
  },
};

/**
 * PatternVisualization Component
 * 
 * Displays detected workflow patterns with comprehensive visualization
 * including confidence levels, occurrence frequency, and trend analysis.
 * 
 * Constitutional Requirements:
 * - <200ms UI response time for pattern filtering and visualization
 * - Executive function support through clear visual hierarchy
 * - ADHD-friendly design with consistent patterns and reduced cognitive load
 */
export const PatternVisualization: React.FC<Props> = ({
  patterns,
  metrics,
  onPatternSelect,
  onRefresh,
  loading = false,
  className = '',
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedStatus, setSelectedStatus] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('confidence');
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  // Filter and sort patterns based on user selections
  const filteredPatterns = useMemo(() => {
    let filtered = patterns.filter(pattern => {
      const categoryMatch = selectedCategory === 'all' || pattern.category === selectedCategory;
      const statusMatch = selectedStatus === 'all' || pattern.status === selectedStatus;
      const searchMatch = searchTerm === '' || 
        pattern.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        pattern.description.toLowerCase().includes(searchTerm.toLowerCase());
      
      return categoryMatch && statusMatch && searchMatch;
    });

    // Sort patterns
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'confidence':
          return b.confidence - a.confidence;
        case 'occurrences':
          return b.occurrences - a.occurrences;
        case 'lastDetected':
          return b.lastDetected.getTime() - a.lastDetected.getTime();
        case 'successRate':
          return b.successRate - a.successRate;
        default:
          return 0;
      }
    });

    return filtered;
  }, [patterns, selectedCategory, selectedStatus, searchTerm, sortBy]);

  const handlePatternClick = (pattern: WorkflowPattern) => {
    // Constitutional compliance: <200ms response time
    const startTime = performance.now();
    
    onPatternSelect(pattern);
    
    const responseTime = performance.now() - startTime;
    if (responseTime > 200) {
      console.warn(`Pattern selection took ${responseTime}ms - exceeds 200ms target`);
    }
  };

  const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return '#4CAF50';
    if (confidence >= 0.6) return '#FF9800';
    return '#f44336';
  };

  const getStatusIcon = (status: string) => {
    return (
      <div
        style={{
          ...styles.statusIcon,
          backgroundColor: STATUS_COLORS[status as keyof typeof STATUS_COLORS],
        }}
        title={status}
      />
    );
  };

  const handleSearchChange = (e: ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const handleCategoryChange = (e: ChangeEvent<HTMLSelectElement>) => {
    setSelectedCategory(e.target.value);
  };

  const handleStatusChange = (e: ChangeEvent<HTMLSelectElement>) => {
    setSelectedStatus(e.target.value);
  };

  const handleSortChange = (e: ChangeEvent<HTMLSelectElement>) => {
    setSortBy(e.target.value);
  };

  if (loading) {
    return (
      <div style={styles.loading}>
        Loading pattern data...
      </div>
    );
  }

  return (
    <div className={`pattern-visualization ${className}`} style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <h2 style={styles.title}>Workflow Pattern Detection</h2>
        <div style={styles.buttonGroup}>
          <button 
            style={styles.button} 
            onClick={onRefresh}
            disabled={loading}
            title="Refresh patterns"
          >
            ↻ Refresh
          </button>
          <button
            style={styles.button}
            onClick={() => setViewMode(viewMode === 'grid' ? 'list' : 'grid')}
          >
            {viewMode === 'grid' ? '☰ List View' : '⊞ Grid View'}
          </button>
        </div>
      </div>

      {/* Metrics Overview */}
      <div style={styles.metricsGrid}>
        <div style={styles.metricCard}>
          <div style={styles.metricTitle}>Total Patterns</div>
          <div style={styles.metricValue}>{metrics.totalPatterns}</div>
        </div>
        <div style={styles.metricCard}>
          <div style={styles.metricTitle}>Active Patterns</div>
          <div style={styles.metricValue}>{metrics.activePatterns}</div>
        </div>
        <div style={styles.metricCard}>
          <div style={styles.metricTitle}>Avg. Confidence</div>
          <div style={styles.metricValue}>
            {(metrics.averageConfidence * 100).toFixed(1)}%
          </div>
        </div>
        <div style={styles.metricCard}>
          <div style={styles.metricTitle}>Detection Rate</div>
          <div style={styles.metricValue}>↗ +12%</div>
        </div>
      </div>

      {/* Filters */}
      <div style={styles.filtersCard}>
        <div style={styles.filtersRow}>
          <input
            type="text"
            placeholder="Search patterns..."
            value={searchTerm}
            onChange={handleSearchChange}
            style={styles.input}
          />
          <select
            value={selectedCategory}
            onChange={handleCategoryChange}
            style={styles.input}
          >
            <option value="all">All Categories</option>
            <option value="automation">Automation</option>
            <option value="data-transformation">Data Transform</option>
            <option value="notification">Notification</option>
            <option value="integration">Integration</option>
          </select>
          <select
            value={selectedStatus}
            onChange={handleStatusChange}
            style={styles.input}
          >
            <option value="all">All Status</option>
            <option value="active">Active</option>
            <option value="learning">Learning</option>
            <option value="inactive">Inactive</option>
          </select>
          <select
            value={sortBy}
            onChange={handleSortChange}
            style={styles.input}
          >
            <option value="confidence">Sort by Confidence</option>
            <option value="occurrences">Sort by Occurrences</option>
            <option value="lastDetected">Sort by Recent</option>
            <option value="successRate">Sort by Success Rate</option>
          </select>
        </div>
      </div>

      {/* Pattern Grid/List */}
      {filteredPatterns.length === 0 ? (
        <div style={styles.alert}>
          No patterns found matching the current filters.
        </div>
      ) : (
        <div style={viewMode === 'grid' ? styles.patternsGrid : undefined}>
          {filteredPatterns.map((pattern) => {
            const cardStyle = {
              ...styles.patternCard,
              borderColor: CATEGORY_COLORS[pattern.category],
            };

            return (
              <div
                key={pattern.id}
                style={cardStyle}
                onClick={() => handlePatternClick(pattern)}
                onMouseEnter={(e) => {
                  Object.assign(e.currentTarget.style, styles.patternCardHover);
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'none';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              >
                <div style={styles.patternHeader}>
                  <h3 style={styles.patternTitle}>{pattern.name}</h3>
                  {getStatusIcon(pattern.status)}
                </div>
                
                <p style={styles.patternDescription}>
                  {pattern.description}
                </p>
                
                <div style={styles.chipContainer}>
                  <span
                    style={{
                      ...styles.chip,
                      backgroundColor: CATEGORY_COLORS[pattern.category],
                      color: 'white',
                    }}
                  >
                    {pattern.category}
                  </span>
                  <span
                    style={{
                      ...styles.chip,
                      border: '1px solid #ccc',
                      backgroundColor: 'transparent',
                    }}
                  >
                    {pattern.occurrences} times
                  </span>
                </div>
                
                <div style={styles.progressContainer}>
                  <div style={styles.progressLabel}>
                    Confidence: {(pattern.confidence * 100).toFixed(1)}%
                  </div>
                  <div style={styles.progressBar}>
                    <div
                      style={{
                        ...styles.progressFill,
                        width: `${pattern.confidence * 100}%`,
                        backgroundColor: getConfidenceColor(pattern.confidence),
                      }}
                    />
                  </div>
                </div>
                
                <div style={{ fontSize: '12px', color: '#666' }}>
                  Last detected: {formatDate(pattern.lastDetected)}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Top Performing Patterns */}
      {metrics.topPerformingPatterns.length > 0 && (
        <div style={{ ...styles.metricCard, marginTop: '24px' }}>
          <h3>Top Performing Patterns</h3>
          {metrics.topPerformingPatterns.slice(0, 5).map((pattern) => (
            <div
              key={pattern.id}
              style={{
                padding: '12px 0',
                borderBottom: '1px solid #eee',
                cursor: 'pointer',
              }}
              onClick={() => handlePatternClick(pattern)}
            >
              <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
                {pattern.name}
              </div>
              <div style={{ fontSize: '12px', color: '#666' }}>
                {(pattern.confidence * 100).toFixed(1)}% confidence • 
                {(pattern.successRate * 100).toFixed(1)}% success • 
                {(pattern.userApprovalRate * 100).toFixed(1)}% approval
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PatternVisualization;