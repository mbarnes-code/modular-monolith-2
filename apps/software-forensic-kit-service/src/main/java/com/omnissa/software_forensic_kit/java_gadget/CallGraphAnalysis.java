package com.omnissa.software_forensic_kit.java_gadget;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;
import java.util.regex.PatternSyntaxException;

/**
 * Core analysis engine that processes JAR files and generates call graphs.
 * 
 * This class is responsible for coordinating the entire analysis process including
 * JAR discovery, bytecode analysis, call graph construction, and result generation.
 */
public class CallGraphAnalysis {
    
    /** Path to the JAR file being analyzed */
    private String jarFile;
    
    /** Configuration options from command line */
    private Map<String, String> optionMap;
    
    /** Forward call graph mapping (caller -> list of callees) */
    private HashMap<String, ArrayList<String>> cgMap;
    
    /** Reverse call graph mapping (callee -> list of callers) */
    private HashMap<String, ArrayList<String>> reverse_cgMap;
    
    /** List of functions discovered during analysis */
    private ArrayList<String> discoveredFuncs;
    
    /** Maximum depth for call graph traversal */
    private int maxDepth;
    
    /** Whether to remove duplicate paths in output */
    private boolean removeDuplicates;
    
    /** Prefix to remove from method names in output */
    private String removeFromStart;
    
    /**
     * Constructor initializing with JAR file path and options.
     * 
     * @param jarFile Path to JAR file to analyze
     * @param optionMap Configuration options
     */
    public CallGraphAnalysis(String jarFile, Map<String, String> optionMap) {
        this.jarFile = jarFile;
        this.optionMap = optionMap != null ? optionMap : new HashMap<>();
        this.cgMap = new HashMap<>();
        this.reverse_cgMap = new HashMap<>();
        this.discoveredFuncs = new ArrayList<>();
        
        // Initialize configuration from options
        this.maxDepth = Integer.parseInt(this.optionMap.getOrDefault("depth", "8"));
        this.removeDuplicates = Boolean.parseBoolean(this.optionMap.getOrDefault("removeDuplicates", "false"));
        this.removeFromStart = this.optionMap.get("removeFromStart");
    }
    
    /**
     * Executes the complete call graph analysis process.
     * 
     * This method coordinates JAR parsing, call graph construction, function discovery,
     * and output generation based on the configured options.
     * 
     * @throws Exception If analysis fails at any stage
     */
    public void run() throws Exception {
        System.out.println("Starting call graph analysis for: " + jarFile);
        
        try {
            // Step 1: Parse JAR file and build call graphs
            System.out.println("Parsing JAR file and extracting call relationships...");
            buildCallGraphFromJar();
            
            // Step 2: Search for functions matching the pattern
            String searchFunction = optionMap.get("searchFunction");
            if (searchFunction != null) {
                System.out.println("Searching for functions matching pattern: " + searchFunction);
                discoverFunctions(searchFunction);
            }
            
            // Step 3: Build call graph trees for discovered functions
            System.out.println("Building call graph trees...");
            List<CallGraphNode> callGraphTrees = buildCallGraphTrees();
            
            // Step 4: Generate output in requested formats
            System.out.println("Generating output...");
            generateOutput(callGraphTrees);
            
            System.out.println("Analysis completed. Found " + discoveredFuncs.size() + " matching functions.");
            
        } catch (Exception e) {
            System.err.println("Analysis failed: " + e.getMessage());
            throw e;
        }
    }
    
    /**
     * Parses JAR file and builds forward and reverse call graph mappings.
     * 
     * This method uses bytecode analysis to extract method call relationships
     * and stores them in bidirectional HashMap structures for efficient lookup.
     */
    private void buildCallGraphFromJar() throws Exception {
        // TODO: Implement JAR parsing using BCEL/ASM
        // This will involve:
        // 1. Opening JAR file and enumerating .class files
        // 2. Parsing each class using BCEL ClassParser
        // 3. Extracting method calls using bytecode analysis
        // 4. Building cgMap (caller -> callees) and reverse_cgMap (callee -> callers)
        
        System.out.println("JAR parsing implementation pending - creating sample data");
        
        // Sample data for testing
        addCallRelationship("com.example.Main:main()", "com.example.Service:process()");
        addCallRelationship("com.example.Service:process()", "com.example.Dao:getData()");
        addCallRelationship("com.example.Service:process()", "com.example.Util:formatData()");
    }
    
    /**
     * Adds a call relationship to both forward and reverse call graph maps.
     * 
     * @param caller Method that makes the call
     * @param callee Method that is called
     */
    private void addCallRelationship(String caller, String callee) {
        // Add to forward map
        cgMap.computeIfAbsent(caller, k -> new ArrayList<>()).add(callee);
        
        // Add to reverse map
        reverse_cgMap.computeIfAbsent(callee, k -> new ArrayList<>()).add(caller);
    }
    
