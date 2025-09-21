import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "../components/ui/use-toast";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

const Signup: React.FC = () => {
  const { signup } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",  // Changed from fullName to match Profile model
    email: "",
    password: "",
    confirmPassword: "",
    role: "",
    terms: false,
  });
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCheckboxChange = (checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      terms: checked
    }));
  };

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      toast({
        title: "Password Mismatch",
        description: "Passwords do not match",
        variant: "destructive",
      });
      return;
    }

    if (!formData.terms) {
      toast({
        title: "Terms Required",
        description: "Please accept the Terms & Conditions",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);

    try {
      await signup(formData.email, formData.password, formData.name, formData.role);
      toast({
        title: "Account Created",
        description: "Welcome to AgentForce!",
      });
      navigate("/");
    } catch (error) {
      toast({
        title: "Signup Failed",
        description: error instanceof Error ? error.message : "Failed to create account",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0A0A0D] px-4">
      <div className="w-full max-w-md glass-card rounded-xl p-8">
        <h1 className="text-3xl font-bold text-gradient mb-6 text-center">
          Create Account
        </h1>
        <form className="space-y-4" onSubmit={handleSignup}>
          <div>
            <Label htmlFor="name">Full Name</Label>
            <Input
              id="name"
              name="name"
              placeholder="Your full name"
              value={formData.name}
              onChange={handleInputChange}
              required
              disabled={loading}
            />
          </div>

          <div>
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="you@example.com"
              value={formData.email}
              onChange={handleInputChange}
              required
              disabled={loading}
            />
          </div>

          <div>
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="Create a password"
              value={formData.password}
              onChange={handleInputChange}
              required
              disabled={loading}
            />
          </div>

          <div>
            <Label htmlFor="confirmPassword">Confirm Password</Label>
            <Input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              placeholder="Confirm your password"
              value={formData.confirmPassword}
              onChange={handleInputChange}
              required
              disabled={loading}
            />
          </div>

          <div>
            <Label htmlFor="role">Your Role / Interest</Label>
            <select
              id="role"
              name="role"
              value={formData.role}
              onChange={handleInputChange}
              className="w-full p-2 rounded-md bg-[#0A0A0D] text-white border border-[#7C3AED] focus:outline-none focus:ring-2 focus:ring-[#7C3AED]"
              disabled={loading}
            >
              <option value="">Select your role (optional)</option>
              <option value="creator">AI Agent Creator</option>
              <option value="entrepreneur">Entrepreneur</option>
              <option value="analyst">Data Analyst</option>
              <option value="researcher">Researcher</option>
              <option value="developer">Developer</option>
            </select>
          </div>

          <div className="flex items-center space-x-2">
            <Checkbox
              id="terms"
              checked={formData.terms}
              onCheckedChange={handleCheckboxChange}
              disabled={loading}
            />
            <Label htmlFor="terms" className="text-sm">
              I agree to the{" "}
              <a href="#" className="text-[#0EA5E9] hover:underline">
                Terms & Conditions
              </a>{" "}
              and{" "}
              <a href="#" className="text-[#0EA5E9] hover:underline">
                Privacy Policy
              </a>
            </Label>
          </div>

          <Button
            type="submit"
            className="w-full bg-gradient-to-r from-[#7C3AED] to-[#5B21B6] hover:scale-105 transition-transform"
            disabled={loading}
          >
            {loading ? "Creating Account..." : "Create Account"}
          </Button>
        </form>
        <p className="mt-4 text-center text-gray-400">
          Already have an account?{" "}
          <Link to="/login" className="text-[#0EA5E9] font-semibold hover:underline">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;
