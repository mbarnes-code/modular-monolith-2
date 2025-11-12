package com.forensic.core.utils;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.regex.Pattern;
import java.util.Set;
import java.util.HashSet;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Security utilities for forensic analysis operations.
 * Provides common security functions used across forensic analysis tools.
 */
public class SecurityUtils {
    
    // Common vulnerable function patterns for security analysis
    private static final Set<Pattern> VULNERABLE_PATTERNS = new HashSet<>();
    
    // Dangerous method signatures that should be flagged
    private static final Set<String> DANGEROUS_METHODS = new HashSet<>();
    
    static {
        // Initialize vulnerable patterns
        VULNERABLE_PATTERNS.add(Pattern.compile(".*exec.*", Pattern.CASE_INSENSITIVE));
        VULNERABLE_PATTERNS.add(Pattern.compile(".*eval.*", Pattern.CASE_INSENSITIVE));
        VULNERABLE_PATTERNS.add(Pattern.compile(".*deserialize.*", Pattern.CASE_INSENSITIVE));
        VULNERABLE_PATTERNS.add(Pattern.compile(".*reflection.*", Pattern.CASE_INSENSITIVE));
        VULNERABLE_PATTERNS.add(Pattern.compile(".*unsafe.*", Pattern.CASE_INSENSITIVE));
        
        // Initialize dangerous methods
        DANGEROUS_METHODS.add("java.lang.Runtime:exec");
        DANGEROUS_METHODS.add("java.lang.ProcessBuilder:<init>");
        DANGEROUS_METHODS.add("java.io.ObjectInputStream:readObject");
        DANGEROUS_METHODS.add("java.lang.reflect.Method:invoke");
        DANGEROUS_METHODS.add("sun.misc.Unsafe:getUnsafe");
    }
    
    /**
     * Calculate SHA-256 hash of a string (useful for JAR file integrity)
     */
    public static String calculateSHA256(String input) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(input.getBytes());
            StringBuilder hexString = new StringBuilder();
            
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) {
                    hexString.append('0');
                }
                hexString.append(hex);
            }
            
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 algorithm not available", e);
        }
    }
    
    /**
     * Validate that a file path is safe for analysis (prevent directory traversal)
     */
    public static boolean isPathSafe(String filePath) {
        if (filePath == null || filePath.trim().isEmpty()) {
            return false;
        }
        
        try {
            Path path = Paths.get(filePath).normalize();
            String normalizedPath = path.toString();
            
            // Check for directory traversal attempts
            if (normalizedPath.contains("..") || 
                normalizedPath.startsWith("/") && !normalizedPath.startsWith("/tmp/") && 
                !normalizedPath.startsWith("/opt/")) {
                return false;
            }
            
            return true;
        } catch (Exception e) {
            return false;
        }
    }
    
    /**
     * Check if a method signature matches known vulnerable patterns
     */
    public static boolean isVulnerableMethod(String methodSignature) {
        if (methodSignature == null) {
            return false;
        }
        
        // Check against dangerous methods list
        if (DANGEROUS_METHODS.contains(methodSignature)) {
            return true;
        }
        
        // Check against vulnerable patterns
        for (Pattern pattern : VULNERABLE_PATTERNS) {
            if (pattern.matcher(methodSignature).matches()) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Sanitize input for safe logging and output
     */
    public static String sanitizeForLogging(String input) {
        if (input == null) {
            return "null";
        }
        
        // Remove potential CRLF injection attempts
        return input.replaceAll("[\\r\\n\\t]", "_")
                   .replaceAll("[^\\p{Print}]", "?")
                   .substring(0, Math.min(input.length(), 500)); // Limit length
    }
    
    /**
     * Validate JAR file name against security criteria
     */
    public static boolean isValidJarName(String jarName) {
        if (jarName == null || jarName.trim().isEmpty()) {
            return false;
        }
        
        // Must end with .jar
        if (!jarName.toLowerCase().endsWith(".jar")) {
            return false;
        }
        
        // Must not contain suspicious characters
        Pattern suspiciousPattern = Pattern.compile("[<>:\"|?*\\x00-\\x1f]");
        if (suspiciousPattern.matcher(jarName).find()) {
            return false;
        }
        
        return true;
    }
    
    /**
     * Get security risk level for a method based on its signature
     */
    public static SecurityRiskLevel getRiskLevel(String methodSignature) {
        if (isVulnerableMethod(methodSignature)) {
            // Further classification based on method type
            if (methodSignature.contains("exec") || methodSignature.contains("ProcessBuilder")) {
                return SecurityRiskLevel.CRITICAL;
            } else if (methodSignature.contains("deserialize") || methodSignature.contains("readObject")) {
                return SecurityRiskLevel.HIGH;
            } else if (methodSignature.contains("reflect") || methodSignature.contains("invoke")) {
                return SecurityRiskLevel.MEDIUM;
            } else {
                return SecurityRiskLevel.LOW;
            }
        }
        
        return SecurityRiskLevel.NONE;
    }
    
    /**
     * Security risk levels for method classification
     */
    public enum SecurityRiskLevel {
        NONE("No known security risk"),
        LOW("Low security risk - requires monitoring"),
        MEDIUM("Medium security risk - requires review"),
        HIGH("High security risk - requires immediate attention"),
        CRITICAL("Critical security risk - immediate action required");
        
        private final String description;
        
        SecurityRiskLevel(String description) {
            this.description = description;
        }
        
        public String getDescription() {
            return description;
        }
    }
    
    /**
     * Create a secure temporary file name for analysis operations
     */
    public static String createSecureTempFileName(String prefix, String suffix) {
        String timestamp = String.valueOf(System.currentTimeMillis());
        String random = String.valueOf((int)(Math.random() * 10000));
        
        return String.format("%s_%s_%s.%s", 
            sanitizeForLogging(prefix), 
            timestamp, 
            random, 
            sanitizeForLogging(suffix));
    }
}