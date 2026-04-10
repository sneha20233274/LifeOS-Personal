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
     🔥 FIXED DATA SOURCE
  ------------------------------ */
  const subtasksForTask = allSubtasks || [];

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
      className={`relative border-l-4 ${statusColors[status]} rounded-xl p-5 shadow-md`}
    >
      {/* HEADER */}
      <div className="flex justify-between mb-4">
        <div>
          {isEditing ? (
            <div>
              {Object.entries(localPayload).map(([key, value]) => {
                if (key === "subtasks") return null;

                return (
                  <input
                    key={key}
                    value={value}
                    onChange={(e) =>
                      setLocalPayload((prev) => ({
                        ...prev,
                        [key]: e.target.value,
                      }))
                    }
                    className="border p-2 mb-2 w-full"
                  />
                );
              })}

              <button onClick={save}>Save</button>
            </div>
          ) : (
            <>
              <h3 className="font-bold text-lg">{task.payload.task_name}</h3>
              <p className="text-sm text-gray-600">
                {task.payload.description}
              </p>

              <p className="text-xs mt-1">{subtasksForTask.length} subtasks</p>
            </>
          )}
        </div>

        {!isEditing && (
          <div className="flex gap-2">
            <button
              onClick={() => onStatusChange(task.proposal_id, "APPROVED")}
            >
              <Check />
            </button>

            <button onClick={() => setIsEditing(true)}>
              <Edit2 />
            </button>

            <button
              onClick={() => onStatusChange(task.proposal_id, "REJECTED")}
            >
              <Trash2 />
            </button>
          </div>
        )}
      </div>

      {/* SUBTASKS */}
      <AnimatePresence>
        {isExpanded && subtasksForTask.length > 0 && (
          <motion.div className="pl-4 border-l mt-4 space-y-2">
            {subtasksForTask.map((subtask) => (
              <SubtaskProposal
                key={subtask.proposal_id}
                subtask={subtask}
                onUpdate={(patch) => onUpdate(subtask.proposal_id, patch)}
                onStatusChange={(status) =>
                  onStatusChange(subtask.proposal_id, status)
                }
              />
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
