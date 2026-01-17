import { useState } from "react";
import { ArrowLeft, Save, ChevronDown } from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";

import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Textarea } from "./ui/Textarea";

import { useCreateTaskMutation } from "../services/tasksApi";

export function CreateTask() {
  const navigate = useNavigate();
  const { goalId } = useParams();

  const [createTask, { isLoading }] = useCreateTaskMutation();

  /* -----------------------------
     FORM STATE (MATCHES BACKEND)
  ------------------------------ */
  const [form, setForm] = useState({
    task_name: "",
    description: "",
    difficulty: 1,
    depends_on_task_id: null,
  });

  const [showAdvanced, setShowAdvanced] = useState(false);
  const [error, setError] = useState(null);

  /* -----------------------------
     SUBMIT
  ------------------------------ */
  const handleSubmit = async () => {
    setError(null);

    if (!form.task_name.trim()) {
      setError("Task name is required");
      return;
    }

    try {
      await createTask({
        task_name: form.task_name,
        description: form.description,
        difficulty: form.difficulty,
        depends_on_task_id: form.depends_on_task_id,
        goal_id: goalId ? Number(goalId) : null,
      }).unwrap();

      navigate(-1);
    } catch {
      setError("Failed to create task");
    }
  };

  /* -----------------------------
     RENDER
  ------------------------------ */
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="max-w-2xl mx-auto px-6 py-10">
        {/* HEADER */}
        <div className="flex items-center gap-4 mb-8">
          <Button variant="ghost" onClick={() => navigate(-1)}>
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back
          </Button>

          <h1 className="text-2xl font-bold">Create New Task</h1>
        </div>

        {/* FORM */}
        <div className="bg-white rounded-xl shadow-lg p-6 animate-in fade-in slide-in-from-bottom-4">
          <div className="space-y-6">
            {error && (
              <div className="bg-red-50 text-red-700 px-4 py-2 rounded-md">
                {error}
              </div>
            )}

            {/* TASK NAME */}
            <div>
              <label className="text-sm font-medium">Task Name *</label>
              <Input
                value={form.task_name}
                onChange={(e) =>
                  setForm({ ...form, task_name: e.target.value })
                }
              />
            </div>

            {/* DESCRIPTION */}
            <div>
              <label className="text-sm font-medium">Description</label>
              <Textarea
                value={form.description}
                onChange={(e) =>
                  setForm({ ...form, description: e.target.value })
                }
              />
            </div>

            {/* ADVANCED */}
            <button
              type="button"
              onClick={() => setShowAdvanced((v) => !v)}
              className="flex items-center text-sm font-medium"
            >
              <ChevronDown
                className={`w-4 h-4 mr-2 ${showAdvanced ? "rotate-180" : ""}`}
              />
              Advanced options
            </button>

            {showAdvanced && (
              <div className="space-y-4">
                {/* DIFFICULTY */}
                <div>
                  <label className="text-sm font-medium">Difficulty</label>
                  <Input
                    type="number"
                    min={1}
                    value={form.difficulty}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        difficulty: Number(e.target.value),
                      })
                    }
                  />
                </div>

                {/* DEPENDS ON TASK (future dropdown) */}
              </div>
            )}

            {/* ACTIONS */}
            <div className="flex justify-end gap-3 pt-6">
              <Button variant="outline" onClick={() => navigate(-1)}>
                Cancel
              </Button>

              <Button
                onClick={handleSubmit}
                disabled={isLoading}
                className="bg-gradient-to-r from-blue-600 to-indigo-600"
              >
                <Save className="w-4 h-4 mr-2" />
                Create Task
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
