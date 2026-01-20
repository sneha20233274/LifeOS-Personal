import { Edit2 } from "lucide-react";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";

const DAY_THEME = {
  monday: {
    header: "bg-pink-500",
    badge: "bg-pink-100 text-pink-700",
    card: "border-pink-300",
  },
  tuesday: {
    header: "bg-orange-500",
    badge: "bg-orange-100 text-orange-700",
    card: "border-orange-300",
  },
  wednesday: {
    header: "bg-emerald-500",
    badge: "bg-emerald-100 text-emerald-700",
    card: "border-emerald-300",
  },
  thursday: {
    header: "bg-sky-500",
    badge: "bg-sky-100 text-sky-700",
    card: "border-sky-300",
  },
  friday: {
    header: "bg-violet-500",
    badge: "bg-violet-100 text-violet-700",
    card: "border-violet-300",
  },
  saturday: {
    header: "bg-yellow-500",
    badge: "bg-yellow-100 text-yellow-700",
    card: "border-yellow-300",
  },
  sunday: {
    header: "bg-gray-500",
    badge: "bg-gray-100 text-gray-700",
    card: "border-gray-300",
  },
};

export function DayCard({ dayKey, day, disabled, onChange }) {
  const theme = DAY_THEME[dayKey];

  return (
    <Card className={`overflow-hidden border-2 shadow-md ${theme.card}`}>
      {/* HEADER */}
      <div className={`p-4 text-white ${theme.header}`}>
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-xl font-bold capitalize">{dayKey}</h3>
            <p className="text-sm opacity-90">
              Focus: {day.focus.replace("_", " ")}
            </p>
          </div>

          {!disabled && (
            <button className="flex items-center gap-1 bg-white/20 hover:bg-white/30 px-3 py-1 rounded-md text-sm">
              <Edit2 className="w-4 h-4" />
              Edit
            </button>
          )}
        </div>
      </div>

      {/* TIMELINE */}
      <CardContent className="space-y-4 p-4 bg-white">
        {Object.entries(day.timeline).map(([time, block]) => (
          <div key={time} className="rounded-xl border p-3 bg-gray-50">
            <div className="flex justify-between items-center mb-2">
              <span className="font-semibold text-sm">{time}</span>
              <Badge className={theme.badge}>{block.block_type}</Badge>
            </div>

            <p className="text-xs text-gray-500 mb-1">
              Category: {block.category}
            </p>

            <textarea
              disabled={disabled}
              className="w-full text-sm rounded-md border p-2 resize-none focus:ring-2 focus:ring-purple-400"
              rows={3}
              value={JSON.stringify(block.details ?? {}, null, 2)}
              onChange={(e) =>
                onChange({
                  ...day,
                  timeline: {
                    ...day.timeline,
                    [time]: {
                      ...block,
                      details: JSON.parse(e.target.value || "{}"),
                    },
                  },
                })
              }
            />
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