    /**
     * Discovers functions matching the search pattern using regex.
     * 
     * @param searchFunction Pattern with wildcard support (e.g., "Class*:method*")
     */
    private void discoverFunctions(String searchFunction) {
        try {
            // Convert wildcard pattern to regex
            String regexPattern = searchFunction.replace("*", ".*");
            Pattern pattern = Pattern.compile(regexPattern);
            
            // Search through all functions in call graph
            discoveredFuncs.clear();
            for (String function : reverse_cgMap.keySet()) {
                if (pattern.matcher(function).matches()) {
                    discoveredFuncs.add(function);
                }
            }
            
            // Also search in forward map keys
            for (String function : cgMap.keySet()) {
                if (pattern.matcher(function).matches() && !discoveredFuncs.contains(function)) {
                    discoveredFuncs.add(function);
                }
            }
            
        } catch (PatternSyntaxException e) {
            System.err.println("Invalid search pattern: " + e.getMessage());
            throw new RuntimeException("Invalid regex pattern", e);
        }
    }
    
    /**
     * Builds CallGraphNode trees for all discovered functions.
     * 
     * @return List of call graph trees rooted at discovered functions
     */
    private List<CallGraphNode> buildCallGraphTrees() {
        List<CallGraphNode> trees = new ArrayList<>();
        
        for (String function : discoveredFuncs) {
            CallGraphNode root = new CallGraphNode(function);
            buildCallGraphTree(root, 0);
            trees.add(root);
        }
        
        return trees;
    }
    
    /**
     * Recursively builds call graph tree using reverse call graph mapping.
     * 
     * @param node Current node in the tree
     * @param currentDepth Current traversal depth
     */
    private void buildCallGraphTree(CallGraphNode node, int currentDepth) {
        if (currentDepth >= maxDepth) {
            return; // Prevent excessive depth
        }
        
        String function = node.getData();
        ArrayList<String> callers = reverse_cgMap.get(function);
        
        if (callers != null) {
            for (String caller : callers) {
                // Check for cycles (simple check)
                if (!isInPath(node, caller)) {
                    CallGraphNode childNode = new CallGraphNode(caller);
                    node.addChild(childNode);
                    buildCallGraphTree(childNode, currentDepth + 1);
                }
            }
        }
    }
    
    /**
     * Checks if a function is already in the current call path (cycle detection).
     * 
     * @param node Current node
     * @param function Function to check
     * @return true if function is in path, false otherwise
     */
    private boolean isInPath(CallGraphNode node, String function) {
        CallGraphNode current = node;
        while (current != null) {
            if (current.getData().equals(function)) {
                return true;
            }
            current = current.getParent();
        }
        return false;
    }
    
    /**
     * Generates output in requested formats based on configuration options.
     * 
     * @param callGraphTrees List of call graph trees to output
     */
    private void generateOutput(List<CallGraphNode> callGraphTrees) {
        boolean prettyPrint = Boolean.parseBoolean(optionMap.getOrDefault("prettyPrint", "false"));
        boolean html = Boolean.parseBoolean(optionMap.getOrDefault("html", "false"));
        boolean graphViz = Boolean.parseBoolean(optionMap.getOrDefault("graphViz", "false"));
        
        if (prettyPrint) {
            generateTextOutput(callGraphTrees);
        }
        
        if (html) {
            generateHtmlOutput(callGraphTrees);
        }
        
        if (graphViz) {
            generateGraphVizOutput(callGraphTrees);
        }
        
        // Default to console output if no specific format requested
        if (!prettyPrint && !html && !graphViz) {
            generateTextOutput(callGraphTrees);
        }
    }
    
    /**
     * Generates text-based console output.
     */
    private void generateTextOutput(List<CallGraphNode> callGraphTrees) {
        System.out.println("\\n=== Call Graph Analysis Results ===");
        
        for (CallGraphNode tree : callGraphTrees) {
            System.out.println("\\nTarget Function: " + tree.getData());
            System.out.println("Call Paths:");
            System.out.println(tree.prettyPrint(removeDuplicates));
            System.out.println(tree.getStatistics());
        }
    }
    
    /**
     * Generates HTML output with vis.js visualization.
     */
    private void generateHtmlOutput(List<CallGraphNode> callGraphTrees) {
        // TODO: Implement HTML generation with vis.js
        System.out.println("HTML output generation not yet implemented");
    }
    
    /**
     * Generates GraphViz DOT format output.
     */
    private void generateGraphVizOutput(List<CallGraphNode> callGraphTrees) {
        // TODO: Implement GraphViz output generation
        System.out.println("GraphViz output generation not yet implemented");
    }
    
    // Getters and Setters
    
    public String getJarFile() {
        return jarFile;
    }
    
    public Map<String, String> getOptionMap() {
        return optionMap;
    }
    
    public HashMap<String, ArrayList<String>> getCgMap() {
        return cgMap;
    }
    
    public HashMap<String, ArrayList<String>> getReverse_cgMap() {
        return reverse_cgMap;
    }
    
    public ArrayList<String> getDiscoveredFuncs() {
        return discoveredFuncs;
    }
    
    public int getMaxDepth() {
        return maxDepth;
    }
    
    public boolean isRemoveDuplicates() {
        return removeDuplicates;
    }
}