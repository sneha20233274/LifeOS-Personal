import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { AnimatePresence } from "framer-motion";
import { Sparkles, Loader2, AlertCircle } from "lucide-react";
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
     NORMALIZE (YOUR LOGIC)
  ------------------------------ */
  useEffect(() => {
    if (!proposals || !thread_id) {
      navigate("/");
      return;
    }

    const normalized = proposals.map((p) => ({
      proposal_id: p.proposal_id, // ✅ backend ID
      action_type: p.action_type,
      payload: p.payload,
      status: p.status,
    }));

    setProposalsState(normalized);
  }, [proposals, thread_id, navigate]);

  if (!proposalsState.length) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-100 via-blue-50 to-pink-100 flex items-center justify-center">
        <Loader2 className="w-12 h-12 animate-spin text-purple-600" />
      </div>
    );
  }

  /* -----------------------------
     HELPERS (YOUR LOGIC)
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
        proposal_id: p.proposal_id, // ✅ send real ID
        status: p.status,
        payload: p.payload,
      })),
    });


    toast.success("Plan approved & execution started 🚀");
    navigate(`/session/${thread_id}`);
  };

  /* -----------------------------
     DERIVED DATA (YOUR LOGIC)
  ------------------------------ */
  const activeGoals = proposalsState.filter(
    (p) => p.action_type === "create_goal"
  );

  const tasks = proposalsState.filter(
    (p) => p.action_type === "create_task"
  );
  const subtasks = proposalsState.filter(
    (p) => p.action_type === "create_subtask"
  );

  /* =============================
     UI (RTK PAGE STYLE)
  ============================== */
  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      {/* ANIMATED GRID BACKGROUND */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.05),transparent_70%)]" />
      <div className="absolute inset-0 bg-[linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px]" />

      <Toaster position="top-right" richColors />

      <div className="relative max-w-7xl mx-auto py-10 px-6">
        {/* HEADER */}
        <div className="mb-10 border border-white/10 rounded-2xl p-6 bg-white/5 backdrop-blur-xl shadow-[0_0_40px_rgba(255,255,255,0.05)]">
          <div className="flex items-center gap-4">
            <div className="p-4 rounded-xl bg-white text-black shadow-lg animate-pulse">
              <Sparkles className="w-8 h-8" />
            </div>
            <div>
              <h1 className="text-4xl font-bold tracking-widest">
                LLM PROPOSAL ENGINE
              </h1>
              <p className="text-gray-400 text-sm mt-1">
                Neural plan generation & execution review interface
              </p>
            </div>
          </div>

          <div className="mt-6 flex gap-6 text-xs uppercase tracking-wider">
            <Legend color="bg-white" label="Pending" />
            <Legend color="bg-green-400" label="Approved" />
            <Legend color="bg-red-400" label="Rejected" />
          </div>
        </div>

        {/* SESSION INFO */}
        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-xl p-6 mb-8 shadow-xl">
          <div className="flex justify-between">
            <div>
              <h2 className="text-2xl font-semibold tracking-wide">
                {proposal_name ?? "AI GENERATED EXECUTION PLAN"}
              </h2>
              {created_at && (
                <p className="text-xs text-gray-400 mt-1">
                  Generated at: {new Date(created_at).toLocaleString()}
                </p>
              )}
            </div>
            <div className="text-right">
              <div className="text-4xl font-bold text-white">
                {activeGoals.length}
              </div>
              <div className="text-xs text-gray-400 tracking-widest">
                ACTIVE GOALS
              </div>
            </div>
          </div>
        </div>

        {/* GOALS */}
        <div className="space-y-8">
          <AnimatePresence mode="popLayout">
            {/* GOALS OR TASK-ONLY MODE */}
            {activeGoals.length > 0 ? (
              <div className="space-y-8">
                <AnimatePresence mode="popLayout">
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
                </AnimatePresence>
              </div>
            ) : (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold tracking-wide">Tasks</h2>

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
            )}
          </AnimatePresence>
        </div>

     

        {/* SUBMIT */}
        <div className="mt-12 flex justify-end">
          <button
            onClick={submitAllChanges}
            className="px-8 py-4 rounded-xl bg-white text-black font-bold tracking-widest hover:bg-gray-200 shadow-[0_0_20px_rgba(255,255,255,0.4)] transition"
          >
            EXECUTE PLAN
          </button>
        </div>
      </div>
    </div>
  );
}
function Legend({ color, label }) {
  return (
    <div className="flex items-center gap-2 text-xs tracking-widest">
      <div className={`w-3 h-3 rounded-full ${color}`} />
      <span className="text-gray-300">{label}</span>
    </div>
  );
}

