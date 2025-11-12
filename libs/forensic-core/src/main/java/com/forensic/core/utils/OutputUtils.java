package com.forensic.core.utils;

import com.forensic.core.analysis.AnalysisResult;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.core.JsonProcessingException;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.Instant;
import java.time.format.DateTimeFormatter;
import java.util.Map;
import java.util.List;

/**
 * Utilities for formatting and outputting forensic analysis results.
 * Supports multiple output formats including JSON, XML, HTML, and plain text.
 */
public class OutputUtils {
    
    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();
    private static final DateTimeFormatter TIMESTAMP_FORMAT = DateTimeFormatter.ISO_INSTANT;
    
    /**
     * Convert analysis result to JSON format
     */
    public static String toJson(AnalysisResult result) {
        try {
            return OBJECT_MAPPER.writerWithDefaultPrettyPrinter()
                               .writeValueAsString(result);
        } catch (JsonProcessingException e) {
            throw new RuntimeException("Failed to serialize analysis result to JSON", e);
        }
    }
    
    /**
     * Convert analysis result to formatted text report
     */
    public static String toTextReport(AnalysisResult result) {
        StringBuilder report = new StringBuilder();
        
        // Header
        report.append("=".repeat(80)).append("\n");
        report.append("FORENSIC ANALYSIS REPORT\n");
        report.append("=".repeat(80)).append("\n\n");
        
        // Basic information
        report.append("Analysis Type: ").append(result.getAnalysisType()).append("\n");
        report.append("Target: ").append(result.getTargetIdentifier()).append("\n");
        report.append("Status: ").append(result.getStatus()).append("\n");
        report.append("Duration: ").append(result.getDurationMs()).append(" ms\n");
        report.append("Timestamp: ").append(formatTimestamp(result.getStartTime())).append("\n\n");
        
        // Summary statistics
        report.append("SUMMARY\n");
        report.append("-".repeat(40)).append("\n");
        
        Map<AnalysisResult.Finding.Severity, Long> severityCounts = result.getSeverityCount();
        report.append("Total Findings: ").append(result.getFindings().size()).append("\n");
        
        for (AnalysisResult.Finding.Severity severity : AnalysisResult.Finding.Severity.values()) {
            long count = severityCounts.getOrDefault(severity, 0L);
            report.append(String.format("  %s: %d\n", severity, count));
        }
        report.append("\n");
        
        // Performance metrics
        if (result.getMetrics() != null) {
            AnalysisResult.AnalysisMetrics metrics = result.getMetrics();
            report.append("PERFORMANCE METRICS\n");
            report.append("-".repeat(40)).append("\n");
            report.append("Memory Used: ").append(metrics.getMemoryUsedMB()).append(" MB\n");
            report.append("CPU Time: ").append(metrics.getCpuTimeMs()).append(" ms\n");
            report.append("Items Processed: ").append(metrics.getItemsProcessed()).append("\n");
            report.append("Items Skipped: ").append(metrics.getItemsSkipped()).append("\n");
            report.append("Errors: ").append(metrics.getErrors()).append("\n");
            report.append("Processing Rate: ").append(String.format("%.2f items/sec\n", metrics.getProcessingRate()));
            report.append("Error Rate: ").append(String.format("%.2f%%\n", metrics.getErrorRate() * 100));
            report.append("\n");
        }
        
        // Detailed findings
        if (!result.getFindings().isEmpty()) {
            report.append("DETAILED FINDINGS\n");
            report.append("-".repeat(40)).append("\n\n");
            
            // Group by severity for better readability
            for (AnalysisResult.Finding.Severity severity : AnalysisResult.Finding.Severity.values()) {
                List<AnalysisResult.Finding> findings = result.getFindingsBySeverity(severity);
                if (!findings.isEmpty()) {
                    report.append(String.format("%s SEVERITY (%d findings)\n", severity, findings.size()));
                    report.append("~".repeat(30)).append("\n");
                    
                    for (int i = 0; i < findings.size(); i++) {
                        AnalysisResult.Finding finding = findings.get(i);
                        report.append(String.format("%d. %s\n", i + 1, finding.getTitle()));
                        report.append("   Location: ").append(finding.getLocation()).append("\n");
                        report.append("   Category: ").append(finding.getCategory()).append("\n");
                        report.append("   Description: ").append(finding.getDescription()).append("\n");
                        
                        if (!finding.getDetails().isEmpty()) {
                            report.append("   Details:\n");
                            for (Map.Entry<String, Object> detail : finding.getDetails().entrySet()) {
                                report.append(String.format("     %s: %s\n", detail.getKey(), detail.getValue()));
                            }
                        }
                        report.append("\n");
                    }
                    report.append("\n");
                }
            }
        }
        
        // Metadata
        if (result.getMetadata() != null && !result.getMetadata().isEmpty()) {
            report.append("METADATA\n");
            report.append("-".repeat(40)).append("\n");
            for (Map.Entry<String, Object> entry : result.getMetadata().entrySet()) {
                report.append(String.format("%s: %s\n", entry.getKey(), entry.getValue()));
            }
        }
        
        report.append("\n").append("=".repeat(80)).append("\n");
        report.append("Report generated at: ").append(formatTimestamp(System.currentTimeMillis()));
        report.append("\n").append("=".repeat(80));
        
        return report.toString();
    }
    
