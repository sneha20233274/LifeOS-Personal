import { useState, useEffect } from "react";
import { ArrowLeft, Plus, Search, Filter, CheckSquare } from "lucide-react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { TaskCard } from "./TaskCard";
import { useNavigate } from "react-router-dom";

// Mock data generator
const generateTasks = (startIndex, count) => {
 
  const categories = ["Work", "Personal", "Health", "Learning", "Home"];
  const statuses = ["completed", "in-progress", "pending"];
  const priorities = ["high", "medium", "low"];
  const tags = ["urgent", "important", "quick", "research", "meeting"];

  return Array.from({ length: count }, (_, i) => ({
    id: startIndex + i,
    title: `Task ${startIndex + i}: ${
      [
        "Complete Project Report",
        "Team Meeting",
        "Code Review",
        "Workout Session",
        "Study Material",
      ][i % 5]
    }`,
    description:
      "A detailed task description that outlines what needs to be accomplished and the expected outcome.",
    category: categories[i % categories.length],
    status: statuses[i % statuses.length],
    priority: priorities[i % priorities.length],
    tags: [tags[i % tags.length], tags[(i + 1) % tags.length]],
    dueDate: `2024-0${(i % 9) + 1}-${15 + (i % 15)}`,
    subtasksCompleted: Math.floor(Math.random() * 8),
    totalSubtasks: 8 + Math.floor(Math.random() * 5),
    assignee: ["John Doe", "Jane Smith", "Mike Johnson", "Sarah Williams"][
      i % 4
    ],
    estimatedTime: `${1 + Math.floor(Math.random() * 4)}h ${Math.floor(
      Math.random() * 60
    )}m`,
  }));
};

export function TasksPage() {
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  // Initial load
  useEffect(() => {
    setTasks(generateTasks(1, 12));
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
  }, [loading, hasMore, tasks.length]);

  const loadMore = () => {
    setLoading(true);
    setTimeout(() => {
      const newTasks = generateTasks(tasks.length + 1, 6);
      setTasks([...tasks, ...newTasks]);
      setLoading(false);

      // Stop loading after 50 items for demo
      if (tasks.length >= 50) {
        setHasMore(false);
      }
    }, 1000);
  };

  const filteredTasks = tasks.filter(
    (task) =>
      task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      task.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <div className="bg-white shadow-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                onClick={() => navigate("/dashboard")}
                className="text-gray-700 hover:text-blue-700"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back
              </Button>
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <CheckSquare className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">
                    All Tasks
                  </h1>
                  <p className="text-sm text-gray-600">
                    {filteredTasks.length} tasks found
                  </p>
                </div>
              </div>
            </div>

            <Button className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700">
              <Plus className="w-5 h-5 mr-2" />
              New Task
            </Button>
          </div>

          {/* Search and Filter */}
          <div className="flex gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <Input
                type="text"
                placeholder="Search tasks..."
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

      {/* Tasks Grid */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}
        </div>

        {/* Loading indicator */}
        {loading && (
          <div className="flex justify-center items-center py-12">
            <div className="flex flex-col items-center gap-3">
              <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
              <p className="text-gray-600">Loading more tasks...</p>
            </div>
          </div>
        )}

        {/* No more data */}
        {!hasMore && tasks.length > 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">
              You've reached the end of your tasks list
            </p>
          </div>
        )}

        {/* Empty state */}
        {filteredTasks.length === 0 && !loading && (
          <div className="text-center py-20">
            <CheckSquare className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No tasks found
            </h3>
            <p className="text-gray-600 mb-6">
              Try adjusting your search or create a new task
            </p>
            <Button className="bg-blue-600 hover:bg-blue-700">
              <Plus className="w-5 h-5 mr-2" />
              Create Your First Task
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
