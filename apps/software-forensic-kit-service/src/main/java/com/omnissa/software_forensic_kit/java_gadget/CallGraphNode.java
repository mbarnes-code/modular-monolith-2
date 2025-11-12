package com.omnissa.software_forensic_kit.java_gadget;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Represents a node in the function call graph for tracking method invocation relationships.
 * 
 * This class forms a tree/graph structure representing method call hierarchy where each node
 * contains a method signature and references to its parent caller and child callees.
 */
public class CallGraphNode {
    
    /** The parent node (caller) in the call graph */
    private CallGraphNode parent;
    
    /** Method signature or identifier for this node */
    private String data;
    
    /** List of child nodes (methods called by this method) */
    private ArrayList<CallGraphNode> children;
    
    /**
     * Default constructor creating an empty node.
     */
    public CallGraphNode() {
        this.parent = null;
        this.data = "";
        this.children = new ArrayList<>();
    }
    
    /**
     * Constructor with method signature.
     * 
     * @param data Method signature or identifier
     */
    public CallGraphNode(String data) {
        this.parent = null;
        this.data = data != null ? data : "";
        this.children = new ArrayList<>();
    }
    
    /**
     * Constructor with parent and data.
     * 
     * @param parent Parent node (caller)
     * @param data Method signature or identifier
     */
    public CallGraphNode(CallGraphNode parent, String data) {
        this.parent = parent;
        this.data = data != null ? data : "";
        this.children = new ArrayList<>();
    }
    
    // Getters and Setters
    
    public CallGraphNode getParent() {
        return parent;
    }
    
    public void setParent(CallGraphNode parent) {
        this.parent = parent;
    }
    
    public String getData() {
        return data;
    }
    
    public void setData(String data) {
        this.data = data != null ? data : "";
    }
    
    public ArrayList<CallGraphNode> getChildren() {
        return children;
    }
    
    public void setChildren(ArrayList<CallGraphNode> children) {
        this.children = children != null ? children : new ArrayList<>();
    }
    
    /**
     * Adds a child node to this node.
     * 
     * @param child Child node to add
     */
    public void addChild(CallGraphNode child) {
        if (child != null) {
            this.children.add(child);
            child.setParent(this);
        }
    }
    
    /**
     * Checks if this node has any children.
     * 
     * @return true if this node has children, false otherwise
     */
    public boolean hasChildren() {
        return !children.isEmpty();
    }
    
    /**
     * Checks if this node is a leaf node (no children).
     * 
     * @return true if this is a leaf node, false otherwise
     */
    public boolean isLeaf() {
        return children.isEmpty();
    }
    
    /**
     * Gets the root node of this call graph tree.
     * 
     * @return The root node (node with no parent)
     */
    public CallGraphNode getRoot() {
        CallGraphNode current = this;
        while (current.parent != null) {
            current = current.parent;
        }
        return current;
    }
    
    /**
     * Gets the depth of this node in the call graph tree.
     * 
     * @return Depth from root (root = 0)
     */
    public int getDepth() {
        int depth = 0;
        CallGraphNode current = this.parent;
        while (current != null) {
            depth++;
            current = current.parent;
        }
        return depth;
    }
    
    /**
     * Finds all leaf nodes (nodes with no children) in the subtree rooted at this node.
     * 
     * @return List of leaf nodes
     */
    public List<CallGraphNode> findLeafs() {
        List<CallGraphNode> leafs = new ArrayList<>();
        findLeafsRecursive(this, leafs, new HashSet<>());
        return leafs;
    }
    
    /**
     * Recursive helper method for finding leaf nodes with cycle detection.
     * 
     * @param node Current node being processed
     * @param leafs List to collect leaf nodes
     * @param visited Set of visited nodes to prevent infinite loops
     */
    private void findLeafsRecursive(CallGraphNode node, List<CallGraphNode> leafs, Set<String> visited) {
        if (node == null || visited.contains(node.getData())) {
            return;
        }
        
        visited.add(node.getData());
        
        if (node.isLeaf()) {
            leafs.add(node);
        } else {
            for (CallGraphNode child : node.getChildren()) {
                findLeafsRecursive(child, leafs, visited);
            }
        }
    }
    
