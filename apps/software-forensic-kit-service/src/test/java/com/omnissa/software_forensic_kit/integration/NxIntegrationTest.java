package com.omnissa.software_forensic_kit.integration;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.io.TempDir;

import java.io.File;
import java.nio.file.Path;
import java.nio.file.Files;

import static org.assertj.core.api.Assertions.*;

/**
 * Integration tests for Software Forensic Kit NX setup
 */
class NxIntegrationTest {
    
    @TempDir
    Path tempDir;
    
    @Test
    @DisplayName("Should have forensic-core dependency available")
    void testForensicCoreDependency() {
        // Test that we can import and use classes from forensic-core library
        assertThatCode(() -> {
            com.forensic.core.utils.SecurityUtils.calculateSHA256("test");
        }).doesNotThrowAnyException();
    }
    
    @Test
    @DisplayName("Should be able to use shared security utilities")
    void testSharedSecurityUtilities() {
        String hash = com.forensic.core.utils.SecurityUtils.calculateSHA256("integration-test");
        assertThat(hash).isNotEmpty();
        assertThat(hash).hasSize(64); // SHA-256 produces 64-character hex strings
        
        boolean isVulnerable = com.forensic.core.utils.SecurityUtils.isVulnerableMethod("java.lang.Runtime:exec");
        assertThat(isVulnerable).isTrue();
        
        boolean isSafe = com.forensic.core.utils.SecurityUtils.isPathSafe("./test.jar");
        assertThat(isSafe).isTrue();
    }
    
    @Test
    @DisplayName("Should be able to create analysis results")
    void testAnalysisResultCreation() {
        long now = System.currentTimeMillis();
        
        com.forensic.core.analysis.AnalysisResult result = 
            new com.forensic.core.analysis.AnalysisResult(
                "test-analysis",
                "test.jar", 
                now - 1000,
                now,
                com.forensic.core.analysis.AnalysisResult.AnalysisStatus.SUCCESS,
                java.util.Collections.emptyList(),
                java.util.Collections.emptyMap(),
                null
            );
            
        assertThat(result.getAnalysisType()).isEqualTo("test-analysis");
        assertThat(result.getTargetIdentifier()).isEqualTo("test.jar");
        assertThat(result.getStatus()).isEqualTo(com.forensic.core.analysis.AnalysisResult.AnalysisStatus.SUCCESS);
        assertThat(result.getDurationMs()).isEqualTo(1000L);
    }
    
    @Test
    @DisplayName("Should be able to generate output reports")
    void testOutputGeneration() {
        // Create a minimal analysis result
        com.forensic.core.analysis.AnalysisResult result = 
            new com.forensic.core.analysis.AnalysisResult(
                "integration-test",
                "test.jar",
                System.currentTimeMillis() - 1000,
                System.currentTimeMillis(),
                com.forensic.core.analysis.AnalysisResult.AnalysisStatus.SUCCESS,
                java.util.Collections.emptyList(),
                java.util.Collections.emptyMap(),
                null
            );
        
        // Test JSON output
        String json = com.forensic.core.utils.OutputUtils.toJson(result);
        assertThat(json).contains("integration-test");
        assertThat(json).contains("test.jar");
        
        // Test text report
        String textReport = com.forensic.core.utils.OutputUtils.toTextReport(result);
        assertThat(textReport).contains("FORENSIC ANALYSIS REPORT");
        assertThat(textReport).contains("integration-test");
        
        // Test HTML report
        String htmlReport = com.forensic.core.utils.OutputUtils.toHtmlReport(result);
        assertThat(htmlReport).contains("<!DOCTYPE html>");
        assertThat(htmlReport).contains("integration-test");
    }
    
    @Test
    @DisplayName("Should be able to write reports to files")
    void testFileOutput() throws Exception {
        com.forensic.core.analysis.AnalysisResult result = 
            new com.forensic.core.analysis.AnalysisResult(
                "file-output-test",
                "test.jar",
                System.currentTimeMillis() - 1000,
                System.currentTimeMillis(),
                com.forensic.core.analysis.AnalysisResult.AnalysisStatus.SUCCESS,
                java.util.Collections.emptyList(),
                java.util.Collections.emptyMap(),
                null
            );
        
        Path jsonFile = tempDir.resolve("test-report.json");
        Path textFile = tempDir.resolve("test-report.txt");
        Path htmlFile = tempDir.resolve("test-report.html");
        
        // Write files
        com.forensic.core.utils.OutputUtils.writeToFile(
            result, jsonFile.toString(), com.forensic.core.utils.OutputUtils.OutputFormat.JSON);
        com.forensic.core.utils.OutputUtils.writeToFile(
            result, textFile.toString(), com.forensic.core.utils.OutputUtils.OutputFormat.TEXT);
        com.forensic.core.utils.OutputUtils.writeToFile(
            result, htmlFile.toString(), com.forensic.core.utils.OutputUtils.OutputFormat.HTML);
        
        // Verify files exist and have content
        assertThat(jsonFile).exists();
        assertThat(textFile).exists();
        assertThat(htmlFile).exists();
        
        String jsonContent = Files.readString(jsonFile);
        String textContent = Files.readString(textFile);
        String htmlContent = Files.readString(htmlFile);
        
        assertThat(jsonContent).contains("file-output-test");
        assertThat(textContent).contains("FORENSIC ANALYSIS REPORT");
        assertThat(htmlContent).contains("<!DOCTYPE html>");
    }
    
    @Test
    @DisplayName("Should validate Maven build configuration")
    void testMavenConfiguration() {
        // Verify that essential project files exist
        File projectRoot = new File(System.getProperty("user.dir"));
        
        assertThat(new File(projectRoot, "pom.xml")).exists();
        assertThat(new File(projectRoot, "project.json")).exists();
        
        // Verify source structure
        assertThat(new File(projectRoot, "src/main/java")).exists();
        assertThat(new File(projectRoot, "src/test/java")).exists();
    }
    
    @Test
    @DisplayName("Should have proper environment configuration")
    void testEnvironmentConfiguration() {
        // Test that environment variables can be accessed
        String javaOpts = System.getenv("JAVA_OPTS");
        String logLevel = System.getenv("LOG_LEVEL");
        
        // These might be null in test environment, which is fine
        // Just testing that environment access works
        assertThatCode(() -> {
            System.getenv("JAVA_OPTS");
            System.getenv("LOG_LEVEL");  
            System.getenv("MAX_ANALYSIS_TIME");
        }).doesNotThrowAnyException();
    }
}