import { motion } from "framer-motion";

import { Clock, Circle, CheckCircle2 } from "lucide-react";
import { Badge } from "./ui/Badge";

/* ------------------------------------
   UI DERIVATION HELPERS (LLM SAFE)
------------------------------------ */
function getIcon(block) {
  if (block.category === "strength") return "🏋️";
  if (block.category === "cardio") return "🔥";
  if (block.category === "mobility") return "🧘";
  if (block.block_type === "break") return "💧";
  return "⏱️";
}

function getTitle(block) {
  if (block.category === "strength" && block.details)
    return block.details.exercise_name;

  if (block.category === "cardio" && block.details)
    return block.details.activity;

  if (block.category === "mobility" && block.details) return block.details.name;

  if (block.block_type === "break") return "Rest / Water Break";

  return "Workout";
}

function getDescription(block) {
  if (!block.details) return null;

  if (block.category === "strength") {
    return `${block.details.sets} sets of ${block.details.reps} reps`;
  }

  if (block.category === "mobility") {
    return block.details.instruction ?? null;
  }

  if (block.category === "cardio") {
    return `Intensity: ${block.details.intensity}`;
  }

  return null;
}


/* ------------------------------------
   COMPONENT (UI UNCHANGED)
------------------------------------ */
export function TimelineExercise({ block, index, onToggle, isLast }) {
  const icon = getIcon(block);
  const title = getTitle(block);
  const description = getDescription(block);

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.08 }}
      className="relative flex items-start gap-4"
    >
      {/* Time */}
      <div className="w-20 text-right flex-shrink-0 pt-3">
        <p className="text-sm text-white/80 font-medium">{block.time}</p>
      </div>

      {/* Icon */}
      <div className="flex-shrink-0 relative">
        <motion.div
          onClick={onToggle} // ✅ IMPORTANT
          role="button"
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") onToggle();
          }}
          className={`
    w-14 h-14 rounded-full flex items-center justify-center shadow-lg relative z-10
    cursor-pointer select-none
    ${
      block.completed
        ? "bg-gradient-to-br from-green-400 to-emerald-500"
        : "bg-white/20 backdrop-blur-md border-2 border-white/40 hover:bg-white/30"
    }
  `}
          whileHover={{ scale: 1.12 }}
          whileTap={{ scale: 0.92 }} // ✅ tactile feedback
          animate={
            block.completed
              ? {
                  boxShadow: [
                    "0 0 0 0 rgba(16, 185, 129, 0.4)",
                    "0 0 0 12px rgba(16, 185, 129, 0)",
                  ],
                }
              : {}
          }
          transition={{
            boxShadow: { duration: 1.5, repeat: Infinity },
            scale: { type: "spring", stiffness: 300, damping: 20 },
          }}
        >
          <span className="text-2xl">{icon}</span>
        </motion.div>
      </div>

      {/* Card */}
      <motion.div
        className={`
          flex-1 rounded-2xl p-4 transition-all duration-300 cursor-pointer
          ${
            block.completed
              ? "bg-green-500/20 backdrop-blur-md border-2 border-green-400/50"
              : "bg-white/90 backdrop-blur-md border-2 border-white/50 hover:bg-white hover:shadow-lg"
          }
        `}
        onClick={onToggle}
        whileHover={{ y: -2 }}
      >
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <h4
                className={`text-lg font-bold ${
                  block.completed ? "text-white" : "text-gray-900"
                }`}
              >
                {title}
              </h4>

              {block.completed && (
                <motion.div
                  initial={{ scale: 0, rotate: -180 }}
                  animate={{ scale: 1, rotate: 0 }}
                >
                  <CheckCircle2 className="w-5 h-5 text-green-400" />
                </motion.div>
              )}
            </div>

            {description && (
              <p
                className={`text-sm mb-2 ${
                  block.completed ? "text-white/80" : "text-gray-600"
                }`}
              >
                {description}
              </p>
            )}

            <div className="flex items-center gap-2 flex-wrap">
              <Badge
                className={`text-xs ${
                  block.completed
                    ? "bg-white/20 text-white border-white/30"
                    : "bg-gray-100 text-gray-700 border-gray-200"
                }`}
              >
                <Clock className="w-3 h-3 mr-1" />
                {block.duration} min
              </Badge>

              {block.category === "strength" && (
                <Badge
                  className={`text-xs ${
                    block.completed
                      ? "bg-white/20 text-white border-white/30"
                      : "bg-orange-100 text-orange-700 border-orange-200"
                  }`}
                >
                  {block.details.sets} × {block.details.reps}
                </Badge>
              )}
            </div>
          </div>

          {/* Checkbox */}
          <motion.div
            className={`
              w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ml-3
              ${
                block.completed
                  ? "bg-green-500"
                  : "bg-white border-2 border-gray-300"
              }
            `}
            whileHover={{ scale: 1.15 }}
            whileTap={{ scale: 0.95 }}
          >
            {block.completed ? (
              <CheckCircle2 className="w-6 h-6 text-white" />
            ) : (
              <Circle className="w-6 h-6 text-gray-400" />
            )}
          </motion.div>
        </div>

        {/* Sets Progress */}
        {block.category === "strength" && !block.completed && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            className="mt-3 pt-3 border-t border-gray-200"
          >
            <div className="flex gap-1.5">
              {[...Array(block.details.sets)].map((_, i) => (
                <div
                  key={i}
                  className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden"
                >
                  <motion.div
                    className="h-full bg-gradient-to-r from-orange-400 to-rose-400"
                    initial={{ width: 0 }}
                    whileInView={{ width: "100%" }}
                    transition={{ delay: i * 0.1, duration: 0.5 }}
                  />
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </motion.div>
    </motion.div>
  );
}
