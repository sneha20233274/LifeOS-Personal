import { useState } from "react";
import { ChevronDown, ChevronUp, Sparkles } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const suggestions = [
  {
    title: "🎯 Goals",
    items: [
      {
        label: "Create a structured goal",
        text: "Help me create a goal to crack DSA in 60 days with a proper roadmap",
      },
      {
        label: "Reading habit goal",
        text: "Create a goal to read 50 pages daily and track consistency",
      },
    ],
  },
  {
    title: "🧠 Analytics",
    items: [
      {
        label: "Productivity breakdown",
        text: "Analyze my coding vs meetings balance for this week",
      },
      {
        label: "Weekly summary",
        text: "Summarize my week's productivity with insights and improvements",
      },
    ],
  },
  {
    title: "🏃 Fitness",
    items: [
      {
        label: "Workout plan",
        text: "Suggest a beginner-friendly weekly workout routine for fat loss",
      },
      {
        label: "Fitness goal",
        text: "Create a fitness plan to improve stamina and strength",
      },
    ],
  },
  {
    title: "📝 Activity Log",
    items: [
      {
        label: "Log study session",
        text: "I studied DSA for 2 hours and solved 5 problems",
      },
      {
        label: "Log workout",
        text: "Completed 30 minutes of cardio and 15 minutes strength training",
      },
    ],
  },
];

export default function SuggestionBar({ onSelect }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="w-full">
      {/* Toggle */}
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-4 py-2 text-sm bg-white border rounded-full shadow-sm hover:bg-slate-50"
      >
        <Sparkles size={16} />
        Smart Suggestions
        {open ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
      </button>

      {/* Dropdown */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 8 }}
            className="mt-3 p-4 bg-white border rounded-2xl shadow-lg space-y-5"
          >
            {suggestions.map((group, idx) => (
              <div key={idx}>
                <h4 className="text-xs font-semibold text-gray-500 mb-3">
                  {group.title}
                </h4>

                <div className="grid md:grid-cols-2 gap-3">
                  {group.items.map((item, i) => (
                    <button
                      key={i}
                      onClick={() => {
                        onSelect?.(item.text);
                        setOpen(false);
                      }}
                      className="text-left p-3 bg-slate-50 rounded-xl border hover:bg-slate-100 transition"
                    >
                      <p className="text-sm font-medium text-gray-800">
                        {item.label}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">{item.text}</p>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