    /**
     * Generate HTML report with interactive elements
     */
    public static String toHtmlReport(AnalysisResult result) {
        StringBuilder html = new StringBuilder();
        
        html.append("<!DOCTYPE html>\n<html>\n<head>\n");
        html.append("<title>Forensic Analysis Report</title>\n");
        html.append("<style>\n");
        html.append("body { font-family: Arial, sans-serif; margin: 40px; }\n");
        html.append(".header { background: #2c3e50; color: white; padding: 20px; text-align: center; }\n");
        html.append(".section { margin: 20px 0; padding: 15px; border-left: 4px solid #3498db; }\n");
        html.append(".critical { border-left-color: #e74c3c; }\n");
        html.append(".high { border-left-color: #f39c12; }\n");
        html.append(".medium { border-left-color: #f1c40f; }\n");
        html.append(".low { border-left-color: #27ae60; }\n");
        html.append(".info { border-left-color: #3498db; }\n");
        html.append(".metric { display: inline-block; margin: 10px; padding: 10px; background: #ecf0f1; border-radius: 5px; }\n");
        html.append("table { width: 100%; border-collapse: collapse; margin: 10px 0; }\n");
        html.append("th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }\n");
        html.append("th { background-color: #f2f2f2; }\n");
        html.append("</style>\n</head>\n<body>\n");
        
        // Header
        html.append("<div class='header'>\n");
        html.append("<h1>Forensic Analysis Report</h1>\n");
        html.append("<p>").append(result.getAnalysisType()).append(" - ").append(result.getTargetIdentifier()).append("</p>\n");
        html.append("</div>\n");
        
        // Summary
        html.append("<div class='section'>\n<h2>Analysis Summary</h2>\n");
        html.append("<div class='metric'><strong>Status:</strong> ").append(result.getStatus()).append("</div>\n");
        html.append("<div class='metric'><strong>Duration:</strong> ").append(result.getDurationMs()).append(" ms</div>\n");
        html.append("<div class='metric'><strong>Findings:</strong> ").append(result.getFindings().size()).append("</div>\n");
        html.append("<div class='metric'><strong>Timestamp:</strong> ").append(formatTimestamp(result.getStartTime())).append("</div>\n");
        html.append("</div>\n");
        
        // Findings by severity
        if (!result.getFindings().isEmpty()) {
            html.append("<div class='section'>\n<h2>Findings by Severity</h2>\n");
            
            Map<AnalysisResult.Finding.Severity, Long> severityCounts = result.getSeverityCount();
            html.append("<table>\n<tr><th>Severity</th><th>Count</th><th>Description</th></tr>\n");
            
            for (AnalysisResult.Finding.Severity severity : AnalysisResult.Finding.Severity.values()) {
                long count = severityCounts.getOrDefault(severity, 0L);
                html.append("<tr class='").append(severity.toString().toLowerCase()).append("'>");
                html.append("<td>").append(severity).append("</td>");
                html.append("<td>").append(count).append("</td>");
                html.append("<td>").append(severity.getDescription()).append("</td>");
                html.append("</tr>\n");
            }
            html.append("</table>\n</div>\n");
            
            // Detailed findings
            html.append("<div class='section'>\n<h2>Detailed Findings</h2>\n");
            
            for (AnalysisResult.Finding.Severity severity : AnalysisResult.Finding.Severity.values()) {
                List<AnalysisResult.Finding> findings = result.getFindingsBySeverity(severity);
                if (!findings.isEmpty()) {
                    html.append("<h3>").append(severity).append(" Severity</h3>\n");
                    
                    for (AnalysisResult.Finding finding : findings) {
                        html.append("<div class='section ").append(severity.toString().toLowerCase()).append("'>\n");
                        html.append("<h4>").append(finding.getTitle()).append("</h4>\n");
                        html.append("<p><strong>Location:</strong> ").append(finding.getLocation()).append("</p>\n");
                        html.append("<p><strong>Category:</strong> ").append(finding.getCategory()).append("</p>\n");
                        html.append("<p>").append(finding.getDescription()).append("</p>\n");
                        
                        if (!finding.getDetails().isEmpty()) {
                            html.append("<h5>Details</h5>\n<ul>\n");
                            for (Map.Entry<String, Object> detail : finding.getDetails().entrySet()) {
                                html.append("<li><strong>").append(detail.getKey()).append(":</strong> ");
                                html.append(detail.getValue()).append("</li>\n");
                            }
                            html.append("</ul>\n");
                        }
                        html.append("</div>\n");
                    }
                }
            }
            html.append("</div>\n");
        }
        
        html.append("</body>\n</html>");
        return html.toString();
    }
    
