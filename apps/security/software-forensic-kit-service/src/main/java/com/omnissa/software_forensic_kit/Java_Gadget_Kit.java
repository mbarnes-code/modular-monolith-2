package com.omnissa.software_forensic_kit;

import com.omnissa.software_forensic_kit.java_gadget.CallGraphAnalysis;
import com.omnissa.software_forensic_kit.java_gadget.local.LocalCalls;
import com.omnissa.software_forensic_kit.java_gadget.remote.RemoteCalls;
import org.apache.commons.cli.*;

import java.util.HashMap;
import java.util.Map;

/**
 * Software Forensic Kit - Main Entry Point
 * 
 * Binary analysis toolkit for identifying code reachability and function usage
 * in Java applications through callgraph analysis and dynamic injection.
 * 
 * @author Software Forensic Kit Team
 * @version 1.0.0
 */
public class Java_Gadget_Kit {
    
    private static final String VERSION = "1.0.0";
    private static final String DESCRIPTION = "Binary analysis toolkit for Java applications";
    
    /**
     * Main entry point for the Software Forensic Kit application.
     * 
     * @param args Command line arguments
     */
    public static void main(String[] args) {
        Options options = createOptions();
        CommandLineParser parser = new DefaultParser();
        HelpFormatter formatter = new HelpFormatter();
        
        try {
            CommandLine cmd = parser.parse(options, args);
            
            // Handle help option
            if (cmd.hasOption("help") || args.length == 0) {
                printHelp(formatter, options);
                return;
            }
            
            // Handle version option
            if (cmd.hasOption("version")) {
                System.out.println("Software Forensic Kit version " + VERSION);
                return;
            }
            
            // Validate required options
            validateRequiredOptions(cmd);
            
            // Build option map for analysis
            Map<String, String> optionMap = buildOptionMap(cmd);
            
            // Execute analysis based on mode (local or remote)
            if (cmd.hasOption("domain")) {
                executeRemoteAnalysis(optionMap);
            } else {
                executeLocalAnalysis(optionMap);
            }
            
        } catch (ParseException e) {
            System.err.println("Error parsing command line: " + e.getMessage());
            printHelp(formatter, options);
            System.exit(1);
        } catch (Exception e) {
            System.err.println("Error during analysis: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
    
    /**
     * Creates command line options configuration.
     */
    private static Options createOptions() {
        Options options = new Options();
        
        // Help and version
        options.addOption("h", "help", false, "Show this help message");
        options.addOption("v", "version", false, "Show version information");
        
        // Core analysis options
        options.addOption(Option.builder("s")
            .longOpt("searchFunction")
            .hasArg()
            .argName("PATTERN")
            .desc("Function to search for (supports wildcards, e.g., 'ExampleClass:function*')")
            .build());
            
        options.addOption(Option.builder("f")
            .longOpt("filter")
            .hasArg()
            .argName("PATH")
            .desc("JAR path filter to include specific files")
            .build());
            
        options.addOption(Option.builder("cd")
            .longOpt("depth")
            .hasArg()
            .argName("NUMBER")
            .type(Number.class)
            .desc("Maximum callgraph depth (default: 8)")
            .build());
        
        // Remote analysis options
        options.addOption(Option.builder("u")
            .longOpt("username")
            .hasArg()
            .argName("USERNAME")
            .desc("Remote server username")
            .build());
            
        options.addOption(Option.builder("p")
            .longOpt("password")
            .hasArg()
            .argName("PASSWORD")
            .desc("Remote server password")
            .build());
            
        options.addOption(Option.builder("d")
            .longOpt("domain")
            .hasArg()
            .argName("IP_ADDRESS")
            .desc("Remote server IP address")
            .build());
        
        // Output format options
        options.addOption("pp", "prettyPrint", false, "Pretty print output to console");
        options.addOption("hi", "html", false, "Generate HTML visualization output");
        options.addOption("g", "graphViz", false, "Generate GraphViz format output");
        
        options.addOption(Option.builder("o")
            .longOpt("output")
            .hasArg()
            .argName("DIRECTORY")
            .desc("Output directory for generated files")
            .build());
            
        // Advanced options
        options.addOption("rd", "removeDuplicates", false, "Remove duplicate paths in output");
        options.addOption("I", "interactive", false, "Interactive mode for parameter entry");
        
        return options;
    }
    
    /**
     * Validates required command line options.
     */
    private static void validateRequiredOptions(CommandLine cmd) throws ParseException {
        if (!cmd.hasOption("interactive")) {
            if (!cmd.hasOption("searchFunction")) {
                throw new ParseException("Missing required option: -s/--searchFunction");
            }
            if (!cmd.hasOption("filter")) {
                throw new ParseException("Missing required option: -f/--filter");
            }
            
            // Remote mode requires additional parameters
            if (cmd.hasOption("domain")) {
                if (!cmd.hasOption("username")) {
                    throw new ParseException("Remote mode requires username (-u/--username)");
                }
                if (!cmd.hasOption("password")) {
                    throw new ParseException("Remote mode requires password (-p/--password)");
                }
            }
        }
    }
    
    /**
     * Builds option map from command line arguments.
     */
    private static Map<String, String> buildOptionMap(CommandLine cmd) {
        Map<String, String> optionMap = new HashMap<>();
        
        // Core options
        if (cmd.hasOption("searchFunction")) {
            optionMap.put("searchFunction", cmd.getOptionValue("searchFunction"));
        }
        if (cmd.hasOption("filter")) {
            optionMap.put("filter", cmd.getOptionValue("filter"));
        }
        
        // Depth setting
        String depth = cmd.getOptionValue("depth", "8");
        optionMap.put("depth", depth);
        
        // Remote options
        if (cmd.hasOption("username")) {
            optionMap.put("username", cmd.getOptionValue("username"));
        }
        if (cmd.hasOption("password")) {
            optionMap.put("password", cmd.getOptionValue("password"));
        }
        if (cmd.hasOption("domain")) {
            optionMap.put("domain", cmd.getOptionValue("domain"));
        }
        
        // Output options
        optionMap.put("prettyPrint", Boolean.toString(cmd.hasOption("prettyPrint")));
        optionMap.put("html", Boolean.toString(cmd.hasOption("html")));
        optionMap.put("graphViz", Boolean.toString(cmd.hasOption("graphViz")));
        optionMap.put("removeDuplicates", Boolean.toString(cmd.hasOption("removeDuplicates")));
        
        if (cmd.hasOption("output")) {
            optionMap.put("output", cmd.getOptionValue("output"));
        }
        
        return optionMap;
    }
    
    /**
     * Executes local JAR analysis.
     */
    private static void executeLocalAnalysis(Map<String, String> optionMap) {
        System.out.println("Starting local analysis...");
        
        try {
            LocalCalls localAnalysis = new LocalCalls();
            localAnalysis.analyze(optionMap);
            
            System.out.println("Local analysis completed successfully.");
            
        } catch (Exception e) {
            throw new RuntimeException("Local analysis failed", e);
        }
    }
    
    /**
     * Executes remote JAR analysis via SSH.
     */
    private static void executeRemoteAnalysis(Map<String, String> optionMap) {
        System.out.println("Starting remote analysis...");
        
        try {
            RemoteCalls remoteAnalysis = new RemoteCalls();
            remoteAnalysis.analyze(optionMap);
            
            System.out.println("Remote analysis completed successfully.");
            
        } catch (Exception e) {
            throw new RuntimeException("Remote analysis failed", e);
        }
    }
    
    /**
     * Prints help message.
     */
    private static void printHelp(HelpFormatter formatter, Options options) {
        System.out.println("Software Forensic Kit v" + VERSION);
        System.out.println(DESCRIPTION);
        System.out.println();
        
        formatter.printHelp("java -jar software-forensic-kit.jar [OPTIONS]", options);
        
        System.out.println();
        System.out.println("Examples:");
        System.out.println("  Local Analysis:");
        System.out.println("    java -jar software-forensic-kit.jar -s \"ExampleClass:functionA\" -f \"/path/to/jars\" -pp");
        System.out.println();
        System.out.println("  Remote Analysis:");
        System.out.println("    java -jar software-forensic-kit.jar -u user -d 192.168.1.100 -p pass -s \"Class:method\" -f \"/remote/path\" -hi");
        System.out.println();
        System.out.println("  Java Agent Mode:");
        System.out.println("    java -javaagent:software-forensic-kit.jar=\"className;methodName\" [target-application]");
        System.out.println();
        System.out.println("For more information, visit: https://github.com/vmware/software-forensic-kit");
    }
}