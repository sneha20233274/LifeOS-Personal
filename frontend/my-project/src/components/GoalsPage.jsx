import { useState, useEffect } from "react";
import { ArrowLeft, Plus, Search, Filter, Target } from "lucide-react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { GoalCard } from "./GoalCard";
import { useNavigate } from "react-router-dom";

// Mock data generator
const generateGoals = (startIndex, count) => {
  const categories = ["Career", "Health", "Learning", "Finance", "Personal"];
  const statuses = ["completed", "in-progress", "not-started"];
  const priorities = ["high", "medium", "low"];

  return Array.from({ length: count }, (_, i) => ({
    id: startIndex + i,
    title: `Goal ${startIndex + i}: ${
      [
        "Launch Product",
        "Build Portfolio",
        "Master Skills",
        "Achieve Fitness",
        "Financial Freedom",
      ][i % 5]
    }`,
    description:
      "This is a comprehensive goal that requires careful planning and execution. Breaking it down into manageable tasks will help achieve success.",
    category: categories[i % categories.length],
    status: statuses[i % statuses.length],
    priority: priorities[i % priorities.length],
    progress: Math.floor(Math.random() * 100),
    tasksCompleted: Math.floor(Math.random() * 15),
    totalTasks: 15 + Math.floor(Math.random() * 10),
    daysLeft: Math.floor(Math.random() * 90),
    collaborators: Math.floor(Math.random() * 5) + 1,
    startDate: "2024-01-01",
    dueDate: "2024-12-31",
  }));
};

export function GoalsPage() {
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const navigate = useNavigate();

  // Initial load
  useEffect(() => {
    setGoals(generateGoals(1, 12));
  }, []);

  // Infinite scroll handler
  useEffect(() => {
    const handleScroll = () => {
      if (
        window.innerHeight + document.documentElement.scrollTop >=
          document.documentElement.offsetHeight - 100 &&
        !loading &&
        hasMore
      ) {
        loadMore();
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [loading, hasMore, goals.length]);

  const loadMore = () => {
    setLoading(true);
    setTimeout(() => {
      const newGoals = generateGoals(goals.length + 1, 6);
      setGoals([...goals, ...newGoals]);
      setLoading(false);

      // Stop loading after 50 items for demo
      if (goals.length >= 50) {
        setHasMore(false);
      }
    }, 1000);
  };

  const filteredGoals = goals.filter(
    (goal) =>
      goal.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      goal.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-indigo-50">
      {/* Header */}
      <div className="bg-white shadow-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                onClick={() => navigate("/dashboard")}
                className="text-gray-700 hover:text-purple-700"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back
              </Button>
              <div className="flex items-center gap-3">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Target className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">
                    All Goals
                  </h1>
                  <p className="text-sm text-gray-600">
                    {filteredGoals.length} goals found
                  </p>
                </div>
              </div>
            </div>

            <Button className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700">
              <Plus className="w-5 h-5 mr-2" />
              New Goal
            </Button>
          </div>

          {/* Search and Filter */}
          <div className="flex gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <Input
                type="text"
                placeholder="Search goals..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            <Button variant="outline">
              <Filter className="w-5 h-5 mr-2" />
              Filter
            </Button>
          </div>
        </div>
      </div>

      {/* Goals Grid */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredGoals.map((goal) => (
            <GoalCard key={goal.id} goal={goal} />
          ))}
        </div>

        {/* Loading indicator */}
        {loading && (
          <div className="flex justify-center items-center py-12">
            <div className="flex flex-col items-center gap-3">
              <div className="w-12 h-12 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin"></div>
              <p className="text-gray-600">Loading more goals...</p>
            </div>
          </div>
        )}

        {/* No more data */}
        {!hasMore && goals.length > 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">
              You've reached the end of your goals list
            </p>
          </div>
        )}

        {/* Empty state */}
        {filteredGoals.length === 0 && !loading && (
          <div className="text-center py-20">
            <Target className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No goals found
            </h3>
            <p className="text-gray-600 mb-6">
              Try adjusting your search or create a new goal
            </p>
            <Button className="bg-purple-600 hover:bg-purple-700">
              <Plus className="w-5 h-5 mr-2" />
              Create Your First Goal
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
