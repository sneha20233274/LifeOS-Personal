import {
  Target,
  Calendar,
  Star,
  MoreVertical,
  Edit,
  Trash2,
  ChevronRight,
} from "lucide-react";
import { Progress } from "./ui/progress";
import { Button } from "./ui/button";
import { useNavigate } from "react-router-dom";

export function GoalCard({ goal }) {
  const navigate = useNavigate();

  const importanceLabel = (level) => {
    if (!level) return null;
    if (level >= 4) return "High";
    if (level === 3) return "Medium";
    return "Low";
  };

  return (
    <div
      onClick={() => navigate(`/goals/${goal.goal_id}/tasks`)}
      className="relative bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden group cursor-pointer"
    >
      {/* Gradient Header */}
      <div className="h-2 bg-gradient-to-r from-purple-500 via-purple-600 to-indigo-600" />

      {/* Hover Overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-600/90 to-indigo-600/90 opacity-0 group-hover:opacity-100 transition-opacity z-10 flex items-center justify-center">
        <div className="text-white text-center space-y-2">
          <div className="flex items-center justify-center gap-2 text-lg font-semibold">
            <ChevronRight className="w-5 h-5" />
            Click to view tasks
          </div>
          <div className="text-sm opacity-90">View tasks • Add new task</div>
        </div>
      </div>

      {/* Content */}
      <div className="p-6 relative z-0">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-start gap-3 flex-1">
            <div className="p-3 bg-purple-100 rounded-xl">
              <Target className="w-6 h-6 text-purple-600" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-purple-600 transition-colors">
                {goal.goal_name}
              </h3>

              {goal.description && (
                <p className="text-gray-600 text-sm line-clamp-2">
                  {goal.description}
                </p>
              )}
            </div>
          </div>

          <Button
            variant="ghost"
            size="icon"
            className="opacity-0 group-hover:opacity-100 transition-opacity"
            onClick={(e) => e.stopPropagation()}
          >
            <MoreVertical className="w-5 h-5" />
          </Button>
        </div>

        {/* Importance */}
        {goal.importance_level && (
          <div className="flex items-center gap-2 mb-4">
            <Star className="w-4 h-4 text-yellow-500" />
            <span className="text-sm font-medium text-gray-700">
              Importance: {importanceLabel(goal.importance_level)} (
              {goal.importance_level}/5)
            </span>
          </div>
        )}

        {/* Progress */}
        {typeof goal.percent_completion === "number" && (
          <div className="mb-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">
                Completion
              </span>
              <span className="text-sm font-bold text-purple-600">
                {Math.round(goal.percent_completion)}%
              </span>
            </div>
            <Progress value={goal.percent_completion} className="h-2" />
          </div>
        )}

        {/* Motivations */}
        {Array.isArray(goal.motivations) && goal.motivations.length > 0 && (
          <div className="mb-4">
            <div className="text-sm font-medium text-gray-700 mb-2">
              Motivations
            </div>
            <div className="flex flex-wrap gap-2">
              {goal.motivations.map((m, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 rounded-full text-xs bg-purple-100 text-purple-700"
                >
                  {m}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Target Date */}
        {goal.target_date && (
          <div className="flex items-center gap-2 text-sm text-gray-500 mb-4">
            <Calendar className="w-4 h-4" />
            <span>Target: {goal.target_date}</span>
          </div>
        )}

        {/* Actions */}
        <div
          className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity"
          onClick={(e) => e.stopPropagation()}
        >
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
