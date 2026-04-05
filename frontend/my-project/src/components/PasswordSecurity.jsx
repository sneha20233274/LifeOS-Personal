import React from "react";
import { Eye, EyeOff, Shield } from "lucide-react";

export default function PasswordSecurity({ onUpdate }) {
  const [editing, setEditing] = React.useState(false);
  const [show, setShow] = React.useState(false);

  const [form, setForm] = React.useState({
    current_password: "",
    new_password: "",
    confirm_password: "",
  });

  return (
    <div className="bg-white rounded-2xl p-8 shadow-sm">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <Shield className="w-5 h-5 text-indigo-600" />
            Password & Security
          </h3>
          <p className="text-sm text-gray-500 mt-1">Keep your account secure</p>
        </div>

        {!editing && (
          <button
            onClick={() => setEditing(true)}
            className="text-indigo-600 font-medium hover:underline"
          >
            Change Password
          </button>
        )}
      </div>

      {!editing ? (
        <div className="text-sm text-gray-600">
          <p>Last changed • 2 months ago</p>
          <p className="mt-2 text-gray-400">
            We recommend updating your password regularly.
          </p>
        </div>
      ) : (
        <>
          <div className="space-y-6 max-w-md">
            {/* Current */}
            <div>
              <p className="text-gray-400 mb-1">Current Password</p>
              <div className="relative">
                <input
                  type={show ? "text" : "password"}
                  placeholder="Enter current password"
                  className="w-full bg-transparent border-b border-gray-300
                             text-gray-900 placeholder-gray-400
                             caret-indigo-600
                             focus:border-indigo-500 outline-none py-2 pr-10"
                  value={form.current_password}
                  onChange={(e) =>
                    setForm({ ...form, current_password: e.target.value })
                  }
                />
                <button
                  type="button"
                  onClick={() => setShow(!show)}
                  className="absolute right-2 top-2 text-gray-400 hover:text-gray-600"
                >
                  {show ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {/* New */}
            <div>
              <p className="text-gray-400 mb-1">New Password</p>
              <input
                type="password"
                placeholder="At least 8 characters"
                className="w-full bg-transparent border-b border-gray-300
                           text-gray-900 placeholder-gray-400
                           caret-indigo-600
                           focus:border-indigo-500 outline-none py-2"
                value={form.new_password}
                onChange={(e) =>
                  setForm({ ...form, new_password: e.target.value })
                }
              />
            </div>

            {/* Confirm */}
            <div>
              <p className="text-gray-400 mb-1">Confirm Password</p>
              <input
                type="password"
                placeholder="Re-enter new password"
                className="w-full bg-transparent border-b border-gray-300
                           text-gray-900 placeholder-gray-400
                           caret-indigo-600
                           focus:border-indigo-500 outline-none py-2"
                value={form.confirm_password}
                onChange={(e) =>
                  setForm({ ...form, confirm_password: e.target.value })
                }
              />
            </div>
          </div>

          {/* Actions */}
          <div className="mt-10 flex gap-4">
            <button
              onClick={() => {
                onUpdate(form);
                setEditing(false);
                setForm({
                  current_password: "",
                  new_password: "",
                  confirm_password: "",
                });
              }}
              className="px-6 py-2 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 transition"
            >
              Update Password
            </button>

            <button
              onClick={() => {
                setEditing(false);
                setForm({
                  current_password: "",
                  new_password: "",
                  confirm_password: "",
                });
              }}
              className="px-6 py-2 rounded-xl bg-gray-100 hover:bg-gray-200 transition"
            >
              Cancel
            </button>
          </div>
        </>
      )}
    </div>
  );
}
