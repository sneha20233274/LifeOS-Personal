import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { AnimatePresence } from "framer-motion";
import { Sparkles, Loader2 } from "lucide-react";
import { Toaster, toast } from "sonner";

import { GoalProposal } from "./GoalProposal";
import { ActivityProposal } from "./ActivityProposal";
import { FitnessProposal } from "./FitnessProposal";
import { useSubmitProposalsMutation } from "../services/ProposalsApi";

export function ProposalsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [submitProposals] = useSubmitProposalsMutation();

  const { proposals, thread_id, proposal_name, created_at } =
    location.state || {};

  const [proposalsState, setProposalsState] = useState([]);

  /* -----------------------------
     NORMALIZE
  ------------------------------ */
  useEffect(() => {
    if (!proposals || !thread_id) {
      navigate("/");
      return;
    }

    const normalized = proposals.map((p) => ({
      proposal_id: p.proposal_id,
      action_type: p.action_type,
      payload: p.payload,
      status: p.status,
    }));

    setProposalsState(normalized);
  }, [proposals, thread_id, navigate]);

  if (!proposalsState.length) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-10 h-10 animate-spin text-emerald-600" />
      </div>
    );
  }

  /* -----------------------------
     HELPERS
  ------------------------------ */
  const updateEntity = (proposal_id, payloadPatch) => {
    setProposalsState((prev) =>
      prev.map((p) =>
        p.proposal_id === proposal_id
          ? { ...p, payload: { ...p.payload, ...payloadPatch } }
          : p,
      ),
    );
  };

  const updateStatus = (proposal_id, status) => {
    setProposalsState((prev) =>
      prev.map((p) => (p.proposal_id === proposal_id ? { ...p, status } : p)),
    );
  };

  const submitAllChanges = async () => {
    await submitProposals({
      thread_id,
      proposals: proposalsState.map((p) => ({
        proposal_id: p.proposal_id,
        status: p.status,
        payload: p.payload,
      })),
    });

    toast.success("Plan approved & execution started 🚀");
    navigate(`/session/${thread_id}`);
  };

  /* -----------------------------
     GROUPING (🔥 FIX)
  ------------------------------ */
  const goals = proposalsState.filter((p) => p.action_type === "create_goal");
  const tasks = proposalsState.filter((p) => p.action_type === "create_task");
  const subtasks = proposalsState.filter(
    (p) => p.action_type === "create_subtask",
  );

  const activities = proposalsState.filter(
    (p) => p.action_type === "log_activity",
  );

  const fitnessProposal = proposalsState.find(
    (p) => p.action_type === "create_weekly_fitness_routine",
  );

  /* -----------------------------
     BUILD TREE (🔥 CORE FIX)
  ------------------------------ */
  const goalTree = goals.map((goal) => {
    const tasksForGoal = tasks; // (can filter later if goal_id exists)

    const enrichedTasks = tasksForGoal.map((task) => ({
      ...task,
      subtasks: subtasks.filter(
        (s) => s.payload?.depends_on_task_key === task.payload?.temp_task_key,
      ),
    }));

    return {
      ...goal,
      tasks: enrichedTasks,
    };
  });

  /* =============================
     UI
  ============================== */
  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-purple-50">
      <Toaster />

      <div className="max-w-7xl mx-auto px-6 py-14">
        {/* HEADER */}
        <div className="mb-12 flex items-center gap-4">
          <Sparkles className="w-8 h-8 text-emerald-600" />
          <h1 className="text-3xl font-bold">Proposal Review</h1>
        </div>

        {/* GOALS */}
        <div className="space-y-8">
          <AnimatePresence>
            {goalTree.map((goal) => (
              <GoalProposal
                key={goal.proposal_id}
                goal={goal}
                onUpdate={updateEntity}
                onStatusChange={updateStatus}
              />
            ))}

            {/* ACTIVITIES (UNCHANGED) */}
            {activities.map((a) => (
              <ActivityProposal
                key={a.proposal_id}
                activity={a}
                onUpdate={updateEntity}
                onStatusChange={updateStatus}
              />
            ))}

            {/* FITNESS (UNCHANGED) */}
            {fitnessProposal && (
              <FitnessProposal
                proposal={fitnessProposal}
                onStatusChange={updateStatus}
              />
            )}
          </AnimatePresence>
        </div>

        {/* SUBMIT */}
        <div className="mt-10 text-right">
          <button
            onClick={submitAllChanges}
            className="px-8 py-3 bg-emerald-600 text-white rounded-xl"
          >
            Execute Plan
          </button>
        </div>
      </div>
    </div>
  );
}
