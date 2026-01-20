import React from "react";
import { Edit2 } from "lucide-react";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";

const STATUS_COLORS = {
  pending: "border-gray-300",
  approved: "border-green-400 bg-green-50",
  rejected: "border-red-400 bg-red-50",
};

export function DayCard({ dayKey, dayData, routineStatus, onEditDay }) {
  return (
    <Card
      className={`border-2 shadow-md transition-all ${
        STATUS_COLORS[routineStatus]
      }`}
    >
      {/* Header */}
      <div className="flex justify-between items-center p-4 border-b">
        <div>
          <h3 className="text-xl font-bold capitalize">{dayKey}</h3>
          <p className="text-sm text-gray-500">Focus: {dayData.focus}</p>
        </div>

        <button
          onClick={() => onEditDay(dayKey)}
          className="flex items-center gap-2 text-sm px-3 py-1 rounded-lg border hover:bg-gray-100"
        >
          <Edit2 className="w-4 h-4" />
          Edit
        </button>
      </div>

      {/* Timeline */}
      <CardContent className="space-y-4 p-4">
        {Object.entries(dayData.timeline).map(([time, block]) => (
          <div key={time} className="p-3 rounded-lg border bg-white">
            <div className="flex justify-between mb-1">
              <span className="font-semibold">{time}</span>
              <Badge variant="outline">{block.block_type}</Badge>
            </div>

            <p className="text-sm text-gray-600">
              <strong>Category:</strong> {block.category}
            </p>
            <p className="text-sm text-gray-700">{block.details}</p>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
