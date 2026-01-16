import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { AnimatePresence } from "framer-motion";
import { Sparkles, Loader2 } from "lucide-react";
import { Toaster, toast } from "sonner";

import { GoalProposal } from "./GoalProposal";
import { TaskProposal } from "./TaskProposal";
import { useSubmitProposalsMutation } from "../services/proposalsApi";

export function ProposalsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [submitProposals] = useSubmitProposalsMutation();

  const { proposals, thread_id, proposal_name, created_at } =
    location.state || {};

  const [proposalsState, setProposalsState] = useState([]);

  /* -----------------------------
     NORMALIZE (UNCHANGED)
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
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-cyan-50 to-purple-50 flex items-center justify-center">
        <Loader2 className="w-10 h-10 animate-spin text-emerald-600" />
      </div>
    );
  }

  /* -----------------------------
     HELPERS (UNCHANGED)
  ------------------------------ */
  const updateEntity = (proposal_id, payloadPatch) => {
    setProposalsState((prev) =>
      prev.map((p) =>
        p.proposal_id === proposal_id
          ? { ...p, payload: { ...p.payload, ...payloadPatch } }
          : p
      )
    );
  };

  const updateStatus = (proposal_id, status) => {
    setProposalsState((prev) =>
      prev.map((p) => (p.proposal_id === proposal_id ? { ...p, status } : p))
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
     DERIVED DATA (UNCHANGED)
  ------------------------------ */
  const activeGoals = proposalsState.filter(
    (p) => p.action_type === "create_goal"
  );
  const tasks = proposalsState.filter((p) => p.action_type === "create_task");
  const subtasks = proposalsState.filter(
    (p) => p.action_type === "create_subtask"
  );

  /* =============================
     UI (LIFE OS THEME)
  ============================== */
  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-cyan-50 to-purple-50 text-gray-900">
      <Toaster position="top-right" richColors />

      <div className="max-w-7xl mx-auto px-6 py-14">
        {/* HEADER */}
        <div className="mb-12 flex items-center gap-4">
          <div className="p-4 rounded-2xl bg-emerald-600 text-white shadow-lg">
            <Sparkles className="w-8 h-8" />
          </div>
          <div>
            <h1 className="text-4xl font-bold">Life OS – Proposal Review</h1>
            <p className="text-gray-600 mt-1">
              Review and approve your AI-generated execution plan
            </p>
          </div>
        </div>

        {/* SESSION CARD */}
        <div className="bg-white rounded-3xl p-8 shadow-xl border border-gray-100 mb-10">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-2xl font-semibold">
                {proposal_name ?? "AI GENERATED EXECUTION PLAN"}
              </h2>
              {created_at && (
                <p className="text-sm text-gray-500 mt-1">
                  Generated at {new Date(created_at).toLocaleString()}
                </p>
              )}
            </div>
            <div className="text-right">
              <div className="text-4xl font-bold text-emerald-600">
                {activeGoals.length}
              </div>
              <div className="text-sm text-gray-500">Active Goals</div>
            </div>
          </div>
        </div>

        {/* CONTENT */}
        <div className="space-y-10">
          <AnimatePresence mode="popLayout">
            {activeGoals.length > 0 ? (
              <div className="space-y-8">
                {activeGoals.map((goal) => (
                  <GoalProposal
                    key={goal.proposal_id}
                    goal={goal}
                    allTasks={tasks}
                    allSubtasks={subtasks}
                    onUpdate={updateEntity}
                    onStatusChange={updateStatus}
                  />
                ))}
              </div>
            ) : (
              <div className="bg-white rounded-3xl p-8 shadow-xl border border-gray-100">
                <h2 className="text-2xl font-bold mb-6">Tasks</h2>

                <div className="space-y-6">
                  {tasks.map((task) => (
                    <TaskProposal
                      key={task.proposal_id}
                      task={task}
                      allSubtasks={subtasks}
                      onUpdate={updateEntity}
                      onStatusChange={updateStatus}
                    />
                  ))}
                </div>
              </div>
            )}
          </AnimatePresence>
        </div>

        {/* SUBMIT */}
        <div className="mt-14 flex justify-end">
          <button
            onClick={submitAllChanges}
            className="px-10 py-4 rounded-2xl bg-emerald-600 text-white font-semibold text-lg shadow-lg hover:bg-emerald-700 transition"
          >
            Execute Plan
          </button>
        </div>
      </div>
    </div>
  );
}
