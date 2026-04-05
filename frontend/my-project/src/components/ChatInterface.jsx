
import { useDispatch, useSelector } from "react-redux";
import { addMessage } from "../store/chatSlice";
import MessageBubble from "./MessageBubble";
import SuggestionBar from "./SuggestionBar";
import { Send, Loader2, Plus } from "lucide-react";
import { useRef, useEffect, useState } from "react";
import { useRunChatMutation } from "../services/chatApi";
import { useFileUpload } from "../hooks/useFileUpload";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import { setSession } from "../store/chatSlice";

export default function ChatInterface() {
  const dispatch = useDispatch();
  const { uploadFile } = useFileUpload();
  const { threadId } = useParams();
 
  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);
  const navigate = useNavigate();

  const [inputValue, setInputValue] = useState("");

  const { messages, activeSessionId } = useSelector((s) => s.chat);

  const [runChat, { isLoading }] = useRunChatMutation();
  useEffect(() => {
    if (threadId) {
      dispatch(setSession(threadId)); // 🔥 FIX
    }
  }, [threadId, dispatch]);
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handlePlusClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    uploadFile(file);
    e.target.value = null;
  };

  const handleSendMessage = async (text) => {
    if (!text.trim() || isLoading) return;

    const currentThread = activeSessionId || threadId;

    if (!currentThread) {
      console.error("No session found");
      return;
    }

    dispatch(
      addMessage({
        id: Date.now() + Math.random(),
        sender: "user",
        text,
      }),
    );

    setInputValue("");

    try {
      const result = await runChat({
        thread_id: currentThread,
        prompt: text,
      }).unwrap();

      if (result.status === "WAITING_FOR_APPROVAL") {
        navigate("/show-plan", {
          state: {
            proposals: result.proposals,
            thread_id: result.thread_id,
          },
        });
        return;
      }

      if (result.messages?.length) {
        result.messages.forEach((msg) => {
          dispatch(
            addMessage({
              id: Date.now() + Math.random(),
              sender: "bot",
              text: msg.content,
            }),
          );
        });
      }
    } catch (err) {
      console.error("Chat run failed", err);
      dispatch(
        addMessage({
          id: Date.now() + Math.random(),
          sender: "bot",
          text: "Something went wrong. Please try again.",
        }),
      );
    }
 };

  return (
    <div className="flex-1 flex flex-col bg-slate-50 w-full overflow-hidden h-full">
      {/* MESSAGES */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 w-full h-0">
        {messages.map((m) => (
          <MessageBubble key={m.id} message={m} isBot={m.sender === "bot"} />
        ))}

        {isLoading && (
          <div className="flex items-center gap-2 text-slate-400">
            <Loader2 className="animate-spin" size={18} />
            <span className="text-sm font-medium">Thinking...</span>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* INPUT */}
      <div className="border-t bg-white p-3 w-full">
        <SuggestionBar />

        <div className="mt-3 flex items-center gap-2 w-full">
          {/* FILE BUTTON */}
          <button
            onClick={handlePlusClick}
            className="p-2 bg-slate-100 rounded-lg hover:bg-slate-200 shrink-0"
          >
            <Plus size={18} />
          </button>

          <input
            ref={fileInputRef}
            type="file"
            hidden
            onChange={handleFileChange}
            accept=".pdf,.doc,.docx,.txt"
          />

          {/* INPUT FIELD */}
          <input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey && !isLoading) {
                handleSendMessage(inputValue);
              }
            }}
            placeholder="Type a message..."
            className="flex-1 min-w-0 p-2 bg-slate-100 rounded-lg outline-none"
          />

          {/* SEND BUTTON */}
          <button
            onClick={() => handleSendMessage(inputValue)}
            disabled={!inputValue.trim() || isLoading}
            className="p-2 bg-indigo-600 text-white rounded-lg shrink-0"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}

  

