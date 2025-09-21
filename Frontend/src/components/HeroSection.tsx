import { Button } from "../components/ui/button";
import { ArrowRight, Zap, Brain, TrendingUp, CheckCircle, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const HeroSection = () => {
  const { user } = useAuth();
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const features = [
    {
      icon: Brain,
      title: "Multi-Agent Collaboration",
      description: "Advanced AI agents work together seamlessly"
    },
    {
      icon: TrendingUp,
      title: "Real-Time Insights",
      description: "Live research and analysis streaming"
    },
    {
      icon: CheckCircle,
      title: "Enterprise Ready",
      description: "Professional-grade security and compliance"
    }
  ];

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-subtle">
      {/* Animated Background Elements */}
      <div className="absolute inset-0">
        {/* Primary gradient mesh */}
        <div className="absolute inset-0 bg-gradient-primary opacity-[0.02] animate-pulse-subtle"></div>

        {/* Floating orbs */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl animate-pulse-subtle" style={{ animationDelay: '1s' }}></div>
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-accent/5 rounded-full blur-3xl animate-pulse-subtle" style={{ animationDelay: '2s' }}></div>
        <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-secondary/5 rounded-full blur-3xl animate-pulse-subtle" style={{ animationDelay: '3s' }}></div>
      </div>

      <div className="container-professional text-center relative z-10 py-20">
        {/* Main Hero Content */}
        <div className="max-w-5xl mx-auto">
          {/* Badge */}
          <div className={`inline-flex items-center px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-8 transition-all duration-700 ${isVisible ? 'animate-fade-in-up' : 'opacity-0 translate-y-4'}`}>
            <Sparkles className="w-4 h-4 text-primary mr-2" />
            <span className="text-sm font-medium text-primary">Next-Generation AI Research Platform</span>
          </div>

          {/* Main Headline */}
          <h1 className={`text-display heading-premium text-gradient mb-6 transition-all duration-700 delay-100 ${isVisible ? 'animate-fade-in-up' : 'opacity-0 translate-y-4'}`}>
            Transform Marketing/Business Research with
            <br />
            <span className="text-gradient-subtle">Intelligent AI Agents</span>
          </h1>

          {/* Subheadline */}
          <p className={`text-body-lg text-premium text-muted-foreground mb-8 max-w-3xl mx-auto transition-all duration-700 delay-200 ${isVisible ? 'animate-fade-in-up' : 'opacity-0 translate-y-4'}`}>
            Experience the future of collaborative AI research. Our platform orchestrates multiple specialized agents
            that work together to deliver comprehensive insights, analysis, and solutions in real-time.
          </p>

          {/* CTA Buttons */}
          <div className={`flex flex-col sm:flex-row gap-4 justify-center mb-16 transition-all duration-700 delay-300 ${isVisible ? 'animate-fade-in-up' : 'opacity-0 translate-y-4'}`}>
            {user ? (
              <Link to="/dashboard">
                <Button className="bg-gradient-primary hover:shadow-xl hover:shadow-primary/25 btn-primary group text-lg px-8 py-4">
                  <Zap className="w-5 h-5 mr-2 group-hover:animate-pulse" />
                  Start Research
                  <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
                </Button>
              </Link>
            ) : (
              <>
                <Link to="/signup">
                  <Button className="bg-gradient-primary hover:shadow-xl hover:shadow-primary/25 btn-primary group text-lg px-8 py-4">
                    <Sparkles className="w-5 h-5 mr-2 group-hover:animate-pulse" />
                    Get Started Free
                    <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
                  </Button>
                </Link>
                <Link to="/professional-chat">
                  <Button variant="outline" className="glass-card-light hover:glass-card btn-secondary text-lg px-8 py-4">
                    <Brain className="w-5 h-5 mr-2" />
                    Watch Demo
                  </Button>
                </Link>
              </>
            )}
          </div>

          {/* Trust Indicators */}
          <div className={`flex flex-col sm:flex-row items-center justify-center gap-6 text-sm text-muted-foreground transition-all duration-700 delay-500 ${isVisible ? 'animate-fade-in-up' : 'opacity-0 translate-y-4'}`}>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-success" />
              <span>No credit card required</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-success" />
              <span>Enterprise-grade security</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-success" />
              <span>24/7 research capabilities</span>
            </div>
          </div>
        </div>

        {/* Feature Cards */}
        <div className={`grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto mt-20 transition-all duration-700 delay-700 ${isVisible ? 'animate-fade-in-up' : 'opacity-0 translate-y-4'}`}>
          {features.map((feature, index) => (
            <div
              key={feature.title}
              className="card-professional text-center group"
              style={{ animationDelay: `${800 + index * 100}ms` }}
            >
              <div className="w-12 h-12 bg-gradient-primary rounded-xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-heading font-semibold text-foreground mb-2">
                {feature.title}
              </h3>
              <p className="text-caption text-muted-foreground">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* Bottom CTA */}
        <div className={`mt-16 transition-all duration-700 delay-1000 ${isVisible ? 'animate-fade-in-up' : 'opacity-0 translate-y-4'}`}>
          <p className="text-micro text-muted-foreground mb-4">Trusted by researchers worldwide</p>
          <div className="flex items-center justify-center gap-8 opacity-60">
            <div className="h-8 w-24 bg-muted rounded animate-shimmer"></div>
            <div className="h-8 w-20 bg-muted rounded animate-shimmer"></div>
            <div className="h-8 w-28 bg-muted rounded animate-shimmer"></div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
