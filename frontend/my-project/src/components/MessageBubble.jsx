import { Zap, FileText } from "lucide-react";
import { GoalSchemaCard } from "./GoalSchemaCard";


export default function MessageBubble({ message, isBot }) {
  return (
    <div
      className={`flex ${isBot ? "justify-start" : "justify-end"} mb-6 group`}
    >
      <div
        className={`flex max-w-[90%] md:max-w-[75%] gap-3 ${
          isBot ? "flex-row" : "flex-row-reverse"
        }`}
      >
        <div
          className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
            isBot
              ? "bg-indigo-100 text-indigo-600"
              : "bg-slate-200 text-slate-600"
          }`}
        >
          {isBot ? (
            <Zap size={16} />
          ) : (
            <div className="text-xs font-bold">ME</div>
          )}
        </div>

        <div className={`flex flex-col ${isBot ? "items-start" : "items-end"}`}>
          {message.text && (
            <div
              className={`py-3 px-4 rounded-2xl text-sm leading-relaxed shadow-sm relative break-words max-w-full ${
                isBot
                  ? "bg-white text-slate-700 border border-slate-100 rounded-tl-none"
                  : "bg-indigo-600 text-white rounded-tr-none"
              }`}
            >
              {message.text}

              {message.fileAttachment && (
                <div className="mt-2 pt-2 border-t border-indigo-500/30 flex items-center gap-2 text-xs opacity-90">
                  <FileText size={12} />
                  Analyzed: {message.fileAttachment}
                </div>
              )}
            </div>
          )}

          {message.type === "goal-schema" && (
            <GoalSchemaCard
              initialData={message.data}
              onSave={(data) => console.log("Goal Saved:", data)}
              onCancel={() => console.log("Goal Cancelled")}
            />
          )}

          <span className="text-[10px] text-slate-400 mt-1 px-1 opacity-0 group-hover:opacity-100 transition-opacity">
            {message.timestamp || "Just now"}
          </span>
        </div>
      </div>
    </div>
  );
}
