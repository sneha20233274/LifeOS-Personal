import {
  ListTodo,
  Clock,
  Link2,
  MoreVertical,
  Edit,
  Trash2,
  CheckCircle2,
  Target,
} from "lucide-react";
import { Button } from "./ui/button";
import { Checkbox } from "./ui/checkbox";

export function SubtaskCard({ subtask }) {
  /* -----------------------------
     DERIVED PROGRESS
  ------------------------------ */
  const hasProgressTarget =
    subtask.subtask_type !== "checkbox" &&
    typeof subtask.target_value === "number" &&
    subtask.target_value > 0;

  const progressPercent = hasProgressTarget
    ? Math.min(
        100,
        Math.round((subtask.current_value / subtask.target_value) * 100)
      )
    : null;

  /* -----------------------------
     TYPE BADGE COLOR
  ------------------------------ */
  const typeColor = {
    checkbox: "bg-green-100 text-green-700",
    count: "bg-blue-100 text-blue-700",
    duration: "bg-purple-100 text-purple-700",
    score: "bg-orange-100 text-orange-700",
  };

  return (
    <div className="relative bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-300 overflow-hidden group border border-gray-200 hover:border-pink-300">
      <div className="p-5">
        {/* ================= HEADER ================= */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-start gap-3 flex-1">
            {/* Checkbox only for checkbox-type */}
            {subtask.subtask_type === "checkbox" && (
              <Checkbox checked={subtask.achieved} />
            )}

            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <h4
                  className={`font-semibold transition-colors ${
                    subtask.achieved
                      ? "line-through text-gray-400"
                      : "text-gray-900 group-hover:text-pink-600"
                  }`}
                >
                  {subtask.subtask_name}
                </h4>

                {subtask.achieved && (
                  <CheckCircle2 className="w-4 h-4 text-green-500" />
                )}
              </div>

              {/* Subtask type badge */}
              <span
                className={`inline-block px-2 py-0.5 rounded-md text-xs font-medium ${
                  typeColor[subtask.subtask_type]
                }`}
              >
                {subtask.subtask_type.toUpperCase()}
              </span>
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

        {/* ================= DEPENDENCY ================= */}
        {subtask.depends_on_subtask_id && (
          <div className="flex items-center gap-2 mb-3 p-2 bg-pink-50 rounded-lg">
            <Link2 className="w-4 h-4 text-pink-600" />
            <span className="text-xs text-gray-600">
              Depends on subtask #{subtask.depends_on_subtask_id}
            </span>
          </div>
        )}

        {/* ================= PROGRESS ================= */}
        {hasProgressTarget && (
          <div className="mb-3">
            <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
              <span className="flex items-center gap-1">
                <Target className="w-3 h-3" />
                {subtask.current_value} / {subtask.target_value}
              </span>
              <span className="font-medium">{progressPercent}%</span>
            </div>

            <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-pink-500 to-purple-500 transition-all"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>
        )}

        {/* ================= META INFO ================= */}
        <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
          {subtask.deadline && (
            <div className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              <span>Due: {subtask.deadline}</span>
            </div>
          )}

          {subtask.weight !== undefined && (
            <span>Weight: {subtask.weight}</span>
          )}
        </div>

        {/* ================= ACTIONS ================= */}
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
