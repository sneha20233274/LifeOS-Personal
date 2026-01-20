import { motion } from "framer-motion";
import { ChevronLeft, Dumbbell, TrendingUp, Clock, Flame } from "lucide-react";
import { Button } from "./ui/Button";
import { useNavigate } from "react-router-dom";
import { useGetWeeklyFitnessRoutineQuery } from "../services/fitnessApi";
import { useSelector } from "react-redux";
import { Badge } from "./ui/Badge";
import { ImageWithFallback } from "./figma/ImageWithFallback";

const DAY_COLORS = {
  monday: "from-pink-400 to-rose-500",
  tuesday: "from-orange-400 to-amber-500",
  wednesday: "from-emerald-400 to-green-500",
  thursday: "from-sky-400 to-blue-500",
  friday: "from-violet-400 to-purple-500",
  saturday: "from-yellow-400 to-orange-500",
  sunday: "from-gray-400 to-gray-600",
};

/* ------------------------------------
   Helpers
------------------------------------ */
function renderDetails(block) {
  if (!block.details) return null;

  return Object.entries(block.details).map(([k, v]) => (
    <p key={k} className="text-xs text-gray-600">
      <span className="capitalize">{k.replace("_", " ")}:</span>{" "}
      <span className="font-medium">{String(v)}</span>
    </p>
  ));
}

export function WeeklyViewFitness() {
  const navigate = useNavigate();
  const { user } = useSelector((s) => s.auth);

  const { data: routine, isLoading } = useGetWeeklyFitnessRoutineQuery(
    user?.user_id,
  );

  if (isLoading || !routine) {
    return <div className="text-white p-6">Loading week view…</div>;
  }

  const plan = routine.plan_snapshot;

  return (
    <div className="relative min-h-screen bg-black text-white overflow-hidden">
      {/* ✅ UPDATED BACKGROUND (ONLY THIS PART CHANGED) */}
      <div className="fixed inset-0 z-0">
        <ImageWithFallback
          src="https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=1600&q=80"
          alt="Fitness Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-black/70" />
      </div>

      <div className="relative z-10">
        {/* HEADER */}
        <div className="px-6 py-4 border-b border-white/20 backdrop-blur">
          <Button
            variant="ghost"
            onClick={() => navigate(-1)}
            className="text-white"
          >
            <ChevronLeft className="w-4 h-4 mr-1" />
            Back
          </Button>

          <h1 className="text-3xl font-bold mt-2">Weekly Workout Plan</h1>
          <p className="text-white/70">Complete 7-day routine overview</p>
        </div>

        {/* PLAN SUMMARY */}
        <div className="max-w-2xl mx-auto px-6 py-6 grid grid-cols-2 gap-4">
          <Info label="Goal" value={plan.goal} />
          <Info label="Experience" value={plan.experience_level} />
          <Info label="Split" value={plan.training_split} />
          <Info
            label="Intensity"
            value={`${plan.intensity.level} (RPE ${plan.intensity.rpe_range.join(
              "-",
            )})`}
          />
          <Info
            label="Frequency"
            value={`${plan.weekly_frequency} days/week`}
          />
          <Info label="Sleep" value={`${plan.recovery.sleep_hours} hours`} />
        </div>

        {/* DAYS */}
        <div className="max-w-2xl mx-auto px-6 pb-10 space-y-6">
          {Object.entries(routine.schedule).map(([dayKey, day], index) => (
            <motion.div
              key={dayKey}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="bg-white/95 text-gray-900 rounded-2xl shadow-xl overflow-hidden"
            >
              {/* DAY HEADER */}
              <div
                className={`px-5 py-4 text-white bg-gradient-to-r ${DAY_COLORS[dayKey]}`}
              >
                <h3 className="text-xl font-bold capitalize">{dayKey}</h3>
                <p className="text-sm opacity-90">
                  Focus: {day.focus.replace("_", " ")}
                </p>
              </div>

              {/* TIMELINE */}
              <div className="p-5 space-y-4">
                {Object.entries(day.timeline).map(([time, block]) => (
                  <div key={time} className="border rounded-xl p-4 bg-gray-50">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-semibold">{time}</span>

                      <Badge className="capitalize bg-purple-100 text-purple-700">
                        {block.block_type}
                      </Badge>
                    </div>

                    <div className="flex gap-2 mb-2 flex-wrap">
                      <Badge className="bg-gray-200 text-gray-700 capitalize">
                        {block.category}
                      </Badge>
                      <Badge className="bg-blue-100 text-blue-700">
                        <Clock className="w-3 h-3 mr-1" />
                        Session
                      </Badge>
                    </div>

                    <div className="space-y-1">{renderDetails(block)}</div>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ------------------------------------
   Small UI helper
------------------------------------ */
function Info({ label, value }) {
  return (
    <div className="bg-white/10 backdrop-blur rounded-xl p-4 border border-white/20">
      <p className="text-xs text-white/60">{label}</p>
      <p className="text-sm font-semibold text-white capitalize">{value}</p>
    </div>
  );
}
