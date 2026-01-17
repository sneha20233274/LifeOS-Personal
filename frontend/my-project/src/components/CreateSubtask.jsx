import { useState } from "react";
import { ArrowLeft, Save, ChevronDown } from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";

import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Textarea } from "./ui/Textarea";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "./ui/select";

import { useCreateSubtaskMutation } from "../services/subtasksApi";

export function CreateSubtask() {
  const navigate = useNavigate();
  const { taskId } = useParams();

  const [createSubtask, { isLoading }] = useCreateSubtaskMutation();

  /* -----------------------------
     FORM STATE (MATCHES BACKEND)
  ------------------------------ */
  const [form, setForm] = useState({
    subtask_name: "",
    subtask_type: "checkbox",

    target_value: null,
    weight: 1,
    deadline: null,
    depends_on_subtask_id: null,
  });

  const [showAdvanced, setShowAdvanced] = useState(false);
  const [error, setError] = useState(null);

  /* -----------------------------
     HELPERS
  ------------------------------ */
  const requiresTarget = form.subtask_type !== "checkbox";

  const targetPlaceholder =
    form.subtask_type === "count"
      ? "e.g. 50"
      : form.subtask_type === "duration"
      ? "e.g. 600 (minutes)"
      : "e.g. 8";

  /* -----------------------------
     SUBMIT HANDLER
  ------------------------------ */
const handleSubmit = async () => {
  setError(null);

  if (!form.subtask_name.trim()) {
    setError("Subtask name is required");
    return;
  }

  if (requiresTarget && form.target_value === null) {
    setError("Target value is required for this subtask type");
    return;
  }

  try {
    await createSubtask({
      task_id: Number(taskId),
      subtask_name: form.subtask_name,
      subtask_type: form.subtask_type,
      target_value: requiresTarget ? form.target_value : null,
      weight: form.weight,
      deadline: form.deadline,
      depends_on_subtask_id: form.depends_on_subtask_id,
    }).unwrap();

    // ✅ IMPORTANT CHANGE HERE
    navigate(`/tasks/${taskId}/subtasks`);
  } catch (err) {
    setError("Failed to create subtask");
  }
};


  /* -----------------------------
     RENDER
  ------------------------------ */
  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-indigo-50">
      <div className="max-w-2xl mx-auto px-6 py-10">
        {/* HEADER */}
        <div className="flex items-center gap-4 mb-8">
          <Button variant="ghost" onClick={() => navigate(-1)}>
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back
          </Button>
          <h1 className="text-2xl font-bold text-gray-900">
            Create New Subtask
          </h1>
        </div>

        {/* FORM CARD */}
        <div className="bg-white rounded-xl shadow-lg p-6 animate-in fade-in slide-in-from-bottom-4 duration-300">
          <div className="space-y-6">
            {/* ERROR */}
            {error && (
              <div className="bg-red-50 text-red-700 px-4 py-2 rounded-md text-sm">
                {error}
              </div>
            )}

            {/* SUBTASK NAME */}
            <div>
              <label className="text-sm font-medium text-gray-700">
                Subtask Name *
              </label>
              <Input
                placeholder="Enter subtask name"
                value={form.subtask_name}
                onChange={(e) =>
                  setForm({ ...form, subtask_name: e.target.value })
                }
              />
            </div>

            {/* SUBTASK TYPE */}
            <div>
              <label className="text-sm font-medium text-gray-700">
                Subtask Type *
              </label>
              <Select
                value={form.subtask_type}
                onValueChange={(value) =>
                  setForm({
                    ...form,
                    subtask_type: value,
                    target_value: null,
                  })
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="checkbox">Checkbox</SelectItem>
                  <SelectItem value="count">Count</SelectItem>
                  <SelectItem value="duration">Duration</SelectItem>
                  <SelectItem value="score">Score</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* TARGET VALUE (CONDITIONAL) */}
            {requiresTarget && (
              <div>
                <label className="text-sm font-medium text-gray-700">
                  Target Value *
                </label>
                <Input
                  type="number"
                  placeholder={targetPlaceholder}
                  value={form.target_value ?? ""}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      target_value: Number(e.target.value),
                    })
                  }
                />
              </div>
            )}

            {/* ADVANCED OPTIONS */}
            <div>
              <button
                type="button"
                onClick={() => setShowAdvanced((v) => !v)}
                className="flex items-center text-sm font-medium text-gray-700 hover:text-gray-900"
              >
                <ChevronDown
                  className={`w-4 h-4 mr-2 transition-transform ${
                    showAdvanced ? "rotate-180" : ""
                  }`}
                />
                Advanced options
              </button>

              {showAdvanced && (
                <div className="mt-4 space-y-4 animate-in fade-in duration-200">
                  {/* WEIGHT */}
                  <div>
                    <label className="text-sm font-medium text-gray-700">
                      Weight
                    </label>
                    <Input
                      type="number"
                      min={1}
                      value={form.weight}
                      onChange={(e) =>
                        setForm({
                          ...form,
                          weight: Number(e.target.value),
                        })
                      }
                    />
                  </div>

                  {/* DEADLINE */}
                  <div>
                    <label className="text-sm font-medium text-gray-700">
                      Deadline
                    </label>
                    <Input
                      type="date"
                      value={form.deadline ?? ""}
                      onChange={(e) =>
                        setForm({
                          ...form,
                          deadline: e.target.value || null,
                        })
                      }
                    />
                  </div>

                  {/* DEPENDS ON (OPTIONAL – FUTURE DROPDOWN) */}
                  {/* Keep null for now */}
                </div>
              )}
            </div>

            {/* ACTIONS */}
            <div className="flex justify-end gap-3 pt-6">
              <Button variant="outline" onClick={() => navigate(-1)}>
                Cancel
              </Button>
              <Button
                onClick={handleSubmit}
                disabled={isLoading}
                className="bg-gradient-to-r from-pink-600 to-purple-600"
              >
                <Save className="w-4 h-4 mr-2" />
                Create Subtask
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
