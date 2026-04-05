import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Dumbbell, Menu, Settings } from "lucide-react";

import { Button } from "./ui/Button";
import { TimelineExercise } from "./TimelineExercise";
import { FitnessIntroAnimation } from "./FitnessIntroAnimation";
import { CelebrationModal } from "./CelebrationModal";

import { useGetWeeklyFitnessRoutineQuery } from "../services/fitnessApi";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { ImageWithFallback } from "./figma/ImageWithFallback";

/* ------------------------------------------------
   HELPERS
------------------------------------------------- */

function getTodayKey() {
  return new Date()
    .toLocaleDateString("en-US", { weekday: "long" })
    .toLowerCase();
}

function getTodayDateString() {
  const date = new Date();
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
}

function timeToMinutes(timeStr) {
  const [h, m] = timeStr.split(":").map(Number);
  return h * 60 + m;
}

function timelineToBlocks(timeline) {
  return Object.entries(timeline).map(([range, block], index) => {
    const [start, end] = range.split("-");
    return {
      id: `${range}-${index}`,
      time: start,
      duration: Math.max(timeToMinutes(end) - timeToMinutes(start), 0),
      block_type: block.block_type,
      category: block.category,
      details: block.details,
      completed: false,
    };
  });
}

/* ------------------------------------------------
   COMPONENT
------------------------------------------------- */

export default function FitnessTab() {
  const navigate = useNavigate();
  const todayKey = getTodayKey();
  const dateString = getTodayDateString();

  const [showIntro, setShowIntro] = useState(true);
  const [blocks, setBlocks] = useState([]);
  const [showCelebration, setShowCelebration] = useState(false);

  const initializedRef = useRef(false);

  const { user } = useSelector((s) => s.auth);
  
  const {
    data: weeklyFitnessRoutine,
    isLoading,
    isError,
  } = useGetWeeklyFitnessRoutineQuery();

  const daySchedule = weeklyFitnessRoutine?.schedule?.[todayKey];
  console.log("todayKey:", todayKey);
  console.log(
    "schedule keys:",
    Object.keys(weeklyFitnessRoutine?.schedule || {}),
  );
  const storageKey = user ? `fitness_data_${user.user_id}_${dateString}` : null;
  const celebrationKey = user
    ? `fitness_celebrated_${user.user_id}_${dateString}`
    : null;

  /* ------------------------------------------------
     INIT / LOAD
  ------------------------------------------------- */
  useEffect(() => {
    if (!daySchedule?.timeline || !storageKey) return;

    if (!initializedRef.current) {
      const saved = localStorage.getItem(storageKey);
      setBlocks(
        saved ? JSON.parse(saved) : timelineToBlocks(daySchedule.timeline),
      );
      initializedRef.current = true;
    }
  }, [daySchedule, storageKey]);

  const completedCount = blocks.filter((b) => b.completed).length;
  const totalCount = blocks.length;
  const progress =
    totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

  useEffect(() => {
    if (!celebrationKey || totalCount === 0) return;

    const celebrated = localStorage.getItem(celebrationKey) === "true";
    if (progress === 100 && !celebrated) {
      setShowCelebration(true);
      localStorage.setItem(celebrationKey, "true");
    }
  }, [progress, totalCount, celebrationKey]);

  if (isLoading) return <div className="text-white p-6">Loading...</div>;
  if (isError) return <div className="text-red-400 p-6">Error loading</div>;
  if (!weeklyFitnessRoutine || !daySchedule)
    return <div className="text-white p-6">No workout today</div>;

  const plan = weeklyFitnessRoutine.plan_snapshot;

  const toggleBlock = (id) => {
    setBlocks((prev) => {
      const updated = prev.map((b) =>
        b.id === id ? { ...b, completed: !b.completed } : b,
      );

      if (storageKey) {
        localStorage.setItem(storageKey, JSON.stringify(updated));

        if (
          updated.filter((b) => b.completed).length < updated.length &&
          celebrationKey
        ) {
          localStorage.removeItem(celebrationKey);
        }
      }
      return updated;
    });
  };

  return (
    <>
      <AnimatePresence>
        {showIntro && (
          <FitnessIntroAnimation onComplete={() => setShowIntro(false)} />
        )}
      </AnimatePresence>

      {!showIntro && (
        <div className="relative min-h-screen overflow-hidden bg-black">
          {/* 🔥 UPDATED BACKGROUND ONLY */}
          <div className="fixed inset-0 z-0">
            <ImageWithFallback
              src="https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1600&q=80"
              alt="Fitness Background"
              className="w-full h-full object-cover"
            />

            <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-black/70" />

            <motion.div
              className="absolute inset-0 bg-gradient-to-br from-orange-500/10 via-transparent to-rose-500/10"
              animate={{ opacity: [0.3, 0.5, 0.3] }}
              transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
            />
          </div>

          {/* CONTENT (UNCHANGED) */}
          <div className="relative z-10">
            <div className="max-w-2xl mx-auto px-6 py-8 text-center">
              <h1 className="text-4xl font-bold text-white">
                {daySchedule.focus.toUpperCase()}
              </h1>
              <p className="text-white/80 mt-1">
                {plan.session_duration_min} min • {plan.goal.replace("_", " ")}
              </p>
            </div>

            <div className="grid grid-cols-3 gap-3 max-w-2xl mx-auto px-6 mb-8">
              {[
                ["Exercises", totalCount],
                ["Completed", completedCount],
                ["Progress", `${progress}%`],
              ].map(([label, value]) => (
                <div
                  key={label}
                  className="bg-white/10 backdrop-blur rounded-xl p-4 text-center border border-white/20"
                >
                  <p className="text-2xl font-bold text-white">{value}</p>
                  <p className="text-xs text-white/70">{label}</p>
                </div>
              ))}
            </div>

            <div className="max-w-2xl mx-auto px-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-bold text-white">Schedule</h3>
                <Button
                  variant="ghost"
                  className="text-white"
                  onClick={() => navigate("/fitness/week")}
                >
                  Week View →
                </Button>
              </div>

              <div className="relative">
                <div className="absolute left-[100px] top-0 bottom-0 border-l-2 border-dashed border-white/30" />

                <div className="space-y-8">
                  {blocks.map((block, index) => (
                    <TimelineExercise
                      key={block.id}
                      block={block}
                      index={index}
                      isLast={index === blocks.length - 1}
                      onToggle={() => toggleBlock(block.id)}
                    />
                  ))}
                </div>
              </div>
            </div>

            <div className="fixed bottom-6 left-0 right-0 px-6 max-w-2xl mx-auto">
              <Button className="w-full py-6 text-lg font-bold rounded-2xl bg-gradient-to-r from-orange-500 to-rose-500">
                {progress === 100 ? "Good Job!" : "Start Workout"}
              </Button>
            </div>
          </div>
        </div>
      )}

      <AnimatePresence>
        {showCelebration && (
          <CelebrationModal
            onClose={() => setShowCelebration(false)}
            calories={420}
            duration={plan.session_duration_min}
            exercises={totalCount}
          />
        )}
      </AnimatePresence>
    </>
  );
}