    /**
     * Write analysis result to file in specified format
     */
    public static void writeToFile(AnalysisResult result, String outputPath, OutputFormat format) {
        try {
            Path path = Paths.get(outputPath);
            String content;
            
            switch (format) {
                case JSON:
                    content = toJson(result);
                    break;
                case HTML:
                    content = toHtmlReport(result);
                    break;
                case TEXT:
                default:
                    content = toTextReport(result);
                    break;
            }
            
            try (FileWriter writer = new FileWriter(path.toFile())) {
                writer.write(content);
            }
            
        } catch (IOException e) {
            throw new RuntimeException("Failed to write analysis result to file: " + outputPath, e);
        }
    }
    
    /**
     * Create a secure file name based on analysis details
     */
    public static String createOutputFileName(AnalysisResult result, OutputFormat format) {
        String timestamp = String.valueOf(result.getStartTime());
        String sanitizedTarget = SecurityUtils.sanitizeForLogging(result.getTargetIdentifier())
                                            .replaceAll("[^a-zA-Z0-9.-]", "_");
        String extension = format.getExtension();
        
        return String.format("%s_%s_%s.%s", 
            result.getAnalysisType().toLowerCase(),
            sanitizedTarget,
            timestamp,
            extension);
    }
    
    /**
     * Format timestamp for human readability
     */
    private static String formatTimestamp(long timestampMs) {
        return TIMESTAMP_FORMAT.format(Instant.ofEpochMilli(timestampMs));
    }
    
    /**
     * Output format options
     */
    public enum OutputFormat {
        JSON("json"),
        HTML("html"),
        TEXT("txt"),
        XML("xml");
        
        private final String extension;
        
        OutputFormat(String extension) {
            this.extension = extension;
        }
        
        public String getExtension() { 
            return extension; 
        }
    }
}