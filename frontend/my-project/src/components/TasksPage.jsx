import { useState } from "react";
import { ArrowLeft, Plus, Search, Filter, CheckSquare } from "lucide-react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { TaskCard } from "./TaskCard";
import { useNavigate, useParams } from "react-router-dom";

import {
  useGetTasksQuery,
  useGetTasksByGoalQuery,
} from "../services/tasksApi";

export function TasksPage() {
  const navigate = useNavigate();
  const { goalId } = useParams();

  const [searchTerm, setSearchTerm] = useState("");

  // 🔹 RTK QUERY (goal-aware)
  const {
    data: tasks = [],
    isLoading,
    isError,
    error,
  } = goalId ? useGetTasksByGoalQuery(goalId) : useGetTasksQuery();

  /* -----------------------------
     SEARCH FILTER
  ------------------------------ */
  const filteredTasks = tasks.filter(
    (t) =>
      t.task_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* HEADER */}
      <div className="bg-white shadow-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                onClick={() => navigate(-1)}
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
                    {goalId ? "Goal Tasks" : "All Tasks"}
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

          {/* SEARCH */}
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

      {/* TASKS GRID */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {isLoading ? (
          <div className="flex justify-center py-20">
            <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin" />
          </div>
        ) : isError ? (
          <div className="text-center py-20 text-red-600">
            Failed to load tasks
            <pre className="text-xs mt-2">{JSON.stringify(error, null, 2)}</pre>
          </div>
        ) : filteredTasks.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredTasks.map((task) => (
              <TaskCard key={task.task_id} task={task} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20">
            <CheckSquare className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No tasks found
            </h3>
            <p className="text-gray-600">Tasks will appear here once created</p>
          </div>
        )}
      </div>
    </div>
  );
}
