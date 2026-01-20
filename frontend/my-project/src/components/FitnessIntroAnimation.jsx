import { motion, AnimatePresence } from "framer-motion";

import { Dumbbell, Heart, Zap, Target } from "lucide-react";

export function FitnessIntroAnimation({ onComplete }) {
  return (
    <motion.div
      className="fixed inset-0 z-50 bg-gradient-to-br from-rose-500 via-pink-500 to-orange-500 flex items-center justify-center overflow-hidden"
      initial={{ opacity: 1 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onAnimationComplete={() => {
        setTimeout(() => {
          if (onComplete) onComplete();
        }, 2000);
      }}
    >
      {/* Animated Background Circles */}
      <motion.div
        className="absolute w-96 h-96 bg-white/10 rounded-full"
        animate={{
          scale: [1, 1.5, 1],
          rotate: [0, 180, 360],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      <motion.div
        className="absolute w-64 h-64 bg-white/10 rounded-full"
        animate={{
          scale: [1, 1.3, 1],
          rotate: [360, 180, 0],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      {/* Main Content */}
      <div className="relative z-10 text-center text-white space-y-8">
        {/* Icons */}
        <div className="flex items-center justify-center gap-8">
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ delay: 0.2, type: "spring" }}
          >
            <Dumbbell className="w-16 h-16" />
          </motion.div>

          <motion.div
            initial={{ scale: 0, rotate: 180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ delay: 0.4, type: "spring" }}
          >
            <Heart className="w-16 h-16" />
          </motion.div>

          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ delay: 0.6, type: "spring" }}
          >
            <Zap className="w-16 h-16" />
          </motion.div>

          <motion.div
            initial={{ scale: 0, rotate: 180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ delay: 0.8, type: "spring" }}
          >
            <Target className="w-16 h-16" />
          </motion.div>
        </div>

        {/* Title */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1 }}
        >
          <h1 className="text-6xl font-bold mb-4">Fitness Trainer AI</h1>
          <p className="text-2xl opacity-90">Let's get started! 💪</p>
        </motion.div>

        {/* Loading Bar */}
        <motion.div
          className="w-64 h-2 bg-white/30 rounded-full mx-auto overflow-hidden"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2 }}
        >
          <motion.div
            className="h-full bg-white rounded-full"
            initial={{ width: 0 }}
            animate={{ width: "100%" }}
            transition={{
              delay: 1.3,
              duration: 1.5,
              ease: "easeInOut",
            }}
          />
        </motion.div>
      </div>
    </motion.div>
  );
}
