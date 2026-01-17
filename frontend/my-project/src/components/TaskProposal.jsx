import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Check,
  Edit2,
  Trash2,
  ChevronDown,
  ChevronUp,
  Save,
  XCircle,
} from "lucide-react";
import { SubtaskProposal } from "./SubtaskProposal";

export function TaskProposal({ task, allSubtasks, onUpdate, onStatusChange }) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [localPayload, setLocalPayload] = useState(task.payload);

  /* -----------------------------
     YOUR LOGIC (UNCHANGED)
  ------------------------------ */
  const subtasksForTask = allSubtasks.filter(
    (subtask) =>
      subtask.payload?.depends_on_task_key === task.payload?.temp_task_key
  );

  const save = () => {
    onUpdate(task.proposal_id, localPayload);
    setIsEditing(false);
  };

  const status = task.status ?? "PENDING";

  const statusColors = {
    PENDING: "border-l-blue-500 bg-gradient-to-r from-blue-50 to-white",
    APPROVED: "border-l-green-500 bg-gradient-to-r from-green-50 to-white",
    REJECTED: "border-l-red-500 bg-gradient-to-r from-red-50 to-white",
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className={`relative border-l-4 ${statusColors[status]} rounded-xl p-5 shadow-md hover:shadow-lg transition-all`}
    >
      {/* ================= HEADER ================= */}
      <div className="flex items-start justify-between gap-4 mb-4">
        <div className="flex-1 min-w-0">
          {isEditing ? (
            <div className="space-y-3">
              {Object.entries(localPayload).map(([key, value]) => {
                if (key === "subtasks") return null;

                return (
                  <div key={key}>
                    <label className="block text-xs font-medium text-gray-600 mb-1 capitalize">
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
                      className="w-full px-4 py-2 border-2 rounded-lg focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                );
              })}

              <div className="flex gap-2 pt-2">
                <button
                  onClick={save}
                  className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg"
                >
                  <Save className="w-4 h-4" />
                  Save
                </button>
                <button
                  onClick={() => {
                    setLocalPayload(task.payload);
                    setIsEditing(false);
                  }}
                  className="flex items-center gap-2 px-4 py-2 bg-gray-500 text-white rounded-lg"
                >
                  <XCircle className="w-4 h-4" />
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <>
              <div className="flex items-center gap-3 mb-2">
                <h3 className="text-lg font-bold text-gray-900">
                  {task.payload.task_name || "Task"}
                </h3>
                {subtasksForTask.length > 0 && (
                  <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full font-medium">
                    {subtasksForTask.length} subtask
                    {subtasksForTask.length !== 1 ? "s" : ""}
                  </span>
                )}
              </div>
              {task.payload.description && (
                <p className="text-sm text-gray-700">
                  {task.payload.description}
                </p>
              )}
            </>
          )}
        </div>

        {!isEditing && (
          <div className="flex items-center gap-2">
            {status === "PENDING" && (
              <>
                <button
                  onClick={() => onStatusChange(task.proposal_id, "APPROVED")}
                  className="p-2 bg-green-100 text-green-600 rounded-lg"
                >
                  <Check />
                </button>

                <button
                  onClick={() => setIsEditing(true)}
                  className="p-2 bg-blue-100 text-blue-600 rounded-lg"
                  title="Edit Task"
                >
                  <Edit2 className="w-5 h-5" />
                </button>
              </>
            )}

            <button
              onClick={() => onStatusChange(task.proposal_id, "REJECTED")}
              className="p-2 bg-red-100 text-red-600 rounded-lg"
            >
              <Trash2 />
            </button>

            {(status === "REJECTED" || status === "APPROVED") && (
              <button
                onClick={() => onStatusChange(task.proposal_id, "PENDING")}
                className="p-2 bg-gray-200 text-gray-700 rounded-lg"
              >
                <XCircle />
              </button>
            )}

            {subtasksForTask.length > 0 && (
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="p-2 bg-gray-100 text-gray-600 rounded-lg"
                title={isExpanded ? "Collapse" : "Expand"}
              >
                {isExpanded ? (
                  <ChevronUp className="w-5 h-5" />
                ) : (
                  <ChevronDown className="w-5 h-5" />
                )}
              </button>
            )}
          </div>
        )}
      </div>

      {/* ================= APPROVED BADGE ================= */}
      {status === "APPROVED" && !isEditing && (
        <div className="absolute top-3 right-3">
          <div className="flex items-center gap-1 px-3 py-1 bg-green-600 text-white text-xs rounded-full font-medium">
            <Check className="w-3 h-3" />
            Approved
          </div>
        </div>
      )}

      {/* ================= SUBTASKS ================= */}
      <AnimatePresence>
        {isExpanded && subtasksForTask.length > 0 && !isEditing && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="mt-4 space-y-3 pl-4 border-l-2 border-gray-200"
          >
            <AnimatePresence mode="popLayout">
              {subtasksForTask.map((subtask) => (
                <SubtaskProposal
                  key={subtask.id}
                  subtask={subtask}
                  onUpdate={(patch) => onUpdate(subtask.proposal_id, patch)}
                  onStatusChange={(status) =>
                    onStatusChange(subtask.proposal_id, status)
                  }
                ></SubtaskProposal>
              ))}
            </AnimatePresence>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
