import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { LogOut, User, Settings, History } from 'lucide-react';

const Dashboard = () => {
  const { user, logout } = useAuth();

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-[#0A0A0D] text-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-heading-xl heading-premium text-gradient mb-2">Dashboard</h1>
            <p className="text-gray-400">Welcome back, {user.name}!</p>
          </div>
          <Button onClick={logout} variant="outline" className="flex items-center gap-2">
            <LogOut className="h-4 w-4" />
            Logout
          </Button>
        </div>

        {/* User Info Card */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                <span className="heading-premium">Profile Information</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <p><strong>Email:</strong> {user.email}</p>
                <p><strong>Name:</strong> {user.name}</p>
                <p><strong>Role:</strong>
                  <Badge variant="secondary" className="ml-2">
                    Not specified
                  </Badge>
                </p>
                <p><strong>Member since:</strong> {new Date(user.created_at).toLocaleDateString()}</p>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <History className="h-5 w-5" />
                <span className="heading-premium">Recent Activity</span>
              </CardTitle>
              <CardDescription>Your latest agent interactions</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center text-gray-400 py-4">
                <p>No recent activity</p>
                <p className="text-sm">Start a research session to see activity here</p>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="h-5 w-5" />
                <span className="heading-premium">Quick Actions</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <Button className="w-full" variant="outline">
                  Start New Research
                </Button>
                <Button className="w-full" variant="outline">
                  View Reports
                </Button>
                <Button className="w-full" variant="outline">
                  Account Settings
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="text-2xl font-bold text-primary">0</div>
              <p className="text-gray-400">Research Sessions</p>
            </CardContent>
          </Card>
          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="text-2xl font-bold text-primary">0</div>
              <p className="text-gray-400">Reports Generated</p>
            </CardContent>
          </Card>
          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="text-2xl font-bold text-primary">0</div>
              <p className="text-gray-400">Hours Saved</p>
            </CardContent>
          </Card>
          <Card className="glass-card">
            <CardContent className="p-6">
              <div className="text-2xl font-bold text-primary">Free</div>
              <p className="text-gray-400">Current Plan</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
