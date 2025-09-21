import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { ScrollArea } from '../components/ui/scroll-area';
import { Badge } from '../components/ui/badge';
import { Terminal, Play, Square, RotateCcw, FileText } from 'lucide-react';
import { Button } from '../components/ui/button';

interface LogEntry {
  timestamp: string;
  level: 'info' | 'warn' | 'error' | 'debug';
  message: string;
  source?: string;
}

interface AgentLoggerProps {
  sessionId?: string;
  topic?: string;
  isRunning: boolean;
  onStart: (topic: string) => void;
  onStop: () => void;
  onClear: () => void;
}

interface ResearchResults {
  topic?: string;
  final_report?: string;
  introduction?: string;
  conclusion?: string;
  sections?: any[];
  analysts?: any[];
}

const AgentLogger: React.FC<AgentLoggerProps> = ({
  sessionId,
  topic = '',
  isRunning,
  onStart,
  onStop,
  onClear
}) => {

  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [researchResults, setResearchResults] = useState<ResearchResults | null>(null);
  const [showResults, setShowResults] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const eventSourceRef = useRef<EventSource | null>(null);
  const currentTextRef = useRef<string>(''); // Accumulate streaming text
  const textBufferRef = useRef<string>(''); // Buffer for chunking
  const intentionallyClosedRef = useRef<boolean>(false); // Track intentional closures

  useEffect(() => {
    // Auto-scroll to bottom when new logs arrive
    if (scrollAreaRef.current) {
      const scrollContainer = scrollAreaRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
      }
    }
  }, [logs]);

  // Cleanup effect when component unmounts
  useEffect(() => {
    return () => {
      // Flush any remaining buffered text
      if (currentTextRef.current.trim()) {
        setLogs(prev => [...prev, {
          timestamp: new Date().toISOString(),
          level: 'info',
          message: currentTextRef.current.trim(),
          source: 'research-agent'
        }]);
        currentTextRef.current = '';
      }
    };
  }, []);

  useEffect(() => {
    if (isRunning && sessionId) {
      // Reset the intentionally closed flag for new connections
      intentionallyClosedRef.current = false;

      // Get auth token from localStorage
      const token = localStorage.getItem('auth_token');

      // Connect to streaming endpoint with token
      const streamUrl = `http://127.0.0.1:8000/api/v1/research-stream?topic=${encodeURIComponent(topic)}&token=${token}&max_analysts=2`;
      console.log('Connecting to stream:', streamUrl); // Debug URL

      const eventSource = new EventSource(streamUrl);
      eventSourceRef.current = eventSource;

      // Add connection opened handler
      eventSource.onopen = () => {
        console.log('EventSource connected successfully');
        const connectLog: LogEntry = {
          timestamp: new Date().toISOString(),
          level: 'info',
          message: '≡ƒöù Connected to research agent stream',
          source: 'system'
        };
        setLogs(prev => [...prev, connectLog]);
      };

      eventSource.onmessage = (event) => {
        try {
          console.log('Raw event data:', event.data); // Debug logging

          // Handle Server-Sent Events format (data: {...})
          let eventDataStr = event.data;
          if (eventDataStr.startsWith('data: ')) {
            eventDataStr = eventDataStr.substring(6);
          }

          if (!eventDataStr.trim()) return; // Skip empty messages

          const data = JSON.parse(eventDataStr);
          console.log('Parsed event:', data); // Debug logging

          let message = '';
          let level: LogEntry['level'] = 'info';

          if (data.type === 'start') {
            message = `≡ƒÜÇ Starting research on "${data.topic || topic || 'topic'}"`;
          } else if (data.type === 'event') {
            // Extract actual content from LLM streaming events
            if (data.event === 'on_chat_model_stream') {
              try {
                // Parse the data to extract the actual text chunk
                const dataStr = data.data || '';
                const chunkMatch = dataStr.match(/content='([^']*)'/);
                if (chunkMatch && chunkMatch[1]) {
                  const chunk = chunkMatch[1];

                  // Accumulate the chunk
                  currentTextRef.current += chunk;

                  // Check if we should flush the buffer (sentence endings or length threshold)
                  const shouldFlush = (
                    chunk.includes('.') ||
                    chunk.includes('!') ||
                    chunk.includes('?') ||
                    chunk.includes('\n') ||
                    currentTextRef.current.length > 200 // Character limit
                  );

                  if (shouldFlush && currentTextRef.current.trim()) {
                    message = currentTextRef.current.trim();
                    currentTextRef.current = ''; // Reset buffer
                  } else {
                    return; // Don't show partial chunks yet
                  }
                } else {
                  return; // Skip if we can't extract content
                }
              } catch (e) {
                console.error('Failed to parse LLM chunk:', e);
                return;
              }
            } else {
              // Show other events with minimal indicators
              switch (data.event) {
                case 'on_chain_start':
                  // Flush any remaining text before showing status
                  if (currentTextRef.current.trim()) {
                    setLogs(prev => [...prev, {
                      timestamp: new Date().toISOString(),
                      level: 'info',
                      message: currentTextRef.current.trim(),
                      source: 'research-agent'
                    }]);
                    currentTextRef.current = '';
                  }
                  message = `≡ƒöä Starting research process...`;
                  break;
                case 'on_tool_start':
                  message = `≡ƒöì Searching for information...`;
                  break;
                case 'on_llm_start':
                  message = `≡ƒºá Analyzing and generating content...`;
                  break;
                case 'on_chain_end':
                  // Flush any remaining text
                  if (currentTextRef.current.trim()) {
                    setLogs(prev => [...prev, {
                      timestamp: new Date().toISOString(),
                      level: 'info',
                      message: currentTextRef.current.trim(),
                      source: 'research-agent'
                    }]);
                    currentTextRef.current = '';
                  }
                  message = `Γ£à Research phase completed`;
                  break;
                case 'on_tool_end':
                  message = `≡ƒôè Data gathered successfully`;
                  break;
                case 'on_llm_end':
                  // Flush any remaining text at the end of LLM generation
                  if (currentTextRef.current.trim()) {
                    setLogs(prev => [...prev, {
                      timestamp: new Date().toISOString(),
                      level: 'info',
                      message: currentTextRef.current.trim(),
                      source: 'research-agent'
                    }]);
                    currentTextRef.current = '';
                  }
                  message = `≡ƒÆí Analysis complete`;
                  break;
                default:
                  return; // Skip unknown events to reduce noise
              }
            }
          } else if (data.type === 'complete') {
            message = `≡ƒÄë Research completed successfully!`;
            level = 'info';


            // Store research results if available
            if (data.results) {
              setResearchResults(data.results);
            }

            // Mark as intentionally closed and stop
            intentionallyClosedRef.current = true;
            onStop();
          } else if (data.type === 'error') {
            message = `Γ¥î Research failed: ${data.error}`;
            level = 'error';
            // Close the EventSource to prevent reconnection on error
            if (eventSourceRef.current) {
              eventSourceRef.current.close();
              eventSourceRef.current = null;
            }
          } else {
            message = `≡ƒô¥ ${JSON.stringify(data)}`;
          }

          const logEntry: LogEntry = {
            timestamp: new Date().toISOString(),
            level: level,
            message: message,
            source: 'research-agent'
          };
          setLogs(prev => [...prev, logEntry]);
        } catch (error) {
          console.error('Failed to parse event data:', error, event.data);
          // Add error log for debugging
          const errorLog: LogEntry = {
            timestamp: new Date().toISOString(),
            level: 'error',
            message: `Failed to process agent message: ${event.data}`,
            source: 'system'
          };
          setLogs(prev => [...prev, errorLog]);
        }
      };

      eventSource.onerror = (error) => {
        console.error('EventSource error:', error);
        // Only show error if we didn't intentionally close the connection
        if (!intentionallyClosedRef.current && eventSourceRef.current && eventSourceRef.current.readyState !== EventSource.CLOSED) {
          const errorLog: LogEntry = {
            timestamp: new Date().toISOString(),
            level: 'error',
            message: 'Connection to agent stream lost',
            source: 'system'
          };
          setLogs(prev => [...prev, errorLog]);
        }
      };

      return () => {
        eventSource.close();
        // Flush any remaining buffered text when stopping
        if (currentTextRef.current.trim()) {
          setLogs(prev => [...prev, {
            timestamp: new Date().toISOString(),
            level: 'info',
            message: currentTextRef.current.trim(),
            source: 'research-agent'
          }]);
          currentTextRef.current = '';
        }
      };
    } else if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
  }, [isRunning, sessionId, topic]);

  const addLog = (message: string, level: LogEntry['level'] = 'info', source: string = 'system') => {
    const logEntry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      source
    };
    setLogs(prev => [...prev, logEntry]);
  };

  const handleStart = () => {
    if (!topic.trim()) {
      addLog('Please enter a research topic', 'error');
      return;
    }
    addLog(`Starting research on: "${topic}"`, 'info');
    onStart(topic);
  };

  const handleStop = () => {
    addLog('Stopping research session', 'warn');
    onStop();
  };

  const handleClear = () => {
    setLogs([]);
    setResearchResults(null);
    setShowResults(false);
    currentTextRef.current = ''; // Clear text buffer
    onClear();
  };

  const getLevelColor = (level: LogEntry['level']) => {
    switch (level) {
      case 'error': return 'destructive';
      case 'warn': return 'secondary';
      case 'debug': return 'outline';
      default: return 'default';
    }
  };

  // Function to process text and make URLs clickable
  const processLineWithLinks = (text: string): React.ReactNode => {
    // URL regex pattern - matches http://, https://, and www. URLs
    const urlRegex = /(https?:\/\/[^\s]+|www\.[^\s]+)/gi;

    // Split text by URLs and process each part
    const parts = text.split(urlRegex);

    return parts.map((part, index) => {
      if (urlRegex.test(part)) {
        // This is a URL, make it clickable
        const href = part.startsWith('http') ? part : `https://${part}`;
        return (
          <a
            key={index}
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary hover:text-primary/80 underline decoration-primary/50 hover:decoration-primary transition-colors duration-200 font-medium"
          >
            {part}
          </a>
        );
      } else {
        // This is regular text
        return part;
      }
    });
  };

  return (
    <Card className="glass-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Terminal className="h-5 w-5" />
          <span className="heading-premium">Agent Execution Logs</span>
          {sessionId && (
            <Badge variant="outline" className="ml-2">
              Session: {sessionId.slice(0, 8)}...
            </Badge>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* Controls */}
        <div className="flex gap-2 mb-4">
          {!isRunning ? (
            <>
              <Button onClick={handleStart} disabled={!topic.trim()}>
                <Play className="h-4 w-4 mr-2" />
                Start Research
              </Button>
              {researchResults ? (
                <Button
                  onClick={() => setShowResults(!showResults)}
                  className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover-lift"
                >
                  <FileText className="h-4 w-4 mr-2" />
                  {showResults ? 'Hide Report' : 'View Research Report'}
                  <svg className={`ml-2 h-4 w-4 transition-transform duration-300 ${showResults ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </Button>
              ) : (
                <div className="text-sm text-muted-foreground flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Waiting for research completion...
                </div>
              )}
            </>
          ) : (
            <Button onClick={handleStop} variant="destructive">
              <Square className="h-4 w-4 mr-2" />
              Stop Research
            </Button>
          )}
          <Button onClick={handleClear} variant="outline">
            <RotateCcw className="h-4 w-4 mr-2" />
            Clear Logs
          </Button>
        </div>

        {/* Logs Display */}
        <ScrollArea className="h-96 w-full rounded-md border border-[#7C3AED]/20 p-4" ref={scrollAreaRef}>
          {logs.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              <Terminal className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No logs yet. Start a research session to see agent activity.</p>
            </div>
          ) : (
            <div className="space-y-2">
              {logs.map((log, index) => (
                <div key={index} className="flex gap-3 text-sm">
                  <span className="text-gray-500 font-mono text-xs min-w-[100px]">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </span>
                  <Badge variant={getLevelColor(log.level)} className="min-w-[60px] justify-center">
                    {log.level.toUpperCase()}
                  </Badge>
                  {log.source && (
                    <Badge variant="outline" className="text-xs">
                      {log.source}
                    </Badge>
                  )}
                  <span className="flex-1 font-mono text-xs break-all">
                    {log.message}
                  </span>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>

        {/* Research Results */}
        {showResults && researchResults && (
            <div className="mt-8 border-t border-glass-border pt-8">
              {/* Header Section */}
              <div className="mb-8 text-center">
                <div className="w-16 h-16 bg-gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                  <FileText className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-heading-xl heading-premium text-gradient mb-2">
                  Research Report
                </h3>
                <p className="text-body text-muted-foreground max-w-md mx-auto">
                  Comprehensive analysis completed by AI agents
                </p>
                {researchResults.topic && (
                  <div className="mt-3 inline-flex items-center px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium">
                    Topic: {researchResults.topic.replace('\n', '')}
                  </div>
                )}
              </div>

              {/* Report Content */}
              <div className="space-y-6 max-h-[600px] overflow-y-auto pr-2 scrollbar-thin scrollbar-track-muted scrollbar-thumb-primary/20">
                {/* Introduction Section */}
                {researchResults.introduction && (
                  <div className="card-professional">
                    <div className="flex items-center gap-3 mb-4">
                      <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <h4 className="text-subheading font-semibold text-foreground heading-premium">Executive Summary</h4>
                    </div>
                    <div className="text-body text-premium whitespace-pre-wrap leading-relaxed pl-11">
                      {researchResults.introduction.split('\n').map((line: string, index: number) => (
                        <p key={index} className="mb-3 last:mb-0">
                          {processLineWithLinks(line)}
                        </p>
                      ))}
                    </div>
                  </div>
                )}

                {/* Main Report Section */}
                {researchResults.final_report && (
                  <div className="card-professional">
                    <div className="flex items-center gap-3 mb-4">
                      <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-emerald-500 rounded-lg flex items-center justify-center">
                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                      <h4 className="text-subheading font-semibold text-foreground heading-premium">Complete Analysis</h4>
                    </div>
                    <div className="text-body text-premium whitespace-pre-wrap leading-relaxed max-h-96 overflow-y-auto pl-11 scrollbar-thin scrollbar-track-muted scrollbar-thumb-primary/20">
                      <div className="prose prose-invert max-w-none">
                        {researchResults.final_report.split('\n').map((line: string, index: number) => {
                          // Add some formatting for headers and sections
                          if (line.startsWith('# ')) {
                            return <h1 key={index} className="text-heading-xl heading-premium text-gradient mt-6 mb-4 first:mt-0">{line.substring(2)}</h1>;
                          } else if (line.startsWith('## ')) {
                            return <h2 key={index} className="text-heading heading-premium text-foreground mt-5 mb-3">{line.substring(3)}</h2>;
                          } else if (line.startsWith('### ')) {
                            return <h3 key={index} className="text-subheading font-semibold text-foreground mt-4 mb-2">{line.substring(4)}</h3>;
                          } else if (line.trim() === '') {
                            return <br key={index} />;
                          } else {
                            // Process line for links and format as paragraph
                            const processedLine = processLineWithLinks(line);
                            return <p key={index} className="mb-3">{processedLine}</p>;
                          }
                        })}
                      </div>
                    </div>
                  </div>
                )}

                {/* Conclusion Section */}
                {researchResults.conclusion && (
                  <div className="card-professional">
                    <div className="flex items-center gap-3 mb-4">
                      <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <h4 className="text-subheading font-semibold text-foreground heading-premium">Key Findings & Conclusions</h4>
                    </div>
                    <div className="text-body text-premium whitespace-pre-wrap leading-relaxed pl-11">
                      {researchResults.conclusion.split('\n').map((line: string, index: number) => (
                        <p key={index} className="mb-3 last:mb-0">
                          {processLineWithLinks(line)}
                        </p>
                      ))}
                    </div>
                  </div>
                )}

                {/* Analysts Section */}
                {researchResults.analysts && researchResults.analysts.length > 0 && (
                  <div className="card-professional">
                    <div className="flex items-center gap-3 mb-4">
                      <div className="w-8 h-8 bg-gradient-to-br from-orange-500 to-red-500 rounded-lg flex items-center justify-center">
                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                      </div>
                      <h4 className="text-subheading font-semibold text-foreground heading-premium">Expert Analysis Team</h4>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pl-11">
                      {researchResults.analysts.map((analyst: any, index: number) => (
                        <div key={index} className="glass-card-light p-4 hover-lift transition-all duration-300">
                          <div className="flex items-center gap-3 mb-2">
                            <div className="w-10 h-10 bg-gradient-primary rounded-full flex items-center justify-center">
                              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                              </svg>
                            </div>
                            <div>
                              <div className="font-semibold text-foreground text-body">{analyst.name}</div>
                              <div className="text-sm text-primary font-medium">{analyst.role}</div>
                            </div>
                          </div>
                          <div className="text-caption text-muted-foreground">
                            {processLineWithLinks(analyst.affiliation)}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Footer */}
                <div className="text-center pt-6 border-t border-glass-border">
                  <p className="text-caption text-muted-foreground">
                    Research completed by Nexus AI Agent System ΓÇó {new Date().toLocaleDateString()}
                  </p>
                </div>
              </div>
            </div>
        )}

        {/* Status */}
        {isRunning && (
          <div className="mt-4 flex items-center gap-2 text-green-400">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-green-400"></div>
            <span className="text-sm">Agent is running...</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default AgentLogger;
