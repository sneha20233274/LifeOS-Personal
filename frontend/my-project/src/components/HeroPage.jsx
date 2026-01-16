import { Calendar, Target, Brain, Sparkles, ArrowRight } from "lucide-react";
import { Button } from "./ui/Button";
import { ImageWithFallback } from "./figma/ImageWithFallback";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";

export function HeroPage() {
  const navigate = useNavigate();

  // ✅ CORRECT FLAG
  const { isAuthenticated } = useSelector((s) => s.auth);

  const handleGetStarted = () => {
    if (isAuthenticated) {
      navigate("/dashboard");
    } else {
      navigate("/login"); // or /signup if you prefer
    }
  };

  return (
    <div className="w-full min-h-screen bg-gradient-to-br from-sky-50 via-teal-50 to-emerald-100">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-6 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-8">
            <div className="inline-flex items-center gap-2 bg-teal-100 text-teal-700 px-4 py-2 rounded-full">
              <Sparkles className="w-4 h-4" />
              <span className="text-sm">
                Your Personal Life Operating System
              </span>
            </div>

            <h1 className="text-5xl lg:text-7xl font-bold text-gray-900 leading-tight">
              Plan Your
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-teal-600 to-emerald-600">
                Entire Life
              </span>
            </h1>

            <p className="text-xl text-gray-600 leading-relaxed">
              Life OS is your ultimate planner that helps you organize every
              aspect of your life.
            </p>

            <div className="flex gap-4">
              <Button
                onClick={handleGetStarted}
                size="lg"
                className="bg-gradient-to-r from-teal-600 to-emerald-600
                hover:from-teal-700 hover:to-emerald-700
                text-white px-8"
              >
                Get Started
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>

              <Button
                variant="outline"
                size="lg"
                className="border-2 border-teal-600 text-teal-700 hover:bg-teal-50"
              >
                Learn More
              </Button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6 pt-8">
              <Stat value="10K+" label="Active Users" />
              <Stat value="95%" label="Success Rate" />
              <Stat value="24/7" label="Support" />
            </div>
          </div>

          {/* Right Image */}
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-teal-400 to-emerald-400 rounded-3xl blur-3xl opacity-30"></div>
            <ImageWithFallback
              src="https://images.unsplash.com/photo-1553034545-32d4cd2168f1"
              alt="Life OS Planner"
              className="relative rounded-3xl shadow-2xl w-full"
            />
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Everything You Need to Thrive
          </h2>
          <p className="text-xl text-gray-600">
            Powerful features to help you organize and optimize your life
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<Calendar className="w-6 h-6 text-teal-600" />}
            bg="bg-teal-100"
            title="Smart Scheduling"
            desc="AI powered scheduling that adapts to your lifestyle."
          />

          <FeatureCard
            icon={<Target className="w-6 h-6 text-sky-600" />}
            bg="bg-sky-100"
            title="Goal Tracking"
            desc="Track progress with powerful goal analytics."
          />

          <FeatureCard
            icon={<Brain className="w-6 h-6 text-emerald-600" />}
            bg="bg-emerald-100"
            title="Habit Building"
            desc="Build habits with daily motivation and insights."
          />
        </div>
      </div>
    </div>
  );
}

/* Helper components */
function FeatureCard({ icon, bg, title, desc }) {
  return (
    <div className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
      <div
        className={`w-12 h-12 ${bg} rounded-xl flex items-center justify-center mb-4`}
      >
        {icon}
      </div>
      <h3 className="text-xl font-semibold text-gray-900 mb-3">{title}</h3>
      <p className="text-gray-600">{desc}</p>
    </div>
  );
}

function Stat({ value, label }) {
  return (
    <div>
      <div className="text-3xl font-bold text-teal-600">{value}</div>
      <div className="text-sm text-gray-600">{label}</div>
    </div>
  );
}
