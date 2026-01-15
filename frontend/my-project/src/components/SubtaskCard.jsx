import {
  ListTodo,
  Clock,
  Link2,
  MoreVertical,
  Edit,
  Trash2,
  CheckCircle2,
} from "lucide-react";
import { Button } from "./ui/button";
import { Checkbox } from "./ui/checkbox";

export function SubtaskCard({ subtask }) {
  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case "hard":
        return "bg-red-100 text-red-700 border-red-300";
      case "medium":
        return "bg-yellow-100 text-yellow-700 border-yellow-300";
      case "easy":
        return "bg-green-100 text-green-700 border-green-300";
      default:
        return "bg-gray-100 text-gray-700 border-gray-300";
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-300 overflow-hidden group border border-gray-200 hover:border-pink-300">
      <div className="p-5">
        {/* Top Section */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-start gap-3 flex-1">
            <Checkbox className="mt-0.5" checked={subtask.completed} />
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <h4
                  className={`font-semibold group-hover:text-pink-600 transition-colors ${
                    subtask.completed
                      ? "line-through text-gray-400"
                      : "text-gray-900"
                  }`}
                >
                  {subtask.title}
                </h4>
                {subtask.completed && (
                  <CheckCircle2 className="w-4 h-4 text-green-500" />
                )}
              </div>
              <p className="text-gray-600 text-sm">{subtask.description}</p>
            </div>
          </div>

          <Button
            variant="ghost"
            size="icon"
            className="opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <MoreVertical className="w-4 h-4" />
          </Button>
        </div>

        {/* Parent Task Link */}
        <div className="flex items-center gap-2 mb-3 p-2 bg-pink-50 rounded-lg">
          <Link2 className="w-4 h-4 text-pink-600" />
          <span className="text-xs text-gray-600">Parent Task:</span>
          <span className="text-xs font-medium text-pink-600">
            {subtask.parentTask}
          </span>
        </div>

        {/* Tags & Info */}
        <div className="flex flex-wrap gap-2 mb-3">
          <span
            className={`px-2 py-1 rounded-md text-xs font-medium border ${getDifficultyColor(
              subtask.difficulty
            )}`}
          >
            {subtask.difficulty.toUpperCase()}
          </span>
          <span className="px-2 py-1 rounded-md text-xs font-medium bg-pink-100 text-pink-700">
            {subtask.category}
          </span>
        </div>

        {/* Time Info */}
        <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
          <div className="flex items-center gap-1">
            <Clock className="w-3 h-3" />
            <span>{subtask.estimatedTime}</span>
          </div>
          <div className="flex items-center gap-1">
            <span>Due: {subtask.dueDate}</span>
          </div>
        </div>

        {/* Progress Bar */}
        {!subtask.completed && (
          <div className="mb-3">
            <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-pink-500 to-purple-500 transition-all duration-300"
                style={{ width: `${subtask.progress || 0}%` }}
              ></div>
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity pt-2 border-t border-gray-100">
          <Button variant="ghost" size="sm" className="flex-1 h-8 text-xs">
            <Edit className="w-3 h-3 mr-1" />
            Edit
          </Button>
          <Button
            variant="ghost"
            size="sm"
            className="flex-1 h-8 text-xs text-red-600 hover:bg-red-50"
          >
            <Trash2 className="w-3 h-3 mr-1" />
            Delete
          </Button>
        </div>
      </div>
    </div>
  );
}
