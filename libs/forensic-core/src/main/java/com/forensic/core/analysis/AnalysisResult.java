package com.forensic.core.analysis;

import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Common interface for forensic analysis results.
 * Provides standardized structure for analysis output across different forensic tools.
 */
public class AnalysisResult {
    
    private final String analysisType;
    private final String targetIdentifier;
    private final long startTime;
    private final long endTime;
    private final AnalysisStatus status;
    private final List<Finding> findings;
    private final Map<String, Object> metadata;
    private final AnalysisMetrics metrics;
    
    public AnalysisResult(String analysisType, String targetIdentifier, 
                         long startTime, long endTime, AnalysisStatus status,
                         List<Finding> findings, Map<String, Object> metadata,
                         AnalysisMetrics metrics) {
        this.analysisType = analysisType;
        this.targetIdentifier = targetIdentifier;
        this.startTime = startTime;
        this.endTime = endTime;
        this.status = status;
        this.findings = findings;
        this.metadata = metadata;
        this.metrics = metrics;
    }
    
    // Getters
    public String getAnalysisType() { return analysisType; }
    public String getTargetIdentifier() { return targetIdentifier; }
    public long getStartTime() { return startTime; }
    public long getEndTime() { return endTime; }
    public AnalysisStatus getStatus() { return status; }
    public List<Finding> getFindings() { return findings; }
    public Map<String, Object> getMetadata() { return metadata; }
    public AnalysisMetrics getMetrics() { return metrics; }
    
    public long getDurationMs() {
        return endTime - startTime;
    }
    
    /**
     * Get findings by severity level
     */
    public List<Finding> getFindingsBySeverity(Finding.Severity severity) {
        return findings.stream()
            .filter(f -> f.getSeverity() == severity)
            .toList();
    }
    
    /**
     * Get total finding count by severity
     */
    public Map<Finding.Severity, Long> getSeverityCount() {
        return findings.stream()
            .collect(java.util.stream.Collectors.groupingBy(
                Finding::getSeverity,
                java.util.stream.Collectors.counting()
            ));
    }
    
    /**
     * Check if analysis has critical findings
     */
    public boolean hasCriticalFindings() {
        return findings.stream()
            .anyMatch(f -> f.getSeverity() == Finding.Severity.CRITICAL);
    }
    
    /**
     * Analysis execution status
     */
    public enum AnalysisStatus {
        SUCCESS,
        PARTIAL_SUCCESS,
        FAILURE,
        TIMEOUT,
        CANCELLED
    }
    
    /**
     * Individual analysis finding
     */
    public static class Finding {
        private final String id;
        private final String title;
        private final String description;
        private final Severity severity;
        private final String category;
        private final Map<String, Object> details;
        private final String location;
        
        public Finding(String id, String title, String description, 
                      Severity severity, String category, 
                      Map<String, Object> details, String location) {
            this.id = id;
            this.title = title;
            this.description = description;
            this.severity = severity;
            this.category = category;
            this.details = details;
            this.location = location;
        }
        
        // Getters
        public String getId() { return id; }
        public String getTitle() { return title; }
        public String getDescription() { return description; }
        public Severity getSeverity() { return severity; }
        public String getCategory() { return category; }
        public Map<String, Object> getDetails() { return details; }
        public String getLocation() { return location; }
        
        public enum Severity {
            INFO("Informational - no action required"),
            LOW("Low severity - monitor for patterns"), 
            MEDIUM("Medium severity - investigate when possible"),
            HIGH("High severity - investigate soon"),
            CRITICAL("Critical severity - investigate immediately");
            
            private final String description;
            
            Severity(String description) {
                this.description = description;
            }
            
            public String getDescription() { return description; }
        }
    }
    
    /**
     * Analysis performance metrics
     */
    public static class AnalysisMetrics {
        private final long memoryUsedMB;
        private final long cpuTimeMs;
        private final int itemsProcessed;
        private final int itemsSkipped;
        private final int errors;
        private final Map<String, Long> timingBreakdown;
        
        public AnalysisMetrics(long memoryUsedMB, long cpuTimeMs, 
                             int itemsProcessed, int itemsSkipped, 
                             int errors, Map<String, Long> timingBreakdown) {
            this.memoryUsedMB = memoryUsedMB;
            this.cpuTimeMs = cpuTimeMs;
            this.itemsProcessed = itemsProcessed;
            this.itemsSkipped = itemsSkipped;
            this.errors = errors;
            this.timingBreakdown = timingBreakdown;
        }
        
        // Getters
        public long getMemoryUsedMB() { return memoryUsedMB; }
        public long getCpuTimeMs() { return cpuTimeMs; }
        public int getItemsProcessed() { return itemsProcessed; }
        public int getItemsSkipped() { return itemsSkipped; }
        public int getErrors() { return errors; }
        public Map<String, Long> getTimingBreakdown() { return timingBreakdown; }
        
        public double getProcessingRate() {
            if (cpuTimeMs == 0) return 0.0;
            return (double) itemsProcessed / (cpuTimeMs / 1000.0);
        }
        
        public double getErrorRate() {
            int total = itemsProcessed + itemsSkipped + errors;
            if (total == 0) return 0.0;
            return (double) errors / total;
        }
    }
}