import { useState } from "react";
import { ArrowLeft, Plus, Search, Filter, ListTodo } from "lucide-react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { SubtaskCard } from "./SubtaskCard";
import { useNavigate, useParams } from "react-router-dom";

import { useGetSubtasksByTaskQuery } from "../services/subtasksApi";

export function SubtasksPage() {
  const navigate = useNavigate();
  const { taskId } = useParams();

  const [searchTerm, setSearchTerm] = useState("");

  // 🔹 RTK QUERY
const {
  data: subtasks = [],
  isLoading,
  isError,
  error,
} = useGetSubtasksByTaskQuery(taskId, {
  refetchOnMountOrArgChange: true,
});


  /* -----------------------------
     SEARCH FILTER
  ------------------------------ */
  const filteredSubtasks = subtasks.filter(
    (s) =>
      s.subtask_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      s.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-indigo-50">
      {/* HEADER */}
      <div className="bg-white shadow-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                onClick={() => navigate(-1)}
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
                  <h1 className="text-2xl font-bold text-gray-900">Subtasks</h1>
                  <p className="text-sm text-gray-600">
                    {filteredSubtasks.length} subtasks found
                  </p>
                </div>
              </div>
            </div>

            <Button
              className="bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700"
              onClick={() => navigate(`/tasks/${taskId}/subtasks/new`)}
            >
              <Plus className="w-5 h-5 mr-2" />
              New Subtask
            </Button>
          </div>

          {/* SEARCH */}
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

      {/* SUBTASKS GRID */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {isLoading ? (
          <div className="flex justify-center items-center py-20">
            <div className="w-12 h-12 border-4 border-pink-200 border-t-pink-600 rounded-full animate-spin" />
          </div>
        ) : isError ? (
          <div className="text-center py-20 text-red-600">
            Failed to load subtasks
            <pre className="text-xs mt-2">{JSON.stringify(error, null, 2)}</pre>
          </div>
        ) : filteredSubtasks.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filteredSubtasks.map((subtask) => (
              <SubtaskCard key={subtask.subtask_id} subtask={subtask} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20">
            <ListTodo className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No subtasks found
            </h3>
            <p className="text-gray-600">
              Subtasks will appear here once created
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
