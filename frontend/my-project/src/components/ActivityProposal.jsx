import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Check,
  Edit2,
  Trash2,
  Clock,
  Save,
  XCircle,
  Calendar,
  CheckCircle2,
} from "lucide-react";
import { categoryConfigs } from "../app/categoryConfig";

export function ActivityProposal({ activity, onUpdate, onStatusChange }) {
  const [isEditing, setIsEditing] = useState(false);

  /* 🔑 Normalize backend → UI */
  const [localPayload, setLocalPayload] = useState(() => ({
    ...activity.payload,
    summary_category: Array.isArray(activity.payload.summary_category)
      ? activity.payload.summary_category
      : activity.payload.summary_category
        ? [activity.payload.summary_category]
        : [],
  }));

  /* ⏱ Auto-calc duration */
  useEffect(() => {
    if (localPayload.start_ts && localPayload.end_ts) {
      const start = new Date(localPayload.start_ts);
      const end = new Date(localPayload.end_ts);
      if (end > start) {
        const minutes = Math.round((end - start) / 60000);
        if (minutes !== localPayload.duration_minutes) {
          setLocalPayload((p) => ({ ...p, duration_minutes: minutes }));
        }
      }
    }
  }, [localPayload.start_ts, localPayload.end_ts]);

  const statusColors = {
    PENDING:
      "border-cyan-500 bg-gradient-to-br from-cyan-50 via-white to-cyan-50",
    APPROVED:
      "border-green-500 bg-gradient-to-br from-green-50 via-white to-green-50",
    REJECTED:
      "border-red-500 bg-gradient-to-br from-red-50 via-white to-red-50",
  };

  const toggleCategory = (category) => {
    setLocalPayload((prev) => ({
      ...prev,
      summary_category: prev.summary_category.includes(category)
        ? prev.summary_category.filter((c) => c !== category)
        : [...prev.summary_category, category],
    }));
  };

  const save = () => {
    onUpdate(activity.proposal_id, localPayload);
    setIsEditing(false);
  };

  return (
    <motion.div
      layout
      className={`border-2 ${statusColors[activity.status]} rounded-2xl p-6 shadow-xl`}
    >
      <div className="flex gap-6">
        {/* ================= LEFT ================= */}
        <div className="flex-1">
          {isEditing ? (
            <div className="space-y-6">
              {/* NAME */}
              <div>
                <label className="text-sm font-medium text-gray-600">
                  Activity Name
                </label>
                <input
                  value={localPayload.activity_name || ""}
                  onChange={(e) =>
                    setLocalPayload((p) => ({
                      ...p,
                      activity_name: e.target.value,
                    }))
                  }
                  className="w-full px-4 py-3 border-2 rounded-xl"
                />
              </div>

              {/* DESCRIPTION */}
              <div>
                <label className="text-sm font-medium text-gray-600">
                  Description
                </label>
                <textarea
                  value={localPayload.activity_description || ""}
                  onChange={(e) =>
                    setLocalPayload((p) => ({
                      ...p,
                      activity_description: e.target.value,
                    }))
                  }
                  className="w-full px-4 py-3 border-2 rounded-xl"
                />
              </div>

              {/* TIME */}
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-600 mb-1">
                    <Calendar className="w-4 h-4 text-green-600" />
                    Start Time
                  </label>
                  <input
                    type="datetime-local"
                    value={localPayload.start_ts || ""}
                    onChange={(e) =>
                      setLocalPayload((p) => ({
                        ...p,
                        start_ts: e.target.value,
                      }))
                    }
                    className="w-full px-4 py-3 border-2 rounded-xl"
                  />
                </div>

                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-600 mb-1">
                    <Calendar className="w-4 h-4 text-green-600" />
                    End Time
                  </label>
                  <input
                    type="datetime-local"
                    value={localPayload.end_ts || ""}
                    onChange={(e) =>
                      setLocalPayload((p) => ({
                        ...p,
                        end_ts: e.target.value,
                      }))
                    }
                    className="w-full px-4 py-3 border-2 rounded-xl"
                  />
                </div>
              </div>

              {/* DURATION */}
              {localPayload.duration_minutes > 0 && (
                <div className="flex items-center gap-2 px-4 py-3 rounded-xl bg-purple-50 border border-purple-200">
                  <Clock className="w-5 h-5 text-purple-600" />
                  <span className="font-semibold text-purple-700">
                    Duration: {localPayload.duration_minutes} minutes
                  </span>
                </div>
              )}

              {/* ================= CATEGORY GRID (NO SCROLL) ================= */}
              <div>
                <label className="text-sm font-medium text-gray-600 mb-3 block">
                  Categories (Select multiple)
                </label>

                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {Object.values(categoryConfigs).map((cfg) => {
                    const selected = localPayload.summary_category.includes(
                      cfg.name,
                    );

                    return (
                      <motion.button
                        key={cfg.name}
                        onClick={() => toggleCategory(cfg.name)}
                        whileHover={{ scale: 1.03 }}
                        whileTap={{ scale: 0.97 }}
                        className={`relative h-36 rounded-xl overflow-hidden border-2 ${
                          selected
                            ? "border-green-500 ring-4 ring-green-200"
                            : "border-gray-200"
                        }`}
                      >
                        {/* IMAGE */}
                        <img
                          src={cfg.image}
                          alt={cfg.label}
                          className="absolute inset-0 w-full h-full object-cover"
                        />

                        {/* OVERLAY */}
                        <div className="absolute inset-0 bg-black/50" />

                        {/* LABEL */}
                        <div className="relative z-10 h-full flex flex-col items-center justify-center text-white">
                          <cfg.icon className="w-8 h-8 mb-1" />
                          <span className="font-semibold text-lg">
                            {cfg.label}
                          </span>
                        </div>

                        {selected && (
                          <div className="absolute top-2 right-2 bg-green-500 rounded-full p-1">
                            <CheckCircle2 className="w-5 h-5 text-white" />
                          </div>
                        )}
                      </motion.button>
                    );
                  })}
                </div>
              </div>

              {/* ACTIONS */}
              <div className="flex gap-3">
                <button
                  onClick={save}
                  className="px-5 py-2 bg-green-600 text-white rounded-xl flex items-center gap-2"
                >
                  <Save className="w-5 h-5" />
                  Save
                </button>
                <button
                  onClick={() => {
                    setLocalPayload(activity.payload);
                    setIsEditing(false);
                  }}
                  className="px-5 py-2 bg-gray-500 text-white rounded-xl flex items-center gap-2"
                >
                  <XCircle className="w-5 h-5" />
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <>
              {/* VIEW MODE */}
              <h2 className="text-2xl font-bold mb-2">
                {localPayload.activity_name}
              </h2>
              <p className="text-gray-700 mb-3">
                {localPayload.activity_description}
              </p>

              <div className="flex flex-wrap gap-2 mb-3">
                {localPayload.summary_category.map((cat) => (
                  <span
                    key={cat}
                    className="px-3 py-1 bg-cyan-100 text-cyan-700 rounded-full text-sm"
                  >
                    {categoryConfigs[cat]?.label || cat}
                  </span>
                ))}
              </div>

              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Clock className="w-4 h-4" />
                {localPayload.duration_minutes} minutes
              </div>
            </>
          )}
        </div>

        {/* ================= RIGHT ACTIONS ================= */}
        {!isEditing && (
          <div className="flex flex-col gap-2">
            {activity.status === "PENDING" && (
              <>
                <button
                  onClick={() =>
                    onStatusChange(activity.proposal_id, "APPROVED")
                  }
                  className="p-3 bg-green-100 text-green-600 rounded-xl"
                >
                  <Check />
                </button>
                <button
                  onClick={() => setIsEditing(true)}
                  className="p-3 bg-blue-100 text-blue-600 rounded-xl"
                >
                  <Edit2 />
                </button>
              </>
            )}

            <button
              onClick={() => onStatusChange(activity.proposal_id, "REJECTED")}
              className="p-3 bg-red-100 text-red-600 rounded-xl"
            >
              <Trash2 />
            </button>

            {(activity.status === "APPROVED" ||
              activity.status === "REJECTED") && (
              <button
                onClick={() => onStatusChange(activity.proposal_id, "PENDING")}
                className="p-3 bg-gray-200 rounded-xl"
              >
                <XCircle />
              </button>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
}
