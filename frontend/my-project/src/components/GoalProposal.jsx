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

export function GoalProposal({ goal, onUpdate, onStatusChange }) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [localPayload, setLocalPayload] = useState(goal.payload);

  /* -----------------------------
     DERIVED DATA (🔥 FIXED)
  ------------------------------ */
  const tasks = goal.tasks || [];

  const totalSubtasks = tasks.reduce(
    (acc, t) => acc + (t.subtasks?.length || 0),
    0,
  );

  const save = () => {
    onUpdate(goal.proposal_id, localPayload);
    setIsEditing(false);
  };

  /* -----------------------------
     STATUS COLORS
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
      } rounded-2xl p-6 shadow-xl`}
    >
      {/* HEADER */}
      <div className="flex justify-between mb-5">
        <div className="flex-1">
          {isEditing ? (
            <div className="space-y-4">
              {Object.entries(localPayload).map(([key, value]) => (
                <input
                  key={key}
                  value={value}
                  onChange={(e) =>
                    setLocalPayload((prev) => ({
                      ...prev,
                      [key]: e.target.value,
                    }))
                  }
                  className="w-full border p-2 rounded"
                />
              ))}

              <button onClick={save}>Save</button>
            </div>
          ) : (
            <>
              <h2 className="text-2xl font-bold flex items-center gap-2">
                <Target className="text-purple-600" />
                {goal.payload.goal_name}
              </h2>

              <p className="text-gray-600 mt-2">{goal.payload.description}</p>

              <div className="mt-3 text-sm flex gap-3">
                <span>{tasks.length} tasks</span>
                <span>{totalSubtasks} subtasks</span>
              </div>
            </>
          )}
        </div>

        {/* ACTIONS */}
        {!isEditing && (
          <div className="flex gap-2">
            <button
              onClick={() => onStatusChange(goal.proposal_id, "APPROVED")}
            >
              <Check />
            </button>

            <button onClick={() => setIsEditing(true)}>
              <Edit2 />
            </button>

            <button
              onClick={() => onStatusChange(goal.proposal_id, "REJECTED")}
            >
              <Trash2 />
            </button>
          </div>
        )}
      </div>

      {/* TASKS */}
      <AnimatePresence>
        {isExpanded && tasks.length > 0 && (
          <motion.div className="mt-6 space-y-4">
            {tasks.map((task) => (
              <TaskProposal
                key={task.proposal_id}
                task={task}
                allSubtasks={task.subtasks}
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
