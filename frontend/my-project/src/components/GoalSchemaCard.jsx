import { useState } from "react";
import { CheckCircle, Sparkles, Loader2, Save } from "lucide-react";

const MockBackend = {
  createGoal: async (data) => new Promise((res) => setTimeout(res, 800)),
};

export const GoalSchemaCard = ({ initialData, onSave, onCancel }) => {
  // Use a fallback object to prevent "controlled vs uncontrolled" input errors
  const [formData, setFormData] = useState({
    title: initialData?.title || "",
    target: initialData?.target || 0,
    unit: initialData?.unit || "tasks",
    frequency: initialData?.frequency || "Daily",
    priority: initialData?.priority || "Medium",
  });

  const [isEditing, setIsEditing] = useState(true);
  const [isSaved, setIsSaved] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "target" ? Number(value) : value,
    }));
  };

  const handleSave = async () => {
    if (!formData.title) return alert("Please enter a title");

    setIsSaving(true);
    try {
      await MockBackend.createGoal(formData);
      setIsSaved(true);
      setIsEditing(false);
      // Notify parent component that goal is finalized
      if (onSave) onSave(formData);
    } catch (error) {
      console.error("Save failed", error);
    } finally {
      setIsSaving(false);
    }
  };

  if (isSaved) {
    return (
      <div className="bg-green-50 border border-green-200 p-4 rounded-xl mt-2 w-full max-w-md flex items-center gap-3 animate-in fade-in slide-in-from-bottom-2 duration-500">
        <div className="bg-green-100 p-2 rounded-full text-green-600 shadow-sm">
          <CheckCircle size={24} />
        </div>
        <div>
          <h4 className="font-semibold text-green-900">
            Goal Created Successfully
          </h4>
          <p className="text-sm text-green-700">
            {formData.title} • {formData.target} {formData.unit} (
            {formData.frequency})
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-lg mt-2 w-full max-w-md overflow-hidden animate-in fade-in slide-in-from-bottom-2 duration-500">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-50 to-indigo-50 px-4 py-3 border-b border-slate-200 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Sparkles size={16} className="text-purple-600" />
          <span className="font-bold text-slate-700 text-sm tracking-tight">
            New Goal Schema
          </span>
        </div>
        <span className="text-[10px] font-bold uppercase tracking-widest bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full">
          Draft
        </span>
      </div>

      {/* Form Body */}
      <div className="p-4 space-y-4">
        <div className="space-y-1">
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
            Goal Title
          </label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            disabled={!isEditing || isSaving}
            className="w-full text-sm font-semibold text-slate-900 border-b border-slate-200 focus:border-purple-500 outline-none py-1 bg-transparent transition-colors placeholder:text-slate-300"
            placeholder="e.g., Learn React"
          />
        </div>

        <div className="grid grid-cols-2 gap-6">
          <div className="space-y-1">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
              Target
            </label>
            <input
              type="number"
              name="target"
              value={formData.target}
              onChange={handleChange}
              disabled={!isEditing || isSaving}
              className="w-full text-sm text-slate-900 border-b border-slate-200 focus:border-purple-500 outline-none py-1 bg-transparent"
            />
          </div>

          <div className="space-y-1">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
              Unit
            </label>
            <select
              name="unit"
              value={formData.unit}
              onChange={handleChange}
              disabled={!isEditing || isSaving}
              className="w-full text-sm text-slate-900 border-b border-slate-200 focus:border-purple-500 outline-none py-1 bg-transparent cursor-pointer"
            >
              <option value="hours">Hours</option>
              <option value="minutes">Minutes</option>
              <option value="tasks">Tasks</option>
              <option value="pages">Pages</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6">
          <div className="space-y-1">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
              Frequency
            </label>
            <select
              name="frequency"
              value={formData.frequency}
              onChange={handleChange}
              disabled={!isEditing || isSaving}
              className="w-full text-sm text-slate-900 border-b border-slate-200 focus:border-purple-500 outline-none py-1 bg-transparent cursor-pointer"
            >
              <option value="Daily">Daily</option>
              <option value="Weekly">Weekly</option>
              <option value="Monthly">Monthly</option>
            </select>
          </div>

          <div className="space-y-1">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
              Priority
            </label>
            <select
              name="priority"
              value={formData.priority}
              onChange={handleChange}
              disabled={!isEditing || isSaving}
              className="w-full text-sm text-slate-900 border-b border-slate-200 focus:border-purple-500 outline-none py-1 bg-transparent cursor-pointer"
            >
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>
        </div>
      </div>

      {/* Footer Actions */}
      <div className="px-4 py-3 bg-slate-50 border-t border-slate-200 flex justify-end gap-2">
        <button
          onClick={onCancel}
          disabled={isSaving}
          className="text-xs font-bold text-slate-400 hover:text-slate-600 px-3 py-2 transition-colors disabled:opacity-50"
        >
          Discard
        </button>
        <button
          onClick={handleSave}
          disabled={isSaving}
          className="bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold px-4 py-2 rounded-lg flex items-center gap-2 transition-all active:scale-95 shadow-md disabled:opacity-70 disabled:cursor-not-allowed"
        >
          {isSaving ? (
            <Loader2 size={14} className="animate-spin" />
          ) : (
            <Save size={14} />
          )}
          {isSaving ? "Creating..." : "Create Goal"}
        </button>
      </div>
    </div>
  );
};
