import { motion, AnimatePresence } from "framer-motion";

import { Clock, CheckCircle2 } from "lucide-react";
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
  if (block.category === "strength") return block.details.exercise_name;
  if (block.category === "cardio") return block.details.activity;
  if (block.category === "mobility") return block.details.name;
  if (block.block_type === "break") return "Rest / Water Break";
  return "Workout Block";
}

function getDescription(block) {
  if (block.category === "strength") {
    return `${block.details.sets} sets × ${block.details.reps} reps`;
  }
  if (block.category === "mobility") {
    return block.details.instruction;
  }
  if (block.category === "cardio") {
    return `Intensity: ${block.details.intensity}`;
  }
  return "Recovery period";
}

/* ------------------------------------
   COMPONENT
------------------------------------ */
export function CircularExerciseTimeline({ blocks, onToggle }) {
  return (
    <div className="space-y-6">
      {blocks.map((block, index) => (
        <motion.div
          key={block.id}
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.1 }}
          className="flex items-center gap-6 group"
        >
          {/* Time */}
          <div className="w-20 text-right">
            <p className="text-sm text-white/70 font-medium">{block.time}</p>
          </div>

          {/* Icon */}
          <motion.div
            whileHover={{ scale: 1.1 }}
            className={`
              relative w-16 h-16 rounded-full flex items-center justify-center
              ${
                block.completed
                  ? "bg-gradient-to-br from-green-400 to-emerald-500 border-4 border-green-300"
                  : "bg-white/20 backdrop-blur-xl border-4 border-white/40"
              }
            `}
          >
            <span className="text-3xl">{getIcon(block)}</span>
            {block.completed && (
              <div className="absolute -bottom-1 -right-1 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center border-2 border-white">
                <CheckCircle2 className="w-4 h-4 text-white" />
              </div>
            )}
          </motion.div>

          {/* Card */}
          <div
            onClick={() => onToggle(block.id)}
            className={`
              flex-1 rounded-2xl p-5 border cursor-pointer transition-all
              ${
                block.completed
                  ? "border-green-400/50 bg-green-400/10"
                  : "border-white/20 bg-white/10 hover:bg-white/15"
              }
            `}
          >
            <div className="flex justify-between items-center">
              <div>
                <h4 className="text-lg font-bold text-white">
                  {getTitle(block)}
                </h4>

                <div className="flex flex-wrap gap-2 mt-2">
                  <Badge className="bg-white/20 text-white text-xs">
                    <Clock className="w-3 h-3 mr-1" />
                    {block.duration} min
                  </Badge>

                  {block.category === "strength" && (
                    <Badge className="bg-white/20 text-white text-xs">
                      {block.details.sets} × {block.details.reps}
                    </Badge>
                  )}

                  {block.category === "cardio" && (
                    <Badge className="bg-orange-400/30 text-white text-xs">
                      {block.details.intensity.toUpperCase()}
                    </Badge>
                  )}
                </div>
              </div>

              {/* Checkbox */}
              <div
                className={`
                  w-10 h-10 rounded-full border-2 flex items-center justify-center
                  ${
                    block.completed
                      ? "bg-green-500 border-green-400"
                      : "bg-white/10 border-white/40"
                  }
                `}
              >
                {block.completed && (
                  <CheckCircle2 className="w-6 h-6 text-white" />
                )}
              </div>
            </div>

            {/* Extra Info */}
            <p className="text-xs text-white/70 mt-3">
              {getDescription(block)}
            </p>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
