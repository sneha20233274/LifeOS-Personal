import { motion } from "framer-motion";
import { ChevronLeft, Dumbbell, TrendingUp } from "lucide-react";
import { Button } from "./ui/Button";
import { useNavigate } from "react-router-dom";
import { useGetWeeklyFitnessRoutineQuery } from "../services/fitnessApi";
import { useSelector } from "react-redux";
import { Badge } from "./ui/Badge";

const DAY_COLORS = {
  monday: "from-pink-400 to-rose-500",
  tuesday: "from-orange-400 to-amber-500",
  wednesday: "from-emerald-400 to-green-500",
  thursday: "from-sky-400 to-blue-500",
  friday: "from-violet-400 to-purple-500",
  saturday: "from-yellow-400 to-orange-500",
  sunday: "from-gray-400 to-gray-600",
};

export function WeeklyViewFitness() {
  const navigate = useNavigate();
  const { user } = useSelector((s) => s.auth);

  const { data: routine, isLoading } = useGetWeeklyFitnessRoutineQuery(
    user?.user_id,
  );

  if (isLoading || !routine) {
    return <div className="text-white p-6">Loading week view…</div>;
  }

  return (
    <div className="relative min-h-screen bg-black text-white">
      {/* SAME BACKGROUND FEEL */}
      <div className="fixed inset-0 -z-10">
        <img
          src="https://images.unsplash.com/photo-1534438327276-14e5300c3a48"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/70" />
      </div>

      {/* HEADER */}
      <div className="px-6 py-4 border-b border-white/20 backdrop-blur">
        <Button
          variant="ghost"
          onClick={() => navigate(-1)}
          className="text-white"
        >
          ← Back
        </Button>

        <h1 className="text-3xl font-bold mt-2">Weekly Workout Plan</h1>
        <p className="text-white/70">Your full 7-day fitness routine</p>
      </div>

      {/* DAYS */}
      <div className="max-w-2xl mx-auto px-6 py-8 space-y-4">
        {Object.entries(routine.schedule).map(([dayKey, day], index) => (
          <motion.div
            key={dayKey}
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            className="bg-white/90 text-gray-900 rounded-2xl p-5 shadow-lg"
          >
            <div className="flex items-center gap-4">
              {/* DAY CIRCLE */}
              <div
                className={`w-14 h-14 rounded-full bg-gradient-to-br ${
                  DAY_COLORS[dayKey]
                } flex items-center justify-center text-xl`}
              >
                💪
              </div>

              {/* INFO */}
              <div className="flex-1">
                <h3 className="text-xl font-bold capitalize">{dayKey}</h3>
                <p className="text-sm text-gray-600">
                  Focus: {day.focus.replace("_", " ")}
                </p>

                <div className="flex gap-2 mt-2 flex-wrap">
                  <Badge className="bg-orange-100 text-orange-700">
                    <Dumbbell className="w-3 h-3 mr-1" />
                    {Object.keys(day.timeline).length} blocks
                  </Badge>
                  <Badge className="bg-blue-100 text-blue-700">
                    <TrendingUp className="w-3 h-3 mr-1" />
                    Active day
                  </Badge>
                </div>
              </div>

              <span className="text-xl">→</span>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
