import React from "react";
import { Target, CheckCircle2 } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function GoalsTasksTabs({ goalsCount = 0, tasksCount = 0 }) {
  const [tab, setTab] = React.useState("goals");
  const navigate = useNavigate();

  return (
    <div className="rounded-2xl p-8 bg-white/5 backdrop-blur border border-white/10">
      <div className="flex gap-8 border-b border-white/10 mb-6">
        {[
          {
            key: "goals",
            label: "Goals",
            icon: <Target size={18} />,
            path: "/goals",
          },
          {
            key: "tasks",
            label: "Tasks",
            icon: <CheckCircle2 size={18} />,
            path: "/tasks",
          },
        ].map((t) => (
          <button
            key={t.key}
            onClick={() => {
              setTab(t.key);
              navigate(t.path);
            }}
            className={`pb-4 flex items-center gap-2 font-medium transition ${
              tab === t.key
                ? "border-b-2 border-indigo-500 text-indigo-400"
                : "text-gray-400 hover:text-gray-200"
            }`}
          >
            {t.icon}
            {t.label}
          </button>
        ))}
      </div>

      <div>
        <p className="text-3xl font-semibold">
          {tab === "goals" ? goalsCount : tasksCount}
        </p>
        <p className="text-gray-400 mt-1">
          {tab === "goals" ? "Active goals" : "Tasks completed"}
        </p>
        <p className="text-sm text-gray-500 mt-4">
          {tab === "goals"
            ? "Focus creates momentum."
            : "Consistency builds excellence."}
        </p>
      </div>
    </div>
  );
}
