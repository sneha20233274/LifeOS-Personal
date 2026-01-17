import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Check,
  Edit2,
  Trash2,
  ChevronDown,
  ChevronUp,
  Target,
  Save,
  XCircle,
} from "lucide-react";
import { TaskProposal } from "./TaskProposal";

export function GoalProposal({
  goal,
  allTasks,
  allSubtasks,
  onUpdate,
  onStatusChange,
}) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [localPayload, setLocalPayload] = useState(goal.payload);

  /* -----------------------------
     YOUR LOGIC (UNCHANGED)
  ------------------------------ */

  const totalSubtasks = allTasks.reduce(
    (acc, t) => acc + (t.payload.subtasks?.length || 0),
    0
  );

  const save = () => {
   onUpdate(goal.proposal_id, localPayload);
    setIsEditing(false);
  };

  /* -----------------------------
     STATUS COLORS (UI ONLY)
  ------------------------------ */
  const statusColors = {
    PENDING:
      "border-purple-500 bg-gradient-to-br from-purple-50 via-white to-purple-50",
    APPROVED:
      "border-green-500 bg-gradient-to-br from-green-50 via-white to-green-50",
    REJECTED:
      "border-red-500 bg-gradient-to-br from-red-50 via-white to-red-50",
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className={`relative border-2 ${
        statusColors[goal.status]
      } rounded-2xl p-6 shadow-xl hover:shadow-2xl transition-all`}
    >
      {/* ================= HEADER ================= */}
      <div className="flex items-start justify-between gap-4 mb-5">
        <div className="flex-1 min-w-0">
          {isEditing ? (
            <div className="space-y-4">
              {Object.entries(localPayload).map(([key, value]) => (
                <div key={key}>
                  <label className="block text-sm font-medium text-gray-600 mb-1 capitalize">
                    {key.replace(/_/g, " ")}
                  </label>
                  <input
                    value={value}
                    onChange={(e) =>
                      setLocalPayload((prev) => ({
                        ...prev,
                        [key]: e.target.value,
                      }))
                    }
                    className="w-full px-4 py-3 border-2 rounded-xl focus:ring-2 focus:ring-purple-500"
                  />
                </div>
              ))}

              <div className="flex gap-3">
                <button
                  onClick={save}
                  className="flex items-center gap-2 px-5 py-2.5 bg-green-600 text-white rounded-xl"
                >
                  <Save className="w-5 h-5" />
                  Save
                </button>
                <button
                  onClick={() => {
                    setLocalPayload(goal.payload);
                    setIsEditing(false);
                  }}
                  className="flex items-center gap-2 px-5 py-2.5 bg-gray-500 text-white rounded-xl"
                >
                  <XCircle className="w-5 h-5" />
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <>
              <div className="flex items-center gap-3 mb-3">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Target className="w-6 h-6 text-purple-600" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900">
                  {goal.payload.goal_name || "Goal"}
                </h2>
              </div>

              <p className="text-gray-700 mb-4">{goal.payload.description}</p>

              <div className="flex items-center gap-3 text-sm">
                {allTasks.length > 0 && (
                  <span className="px-3 py-1.5 bg-purple-100 text-purple-700 rounded-full font-medium">
                    {allTasks.length} task
                    {allTasks.length !== 1 ? "s" : ""}
                  </span>
                )}
                {totalSubtasks > 0 && (
                  <span className="px-3 py-1.5 bg-blue-100 text-blue-700 rounded-full font-medium">
                    {totalSubtasks} subtask
                    {totalSubtasks !== 1 ? "s" : ""}
                  </span>
                )}
              </div>
            </>
          )}
        </div>

        {!isEditing && (
          <div className="flex items-center gap-2">
            {goal.status === "PENDING" && (
              <>
                <button
                  onClick={() => onStatusChange(goal.proposal_id, "APPROVED")}
                  className="p-3 bg-green-100 text-green-600 rounded-xl"
                >
                  <Check />
                </button>
                <button
                  onClick={() => setIsEditing(true)}
                  className="p-3 bg-blue-100 text-blue-600 rounded-xl"
                  title="Edit"
                >
                  <Edit2 className="w-6 h-6" />
                </button>
              </>
            )}
            <button
              onClick={() => onStatusChange(goal.proposal_id, "REJECTED")}
              className="p-3 bg-red-100 text-red-600 rounded-xl"
            >
              <Trash2 />
            </button>
            {(goal.status === "REJECTED" || goal.status==="APPROVED") &&  (
              <button
                onClick={() => onStatusChange(goal.proposal_id, "PENDING")}
                className="p-3 bg-gray-200 text-gray-700 rounded-xl"
                title="Undo delete"
              >
                <XCircle />
              </button>
            )}

            {allTasks.length > 0 && (
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="p-3 bg-gray-100 text-gray-600 rounded-xl"
              >
                {isExpanded ? (
                  <ChevronUp className="w-6 h-6" />
                ) : (
                  <ChevronDown className="w-6 h-6" />
                )}
              </button>
            )}
          </div>
        )}
      </div>

      {/* ================= APPROVED BADGE ================= */}
      {goal.status === "APPROVED" && !isEditing && (
        <div className="absolute top-4 right-4">
          <div className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-full font-medium shadow-lg">
            <Check className="w-4 h-4" />
            Approved
          </div>
        </div>
      )}

      {/* ================= TASKS ================= */}
      <AnimatePresence>
        {isExpanded && allTasks.length > 0 && !isEditing && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="mt-6 space-y-4"
          >
            <div className="flex items-center gap-2 mb-4">
              <div className="h-px flex-1 bg-gradient-to-r from-transparent via-gray-300 to-transparent" />
              <span className="text-sm font-medium text-gray-500 uppercase">
                Tasks
              </span>
              <div className="h-px flex-1 bg-gradient-to-r from-transparent via-gray-300 to-transparent" />
            </div>

            {allTasks.map((task) => (
              <TaskProposal
                key={task.proposal_id}
                task={task}
                allSubtasks={allSubtasks}
                onUpdate={onUpdate}
                onStatusChange={onStatusChange}
              />
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
