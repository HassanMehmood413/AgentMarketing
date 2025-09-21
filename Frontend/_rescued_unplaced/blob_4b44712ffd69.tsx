import AgentCard from "./AgentCard";

const featuredAgents = [
  {
    id: "1",
    name: "Alex Chen",
    role: "Business Intelligence Specialist",
    avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
    rating: 4.9,
    reviews: 127,
    price: 89,
    responseTime: "2 min",
    skills: ["Data Analysis", "Market Research", "Excel Automation", "Power BI", "SQL"],
    isOnline: true,
    isTopRated: true,
  },
  {
    id: "2",
    name: "Sarah Kim",
    role: "Content Creation Expert",
    avatar: "https://images.unsplash.com/photo-1494790108755-2616b332c5d4?w=150&h=150&fit=crop&crop=face",
    rating: 4.8,
    reviews: 89,
    price: 65,
    responseTime: "5 min",
    skills: ["Copywriting", "SEO", "Social Media", "Brand Strategy"],
    isOnline: true,
  },
  {
    id: "3",
    name: "Marcus Johnson",
    role: "Development Automation",
    avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
    rating: 4.9,
    reviews: 156,
    price: 120,
    responseTime: "1 min",
    skills: ["Python", "API Integration", "DevOps", "Cloud Computing"],
    isOnline: false,
    isTopRated: true,
  },
];

const AgentShowcase = () => {
  return (
    <section className="py-24 px-4 lg:px-8">
      <div className="container mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-heading text-gradient mb-4">
            Meet Elite AI Agents
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Handpicked specialists ready to tackle your most complex challenges with precision and speed
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          {featuredAgents.map((agent) => (
            <AgentCard key={agent.id} agent={agent} />
          ))}
        </div>

        <div className="text-center mt-12">
          <p className="text-muted-foreground mb-6">
            Ready to find your perfect agent match?
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="px-8 py-3 bg-gradient-to-r from-primary to-accent text-white rounded-xl font-semibold hover:scale-105 transition-transform duration-300">
              Browse All Agents
            </button>
            <button className="px-8 py-3 glass-card text-white rounded-xl font-semibold hover:bg-white/10 transition-colors duration-300">
              Create Custom Team
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AgentShowcase;
