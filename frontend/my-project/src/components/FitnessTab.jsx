import { useEffect, useRef, useState } from "react";
import { AnimatePresence } from "framer-motion";
import { Dumbbell, Menu, Settings } from "lucide-react";

import { Button } from "./ui/Button";
import { TimelineExercise } from "./TimelineExercise";
import { FitnessIntroAnimation } from "./FitnessIntroAnimation";
import { CelebrationModal } from "./CelebrationModal";

import { useGetWeeklyFitnessRoutineQuery } from "../services/fitnessApi";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

/* ------------------------------------------------
   HELPERS
------------------------------------------------- */

function getTodayKey() {
  return new Date()
    .toLocaleDateString("en-US", { weekday: "long" })
    .toLowerCase();
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

  const [showIntro, setShowIntro] = useState(true);
  const [blocks, setBlocks] = useState([]);
  const [showCelebration, setShowCelebration] = useState(false);

  const initializedRef = useRef(false); // 🔒 important

  const { user } = useSelector((s) => s.auth);

  const {
    data: weeklyFitnessRoutine,
    isLoading,
    isError,
  } = useGetWeeklyFitnessRoutineQuery(user?.user_id);

  const daySchedule = weeklyFitnessRoutine?.schedule?.[todayKey];

  /* ------------------------------------------------
     INITIALIZE BLOCKS (ONCE PER DAY)
  ------------------------------------------------- */
  useEffect(() => {
    if (!daySchedule?.timeline) return;

    if (!initializedRef.current) {
      setBlocks(timelineToBlocks(daySchedule.timeline));
      initializedRef.current = true;
      setShowCelebration(false);
    }
  }, [daySchedule]);

  /* ------------------------------------------------
     PROGRESS
  ------------------------------------------------- */
  const completedCount = blocks.filter((b) => b.completed).length;
  const totalCount = blocks.length;

  const progress =
    totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

  /* ------------------------------------------------
     CELEBRATION TRIGGER
  ------------------------------------------------- */
  useEffect(() => {
    if (progress === 100 && totalCount > 0) {
      setShowCelebration(true);
    }
  }, [progress, totalCount]);

  /* ------------------------------------------------
     GUARDS
  ------------------------------------------------- */
  if (isLoading) {
    return <div className="text-white p-6">Loading workout…</div>;
  }

  if (isError) {
    return <div className="text-red-400 p-6">Failed to load routine</div>;
  }

  if (!weeklyFitnessRoutine || !daySchedule) {
    return <div className="text-white p-6">No workout scheduled today</div>;
  }

  const plan = weeklyFitnessRoutine.plan_snapshot;

  /* ------------------------------------------------
     ACTIONS
  ------------------------------------------------- */
  const toggleBlock = (id) => {
    setBlocks((prev) =>
      prev.map((b) => (b.id === id ? { ...b, completed: !b.completed } : b)),
    );
  };

  /* ------------------------------------------------
     UI
  ------------------------------------------------- */
  return (
    <>
      <AnimatePresence>
        {showIntro && (
          <FitnessIntroAnimation onComplete={() => setShowIntro(false)} />
        )}
      </AnimatePresence>

      {!showIntro && (
        <div className="relative min-h-screen overflow-hidden bg-black">
          {/* Background */}
          <div className="fixed inset-0 -z-10">
            <img
              src="https://images.unsplash.com/photo-1534438327276-14e5300c3a48"
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-black/70" />
          </div>

          {/* Top Bar */}
          <div className="backdrop-blur bg-white/10 border-b border-white/20">
            <div className="flex items-center justify-between px-6 py-4">
              <Menu className="text-white" />
              <div className="flex items-center gap-2 text-white font-semibold">
                <Dumbbell className="w-5 h-5" />
                FitLife
              </div>
              <Settings className="text-white" />
            </div>
          </div>

          {/* Header */}
          <div className="max-w-2xl mx-auto px-6 py-8 text-center">
            <p className="text-white/70 text-sm">Today's Workout</p>
            <h1 className="text-4xl font-bold text-white">
              {daySchedule.focus.toUpperCase()} DAY WORKOUT
            </h1>
            <p className="text-white/80 mt-1">
              {plan.session_duration_min} minutes •{" "}
              {plan.goal.replace("_", " ")}
            </p>
          </div>

          {/* Stats */}
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

          {/* Timeline */}
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

          {/* Action */}
          <div className="max-w-2xl mx-auto px-6 py-10">
            <Button className="w-full py-6 text-lg font-bold rounded-2xl bg-gradient-to-r from-orange-500 to-rose-500">
              Start Workout
            </Button>
          </div>
        </div>
      )}

      {/* 🔥 Celebration Modal (TOP LEVEL) */}
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

/* ------------------------------------------------
   INFO TILE
------------------------------------------------- */
function Info({ label, value }) {
  return (
    <div className="bg-white/10 backdrop-blur rounded-xl p-4 border border-white/20">
      <p className="text-xs text-white/60">{label}</p>
      <p className="text-sm font-semibold text-white capitalize">{value}</p>
    </div>
  );
}
