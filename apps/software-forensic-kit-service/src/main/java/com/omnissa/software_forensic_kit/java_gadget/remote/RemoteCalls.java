package com.omnissa.software_forensic_kit.java_gadget.remote;

import com.omnissa.software_forensic_kit.java_gadget.CallGraphAnalysis;
import com.jcraft.jsch.*;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Handles remote JAR file analysis operations via SSH/SFTP.
 * 
 * This class manages SSH connections, remote file discovery, file transfers,
 * and coordinates remote analysis execution.
 */
public class RemoteCalls {
    
    private Session session;
    private ChannelSftp sftpChannel;
    
    /**
     * Executes remote JAR analysis based on provided configuration.
     * 
     * @param optionMap Configuration options including SSH credentials
     * @throws Exception If remote analysis fails
     */
    public void analyze(Map<String, String> optionMap) throws Exception {
        String username = optionMap.get("username");
        String password = optionMap.get("password");
        String domain = optionMap.get("domain");
        String filter = optionMap.get("filter");
        
        if (username == null || password == null || domain == null || filter == null) {
            throw new IllegalArgumentException("Remote analysis requires username, password, domain, and filter");
        }
        
        try {
            // Establish SSH connection
            System.out.println("Connecting to remote server: " + domain);
            connect(username, password, domain);
            
            // Discover remote JAR files
            System.out.println("Discovering remote JAR files with filter: " + filter);
            List<String> remoteJarFiles = findRemoteJarFiles(filter);
            
            if (remoteJarFiles.isEmpty()) {
                System.out.println("No JAR files found on remote server matching filter: " + filter);
                return;
            }
            
            System.out.println("Found " + remoteJarFiles.size() + " JAR files to analyze on remote server");
            
            // Process each remote JAR file
            for (String remoteJarFile : remoteJarFiles) {
                try {
                    analyzeRemoteJar(remoteJarFile, optionMap);
                } catch (Exception e) {
                    System.err.println("Failed to analyze remote JAR " + remoteJarFile + ": " + e.getMessage());
                    // Continue with next JAR file
                }
            }
            
        } finally {
            // Clean up connections
            disconnect();
        }
    }
    
    /**
     * Establishes SSH connection to remote server.
     * 
     * @param username SSH username
     * @param password SSH password
     * @param host Remote host IP address
     * @throws Exception If connection fails
     */
    public void connect(String username, String password, String host) throws Exception {
        try {
            JSch jsch = new JSch();
            
            // Create session
            session = jsch.getSession(username, host, 22);
            session.setPassword(password);
            
            // Disable strict host key checking (security risk - should be configurable)
            session.setConfig("StrictHostKeyChecking", "no");
            
            // Set connection timeout
            session.setTimeout(30000); // 30 seconds
            
            // Connect
            session.connect();
            
            System.out.println("SSH connection established to " + host);
            
            // Open SFTP channel for file operations
            Channel channel = session.openChannel("sftp");
            channel.connect();
            sftpChannel = (ChannelSftp) channel;
            
            System.out.println("SFTP channel opened");
            
        } catch (JSchException e) {
            throw new Exception("Failed to connect to remote server: " + e.getMessage(), e);
        }
    }
    
    /**
     * Disconnects from remote server and cleans up resources.
     */
    public void disconnect() {
        try {
            if (sftpChannel != null && sftpChannel.isConnected()) {
                sftpChannel.disconnect();
                System.out.println("SFTP channel disconnected");
            }
            
            if (session != null && session.isConnected()) {
                session.disconnect();
                System.out.println("SSH session disconnected");
            }
            
        } catch (Exception e) {
            System.err.println("Error during disconnect: " + e.getMessage());
        }
    }
    
    /**
     * Discovers JAR files on remote server matching the filter pattern.
     * 
     * @param filter Remote path filter
     * @return List of remote JAR file paths
     * @throws Exception If remote file discovery fails
     */
    public List<String> findRemoteJarFiles(String filter) throws Exception {
        List<String> jarFiles = new ArrayList<>();
        
        try {
            // Execute remote find command to locate JAR files
            String findCommand = "find " + filter + " -name '*.jar' -type f 2>/dev/null";
            String result = executeRemoteCommand(findCommand);
            
            if (result != null && !result.trim().isEmpty()) {
                String[] lines = result.split("\\n");
                for (String line : lines) {
                    String jarPath = line.trim();
                    if (!jarPath.isEmpty() && jarPath.endsWith(".jar")) {
                        jarFiles.add(jarPath);
                    }
                }
            }
            
        } catch (Exception e) {
            System.err.println("Error discovering remote JAR files: " + e.getMessage());
        }
        
        return jarFiles;
    }
    
