import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { Star, Clock, CheckCircle2, Heart, Eye } from "lucide-react";
import { useState } from "react";

interface AgentCardProps {
  agent: {
    id: string;
    name: string;
    role: string;
    avatar: string;
    rating: number;
    reviews: number;
    price: number;
    responseTime: string;
    skills: string[];
    isOnline: boolean;
    isTopRated?: boolean;
  };
}

const AgentCard = ({ agent }: AgentCardProps) => {
  const [isFavorited, setIsFavorited] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      className="glass-card rounded-2xl p-6 hover:scale-105 transition-all duration-300 group relative overflow-hidden"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Top Rated Badge */}
      {agent.isTopRated && (
        <div className="absolute top-4 right-4 z-10">
          <Badge variant="secondary" className="bg-neon text-neon-foreground">
            Top Rated
          </Badge>
        </div>
      )}

      {/* Gradient Border Effect on Hover */}
      <div className="absolute inset-0 bg-gradient-to-r from-primary via-accent to-secondary opacity-0 group-hover:opacity-20 transition-opacity duration-300 rounded-2xl" />

      {/* Avatar Section */}
      <div className="flex items-start space-x-4 mb-4">
        <div className="relative">
          <img
            src={agent.avatar}
            alt={agent.name}
            className="w-16 h-16 rounded-full object-cover"
          />
          {agent.isOnline && (
            <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-success rounded-full border-2 border-card animate-pulse" />
          )}
        </div>
        
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-foreground mb-1">{agent.name}</h3>
          <p className="text-sm text-muted-foreground mb-2">{agent.role}</p>
          
          <div className="flex items-center space-x-2">
            <div className="flex items-center space-x-1">
              <Star className="h-4 w-4 text-yellow-400 fill-current" />
              <span className="text-sm font-medium">{agent.rating}</span>
            </div>
            <span className="text-xs text-muted-foreground">
              ({agent.reviews} reviews)
            </span>
          </div>
        </div>

        <Button
          variant="ghost"
          size="icon"
          className="opacity-0 group-hover:opacity-100 transition-opacity"
          onClick={() => setIsFavorited(!isFavorited)}
        >
          <Heart className={`h-4 w-4 ${isFavorited ? 'fill-neon text-neon' : 'text-muted-foreground'}`} />
        </Button>
      </div>

      {/* Response Time & Price */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-1 text-sm text-muted-foreground">
          <Clock className="h-4 w-4" />
          <span>{agent.responseTime}</span>
        </div>
        
        <div className="text-right">
          <div className="text-2xl font-bold text-gradient">${agent.price}</div>
          <div className="text-xs text-muted-foreground">per task</div>
        </div>
      </div>

      {/* Skills */}
      <div className="mb-4">
        <div className="flex flex-wrap gap-2">
          {agent.skills.slice(0, 3).map((skill, index) => (
            <Badge key={index} variant="outline" className="text-xs">
              {skill}
            </Badge>
          ))}
          {agent.skills.length > 3 && (
            <Badge variant="outline" className="text-xs">
              +{agent.skills.length - 3} more
            </Badge>
          )}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="space-y-2">
        <Button 
          variant="hero" 
          className="w-full group"
          size="sm"
        >
          Quick Hire
          <CheckCircle2 className="ml-2 h-4 w-4 transition-transform group-hover:scale-110" />
        </Button>
        
        {isHovered && (
          <Button 
            variant="outline" 
            className="w-full animate-fade-in"
            size="sm"
          >
            <Eye className="mr-2 h-4 w-4" />
            Preview Work
          </Button>
        )}
      </div>
    </div>
  );
};

export default AgentCard;
