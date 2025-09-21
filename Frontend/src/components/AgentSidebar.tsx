import { BarChart3, PenTool, Code, Database, Headphones, Search } from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "../components/ui/sidebar";

const categories = [
  { name: "Business Intelligence", count: 342, icon: BarChart3, color: "text-blue-400" },
  { name: "Content & Marketing", count: 486, icon: PenTool, color: "text-purple-400" },
  { name: "Development & Tech", count: 623, icon: Code, color: "text-green-400" },
  { name: "Data Analysis", count: 298, icon: Database, color: "text-orange-400" },
  { name: "Customer Support", count: 187, icon: Headphones, color: "text-pink-400" },
  { name: "Research & Strategy", count: 234, icon: Search, color: "text-cyan-400" },
];

const totalAgents = categories.reduce((sum, cat) => sum + cat.count, 0);

const AgentSidebar = () => {
  return (
    <Sidebar className="w-64 glass-card border-r border-border/50">
      <SidebarContent className="p-6">
        <SidebarGroup>
          <SidebarGroupLabel className="text-lg font-semibold text-foreground mb-6">
            Categories
          </SidebarGroupLabel>
          
          <SidebarGroupContent>
            <SidebarMenu className="space-y-2">
              {categories.map((category) => {
                const IconComponent = category.icon;
                return (
                  <SidebarMenuItem key={category.name}>
                    <SidebarMenuButton className="w-full justify-between p-3 rounded-lg hover:bg-muted/50 transition-colors group">
                      <div className="flex items-center gap-3">
                        <IconComponent className={`h-5 w-5 ${category.color}`} />
                        <span className="text-foreground group-hover:text-primary transition-colors">
                          {category.name}
                        </span>
                      </div>
                      <span className="text-sm text-muted-foreground font-medium">
                        {category.count}
                      </span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <div className="pt-4 border-t border-border/50 mt-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-gradient">
              {totalAgents.toLocaleString()}
            </div>
            <div className="text-sm text-muted-foreground">total agents</div>
          </div>
        </div>
      </SidebarContent>
    </Sidebar>
  );
};

export default AgentSidebar;
