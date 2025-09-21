import { useState } from "react";
import Header from "../components/Header";
import HeroSection from "../components/HeroSection";
import SearchBar from "../components/SearchBar";
import AgentShowcase from "../components/AgentShowcase";
import AgentSidebar from "../components/AgentSidebar";
import { SidebarProvider, SidebarTrigger } from "../components/ui/sidebar";
import { Button } from "../components/ui/button";
import { Grid, List } from "lucide-react";

const Index = () => {
  const [showSidebar, setShowSidebar] = useState(false);

  return (
    <SidebarProvider>
      <div className="min-h-screen bg-background w-full">
        <Header />
        <div className="flex w-full">
          {showSidebar && <AgentSidebar />}
          <main className="flex-1">
            <div className="p-4 border-b border-border/50">
              <Button
                variant="outline"
                onClick={() => setShowSidebar(!showSidebar)}
                className="flex items-center gap-2"
              >
                {showSidebar ? <List className="h-4 w-4" /> : <Grid className="h-4 w-4" />}
                {showSidebar ? "Hide Categories" : "All Categories"}
              </Button>
            </div>
            <HeroSection />
            <SearchBar />
            <AgentShowcase />
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
};

export default Index;
