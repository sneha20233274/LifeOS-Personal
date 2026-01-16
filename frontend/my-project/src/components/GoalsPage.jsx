import { useState, useEffect } from "react";
import { ArrowLeft, Search, Filter, Target } from "lucide-react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { GoalCard } from "./GoalCard";
import { useNavigate } from "react-router-dom";

export function GoalsPage() {
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const navigate = useNavigate();

  /* -----------------------------
     FETCH GOALS FROM BACKEND
  ------------------------------ */
  useEffect(() => {
    const fetchGoals = async () => {
      setLoading(true);
      try {
        const res = await fetch("/api/goals");
        const data = await res.json();
        setGoals(data);
      } catch (err) {
        console.error("Failed to fetch goals", err);
      } finally {
        setLoading(false);
      }
    };

    fetchGoals();
  }, []);

  /* -----------------------------
     SEARCH FILTER
  ------------------------------ */
  const filteredGoals = goals.filter(
    (goal) =>
      goal.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      goal.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-indigo-50">
      {/* HEADER */}
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
                    Your Goals
                  </h1>
                  <p className="text-sm text-gray-600">
                    {filteredGoals.length} goals found
                  </p>
                </div>
              </div>
            </div>

            {/* ❌ Create Goal button REMOVED */}
          </div>

          {/* SEARCH */}
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

      {/* GOALS GRID */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="w-12 h-12 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin"></div>
          </div>
        ) : filteredGoals.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredGoals.map((goal) => (
              <GoalCard key={goal.id} goal={goal} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20">
            <Target className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No goals found
            </h3>
            <p className="text-gray-600">
              Goals will appear here once created by AI or you
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
