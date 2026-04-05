import { useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";

export default function AppLayout() {
  const navigate = useNavigate();

  return (
    <div className="flex h-screen">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        {/* 🔙 Back Button */}
        <div className="p-3 border-b bg-white">
          <button
            onClick={() => navigate("/")}
            className="flex items-center gap-2 text-sm text-slate-600 hover:text-black"
          >
            <ArrowLeft size={16} />
            Back to Home
          </button>
        </div>

        <div className="flex-1 overflow-hidden">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
