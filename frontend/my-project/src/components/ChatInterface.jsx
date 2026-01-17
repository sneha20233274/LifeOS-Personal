
import { useDispatch, useSelector } from "react-redux";
import { addMessage } from "../store/chatSlice";
import MessageBubble from "./MessageBubble";
import SuggestionBar from "./SuggestionBar";
import { Send, Loader2, Plus } from "lucide-react";
import { useRef, useEffect, useState } from "react";
import { useRunChatMutation } from "../services/chatApi";
import { useFileUpload } from "../hooks/useFileUpload";
import { useNavigate } from "react-router-dom";

export default function ChatInterface() {
  const dispatch = useDispatch();
  const { uploadFile } = useFileUpload();

  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);
  const navigate = useNavigate();

  const [inputValue, setInputValue] = useState("");

  const { messages, activeSessionId } = useSelector((s) => s.chat);

  const [runChat, { isLoading }] = useRunChatMutation();

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
    if (!text.trim() || isLoading || !activeSessionId) return;

    // 1️⃣ Add user message
    dispatch(
      addMessage({
        id: Date.now(),
        sender: "user",
        text,
      })
    );

    setInputValue("");

    try {
      // 2️⃣ Call backend /chat/run
      const result = await runChat({
        thread_id: activeSessionId,
        prompt: text,
      }).unwrap();

      // 3️⃣ Handle interrupt (proposals)
     if (result.status === "WAITING_FOR_APPROVAL") {
       navigate("/show-plan", {
         state: {
           proposals: result.proposals,
           thread_id: result.thread_id,
         },
       });
       return;
     }

      // 4️⃣ Handle completed chat
      if (result.messages?.length) {
        result.messages.forEach((msg) => {
          dispatch(
            addMessage({
              id: Date.now() + Math.random(),
              sender: "bot",
              text: msg.content,
            })
          );
        });
      }
    } catch (err) {
      console.error("Chat run failed", err);
      dispatch(
        addMessage({
          id: Date.now() + 1,
          sender: "bot",
          text: "Something went wrong. Please try again.",
        })
      );
    }
  };

  return (
    <div className="flex-1 flex flex-col bg-slate-50">
      <div className="flex-1 overflow-y-auto p-8 space-y-4">
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

      {/* Input */}
      <div className="border-t bg-white p-4">
        <SuggestionBar />

        <div className="mt-3 flex gap-3 items-center">
          <button
            onClick={handlePlusClick}
            className="p-3 bg-slate-100 rounded-xl hover:bg-slate-200"
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

          <input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) =>
              e.key === "Enter" && !e.shiftKey && handleSendMessage(inputValue)
            }
            placeholder="Type a message..."
            className="flex-1 p-3 bg-slate-100 rounded-xl outline-none"
          />

          <button
            onClick={() => handleSendMessage(inputValue)}
            disabled={!inputValue.trim() || isLoading}
            className="p-3 bg-indigo-600 text-white rounded-xl"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}

  