    /**
     * Pretty prints the call graph starting from this node with proper indentation.
     * 
     * @param removeDuplicates Whether to remove duplicate paths
     * @return Formatted string representation of the call graph
     */
    public String prettyPrint(boolean removeDuplicates) {
        StringBuilder sb = new StringBuilder();
        Set<String> printedPaths = removeDuplicates ? new HashSet<>() : null;
        prettyPrintRecursive(this, "", sb, printedPaths, new HashSet<>());
        return sb.toString();
    }
    
    /**
     * Recursive helper method for pretty printing with cycle detection.
     * 
     * @param node Current node being printed
     * @param indent Current indentation level
     * @param sb StringBuilder to accumulate output
     * @param printedPaths Set of already printed paths (for duplicate removal)
     * @param currentPath Set representing current traversal path (for cycle detection)
     */
    private void prettyPrintRecursive(CallGraphNode node, String indent, StringBuilder sb, 
                                    Set<String> printedPaths, Set<String> currentPath) {
        if (node == null) {
            return;
        }
        
        String nodeData = node.getData();
        
        // Cycle detection
        if (currentPath.contains(nodeData)) {
            sb.append(indent).append(nodeData).append(" [CYCLE DETECTED]\\n");
            return;
        }
        
        // Build call path for duplicate detection
        String callPath = buildCallPath(node);
        
        // Check for duplicates if requested
        if (printedPaths != null && printedPaths.contains(callPath)) {
            return; // Skip duplicate path
        }
        
        // Add current node to path
        currentPath.add(nodeData);
        if (printedPaths != null) {
            printedPaths.add(callPath);
        }
        
        // Print current node
        sb.append(indent).append(nodeData).append("\\n");
        
        // Print children with increased indentation
        String childIndent = indent + "    ";
        for (CallGraphNode child : node.getChildren()) {
            prettyPrintRecursive(child, childIndent, sb, printedPaths, new HashSet<>(currentPath));
        }
        
        // Remove current node from path (backtrack)
        currentPath.remove(nodeData);
    }
    
    /**
     * Builds a string representation of the call path from root to this node.
     * 
     * @param node Target node
     * @return Call path as string
     */
    private String buildCallPath(CallGraphNode node) {
        List<String> path = new ArrayList<>();
        CallGraphNode current = node;
        
        // Build path from node to root
        while (current != null) {
            path.add(0, current.getData()); // Add to beginning
            current = current.getParent();
        }
        
        return String.join(" -> ", path);
    }
    
    /**
     * Returns the string representation of this node (method signature).
     * 
     * @return Method signature or identifier
     */
    @Override
    public String toString() {
        return data;
    }
    
    /**
     * Checks equality based on data content.
     * 
     * @param obj Object to compare
     * @return true if objects have same data, false otherwise
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        
        CallGraphNode that = (CallGraphNode) obj;
        return data.equals(that.data);
    }
    
    /**
     * Returns hash code based on data content.
     * 
     * @return Hash code
     */
    @Override
    public int hashCode() {
        return data.hashCode();
    }
    
    /**
     * Creates a copy of this node (without parent/children relationships).
     * 
     * @return New CallGraphNode with same data
     */
    public CallGraphNode copy() {
        return new CallGraphNode(this.data);
    }
    
    /**
     * Returns statistics about the call graph rooted at this node.
     * 
     * @return String containing node count, depth, and other metrics
     */
    public String getStatistics() {
        Set<String> uniqueNodes = new HashSet<>();
        int maxDepth = calculateStatistics(this, uniqueNodes, new HashSet<>(), 0);
        
        return String.format("Call Graph Statistics:\\n" +
                           "  Unique Nodes: %d\\n" +
                           "  Maximum Depth: %d\\n" +
                           "  Leaf Nodes: %d",
                           uniqueNodes.size(),
                           maxDepth,
                           findLeafs().size());
    }
    
    /**
     * Helper method to calculate call graph statistics.
     */
    private int calculateStatistics(CallGraphNode node, Set<String> uniqueNodes, 
                                  Set<String> visited, int currentDepth) {
        if (node == null || visited.contains(node.getData())) {
            return currentDepth;
        }
        
        visited.add(node.getData());
        uniqueNodes.add(node.getData());
        
        int maxDepth = currentDepth;
        for (CallGraphNode child : node.getChildren()) {
            int childDepth = calculateStatistics(child, uniqueNodes, visited, currentDepth + 1);
            maxDepth = Math.max(maxDepth, childDepth);
        }
        
        return maxDepth;
    }
}