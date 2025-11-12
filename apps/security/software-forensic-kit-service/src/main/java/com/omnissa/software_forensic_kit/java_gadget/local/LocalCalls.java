package com.omnissa.software_forensic_kit.java_gadget.local;

import com.omnissa.software_forensic_kit.java_gadget.CallGraphAnalysis;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Handles local JAR file analysis operations.
 * 
 * This class coordinates local file discovery, JAR analysis, and result processing
 * without requiring remote connections.
 */
public class LocalCalls {
    
    /**
     * Executes local JAR analysis based on provided configuration.
     * 
     * @param optionMap Configuration options from command line
     * @throws Exception If local analysis fails
     */
    public void analyze(Map<String, String> optionMap) throws Exception {
        String filter = optionMap.get("filter");
        if (filter == null || filter.trim().isEmpty()) {
            throw new IllegalArgumentException("Filter parameter is required for local analysis");
        }
        
        System.out.println("Discovering JAR files with filter: " + filter);
        List<String> jarFiles = findJarFiles(filter);
        
        if (jarFiles.isEmpty()) {
            System.out.println("No JAR files found matching filter: " + filter);
            return;
        }
        
        System.out.println("Found " + jarFiles.size() + " JAR files to analyze");
        
        // Analyze each JAR file
        for (String jarFile : jarFiles) {
            try {
                System.out.println("\\nAnalyzing: " + jarFile);
                CallGraphAnalysis analysis = new CallGraphAnalysis(jarFile, optionMap);
                analysis.run();
                
            } catch (Exception e) {
                System.err.println("Failed to analyze " + jarFile + ": " + e.getMessage());
                // Continue with next JAR file
            }
        }
    }
    
    /**
     * Discovers JAR files matching the specified filter pattern.
     * 
     * @param filter File path filter (can include wildcards)
     * @return List of JAR file paths found
     */
    public List<String> findJarFiles(String filter) {
        List<String> jarFiles = new ArrayList<>();
        
        try {
            File filterFile = new File(filter);
            
            if (filterFile.isFile() && filter.toLowerCase().endsWith(".jar")) {
                // Single JAR file specified
                jarFiles.add(filterFile.getAbsolutePath());
                
            } else if (filterFile.isDirectory()) {
                // Directory specified - search recursively
                findJarFilesRecursive(filterFile, jarFiles);
                
            } else {
                // Handle wildcard patterns or specific paths
                File parent = filterFile.getParentFile();
                if (parent != null && parent.isDirectory()) {
                    String pattern = filterFile.getName();
                    findJarFilesWithPattern(parent, pattern, jarFiles);
                } else {
                    System.err.println("Invalid filter path: " + filter);
                }
            }
            
        } catch (Exception e) {
            System.err.println("Error discovering JAR files: " + e.getMessage());
        }
        
        return jarFiles;
    }
    
    /**
     * Recursively searches for JAR files in a directory.
     * 
     * @param directory Directory to search
     * @param jarFiles List to accumulate found JAR files
     */
    private void findJarFilesRecursive(File directory, List<String> jarFiles) {
        File[] files = directory.listFiles();
        if (files == null) {
            return;
        }
        
        for (File file : files) {
            if (file.isDirectory()) {
                findJarFilesRecursive(file, jarFiles);
            } else if (file.getName().toLowerCase().endsWith(".jar")) {
                jarFiles.add(file.getAbsolutePath());
            }
        }
    }
    
    /**
     * Finds JAR files matching a pattern in a specific directory.
     * 
     * @param directory Directory to search in
     * @param pattern File name pattern
     * @param jarFiles List to accumulate found JAR files
     */
    private void findJarFilesWithPattern(File directory, String pattern, List<String> jarFiles) {
        File[] files = directory.listFiles();
        if (files == null) {
            return;
        }
        
        // Convert simple wildcard pattern to regex
        String regexPattern = pattern.replace("*", ".*").replace("?", ".");
        
        for (File file : files) {
            if (file.isFile() && 
                file.getName().toLowerCase().endsWith(".jar") &&
                file.getName().matches(regexPattern)) {
                jarFiles.add(file.getAbsolutePath());
            }
        }
    }
    
    /**
     * Validates that a JAR file is readable and accessible.
     * 
     * @param jarPath Path to JAR file
     * @return true if JAR file is valid and readable
     */
    public boolean validateJarFile(String jarPath) {
        try {
            File jarFile = new File(jarPath);
            return jarFile.exists() && jarFile.isFile() && jarFile.canRead();
            
        } catch (Exception e) {
            System.err.println("JAR validation failed for " + jarPath + ": " + e.getMessage());
            return false;
        }
    }
    
    /**
     * Gets file size information for a JAR file.
     * 
     * @param jarPath Path to JAR file
     * @return File size in bytes, or -1 if error
     */
    public long getJarFileSize(String jarPath) {
        try {
            File jarFile = new File(jarPath);
            return jarFile.length();
        } catch (Exception e) {
            return -1;
        }
    }
    
    /**
     * Estimates analysis time based on JAR file size.
     * 
     * @param jarPath Path to JAR file
     * @return Estimated analysis time in seconds
     */
    public int estimateAnalysisTime(String jarPath) {
        long sizeBytes = getJarFileSize(jarPath);
        if (sizeBytes <= 0) {
            return 30; // Default estimate
        }
        
        // Rough estimates based on file size
        long sizeMB = sizeBytes / (1024 * 1024);
        
        if (sizeMB < 1) {
            return 10;
        } else if (sizeMB < 10) {
            return 30;
        } else if (sizeMB < 100) {
            return 120; // 2 minutes
        } else {
            return 300; // 5 minutes
        }
    }
}