    /**
     * Executes a command on the remote server and returns the output.
     * 
     * @param command Command to execute
     * @return Command output as string
     * @throws Exception If command execution fails
     */
    public String executeRemoteCommand(String command) throws Exception {
        Channel channel = null;
        StringBuilder output = new StringBuilder();
        
        try {
            channel = session.openChannel("exec");
            ((ChannelExec) channel).setCommand(command);
            
            InputStream in = channel.getInputStream();
            channel.connect();
            
            byte[] buffer = new byte[1024];
            while (true) {
                while (in.available() > 0) {
                    int bytesRead = in.read(buffer, 0, 1024);
                    if (bytesRead < 0) break;
                    output.append(new String(buffer, 0, bytesRead));
                }
                
                if (channel.isClosed()) {
                    if (in.available() > 0) continue;
                    break;
                }
                
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
            
        } finally {
            if (channel != null) {
                channel.disconnect();
            }
        }
        
        return output.toString();
    }
    
    /**
     * Analyzes a remote JAR file by downloading it and performing local analysis.
     * 
     * @param remoteJarPath Path to JAR file on remote server
     * @param optionMap Analysis configuration options
     * @throws Exception If analysis fails
     */
    private void analyzeRemoteJar(String remoteJarPath, Map<String, String> optionMap) throws Exception {
        String localTempPath = null;
        
        try {
            // Download JAR file to local temporary location
            System.out.println("Downloading remote JAR: " + remoteJarPath);
            localTempPath = downloadRemoteJar(remoteJarPath);
            
            // Perform local analysis on downloaded JAR
            System.out.println("Analyzing downloaded JAR: " + localTempPath);
            CallGraphAnalysis analysis = new CallGraphAnalysis(localTempPath, optionMap);
            analysis.run();
            
        } finally {
            // Clean up temporary file
            if (localTempPath != null) {
                try {
                    File tempFile = new File(localTempPath);
                    if (tempFile.exists()) {
                        tempFile.delete();
                        System.out.println("Cleaned up temporary file: " + localTempPath);
                    }
                } catch (Exception e) {
                    System.err.println("Failed to clean up temporary file: " + e.getMessage());
                }
            }
        }
    }
    
    /**
     * Downloads a remote JAR file to local temporary storage.
     * 
     * @param remoteJarPath Path to JAR file on remote server
     * @return Path to local temporary file
     * @throws Exception If download fails
     */
    private String downloadRemoteJar(String remoteJarPath) throws Exception {
        try {
            // Create local temporary file
            String fileName = new File(remoteJarPath).getName();
            File localTempFile = File.createTempFile("remote-jar-", "-" + fileName);
            String localPath = localTempFile.getAbsolutePath();
            
            // Download via SFTP
            sftpChannel.get(remoteJarPath, new FileOutputStream(localTempFile));
            
            System.out.println("Downloaded " + remoteJarPath + " to " + localPath);
            return localPath;
            
        } catch (SftpException e) {
            throw new Exception("Failed to download remote JAR: " + e.getMessage(), e);
        }
    }
    
    /**
     * Checks if remote server connection is active.
     * 
     * @return true if connected, false otherwise
     */
    public boolean isConnected() {
        return session != null && session.isConnected() && 
               sftpChannel != null && sftpChannel.isConnected();
    }
    
    /**
     * Gets remote file size for a JAR file.
     * 
     * @param remoteJarPath Path to remote JAR file
     * @return File size in bytes, or -1 if error
     */
    public long getRemoteFileSize(String remoteJarPath) {
        try {
            SftpATTRS attrs = sftpChannel.stat(remoteJarPath);
            return attrs.getSize();
        } catch (Exception e) {
            System.err.println("Failed to get remote file size: " + e.getMessage());
            return -1;
        }
    }
    
    /**
     * Tests remote connection with a simple command.
     * 
     * @return true if connection test succeeds
     */
    public boolean testConnection() {
        try {
            String result = executeRemoteCommand("echo 'connection test'");
            return result.contains("connection test");
        } catch (Exception e) {
            System.err.println("Connection test failed: " + e.getMessage());
            return false;
        }
    }
}