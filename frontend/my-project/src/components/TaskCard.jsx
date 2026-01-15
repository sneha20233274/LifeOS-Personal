import {
  CheckSquare,
  Clock,
  Flag,
  MoreVertical,
  Edit,
  Trash2,
  ChevronRight,
} from "lucide-react";
import { Button } from "./ui/button";
import { Checkbox } from "./ui/checkbox";


export function TaskCard({ task }) {
  
  const getPriorityColor = (priority) => {
    switch (priority) {
      case "high":
        return "text-red-600 bg-red-50 border-red-200";
      case "medium":
        return "text-yellow-600 bg-yellow-50 border-yellow-200";
      case "low":
        return "text-green-600 bg-green-50 border-green-200";
      default:
        return "text-gray-600 bg-gray-50 border-gray-200";
    }
  };

  const getStatusIcon = (status) => {
    if (status === "completed") return "✓";
    if (status === "in-progress") return "⏳";
    return "○";
  };

  return (
    <div className="bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden group border-l-4 border-blue-500">
      <div className="p-6">
        {/* Top Section */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-start gap-3 flex-1">
            <Checkbox className="mt-1" checked={task.status === "completed"} />
            <div className="flex-1">
              <h3
                className={`text-lg font-bold mb-2 group-hover:text-blue-600 transition-colors ${
                  task.status === "completed"
                    ? "line-through text-gray-400"
                    : "text-gray-900"
                }`}
              >
                {task.title}
              </h3>
              <p className="text-gray-600 text-sm line-clamp-2">
                {task.description}
              </p>
            </div>
          </div>

          <Button
            variant="ghost"
            size="icon"
            className="opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <MoreVertical className="w-5 h-5" />
          </Button>
        </div>

        {/* Tags Section */}
        <div className="flex flex-wrap gap-2 mb-4">
          <span
            className={`px-3 py-1 rounded-lg text-xs font-medium border ${getPriorityColor(
              task.priority
            )}`}
          >
            <Flag className="w-3 h-3 inline mr-1" />
            {task.priority.toUpperCase()}
          </span>
          <span className="px-3 py-1 rounded-lg text-xs font-medium bg-blue-100 text-blue-700">
            {task.category}
          </span>
          {task.tags.map((tag, index) => (
            <span
              key={index}
              className="px-3 py-1 rounded-lg text-xs font-medium bg-gray-100 text-gray-700"
            >
              #{tag}
            </span>
          ))}
        </div>

        {/* Time & Stats Section */}
        <div className="grid grid-cols-2 gap-4 mb-4 p-3 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl">
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-blue-600" />
            <div>
              <div className="text-xs text-gray-500">Due Date</div>
              <div className="text-sm font-semibold text-gray-900">
                {task.dueDate}
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <CheckSquare className="w-4 h-4 text-blue-600" />
            <div>
              <div className="text-xs text-gray-500">Subtasks</div>
              <div className="text-sm font-semibold text-gray-900">
                {task.subtasksCompleted}/{task.totalSubtasks}
              </div>
            </div>
          </div>
        </div>

        {/* Assignee & Time */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-400 to-indigo-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
              {task.assignee.charAt(0)}
            </div>
            <span className="text-sm font-medium text-gray-700">
              {task.assignee}
            </span>
          </div>
          <div className="text-sm text-gray-500">{task.estimatedTime}</div>
        </div>

        {/* Actions */}
        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity pt-3 border-t border-gray-100">
          <Button variant="outline" size="sm" className="flex-1">
            <Edit className="w-4 h-4 mr-2" />
            Edit
          </Button>
          <Button
            variant="outline"
            size="sm"
            className="text-blue-600 hover:bg-blue-50"
          >
            <ChevronRight className="w-4 h-4" />
          </Button>
          <Button
            variant="outline"
            size="sm"
            className="text-red-600 hover:bg-red-50"
          >
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
