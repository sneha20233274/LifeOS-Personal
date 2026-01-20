import React from "react";
import {
  Dumbbell,
  CheckCircle2,
  XCircle,
  RotateCcw,
  Target,
  Calendar,
  Flame,
} from "lucide-react";
import { motion } from "framer-motion";

import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Separator } from "./ui/separator";

/* ---------------------------------------------
   COLOR MAPS
---------------------------------------------- */
const STATUS_STYLES = {
  pending: "border-gray-300",
  approved: "border-green-400 bg-green-50",
  rejected: "border-red-400 bg-red-50",
};

const BLOCK_COLORS = {
  warmup: "bg-yellow-100 text-yellow-800",
  exercise: "bg-blue-100 text-blue-800",
  rest: "bg-gray-100 text-gray-700",
  cooldown: "bg-purple-100 text-purple-800",
};

/* =============================================
   FITNESS PROPOSAL
============================================= */
export function FitnessProposal({ proposal, onStatusChange }) {
  const { proposal_id, payload, status } = proposal;

  const { plan_snapshot, schedule } = payload;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className={`rounded-3xl border-2 shadow-xl transition-all ${
        STATUS_STYLES[status]
      }`}
    >
      {/* HEADER */}
      <div className="p-6 flex items-center gap-4">
        <div className="p-4 rounded-2xl bg-gradient-to-r from-orange-500 to-rose-500 text-white shadow">
          <Dumbbell className="w-6 h-6" />
        </div>
        <div className="flex-1">
          <h2 className="text-3xl font-bold">Weekly Fitness Routine</h2>
          <p className="text-gray-600 text-sm">
            AI-generated fitness plan proposal
          </p>
        </div>

        <Badge variant="outline" className="capitalize">
          {status}
        </Badge>
      </div>

      <Separator />

      {/* PLAN SNAPSHOT */}
      <CardContent className="p-6 grid grid-cols-2 md:grid-cols-3 gap-4">
        <Info label="Goal" value={plan_snapshot.goal} icon={Target} />
        <Info
          label="Split"
          value={plan_snapshot.training_split}
          icon={Dumbbell}
        />
        <Info
          label="Session"
          value={`${plan_snapshot.session_duration_min} min`}
          icon={Calendar}
        />
        <Info
          label="Frequency"
          value={`${plan_snapshot.weekly_frequency} days/week`}
          icon={Calendar}
        />
        <Info
          label="Intensity"
          value={`${plan_snapshot.intensity.level} (RPE ${plan_snapshot.intensity.rpe_range.join(
            "-",
          )})`}
          icon={Flame}
        />
        <Info
          label="Recovery"
          value={`${plan_snapshot.recovery.sleep_hours}h sleep`}
          icon={Calendar}
        />
      </CardContent>

      <Separator />

      {/* WEEKLY SCHEDULE */}
      <CardContent className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {Object.entries(schedule).map(([dayKey, day]) => (
          <div key={dayKey} className="rounded-2xl border bg-white shadow-sm">
            {/* DAY HEADER */}
            <div className="p-4 border-b flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold capitalize">{dayKey}</h3>
                <p className="text-sm text-gray-500">Focus: {day.focus}</p>
              </div>

              <Button size="sm" variant="outline">
                Edit
              </Button>
            </div>

            {/* TIMELINE */}
            <div className="p-4 space-y-3">
              {Object.entries(day.timeline).map(([time, block]) => (
                <div key={time} className="p-3 rounded-xl border bg-gray-50">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-semibold">{time}</span>
                    <Badge
                      className={
                        BLOCK_COLORS[block.block_type] ??
                        "bg-gray-100 text-gray-700"
                      }
                    >
                      {block.block_type}
                    </Badge>
                  </div>

                  <p className="text-sm text-gray-600">
                    <strong>Category:</strong> {block.category}
                  </p>
                  <p className="text-sm text-gray-700">{block.details}</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </CardContent>

      <Separator />

      {/* ACTIONS */}
      <CardContent className="p-6 flex justify-end gap-3">
        {status !== "approved" && (
          <Button
            onClick={() => onStatusChange(proposal_id, "approved")}
            className="bg-green-600 hover:bg-green-700 text-white"
          >
            <CheckCircle2 className="w-4 h-4 mr-2" />
            Approve
          </Button>
        )}

        {status !== "rejected" && (
          <Button
            variant="destructive"
            onClick={() => onStatusChange(proposal_id, "rejected")}
          >
            <XCircle className="w-4 h-4 mr-2" />
            Reject
          </Button>
        )}

        {status !== "pending" && (
          <Button
            variant="outline"
            onClick={() => onStatusChange(proposal_id, "pending")}
          >
            <RotateCcw className="w-4 h-4 mr-2" />
            Restore
          </Button>
        )}
      </CardContent>
    </motion.div>
  );
}

/* ---------------------------------------------
   INFO TILE
---------------------------------------------- */
function Info({ label, value, icon: Icon }) {
  return (
    <div className="bg-gray-50 rounded-xl p-4 border">
      <div className="flex items-center gap-2 mb-1 text-gray-600 text-xs">
        <Icon className="w-4 h-4" />
        {label}
      </div>
      <div className="font-semibold capitalize">{value}</div>
    </div>
  );
}
