import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";

import {Navbar} from "./Navbar";
import Sidebar from "./Sidebar";
import ChatInterface from "./ChatInterface";

import { setSession, addToHistory } from "../store/chatSlice";
import { useCreateNewChatMutation } from "../services/chatApi";

export default function SessionPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [createNewChat] = useCreateNewChatMutation();

  useEffect(() => {
    const createSession = async () => {
      try {
        const res = await createNewChat().unwrap();
        const threadId = res.thread_id;

        dispatch(setSession(threadId));
        dispatch(
          addToHistory({
            id: threadId,
            title: "New Chat",
            date: "Just now",
          })
        );

        navigate(`/session/${threadId}`);
      } catch (err) {
        console.error("Failed to create session", err);
      }
    };

    createSession();
  }, []);

  return (
    <div className="h-screen flex flex-col">
      {/* Navbar */}
      <Navbar />

      {/* Body */}
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <div className="flex-1 bg-gray-50">
          <ChatInterface />
        </div>
      </div>
    </div>
  );
}
