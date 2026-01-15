import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./components/MainPage";
import { LoginPage } from "./components/LoginPage";
import { SignupPage } from "./components/SignupPage";
import { Dashboard } from "./components/Dashboard";
import { GoalsPage } from "./components/GoalsPage";
import { TasksPage } from "./components/TasksPage";
import { SubtasksPage } from "./components/SubtasksPage";
import Sidebar from "./components/Sidebar";
import { ProposalsPage } from "./components/ProposalsPage";
import ChatInterface from "./components/ChatInterface";
import SessionPage from "./components/SessionPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<MainPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/goals" element={<GoalsPage />} />
      <Route path="/tasks" element={<TasksPage />} />
      <Route path="/subtasks" element={<SubtasksPage />} />
      <Route path="/planner" element={<SessionPage />} />
      <Route path="/session/:threadId" element={<ChatInterface />} />
      <Route path="/show-plan" element={<ProposalsPage />} />
    </Routes>
  );
}
