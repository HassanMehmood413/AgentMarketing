import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Brain, TrendingUp, Zap, CheckCircle, Star } from "lucide-react";

const AgentShowcase = () => {
  const agents = [
    {
      name: "Market Analyst",
      description: "Deep market research and competitive analysis",
      icon: TrendingUp,
      rating: 4.9,
      skills: ["Market Research", "Data Analysis", "Competitive Intelligence"],
      status: "online"
    },
    {
      name: "Content Creator",
      description: "AI-powered content generation and optimization",
      icon: Brain,
      rating: 4.8,
      skills: ["Copywriting", "SEO", "Content Strategy"],
      status: "online"
    },
    {
      name: "Strategy Advisor",
      description: "Business strategy and growth planning",
      icon: Zap,
      rating: 5.0,
      skills: ["Strategic Planning", "Market Analysis", "Growth Strategy"],
      status: "online"
    }
  ];

  return (
    <section className="py-16 px-4">
      <div className="container-professional">
        <div className="text-center mb-12">
          <h2 className="text-heading-xl heading-premium mb-4">
            Meet Our AI Agents
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Specialized AI agents that collaborate seamlessly to solve complex business challenges
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent, index) => (
            <Card key={index} className="glass-card hover:scale-105 transition-all duration-300">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-gradient-primary rounded-xl flex items-center justify-center">
                      <agent.icon className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <CardTitle className="text-lg">{agent.name}</CardTitle>
                      <div className="flex items-center space-x-1">
                        <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                        <span className="text-sm text-muted-foreground">{agent.rating}</span>
                      </div>
                    </div>
                  </div>
                  <Badge variant="success" className="text-xs">
                    <CheckCircle className="w-3 h-3 mr-1" />
                    {agent.status}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="mb-4">
                  {agent.description}
                </CardDescription>
                <div className="flex flex-wrap gap-2 mb-4">
                  {agent.skills.map((skill, skillIndex) => (
                    <Badge key={skillIndex} variant="secondary" className="text-xs">
                      {skill}
                    </Badge>
                  ))}
                </div>
                <Button className="w-full" variant="hero">
                  Hire Agent
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="text-center mt-12">
          <Button size="lg" variant="hero" className="px-8 py-3">
            View All Agents
          </Button>
        </div>
      </div>
    </section>
  );
};

export default AgentShowcase;
