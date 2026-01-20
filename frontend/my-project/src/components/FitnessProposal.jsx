import React from "react";
import { motion } from "framer-motion";
import {
  Dumbbell,
  Target,
  Calendar,
  Flame,
  Edit2,
  CheckCircle2,
  XCircle,
  RotateCcw,
} from "lucide-react";

import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Card, CardContent } from "./ui/card";
import { Separator } from "./ui/separator";
import { DayCard }  from "./DayCard";
/* ---------------------------------------------
   HELPERS
---------------------------------------------- */

const STATUS_BORDER = {
  PENDING: "border-gray-300",
  APPROVED: "border-green-400",
  REJECTED: "border-red-400",
};

/* ---------------------------------------------
   FITNESS PROPOSAL ROOT
---------------------------------------------- */
export function FitnessProposal({ proposal, onStatusChange, onUpdate }) {
  const { proposal_id, payload, status } = proposal;

  const [draft, setDraft] = React.useState(payload);
  const isLocked = status === "approved";

  const updateDraft = (patch) => {
    setDraft((prev) => {
      const updated = { ...prev, ...patch };
      onUpdate(proposal_id, updated);
      return updated;
    });
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className={`rounded-3xl border-2 shadow-xl bg-white ${
        STATUS_BORDER[status]
      }`}
    >
      {/* HEADER */}
      <div className="p-8 text-center">
        <Badge className="mb-3 bg-purple-100 text-purple-700">
          ✨ AI Generated Proposal
        </Badge>

        <h1 className="text-4xl font-bold">Weekly Fitness Routine</h1>
        <p className="text-gray-500 mt-2">
          Review and customize your personalized workout plan
        </p>
      </div>

      <Separator />

      {/* PLAN SUMMARY */}
      <PlanSummary
        plan={draft.plan_snapshot}
        disabled={isLocked}
        onChange={(plan) => updateDraft({ plan_snapshot: plan })}
      />

      <Separator />

      {/* DAYS */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
        {Object.entries(draft.schedule).map(([dayKey, day]) => (
          <DayCard
            key={dayKey}
            dayKey={dayKey}
            day={day}
            disabled={isLocked}
            onChange={(updatedDay) =>
              updateDraft({
                schedule: {
                  ...draft.schedule,
                  [dayKey]: updatedDay,
                },
              })
            }
          />
        ))}
      </div>

      {/* ACTION BAR */}
      <div className="sticky bottom-0 bg-white border-t p-6 flex justify-end gap-4 rounded-b-3xl">
        {status !== "approved" && (
          <Button
            className="bg-green-600 text-white"
            onClick={() => onStatusChange(proposal_id, "APPROVED")}
          >
            <CheckCircle2 className="w-4 h-4 mr-2" />
            Approve & Continue
          </Button>
        )}

        {status !== "rejected" && (
          <Button
            variant="destructive"
            onClick={() => onStatusChange(proposal_id, "REJECTED")}
          >
            <XCircle className="w-4 h-4 mr-2" />
            Delete Routine
          </Button>
        )}

        {status !== "pending" && (
          <Button
            variant="outline"
            onClick={() => onStatusChange(proposal_id, "PENDING")}
          >
            <RotateCcw className="w-4 h-4 mr-2" />
            Restore
          </Button>
        )}
      </div>
    </motion.div>
  );
}

/* ---------------------------------------------
   PLAN SUMMARY CARD (EDITABLE)
---------------------------------------------- */
function PlanSummary({ plan, disabled, onChange }) {
  const update = (key, value) => onChange({ ...plan, [key]: value });

  return (
    <div className="p-6 grid grid-cols-2 md:grid-cols-3 gap-4">
      <Field
        label="Goal"
        icon={Target}
        value={plan.goal}
        disabled={disabled}
        onChange={(v) => update("goal", v)}
      />

      <Field
        label="Training Split"
        icon={Dumbbell}
        value={plan.training_split}
        disabled={disabled}
        onChange={(v) => update("training_split", v)}
      />

      <Field
        label="Session (min)"
        icon={Calendar}
        value={plan.session_duration_min}
        disabled={disabled}
        type="number"
        onChange={(v) => update("session_duration_min", Number(v))}
      />

      <Field
        label="Frequency / week"
        icon={Calendar}
        value={plan.weekly_frequency}
        disabled={disabled}
        type="number"
        onChange={(v) => update("weekly_frequency", Number(v))}
      />

      <Field
        label="Intensity"
        icon={Flame}
        value={plan.intensity.level}
        disabled={disabled}
        onChange={(v) =>
          update("intensity", {
            ...plan.intensity,
            level: v,
          })
        }
      />

      <Field
        label="Sleep (hrs)"
        icon={Calendar}
        value={plan.recovery.sleep_hours}
        disabled={disabled}
        type="number"
        onChange={(v) =>
          update("recovery", {
            ...plan.recovery,
            sleep_hours: Number(v),
          })
        }
      />
    </div>
  );
}

/* ---------------------------------------------
   DAY CARD (EDITABLE)

/* ---------------------------------------------
   SMALL FIELD COMPONENT
---------------------------------------------- */
function Field({
  label,
  value,
  icon: Icon,
  onChange,
  disabled,
  type = "text",
}) {
  return (
    <div className="bg-gray-50 rounded-xl p-4 border">
      <div className="flex items-center gap-2 text-xs text-gray-600 mb-1">
        <Icon className="w-4 h-4" />
        {label}
      </div>
      <input
        disabled={disabled}
        type={type}
        className="w-full bg-transparent font-semibold focus:outline-none"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}
