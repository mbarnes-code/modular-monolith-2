package com.forensic.core.utils;

import com.forensic.core.analysis.AnalysisResult;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Path;
import java.util.*;

import static org.assertj.core.api.Assertions.*;

/**
 * Unit tests for OutputUtils class
 */
class OutputUtilsTest {
    
    private AnalysisResult sampleResult;
    
    @TempDir
    Path tempDir;
    
    @BeforeEach
    void setUp() {
        // Create sample analysis result for testing
        long startTime = System.currentTimeMillis() - 5000;
        long endTime = System.currentTimeMillis();
        
        // Create sample findings
        List<AnalysisResult.Finding> findings = Arrays.asList(
            new AnalysisResult.Finding(
                "F001",
                "Critical Security Issue",
                "Found dangerous method call",
                AnalysisResult.Finding.Severity.CRITICAL,
                "security",
                Map.of("method", "java.lang.Runtime:exec", "line", 123),
                "com.example.Service:processData"
            ),
            new AnalysisResult.Finding(
                "F002",
                "Reflection Usage",
                "Dynamic method invocation detected",
                AnalysisResult.Finding.Severity.MEDIUM,
                "security",
                Map.of("method", "java.lang.reflect.Method:invoke"),
                "com.example.Utils:reflectiveCall"
            )
        );
        
        // Create metrics
        AnalysisResult.AnalysisMetrics metrics = new AnalysisResult.AnalysisMetrics(
            256L, // memory used MB
            3000L, // CPU time ms
            150, // items processed
            5, // items skipped
            2, // errors
            Map.of("parsing", 1000L, "analysis", 2000L)
        );
        
        // Create metadata
        Map<String, Object> metadata = Map.of(
            "jarFile", "test-app.jar",
            "analysisMode", "local",
            "searchPattern", "*vulnerable*"
        );
        
        sampleResult = new AnalysisResult(
            "callgraph-analysis",
            "test-app.jar",
            startTime,
            endTime,
            AnalysisResult.AnalysisStatus.SUCCESS,
            findings,
            metadata,
            metrics
        );
    }
    
    @Test
    @DisplayName("Should convert analysis result to JSON")
    void testToJson() {
        String json = OutputUtils.toJson(sampleResult);
        
        assertThat(json).isNotEmpty();
        assertThat(json).contains("callgraph-analysis");
        assertThat(json).contains("test-app.jar");
        assertThat(json).contains("Critical Security Issue");
        assertThat(json).contains("SUCCESS");
    }
    
    @Test
    @DisplayName("Should create text report")
    void testToTextReport() {
        String report = OutputUtils.toTextReport(sampleResult);
        
        assertThat(report).contains("FORENSIC ANALYSIS REPORT");
        assertThat(report).contains("Analysis Type: callgraph-analysis");
        assertThat(report).contains("Target: test-app.jar");
        assertThat(report).contains("Status: SUCCESS");
        assertThat(report).contains("Total Findings: 2");
        assertThat(report).contains("CRITICAL: 1");
        assertThat(report).contains("MEDIUM: 1");
        assertThat(report).contains("Memory Used: 256 MB");
        assertThat(report).contains("Items Processed: 150");
        assertThat(report).contains("Critical Security Issue");
        assertThat(report).contains("Reflection Usage");
    }
    
    @Test
    @DisplayName("Should create HTML report")
    void testToHtmlReport() {
        String html = OutputUtils.toHtmlReport(sampleResult);
        
        assertThat(html).contains("<!DOCTYPE html>");
        assertThat(html).contains("<title>Forensic Analysis Report</title>");
        assertThat(html).contains("callgraph-analysis");
        assertThat(html).contains("test-app.jar");
        assertThat(html).contains("Critical Security Issue");
        assertThat(html).contains("class='critical'");
        assertThat(html).contains("class='medium'");
    }
    
    @Test
    @DisplayName("Should write to file in different formats")
    void testWriteToFile() {
        Path jsonFile = tempDir.resolve("report.json");
        Path textFile = tempDir.resolve("report.txt");
        Path htmlFile = tempDir.resolve("report.html");
        
        OutputUtils.writeToFile(sampleResult, jsonFile.toString(), OutputUtils.OutputFormat.JSON);
        OutputUtils.writeToFile(sampleResult, textFile.toString(), OutputUtils.OutputFormat.TEXT);
        OutputUtils.writeToFile(sampleResult, htmlFile.toString(), OutputUtils.OutputFormat.HTML);
        
        assertThat(jsonFile).exists();
        assertThat(textFile).exists();
        assertThat(htmlFile).exists();
    }
    
    @Test
    @DisplayName("Should create secure output file names")
    void testCreateOutputFileName() {
        String fileName = OutputUtils.createOutputFileName(sampleResult, OutputUtils.OutputFormat.JSON);
        
        assertThat(fileName).matches("callgraph-analysis_test-app_jar_\\d+\\.json");
        assertThat(fileName).contains("callgraph-analysis");
        assertThat(fileName).endsWith(".json");
    }
    
    @Test
    @DisplayName("Should handle output format extensions")
    void testOutputFormatExtensions() {
        assertThat(OutputUtils.OutputFormat.JSON.getExtension()).isEqualTo("json");
        assertThat(OutputUtils.OutputFormat.HTML.getExtension()).isEqualTo("html");
        assertThat(OutputUtils.OutputFormat.TEXT.getExtension()).isEqualTo("txt");
        assertThat(OutputUtils.OutputFormat.XML.getExtension()).isEqualTo("xml");
    }
    
    @Test
    @DisplayName("Should handle empty findings gracefully")
    void testEmptyFindings() {
        AnalysisResult emptyResult = new AnalysisResult(
            "test-analysis",
            "empty.jar",
            System.currentTimeMillis() - 1000,
            System.currentTimeMillis(),
            AnalysisResult.AnalysisStatus.SUCCESS,
            Collections.emptyList(),
            Collections.emptyMap(),
            null
        );
        
        String textReport = OutputUtils.toTextReport(emptyResult);
        String htmlReport = OutputUtils.toHtmlReport(emptyResult);
        String jsonReport = OutputUtils.toJson(emptyResult);
        
        assertThat(textReport).contains("Total Findings: 0");
        assertThat(htmlReport).contains("Findings: 0");
        assertThat(jsonReport).contains("test-analysis");
    }
    
    @Test
    @DisplayName("Should handle special characters in output")
    void testSpecialCharacters() {
        AnalysisResult specialResult = new AnalysisResult(
            "test<>&analysis",
            "test-app.jar",
            System.currentTimeMillis() - 1000,
            System.currentTimeMillis(),
            AnalysisResult.AnalysisStatus.SUCCESS,
            Arrays.asList(
                new AnalysisResult.Finding(
                    "F001",
                    "Title with <special> & characters",
                    "Description with \"quotes\" and 'apostrophes'",
                    AnalysisResult.Finding.Severity.HIGH,
                    "test",
                    Map.of("special", "<script>alert('test')</script>"),
                    "location"
                )
            ),
            Collections.emptyMap(),
            null
        );
        
        String fileName = OutputUtils.createOutputFileName(specialResult, OutputUtils.OutputFormat.HTML);
        assertThat(fileName).doesNotContain("<");
        assertThat(fileName).doesNotContain(">");
        assertThat(fileName).doesNotContain("&");
        
        String htmlReport = OutputUtils.toHtmlReport(specialResult);
        // HTML should be properly escaped or at least not break the document structure
        assertThat(htmlReport).contains("<!DOCTYPE html>");
        assertThat(htmlReport).contains("</html>");
    }
}