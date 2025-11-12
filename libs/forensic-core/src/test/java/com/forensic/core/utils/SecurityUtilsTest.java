package com.forensic.core.utils;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.assertj.core.api.Assertions.*;

/**
 * Unit tests for SecurityUtils class
 */
class SecurityUtilsTest {
    
    @Test
    @DisplayName("Should calculate SHA-256 hash correctly")
    void testCalculateSHA256() {
        String input = "test input";
        String expectedHash = "c619b86cb5c0fb0551988aa720b25095e0494eabcd9aeb72d2ece0b6e1b3380b";
        
        String actualHash = SecurityUtils.calculateSHA256(input);
        
        assertThat(actualHash).isEqualTo(expectedHash);
    }
    
    @Test
    @DisplayName("Should validate safe file paths")
    void testIsPathSafe() {
        // Safe paths
        assertThat(SecurityUtils.isPathSafe("/tmp/analysis/test.jar")).isTrue();
        assertThat(SecurityUtils.isPathSafe("/opt/app/lib/app.jar")).isTrue();
        assertThat(SecurityUtils.isPathSafe("./local/test.jar")).isTrue();
        assertThat(SecurityUtils.isPathSafe("test.jar")).isTrue();
        
        // Unsafe paths
        assertThat(SecurityUtils.isPathSafe("../../../etc/passwd")).isFalse();
        assertThat(SecurityUtils.isPathSafe("/etc/passwd")).isFalse();
        assertThat(SecurityUtils.isPathSafe("")).isFalse();
        assertThat(SecurityUtils.isPathSafe(null)).isFalse();
    }
    
    @Test
    @DisplayName("Should identify vulnerable methods")
    void testIsVulnerableMethod() {
        // Vulnerable methods
        assertThat(SecurityUtils.isVulnerableMethod("java.lang.Runtime:exec")).isTrue();
        assertThat(SecurityUtils.isVulnerableMethod("java.lang.ProcessBuilder:<init>")).isTrue();
        assertThat(SecurityUtils.isVulnerableMethod("java.io.ObjectInputStream:readObject")).isTrue();
        assertThat(SecurityUtils.isVulnerableMethod("sun.misc.Unsafe:getUnsafe")).isTrue();
        assertThat(SecurityUtils.isVulnerableMethod("com.example.Reflection:invoke")).isTrue();
        
        // Safe methods
        assertThat(SecurityUtils.isVulnerableMethod("java.lang.String:valueOf")).isFalse();
        assertThat(SecurityUtils.isVulnerableMethod("com.example.Service:processData")).isFalse();
        assertThat(SecurityUtils.isVulnerableMethod(null)).isFalse();
    }
    
    @Test
    @DisplayName("Should sanitize input for logging")
    void testSanitizeForLogging() {
        assertThat(SecurityUtils.sanitizeForLogging("normal string")).isEqualTo("normal string");
        assertThat(SecurityUtils.sanitizeForLogging("line\nbreak")).isEqualTo("line_break");
        assertThat(SecurityUtils.sanitizeForLogging("tab\there")).isEqualTo("tab_here");
        assertThat(SecurityUtils.sanitizeForLogging("carriage\rreturn")).isEqualTo("carriage_return");
        assertThat(SecurityUtils.sanitizeForLogging(null)).isEqualTo("null");
        
        // Test length limiting
        String longInput = "a".repeat(600);
        String sanitized = SecurityUtils.sanitizeForLogging(longInput);
        assertThat(sanitized).hasSize(500);
    }
    
    @Test
    @DisplayName("Should validate JAR file names")
    void testIsValidJarName() {
        // Valid JAR names
        assertThat(SecurityUtils.isValidJarName("app.jar")).isTrue();
        assertThat(SecurityUtils.isValidJarName("my-library-1.0.0.jar")).isTrue();
        assertThat(SecurityUtils.isValidJarName("test_app.jar")).isTrue();
        
        // Invalid JAR names
        assertThat(SecurityUtils.isValidJarName("app.txt")).isFalse();
        assertThat(SecurityUtils.isValidJarName("app")).isFalse();
        assertThat(SecurityUtils.isValidJarName("")).isFalse();
        assertThat(SecurityUtils.isValidJarName(null)).isFalse();
        assertThat(SecurityUtils.isValidJarName("app<malicious>.jar")).isFalse();
    }
    
    @Test
    @DisplayName("Should assess security risk levels correctly")
    void testGetRiskLevel() {
        assertThat(SecurityUtils.getRiskLevel("java.lang.Runtime:exec"))
            .isEqualTo(SecurityUtils.SecurityRiskLevel.CRITICAL);
            
        assertThat(SecurityUtils.getRiskLevel("java.io.ObjectInputStream:readObject"))
            .isEqualTo(SecurityUtils.SecurityRiskLevel.HIGH);
            
        assertThat(SecurityUtils.getRiskLevel("java.lang.reflect.Method:invoke"))
            .isEqualTo(SecurityUtils.SecurityRiskLevel.MEDIUM);
            
        assertThat(SecurityUtils.getRiskLevel("java.lang.String:valueOf"))
            .isEqualTo(SecurityUtils.SecurityRiskLevel.NONE);
    }
    
    @Test
    @DisplayName("Should create secure temporary file names")
    void testCreateSecureTempFileName() {
        String fileName = SecurityUtils.createSecureTempFileName("analysis", "json");
        
        assertThat(fileName).matches("analysis_\\d+_\\d+\\.json");
        assertThat(fileName).contains("analysis");
        assertThat(fileName).endsWith(".json");
    }
    
    @Test
    @DisplayName("Should handle security risk level descriptions")
    void testSecurityRiskLevelDescriptions() {
        for (SecurityUtils.SecurityRiskLevel level : SecurityUtils.SecurityRiskLevel.values()) {
            assertThat(level.getDescription()).isNotEmpty();
        }
        
        assertThat(SecurityUtils.SecurityRiskLevel.CRITICAL.getDescription())
            .contains("immediate action required");
        assertThat(SecurityUtils.SecurityRiskLevel.NONE.getDescription())
            .contains("No known security risk");
    }
}