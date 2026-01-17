import { useState } from "react";
import { motion } from "framer-motion";
import { Check, Edit2, Trash2, Save, XCircle } from "lucide-react";

export function SubtaskProposal({ subtask, onUpdate, onStatusChange }) {
  const [isEditing, setIsEditing] = useState(false);
  const [localPayload, setLocalPayload] = useState(subtask.payload);

  const save = () => {
    onUpdate(localPayload);
    setIsEditing(false);
  };

  // ✅ CRITICAL FIX
  const status = subtask.status ?? "PENDING";

  const statusColors = {
    PENDING: "border-l-amber-400 bg-amber-50",
    APPROVED: "border-l-green-400 bg-green-50",
    REJECTED: "border-l-red-400 bg-red-50",
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, x: -100 }}
      className={`relative border-l-4 ${statusColors[status]} rounded-lg p-4 shadow-sm hover:shadow-md transition-all`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          {isEditing ? (
            <div className="space-y-3">
              {Object.entries(localPayload).map(([key, value]) => (
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
                    className="w-full px-3 py-2 border rounded-lg"
                  />
                </div>
              ))}

              <div className="flex gap-2">
                <button
                  onClick={save}
                  className="flex items-center gap-1 px-3 py-1.5 bg-green-600 text-white rounded-lg text-sm"
                >
                  <Save className="w-4 h-4" />
                  Save
                </button>
                <button
                  onClick={() => {
                    setLocalPayload(subtask.payload);
                    setIsEditing(false);
                  }}
                  className="flex items-center gap-1 px-3 py-1.5 bg-gray-500 text-white rounded-lg text-sm"
                >
                  <XCircle className="w-4 h-4" />
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <>
              <h4 className="text-sm font-semibold text-gray-800 mb-1">
                {subtask.payload.subtask_name || "Subtask"}
              </h4>

              <div className="text-xs text-gray-600 space-y-0.5">
                {Object.entries(subtask.payload).map(([key, value]) => {
                  if (key === "subtask_name") return null;
                  if (!value) return null;

                  return (
                    <div key={key}>
                      <span className="font-medium capitalize">
                        {key.replace(/_/g, " ")}:
                      </span>{" "}
                      {String(value)}
                    </div>
                  );
                })}
              </div>
            </>
          )}
        </div>

        {/* ===== ACTION BUTTONS ===== */}
        {!isEditing && (
          <div className="flex items-center gap-2">
            {status === "PENDING" && (
              <>
                <button
                  onClick={() => onStatusChange("APPROVED")}
                  className="p-1.5 bg-green-100 text-green-600 rounded-lg"
                >
                  <Check />
                </button>

                <button
                  onClick={() => setIsEditing(true)}
                  className="p-1.5 bg-blue-100 text-blue-600 rounded-lg"
                >
                  <Edit2 />
                </button>
              </>
            )}

            <button
              onClick={() => onStatusChange("REJECTED")}
              className="p-1.5 bg-red-100 text-red-600 rounded-lg"
            >
              <Trash2 />
            </button>

            {(status === "REJECTED" || status === "APPROVED") && (
              <button
                onClick={() => onStatusChange("PENDING")}
                className="p-1.5 bg-gray-200 text-gray-700 rounded-lg"
              >
                <XCircle />
              </button>
            )}
          </div>
        )}
      </div>

      {/* ===== APPROVED BADGE ===== */}
      {status === "APPROVED" && !isEditing && (
        <div className="absolute top-2 right-2">
          <div className="flex items-center gap-1 px-2 py-0.5 bg-green-600 text-white text-xs rounded-full">
            <Check className="w-3 h-3" />
            Approved
          </div>
        </div>
      )}
    </motion.div>
  );
}
