import { Button } from "../components/ui/button";
import { Search, Sparkles, Target, Zap, Lightbulb, TrendingUp } from "lucide-react";
import { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "./ui/use-toast";
import AgentLogger from "./AgentLogger";

const SearchBar = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  const [searchQuery, setSearchQuery] = useState("");
  const [maxAnalysts, setMaxAnalysts] = useState(2);
  const [isAgentRunning, setIsAgentRunning] = useState(false);
  const [currentSessionId, setCurrentSessionId] = useState<string>();
  const [isFocused, setIsFocused] = useState(false);

  const researchTemplates = [
    {
      icon: Target,
      title: "Market Analysis",
      query: "comprehensive market analysis for [industry]",
      description: "Deep market insights and competitive landscape"
    },
    {
      icon: TrendingUp,
      title: "Business Strategy",
      query: "strategic business analysis for [company/product]",
      description: "Strategic recommendations and growth opportunities"
    },
    {
      icon: Lightbulb,
      title: "Innovation Research",
      query: "emerging trends and innovations in [field]",
      description: "Cutting-edge developments and future predictions"
    },
    {
      icon: Zap,
      title: "Competitive Intelligence",
      query: "competitive analysis of [company] in [market]",
      description: "Competitor strategies and market positioning"
    }
  ];

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      toast({
        title: "Empty Query",
        description: "Please enter a research topic",
        variant: "destructive",
      });
      return;
    }

    if (!user) {
      toast({
        title: "Authentication Required",
        description: "Please login to use the research agent",
        variant: "destructive",
      });
      return;
    }

    // Generate session ID and start immediately
    const sessionId = `session-${Date.now()}`;
    setCurrentSessionId(sessionId);
    setIsAgentRunning(true);

    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch('http://127.0.0.1:8000/api/v1/run-research', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          topic: searchQuery,
          max_analysts: maxAnalysts,
          session_id: sessionId
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Research failed');
      }

      const result = await response.json();

      toast({
        title: "Research Started",
        description: result.message,
      });

    } catch (error) {
      toast({
        title: "Research Failed",
        description: error instanceof Error ? error.message : "Unknown error",
        variant: "destructive",
      });
      setIsAgentRunning(false);
      setCurrentSessionId(undefined);
    }
  };

  const handleTemplateClick = (template: typeof researchTemplates[0]) => {
    setSearchQuery(template.query);
  };

  const handleAgentStop = () => {
    setIsAgentRunning(false);
    // Don't clear currentSessionId - we need it to keep results visible
  };

         const handleAgentClear = () => {
           setIsAgentRunning(false);
           setCurrentSessionId(undefined);
           setSearchQuery("");
         };

  if (!user) {
    return (
      <section className="py-20 px-4">
        <div className="container-professional">
          <div className="max-w-2xl mx-auto text-center">
            <div className="w-16 h-16 bg-gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-6">
              <Search className="w-8 h-8 text-white" />
            </div>
            <h2 className="text-heading-xl font-bold text-foreground mb-4">
              Start Your Research Journey
            </h2>
            <p className="text-body text-muted-foreground mb-8">
              Join thousands of researchers using our AI-powered platform for comprehensive analysis and insights.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button className="bg-gradient-primary btn-primary">
                Sign Up Free
              </Button>
              <Button variant="outline" className="glass-card-light btn-secondary">
                Watch Demo
              </Button>
            </div>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-20 px-4 bg-gradient-subtle">
      <div className="container-professional">
        {/* Research Templates */}
        <div className="max-w-6xl mx-auto mb-12">
          <div className="text-center mb-8">
            <h2 className="text-heading-xl heading-premium text-foreground mb-4">
              Choose Your Research Focus
            </h2>
            <p className="text-body text-premium text-muted-foreground max-w-2xl mx-auto">
              Select a research template or enter your own query to get started with AI-powered analysis
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {researchTemplates.map((template, index) => (
              <button
                key={template.title}
                onClick={() => handleTemplateClick(template)}
                className="card-professional text-left group hover-lift"
              >
                <div className="w-10 h-10 bg-gradient-primary rounded-lg flex items-center justify-center mb-3 group-hover:scale-110 transition-transform duration-300">
                  <template.icon className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-subheading font-semibold text-foreground mb-1">
                  {template.title}
                </h3>
                <p className="text-caption text-muted-foreground">
                  {template.description}
                </p>
              </button>
            ))}
          </div>
        </div>

        {/* Main Search Interface */}
        <div className="max-w-4xl mx-auto">
          <div className="card-professional">
            <div className="p-8">
            <div className="text-center mb-8">
              <h3 className="text-heading heading-premium text-foreground mb-2">
                Custom Research Query
              </h3>
              <p className="text-caption text-premium text-muted-foreground">
                Describe your research needs in detail for the best results
              </p>
            </div>

              {/* Search Input */}
              <div className="relative mb-6">
                <div className={`relative transition-all duration-300 ${isFocused ? 'ring-2 ring-primary/50' : ''}`}>
                  <Search className="absolute left-4 top-4 w-5 h-5 text-muted-foreground" />
                  <textarea
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setIsFocused(false)}
                    placeholder="e.g., 'Analyze the competitive landscape for electric vehicles in the US market, including key players, market share, and future trends'"
                    className="input-primary w-full pl-12 pr-4 py-4 text-body resize-none rounded-xl min-h-[100px] placeholder:text-muted-foreground/60"
                    disabled={isAgentRunning}
                  />
                </div>
                     </div>

                     {/* Analyst Configuration */}
                     <div className="mt-6 p-4 bg-muted/20 rounded-xl border border-muted/30">
                       <div className="flex items-center justify-between mb-3">
                         <label className="text-sm font-medium text-foreground flex items-center gap-2">
                           <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                           </svg>
                           Number of Analysts
                         </label>
                         <span className="text-sm font-semibold text-primary bg-primary/10 px-2 py-1 rounded-md">
                           {maxAnalysts}
                         </span>
                       </div>

                       <div className="space-y-2">
                         <input
                           type="range"
                           min="1"
                           max="5"
                           value={maxAnalysts}
                           onChange={(e) => setMaxAnalysts(parseInt(e.target.value))}
                           className="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer slider-primary"
                           disabled={isAgentRunning}
                         />
                         <div className="flex justify-between text-xs text-muted-foreground">
                           <span>1</span>
                           <span>2</span>
                           <span>3</span>
                           <span>4</span>
                           <span>5</span>
                         </div>
                       </div>

                       <p className="text-xs text-muted-foreground mt-2">
                         More analysts provide deeper analysis but take longer to complete
                       </p>
                     </div>

                     {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button
                  onClick={handleSearch}
                  disabled={isAgentRunning || !searchQuery.trim()}
                  className="bg-gradient-primary hover:shadow-xl hover:shadow-primary/25 btn-primary group flex-1 sm:flex-none"
                >
                  {isAgentRunning ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Research in Progress...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5 mr-2 group-hover:animate-pulse" />
                      Start Research
                    </>
                  )}
                </Button>

                {isAgentRunning && (
                  <Button
                    onClick={handleAgentStop}
                    variant="outline"
                    className="glass-card-light hover:bg-destructive/10 hover:text-destructive btn-secondary"
                  >
                    Stop Research
                  </Button>
                )}
              </div>

              {/* Status */}
              {isAgentRunning && (
                <div className="mt-6 text-center">
                  <div className="inline-flex items-center px-4 py-2 rounded-full bg-primary/10 border border-primary/20">
                    <div className="animate-pulse w-2 h-2 bg-primary rounded-full mr-3"></div>
                    <span className="text-sm font-medium text-primary">
                      AI agents are analyzing your query...
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Agent Logger */}
        {(isAgentRunning || currentSessionId) && (
          <div className="max-w-4xl mx-auto mt-8">
            <AgentLogger
              sessionId={currentSessionId}
              topic={searchQuery}
              isRunning={isAgentRunning}
              onStart={() => {}}
              onStop={handleAgentStop}
              onClear={handleAgentClear}
            />
          </div>
        )}
      </div>
    </section>
  );
};

export default SearchBar;
