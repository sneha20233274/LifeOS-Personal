import {
  User,
  CheckCircle2,
  Circle,
  LogOut,
  Home,
  Dumbbell,
  Sparkles,
  BarChart3,
  CalendarDays,
} from "lucide-react";
import { Bell } from "lucide-react";
import { Button } from "./ui/Button";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate, useLocation } from "react-router-dom";
import { logout } from "../store/authSlice";
import { useLogoutMutation } from "../services/authApi";
import { useCreateNewChatMutation } from "../services/chatApi";


export function Navbar({ isRoutineCompleted }) {
  const { isAuthenticated } = useSelector((s) => s.auth);
  const [createNewChat] = useCreateNewChatMutation();
  const dispatch = useDispatch();
   const [logoutApi] = useLogoutMutation();
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  const navItem = (label, Icon, path) => (
    <button
      onClick={() => navigate(path)}
      className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all
        ${
          isActive(path)
            ? "bg-white text-purple-700 shadow-lg"
            : "text-white/80 hover:bg-white/20 hover:text-white"
        }`}
    >
      <Icon className="w-4 h-4" />
      {label}
    </button>
  );

  return (
    <nav
      className={`w-full px-6 py-4 transition-colors duration-300 ${
        isRoutineCompleted
          ? "bg-gradient-to-r from-emerald-500 to-teal-600"
          : "bg-gradient-to-r from-indigo-600 to-purple-700"
      }`}
    >
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* LEFT */}
        <div className="flex items-center gap-6">
          {/* Logo */}
          <div
            onClick={() => navigate("/")}
            className="cursor-pointer flex items-center gap-3"
          >
            <h1 className="text-2xl font-bold text-white">Life OS</h1>
          </div>

          {/* Status Badge */}
          <div className="flex items-center gap-2 bg-white/20 px-3 py-1.5 rounded-full">
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

        {/* CENTER NAV */}
        {isAuthenticated && (
          <div className="hidden md:flex items-center gap-2 bg-white/10 p-1 rounded-full">
            {navItem("Home", Home, "/")}
            {navItem("Fitness", Dumbbell, "/fitness")}
            <button
              onClick={async () => {
                try {
                  const res = await createNewChat().unwrap();
                  const threadId = res.thread_id;
                  navigate(`/session/${threadId}`);
                } catch (err) {
                  console.error("Failed to start AI Planner", err);
                }
              }}
              className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all ${
                isActive("/planner")
                  ? "bg-white text-purple-700 shadow-lg"
                  : "text-white/80 hover:bg-white/20 hover:text-white"
              }`}
            >
              <Sparkles className="w-4 h-4" />
              AI Planner
            </button>
            {navItem("DayCraft", CalendarDays, "/calender")}
            {navItem("Dashboard", BarChart3, "/dashboard")}
          </div>
        )}

        {/* RIGHT */}
        <div className="flex items-center gap-3">
          {!isAuthenticated ? (
            <>
              <Button
                onClick={() => navigate("/login")}
                variant="ghost"
                className="text-white hover:bg-white/20"
              >
                Login
              </Button>
              <Button
                onClick={() => navigate("/signup")}
                className="bg-white text-purple-700 hover:bg-gray-100"
              >
                Sign Up
              </Button>
            </>
          ) : (
            <>
              {/* Profile */}
              <Button
                variant="ghost"
                size="icon"
                className="rounded-full bg-white/20 hover:bg-white/30 text-white"
                onClick={() => navigate("/profile")}
              >
                <User className="w-5 h-5" />
              </Button>

              {/* Logout */}
              <Button
                onClick={async () => {
                  await logoutApi();
                  navigate("/");
                }}
                variant="ghost"
                className="flex items-center gap-2 text-white hover:bg-white/20"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </Button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
