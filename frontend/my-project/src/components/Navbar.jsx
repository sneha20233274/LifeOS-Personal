import { User, CheckCircle2, Circle } from "lucide-react";
import { Button } from "./ui/Button";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

export function Navbar({ isRoutineCompleted }) {
  const { isLoggedIn } = useSelector((s) => s.auth);
  const navigate = useNavigate();
  return (
    <nav
      className={`w-full px-6 py-4 transition-colors duration-300 ${
        isRoutineCompleted
          ? "bg-gradient-to-r from-emerald-500 to-teal-600"
          : "bg-gradient-to-r from-indigo-600 to-purple-700"
      }`}
    >
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Logo/Brand */}
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-white">Life OS</h1>
          {/* Daily Routine Indicator */}
          <div className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-3 py-1.5 rounded-full">
            {isRoutineCompleted ? (
              <CheckCircle2 className="w-5 h-5 text-white" />
            ) : (
              <Circle className="w-5 h-5 text-white/70" />
            )}
            <span className="text-sm text-white">
              {isRoutineCompleted ? "Daily Goals Complete!" : "Goals Pending"}
            </span>
          </div>
        </div>

        {/* Right Side - Auth Buttons & Profile */}
        <div className="flex items-center gap-4">
          {!isLoggedIn ? (
            <div className="flex items-center gap-2">
              <Button
                onClick={() => navigate("/login")}
                variant="ghost"
                className="text-white hover:bg-white/20 hover:text-white"
              >
                Login
              </Button>
              <Button
                onClick={() => navigate("/signup")}
                className="bg-white text-purple-700 hover:bg-gray-100"
              >
                Sign Up
              </Button>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <Button
                variant="ghost"
                size="icon"
                className="rounded-full bg-white/20 hover:bg-white/30 text-white"
              >
                <User className="w-5 h-5" />
              </Button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
