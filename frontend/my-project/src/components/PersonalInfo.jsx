import React from "react";
import { useUpdateProfileMutation } from "../services/userApi";

export default function PersonalInfo({ user }) {
  const [editing, setEditing] = React.useState(false);
  const [form, setForm] = React.useState(user);

  const [updateProfile, { isLoading }] = useUpdateProfileMutation();

  React.useEffect(() => {
    setForm(user);
  }, [user]);

  if (!form) return null;

  const handleSave = async () => {
    await updateProfile({
      first_name: form.first_name,
      middle_name: form.middle_name,
      last_name: form.last_name,
      username: form.username,
    }).unwrap();

    setEditing(false);
  };

  return (
    <div className="rounded-2xl p-8 bg-white/5 border border-white/10">
      <div className="flex justify-between mb-6">
        <h3 className="text-lg font-semibold">Personal Information</h3>
        {!editing && (
          <button onClick={() => setEditing(true)} className="text-indigo-400">
            Edit
          </button>
        )}
      </div>

      <div className="grid md:grid-cols-2 gap-6 text-sm">
        {[
          ["First Name", "first_name"],
          ["Middle Name", "middle_name"],
          ["Last Name", "last_name"],
          ["Username", "username"],
        ].map(([label, key]) => (
          <div key={key}>
            <p className="text-gray-400 mb-1">{label}</p>
            {editing ? (
              <input
                className="w-full bg-transparent border-b border-white/20 focus:border-indigo-400 outline-none py-1"
                value={form[key] || ""}
                onChange={(e) => setForm({ ...form, [key]: e.target.value })}
              />
            ) : (
              <p className="font-medium">{form[key] || "-"}</p>
            )}
          </div>
        ))}

        {/* Email (READ ONLY) */}
        <div>
          <p className="text-gray-400 mb-1">Email</p>
          <p className="text-gray-500 cursor-not-allowed">{form.email_id}</p>
        </div>
      </div>

      {editing && (
        <div className="mt-10 flex gap-4">
          <button
            onClick={handleSave}
            disabled={isLoading}
            className="px-6 py-2 rounded-xl bg-indigo-600 text-white"
          >
            {isLoading ? "Saving..." : "Save Changes"}
          </button>

          <button
            onClick={() => {
              setForm(user);
              setEditing(false);
            }}
            className="px-6 py-2 rounded-xl bg-white/10"
          >
            Cancel
          </button>
        </div>
      )}
    </div>
  );
}
