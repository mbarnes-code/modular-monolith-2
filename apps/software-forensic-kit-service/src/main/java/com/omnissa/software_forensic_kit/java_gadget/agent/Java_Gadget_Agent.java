package com.omnissa.software_forensic_kit.java_gadget.agent;

import java.lang.instrument.Instrumentation;
import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.IllegalClassFormatException;
import java.security.ProtectionDomain;

/**
 * Java Agent for runtime bytecode instrumentation and method interception.
 * 
 * This agent can be attached to running Java applications to monitor specific
 * method calls and provide runtime execution details for security analysis.
 */
public class Java_Gadget_Agent {
    
    private static Instrumentation instrumentation;
    private static String agentArgs;
    
    /**
     * Premain method called when agent is loaded at JVM startup.
     * 
     * @param args Agent arguments in format "className;methodName" or "class1;method1~class2;method2"
     * @param inst Instrumentation interface provided by JVM
     */
    public static void premain(String args, Instrumentation inst) {
        System.out.println("Software Forensic Kit Agent starting...");
        
        instrumentation = inst;
        agentArgs = args;
        
        if (args == null || args.trim().isEmpty()) {
            System.err.println("Agent requires arguments in format: className;methodName");
            return;
        }
        
        try {
            setupInstrumentation(args);
            System.out.println("Agent instrumentation setup complete");
            
        } catch (Exception e) {
            System.err.println("Agent initialization failed: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Agentmain method called when agent is attached to running JVM.
     * 
     * @param args Agent arguments
     * @param inst Instrumentation interface
     */
    public static void agentmain(String args, Instrumentation inst) {
        System.out.println("Software Forensic Kit Agent attaching to running JVM...");
        premain(args, inst);
    }
    
    /**
     * Sets up instrumentation for specified classes and methods.
     * 
     * @param args Agent arguments specifying target classes and methods
     */
    private static void setupInstrumentation(String args) {
        String[] targets = args.split("~");
        
        for (String target : targets) {
            String[] parts = target.split(";");
            if (parts.length != 2) {
                System.err.println("Invalid target format: " + target + " (expected: className;methodName)");
                continue;
            }
            
            String className = parts[0].trim();
            String methodName = parts[1].trim();
            
            try {
                setupClassInstrumentation(className, methodName);
            } catch (Exception e) {
                System.err.println("Failed to setup instrumentation for " + className + ":" + methodName + " - " + e.getMessage());
            }
        }
    }
    
    /**
     * Sets up instrumentation for a specific class and method.
     * 
     * @param className Target class name
     * @param methodName Target method name
     */
    private static void setupClassInstrumentation(String className, String methodName) {
        System.out.println("Setting up instrumentation for " + className + ":" + methodName);
        
        // Create transformer for this class/method combination
        ClassFileTransformer transformer = new Java_Gadget_AgentTransformer(className, methodName);
        
        // Add transformer to instrumentation
        instrumentation.addTransformer(transformer, true);
        
        // Try to retransform already loaded classes
        try {
            Class<?>[] loadedClasses = instrumentation.getAllLoadedClasses();
            for (Class<?> clazz : loadedClasses) {
                if (clazz.getName().equals(className) && instrumentation.isModifiableClass(clazz)) {
                    System.out.println("Retransforming already loaded class: " + className);
                    instrumentation.retransformClasses(clazz);
                }
            }
        } catch (Exception e) {
            System.err.println("Failed to retransform classes: " + e.getMessage());
        }
    }
    
    /**
     * Gets the instrumentation instance.
     * 
     * @return Instrumentation interface
     */
    public static Instrumentation getInstrumentation() {
        return instrumentation;
    }
    
    /**
     * Gets the agent arguments.
     * 
     * @return Agent arguments string
     */
    public static String getAgentArgs() {
        return agentArgs;
    }
}

/**
 * ClassFileTransformer implementation for method interception.
 */
class Java_Gadget_AgentTransformer implements ClassFileTransformer {
    
    private final String targetClassName;
    private final String targetMethodName;
    
    public Java_Gadget_AgentTransformer(String className, String methodName) {
        this.targetClassName = className;
        this.targetMethodName = methodName;
    }
    
    @Override
    public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined,
                          ProtectionDomain protectionDomain, byte[] classfileBuffer) 
                          throws IllegalClassFormatException {
        
        // Convert internal class name format to standard format
        String normalizedClassName = className.replace('/', '.');
        
        if (!normalizedClassName.equals(targetClassName)) {
            return null; // No transformation needed
        }
        
        try {
            System.out.println("Transforming class: " + normalizedClassName + " for method: " + targetMethodName);
            
            // TODO: Implement actual bytecode transformation using ASM
            // This would involve:
            // 1. Parse existing bytecode using ASM ClassReader
            // 2. Locate target method
            // 3. Inject monitoring code at method entry/exit
            // 4. Return modified bytecode
            
            // For now, just log the transformation attempt
            System.out.println("Bytecode transformation not yet implemented - method monitoring will not be active");
            
            return null; // Return null = no transformation
            
        } catch (Exception e) {
            System.err.println("Transformation failed for " + normalizedClassName + ": " + e.getMessage());
            return null;
        }
    }
}