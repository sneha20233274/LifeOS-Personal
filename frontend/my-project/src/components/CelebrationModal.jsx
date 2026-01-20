import { motion, AnimatePresence } from "framer-motion";
import { Trophy, X, Sparkles } from "lucide-react";
import { Button } from "./ui/Button";

export function CelebrationModal({
  open,
  onClose,
  calories,
  duration,
  exercises,
}) {
  if (!open) return null;

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.7 }}
          animate={{ scale: 1 }}
          exit={{ scale: 0.7 }}
          onClick={(e) => e.stopPropagation()}
          className="bg-white/20 backdrop-blur-xl border border-white/40 rounded-3xl p-8 text-white w-[90%] max-w-md relative"
        >
          <Button
            variant="ghost"
            size="icon"
            className="absolute top-4 right-4"
            onClick={onClose}
          >
            <X />
          </Button>

          <div className="text-center space-y-4">
            <div className="mx-auto w-24 h-24 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center">
              <Trophy className="w-12 h-12" />
            </div>

            <h2 className="text-4xl font-bold">Congratulations 🎉</h2>
            <p className="text-white/80">Workout completed successfully!</p>

            <div className="grid grid-cols-3 gap-3 mt-6">
              <Stat label="Calories" value={calories} />
              <Stat label="Minutes" value={duration} />
              <Stat label="Exercises" value={exercises} />
            </div>

            <Button
              className="w-full mt-6 bg-white/30 hover:bg-white/40"
              onClick={onClose}
            >
              <Sparkles className="mr-2" />
              Awesome!
            </Button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

function Stat({ label, value }) {
  return (
    <div className="bg-white/20 rounded-xl p-3 text-center">
      <div className="text-2xl font-bold">{value}</div>
      <div className="text-xs text-white/70">{label}</div>
    </div>
  );
}
