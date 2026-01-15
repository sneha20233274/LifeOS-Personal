import {
  Target,
  Calendar,
  TrendingUp,
  MoreVertical,
  Edit,
  Trash2,
} from "lucide-react";
import { Progress } from "./ui/progress";
import { Button } from "./ui/button";

export function GoalCard({ goal }) {
  const getPriorityColor = (priority) => {
    switch (priority) {
      case "high":
        return "bg-red-500";
      case "medium":
        return "bg-yellow-500";
      case "low":
        return "bg-green-500";
      default:
        return "bg-gray-500";
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "completed":
        return "text-green-600 bg-green-100";
      case "in-progress":
        return "text-blue-600 bg-blue-100";
      case "not-started":
        return "text-gray-600 bg-gray-100";
      default:
        return "text-gray-600 bg-gray-100";
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden group">
      {/* Header with gradient */}
      <div className="h-2 bg-gradient-to-r from-purple-500 via-purple-600 to-indigo-600"></div>

      <div className="p-6">
        {/* Top Section */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-start gap-3 flex-1">
            <div className="p-3 bg-purple-100 rounded-xl">
              <Target className="w-6 h-6 text-purple-600" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-purple-600 transition-colors">
                {goal.title}
              </h3>
              <p className="text-gray-600 text-sm line-clamp-2">
                {goal.description}
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

        {/* Tags/Categories */}
        <div className="flex flex-wrap gap-2 mb-4">
          <span
            className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(
              goal.status
            )}`}
          >
            {goal.status.replace("-", " ").toUpperCase()}
          </span>
          <span className="px-3 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-700">
            {goal.category}
          </span>
          <div className="flex items-center gap-1">
            <div
              className={`w-2 h-2 rounded-full ${getPriorityColor(
                goal.priority
              )}`}
            ></div>
            <span className="text-xs font-medium text-gray-600 capitalize">
              {goal.priority} Priority
            </span>
          </div>
        </div>

        {/* Progress Section */}
        <div className="mb-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Progress</span>
            <span className="text-sm font-bold text-purple-600">
              {goal.progress}%
            </span>
          </div>
          <Progress value={goal.progress} className="h-2" />
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-4 pt-4 border-t border-gray-100">
          <div className="text-center">
            <div className="text-lg font-bold text-gray-900">
              {goal.tasksCompleted}/{goal.totalTasks}
            </div>
            <div className="text-xs text-gray-500">Tasks</div>
          </div>
          <div className="text-center border-l border-r border-gray-100">
            <div className="text-lg font-bold text-gray-900">
              {goal.daysLeft}
            </div>
            <div className="text-xs text-gray-500">Days Left</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-gray-900">
              {goal.collaborators}
            </div>
            <div className="text-xs text-gray-500">Team</div>
          </div>
        </div>

        {/* Dates */}
        <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4" />
            <span>Start: {goal.startDate}</span>
          </div>
          <div className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4" />
            <span>Due: {goal.dueDate}</span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <Button variant="outline" size="sm" className="flex-1">
            <Edit className="w-4 h-4 mr-2" />
            Edit
          </Button>
          <Button
            variant="outline"
            size="sm"
            className="flex-1 text-red-600 hover:bg-red-50 hover:text-red-700"
          >
            <Trash2 className="w-4 h-4 mr-2" />
            Delete
          </Button>
        </div>
      </div>
    </div>
  );
}
