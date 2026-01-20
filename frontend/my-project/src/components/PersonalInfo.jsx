import React from "react";

export default function ProfileInfo({ user, onSave }) {
  const [editing, setEditing] = React.useState(false);
  const [form, setForm] = React.useState(null);

  React.useEffect(() => {
    if (user) setForm(user);
  }, [user]);

  if (!user || !form) {
    return (
      <div className="rounded-2xl p-8 bg-white/5 text-gray-400">
        Loading personal information...
      </div>
    );
  }

  return (
    <div className="rounded-2xl p-8 bg-white/5 backdrop-blur border border-white/10">
      <div className="flex justify-between mb-6">
        <h3 className="text-lg font-semibold">Personal Information</h3>
        {!editing && (
          <button
            onClick={() => setEditing(true)}
            className="text-indigo-400 hover:text-indigo-300"
          >
            Edit
          </button>
        )}
      </div>

      <div className="grid md:grid-cols-2 gap-8 text-sm">
        {["name", "phone", "location"].map((key) => (
          <div key={key}>
            <p className="text-gray-400 mb-1 capitalize">{key}</p>
            {!editing ? (
              <p className="font-medium">{user[key]}</p>
            ) : (
              <input
                className="w-full bg-transparent border-b border-white/20 focus:border-indigo-400 outline-none py-1"
                value={form[key]}
                onChange={(e) => setForm({ ...form, [key]: e.target.value })}
              />
            )}
          </div>
        ))}

        <div>
          <p className="text-gray-400 mb-1">Email</p>
          <p className="text-gray-300">{user.email}</p>
        </div>
      </div>

      {editing && (
        <div className="mt-10 flex gap-4">
          <button
            onClick={() => {
              onSave?.(form);
              setEditing(false);
            }}
            className="px-6 py-2 rounded-xl bg-indigo-600 text-white"
          >
            Save Changes
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
