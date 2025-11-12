package com.omnissa.software_forensic_kit.java_gadget;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

/**
 * Unit tests for CallGraphNode class.
 */
public class CallGraphNodeTest {
    
    private CallGraphNode rootNode;
    private CallGraphNode childNode1;
    private CallGraphNode childNode2;
    private CallGraphNode grandChildNode;
    
    @BeforeEach
    void setUp() {
        // Create test call graph structure
        rootNode = new CallGraphNode("com.example.Main:main()");
        childNode1 = new CallGraphNode("com.example.Service:process()");
        childNode2 = new CallGraphNode("com.example.Util:helper()");
        grandChildNode = new CallGraphNode("com.example.Dao:getData()");
        
        // Build hierarchy: main -> service -> dao
        //                       -> util
        rootNode.addChild(childNode1);
        rootNode.addChild(childNode2);
        childNode1.addChild(grandChildNode);
    }
    
    @Test
    @DisplayName("Constructor should initialize node correctly")
    void testConstructor() {
        CallGraphNode node = new CallGraphNode("test.method()");
        
        assertEquals("test.method()", node.getData());
        assertNull(node.getParent());
        assertTrue(node.getChildren().isEmpty());
    }
    
    @Test
    @DisplayName("Default constructor should create empty node")
    void testDefaultConstructor() {
        CallGraphNode node = new CallGraphNode();
        
        assertEquals("", node.getData());
        assertNull(node.getParent());
        assertTrue(node.getChildren().isEmpty());
    }
    
    @Test
    @DisplayName("Constructor with null data should handle gracefully")
    void testConstructorWithNullData() {
        CallGraphNode node = new CallGraphNode(null);
        
        assertEquals("", node.getData());
        assertNull(node.getParent());
        assertTrue(node.getChildren().isEmpty());
    }
    
    @Test
    @DisplayName("addChild should establish parent-child relationship")
    void testAddChild() {
        CallGraphNode parent = new CallGraphNode("parent");
        CallGraphNode child = new CallGraphNode("child");
        
        parent.addChild(child);
        
        assertTrue(parent.getChildren().contains(child));
        assertEquals(parent, child.getParent());
        assertTrue(parent.hasChildren());
        assertFalse(parent.isLeaf());
    }
    
    @Test
    @DisplayName("addChild with null should handle gracefully")
    void testAddChildWithNull() {
        CallGraphNode parent = new CallGraphNode("parent");
        
        parent.addChild(null);
        
        assertTrue(parent.getChildren().isEmpty());
        assertFalse(parent.hasChildren());
        assertTrue(parent.isLeaf());
    }
    
    @Test
    @DisplayName("getRoot should return root node")
    void testGetRoot() {
        assertEquals(rootNode, rootNode.getRoot());
        assertEquals(rootNode, childNode1.getRoot());
        assertEquals(rootNode, grandChildNode.getRoot());
    }
    
    @Test
    @DisplayName("getDepth should calculate correct depth")
    void testGetDepth() {
        assertEquals(0, rootNode.getDepth());
        assertEquals(1, childNode1.getDepth());
        assertEquals(1, childNode2.getDepth());
        assertEquals(2, grandChildNode.getDepth());
    }
    
    @Test
    @DisplayName("isLeaf should identify leaf nodes correctly")
    void testIsLeaf() {
        assertFalse(rootNode.isLeaf());
        assertFalse(childNode1.isLeaf());
        assertTrue(childNode2.isLeaf());
        assertTrue(grandChildNode.isLeaf());
    }
    
    @Test
    @DisplayName("findLeafs should return all leaf nodes")
    void testFindLeafs() {
        List<CallGraphNode> leafs = rootNode.findLeafs();
        
        assertEquals(2, leafs.size());
        assertTrue(leafs.contains(childNode2));
        assertTrue(leafs.contains(grandChildNode));
        assertFalse(leafs.contains(rootNode));
        assertFalse(leafs.contains(childNode1));
    }
    
    @Test
    @DisplayName("findLeafs on leaf node should return itself")
    void testFindLeafsOnLeafNode() {
        List<CallGraphNode> leafs = grandChildNode.findLeafs();
        
        assertEquals(1, leafs.size());
        assertTrue(leafs.contains(grandChildNode));
    }
    
    @Test
    @DisplayName("prettyPrint should format tree structure")
    void testPrettyPrint() {
        String output = rootNode.prettyPrint(false);
        
        assertNotNull(output);
        assertTrue(output.contains("com.example.Main:main()"));
        assertTrue(output.contains("com.example.Service:process()"));
        assertTrue(output.contains("com.example.Util:helper()"));
        assertTrue(output.contains("com.example.Dao:getData()"));
    }
    
    @Test
    @DisplayName("toString should return node data")
    void testToString() {
        assertEquals("com.example.Main:main()", rootNode.toString());
        assertEquals("com.example.Service:process()", childNode1.toString());
    }
    
    @Test
    @DisplayName("equals should compare based on data")
    void testEquals() {
        CallGraphNode node1 = new CallGraphNode("same.method()");
        CallGraphNode node2 = new CallGraphNode("same.method()");
        CallGraphNode node3 = new CallGraphNode("different.method()");
        
        assertEquals(node1, node2);
        assertNotEquals(node1, node3);
        assertNotEquals(node1, null);
        assertNotEquals(node1, "string");
    }
    
    @Test
    @DisplayName("hashCode should be consistent with equals")
    void testHashCode() {
        CallGraphNode node1 = new CallGraphNode("same.method()");
        CallGraphNode node2 = new CallGraphNode("same.method()");
        
        assertEquals(node1.hashCode(), node2.hashCode());
    }
    
    @Test
    @DisplayName("copy should create node with same data")
    void testCopy() {
        CallGraphNode original = new CallGraphNode("original.method()");
        CallGraphNode copy = original.copy();
        
        assertEquals(original.getData(), copy.getData());
        assertNull(copy.getParent());
        assertTrue(copy.getChildren().isEmpty());
    }
    
    @Test
    @DisplayName("getStatistics should provide call graph metrics")
    void testGetStatistics() {
        String stats = rootNode.getStatistics();
        
        assertNotNull(stats);
        assertTrue(stats.contains("Unique Nodes"));
        assertTrue(stats.contains("Maximum Depth"));
        assertTrue(stats.contains("Leaf Nodes"));
    }
    
    @Test
    @DisplayName("Cycle detection should prevent infinite loops")
    void testCycleDetection() {
        // Create a cycle: A -> B -> C -> A
        CallGraphNode nodeA = new CallGraphNode("A");
        CallGraphNode nodeB = new CallGraphNode("B");
        CallGraphNode nodeC = new CallGraphNode("C");
        
        nodeA.addChild(nodeB);
        nodeB.addChild(nodeC);
        // This would create a cycle, but findLeafs should handle it
        nodeC.addChild(nodeA);
        
        // Should not cause infinite loop
        List<CallGraphNode> leafs = nodeA.findLeafs();
        assertNotNull(leafs);
        
        String prettyPrint = nodeA.prettyPrint(false);
        assertNotNull(prettyPrint);
    }
    
    @Test
    @DisplayName("Empty tree should handle operations gracefully")
    void testEmptyTree() {
        CallGraphNode emptyNode = new CallGraphNode("");
        
        assertTrue(emptyNode.isLeaf());
        assertEquals(0, emptyNode.getDepth());
        assertEquals(emptyNode, emptyNode.getRoot());
        
        List<CallGraphNode> leafs = emptyNode.findLeafs();
        assertEquals(1, leafs.size());
        assertEquals(emptyNode, leafs.get(0));
    }
}