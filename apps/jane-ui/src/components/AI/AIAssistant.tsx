'use client';

import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Textarea } from '@/components/ui/textarea';
import { useToast } from '@/hooks/use-toast';
import { Bot, Loader2, Maximize2, Minimize2, Send, User } from 'lucide-react';
import React, { useEffect, useRef, useState } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  context?: string[];
  tools?: string[];
}

interface AIAssistantProps {
  className?: string;
  isExpanded?: boolean;
  onToggleExpand?: () => void;
  activeTool?: string;
  activeContext?: string[];
}

export function AIAssistant({
  className = '',
  isExpanded = false,
  onToggleExpand,
  activeTool,
  activeContext = []
}: AIAssistantProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [contextVisible, setContextVisible] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { toast } = useToast();

  // Executive function accommodation: Auto-scroll to new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Executive function accommodation: Auto-focus input with delay
  useEffect(() => {
    if (!isLoading) {
      const timer = setTimeout(() => {
        textareaRef.current?.focus();
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [isLoading]);

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
      context: activeContext,
      tools: activeTool ? [activeTool] : undefined
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input.trim(),
          context: activeContext,
          activeTool,
          history: messages.slice(-10) // Send last 10 messages for context
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get AI response');
      }

      const data = await response.json();
      
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        context: data.usedContext,
        tools: data.suggestedTools
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('AI Assistant error:', error);
      toast({
        title: 'AI Assistant Error',
        description: 'Failed to get response. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    // Executive function accommodation: Ctrl+Enter to send (accessible alternative)
    if (e.key === 'Enter') {
      if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
        handleSendMessage();
      } else if (!e.shiftKey) {
        // Regular Enter sends message unless Shift is held (for multi-line)
        e.preventDefault();
        handleSendMessage();
      }
    }
  };

  const formatMessage = (content: string) => {
    // Executive function accommodation: Highlight important information
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-blue-600">$1</strong>')
      .replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')
      .replace(/`(.*?)`/g, '<code class="bg-gray-100 px-1 py-0.5 rounded text-sm font-mono">$1</code>');
  };

  return (
    <Card className={`flex flex-col ${className} ${isExpanded ? 'h-[600px]' : 'h-[400px]'}`}>
      <CardHeader className="flex-shrink-0 pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2 text-lg">
            <Bot className="h-5 w-5 text-blue-600" />
            AI Assistant
            {activeTool && (
              <Badge variant="outline" className="text-xs">
                {activeTool}
              </Badge>
            )}
          </CardTitle>
          <div className="flex items-center gap-2">
            {/* Context visibility toggle */}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setContextVisible(!contextVisible)}
              className="text-xs"
            >
              Context {contextVisible ? 'ON' : 'OFF'}
            </Button>
            {/* Expand/minimize toggle */}
            {onToggleExpand && (
              <Button
                variant="ghost"
                size="sm"
                onClick={onToggleExpand}
                aria-label={isExpanded ? 'Minimize assistant' : 'Expand assistant'}
              >
                {isExpanded ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
              </Button>
            )}
          </div>
        </div>
        
        {/* Context indicators - Executive function accommodation */}
        {contextVisible && activeContext.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-2">
            <span className="text-xs text-gray-600 mr-2">Context:</span>
            {activeContext.map((ctx, index) => (
              <Badge 
                key={index} 
                variant="secondary" 
                className="text-xs bg-blue-50 text-blue-700"
              >
                {ctx}
              </Badge>
            ))}
          </div>
        )}
      </CardHeader>

      <CardContent className="flex-1 flex flex-col min-h-0 p-0">
        {/* Messages area */}
        <ScrollArea className="flex-1 px-4">
          <div className="space-y-4 pb-4">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 py-8">
                <Bot className="h-12 w-12 mx-auto mb-3 text-gray-300" />
                <p className="text-sm">
                  Hi! I'm your AI assistant for executive function support.
                  I can help you break down tasks, manage workflows, and navigate between tools.
                </p>
                <p className="text-xs mt-2 text-gray-400">
                  Tip: Use Ctrl+Enter or just Enter to send messages
                </p>
              </div>
            )}
            
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                {message.role === 'assistant' && (
                  <div className="flex-shrink-0">
                    <Bot className="h-6 w-6 text-blue-600 mt-1" />
                  </div>
                )}
                
                <div
                  className={`max-w-[80%] rounded-lg px-3 py-2 text-sm ${
                    message.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <div 
                    dangerouslySetInnerHTML={{ 
                      __html: formatMessage(message.content) 
                    }} 
                  />
                  
                  {/* Tool suggestions */}
                  {message.tools && message.tools.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-opacity-20 border-gray-300">
                      <div className="flex flex-wrap gap-1">
                        <span className="text-xs opacity-75">Suggested tools:</span>
                        {message.tools.map((tool, index) => (
                          <Badge 
                            key={index} 
                            variant="outline" 
                            className="text-xs"
                          >
                            {tool}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  <div className="text-xs opacity-60 mt-1">
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                </div>
                
                {message.role === 'user' && (
                  <div className="flex-shrink-0">
                    <User className="h-6 w-6 text-gray-600 mt-1" />
                  </div>
                )}
              </div>
            ))}
            
            {isLoading && (
              <div className="flex justify-start gap-3">
                <Bot className="h-6 w-6 text-blue-600 mt-1" />
                <div className="bg-gray-100 rounded-lg px-3 py-2 flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-sm text-gray-600">Thinking...</span>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>

        {/* Input area */}
        <div className="flex-shrink-0 p-4 border-t">
          <div className="flex gap-2">
            <Textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Ask me anything about your tasks or tools..."
              className="min-h-[44px] max-h-[120px] resize-none"
              disabled={isLoading}
              rows={1}
            />
            <Button
              onClick={handleSendMessage}
              disabled={!input.trim() || isLoading}
              size="sm"
              className="px-3"
              aria-label="Send message"
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </div>
          
          {/* Executive function accommodation: Input hints */}
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>Enter to send • Shift+Enter for new line</span>
            <span>{input.length}/1000</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default AIAssistant;