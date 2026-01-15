import { useState, useEffect } from "react";
import { ArrowLeft, Plus, Search, Filter, ListTodo } from "lucide-react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { SubtaskCard } from "./SubtaskCard";
import { useNavigate } from "react-router-dom";


// Mock data generator
const generateSubtasks = (startIndex, count) => {
  const categories = [
    "Development",
    "Design",
    "Research",
    "Testing",
    "Documentation",
  ];
  const difficulties = ["easy", "medium", "hard"];
  const parentTasks = [
    "Project Setup",
    "Feature Development",
    "Bug Fixes",
    "Optimization",
    "Deployment",
  ];

  return Array.from({ length: count }, (_, i) => ({
    id: startIndex + i,
    title: `Subtask ${startIndex + i}: ${
      [
        "Update UI Component",
        "Write Tests",
        "Fix Bug",
        "Add Feature",
        "Refactor Code",
      ][i % 5]
    }`,
    description:
      "A specific subtask that contributes to the completion of a larger task.",
    category: categories[i % categories.length],
    difficulty: difficulties[i % difficulties.length],
    completed: Math.random() > 0.6,
    progress: Math.floor(Math.random() * 100),
    parentTask: parentTasks[i % parentTasks.length],
    estimatedTime: `${30 + Math.floor(Math.random() * 90)}min`,
    dueDate: `Jan ${10 + (i % 20)}`,
  }));
};

export function SubtasksPage() {
  const navigate = useNavigate(); 
  const [subtasks, setSubtasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  // Initial load
  useEffect(() => {
    setSubtasks(generateSubtasks(1, 15));
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
  }, [loading, hasMore, subtasks.length]);

  const loadMore = () => {
    setLoading(true);
    setTimeout(() => {
      const newSubtasks = generateSubtasks(subtasks.length + 1, 9);
      setSubtasks([...subtasks, ...newSubtasks]);
      setLoading(false);

      // Stop loading after 60 items for demo
      if (subtasks.length >= 60) {
        setHasMore(false);
      }
    }, 1000);
  };

  const filteredSubtasks = subtasks.filter(
    (subtask) =>
      subtask.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      subtask.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-indigo-50">
      {/* Header */}
      <div className="bg-white shadow-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                onClick={() => navigate("/dashboard")}
                className="text-gray-700 hover:text-pink-700"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back
              </Button>
              <div className="flex items-center gap-3">
                <div className="p-2 bg-pink-100 rounded-lg">
                  <ListTodo className="w-6 h-6 text-pink-600" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">
                    All Subtasks
                  </h1>
                  <p className="text-sm text-gray-600">
                    {filteredSubtasks.length} subtasks found
                  </p>
                </div>
              </div>
            </div>

            <Button className="bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700">
              <Plus className="w-5 h-5 mr-2" />
              New Subtask
            </Button>
          </div>

          {/* Search and Filter */}
          <div className="flex gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <Input
                type="text"
                placeholder="Search subtasks..."
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

      {/* Subtasks Grid */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredSubtasks.map((subtask) => (
            <SubtaskCard key={subtask.id} subtask={subtask} />
          ))}
        </div>

        {/* Loading indicator */}
        {loading && (
          <div className="flex justify-center items-center py-12">
            <div className="flex flex-col items-center gap-3">
              <div className="w-12 h-12 border-4 border-pink-200 border-t-pink-600 rounded-full animate-spin"></div>
              <p className="text-gray-600">Loading more subtasks...</p>
            </div>
          </div>
        )}

        {/* No more data */}
        {!hasMore && subtasks.length > 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">
              You've reached the end of your subtasks list
            </p>
          </div>
        )}

        {/* Empty state */}
        {filteredSubtasks.length === 0 && !loading && (
          <div className="text-center py-20">
            <ListTodo className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No subtasks found
            </h3>
            <p className="text-gray-600 mb-6">
              Try adjusting your search or create a new subtask
            </p>
            <Button className="bg-pink-600 hover:bg-pink-700">
              <Plus className="w-5 h-5 mr-2" />
              Create Your First Subtask
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
