// import { useDispatch, useSelector } from "react-redux";
// import { useSendChatPromptMutation } from "../services/geminiApi";
// import { GoalSchemaCard } from "./GoalSchemaCard";
// import { useFileUpload } from "../hooks/useFileUpload"; // your hook path

// import {
//   addMessage,
//   setSession,
//   addToHistory,
  
// } from "../store/chatSlice";

// import MessageBubble from "./MessageBubble";
// import SuggestionBar from "./SuggestionBar";
// import { Send, Loader2, Plus } from "lucide-react";
// import { useRef, useEffect, useState } from "react";
// const GOAL_SYSTEM_CONTEXT = `
// You are a helpful assistant.
// TASK: Determine if the user wants to create a specific goal, task, or habit.

// 1. If it IS a goal (e.g., "I want to read 50 pages", "set a target for DSA"):
//    Respond ONLY with this JSON:
//    {
//      "isGoal": true,
//      "data": { "title": "...", "target": 0, "unit": "...", "frequency": "...", "priority": "..." }
//    }

// 2. If it is NOT a goal (e.g., "Hello", "How are you?", "What is 2+2?"):
//    Respond ONLY with this JSON:
//    {
//      "isGoal": false,
//      "reply": "Your helpful conversational response here"
//    }
// `;

// export default function ChatInterface() {
//   const dispatch = useDispatch();
//   const { uploadFile } = useFileUpload();
//   const fileInputRef = useRef(null);

//   const handlePlusClick = () => {
//     fileInputRef.current?.click();
//   };

//   const handleFileChange = (e) => {
//     const file = e.target.files[0];
//     if (!file) return;
//     uploadFile(file);
//     e.target.value = null; // reset input to allow re-upload of same file
//   };

//   const [inputValue, setInputValue] = useState("");

//   const { messages, activeSessionId } = useSelector((s) => s.chat);
//   const { currentMode, fileContext } = useSelector((s) => s.app);

//   const [sendPrompt, { isLoading }] = useSendChatPromptMutation();
//   const chatEndRef = useRef(null);

//   useEffect(() => {
//     chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [messages, isLoading]);
   
//  const handleSendMessage = async (text) => {
//    if (!text.trim() || isLoading) return;

//    // 1. Add User Message to UI
//    dispatch(addMessage({ id: Date.now(), text, sender: "user" }));
//    setInputValue("");

//    // Create new session if none exists (keeping your original logic)
//    if (!activeSessionId) {
//      const newId = Date.now().toString();
//      dispatch(setSession(newId));
//      dispatch(addToHistory({ id: newId, title: text, date: "Just now" }));
//    }

//    try {
//      const systemContext = `${GOAL_SYSTEM_CONTEXT}\nMode: ${currentMode}. File: ${
//        fileContext?.name || "None"
//      }`;

//      // 2. Call Gemini API
//      const aiRawResponse = await sendPrompt({
//        prompt: text,
//        systemContext,
//        isJson: true,
//      }).unwrap();

//      // 3. Parse the JSON response
//      const parsed = JSON.parse(aiRawResponse);

//      // 4. Determine how to display the response
//      if (parsed.isGoal === true || parsed.isGoal === "true") {
//        // If it is a goal, dispatch with type 'goal_schema' to trigger the Card UI
//        dispatch(
//          addMessage({
//            id: Date.now() + 1,
//            sender: "bot",
//            type: "goal_schema", // This matches your conditional rendering logic
//            goalData: parsed.data,
//          })
//        );
//      } else {
//        // If it is NOT a goal, only dispatch the 'reply' string
//        // This prevents raw JSON from appearing in the MessageBubble
//        dispatch(
//          addMessage({
//            id: Date.now() + 1,
//            sender: "bot",
//            text: parsed.reply || "How can I help you today?",
//          })
//        );
//      }
//    } catch (error) {
//      console.error("Error parsing AI response:", error);
//      // Fallback if parsing fails (Gemini might sometimes return plain text despite isJson: true)
//      dispatch(
//        addMessage({
//          id: Date.now() + 1,
//          text: "I encountered an error parsing the goal. Let's try chatting normally!",
//          sender: "bot",
//        })
//      );
//    }
//  };
//   return (
//     <div className="flex-1 flex flex-col bg-slate-50">
//       <div className="flex-1 overflow-y-auto p-8 space-y-4">
//         {messages.map((m) => (
//           <div key={m.id}>
//             {/* 1. Check if the message is a Goal Schema */}
//             {m.type === "goal_schema" ? (
//               <div className="flex flex-col items-start gap-2">
//                 <p className="text-sm text-slate-500 ml-2 italic">
//                   I've drafted a goal based on your request. You can refine it
//                   below.
//                 </p>
//                 <GoalSchemaCard
//                   initialData={m.goalData}
//                   onSave={(finalData) => {
//                     console.log("Goal Saved:", finalData);
//                     // You can add logic here to update the message status in Redux if needed
//                   }}
//                   onCancel={() => {
//                     // Logic to ignore/remove the draft
//                   }}
//                 />
//               </div>
//             ) : (
//               /* 2. Otherwise, render the standard Message Bubble */
//               <MessageBubble message={m} isBot={m.sender === "bot"} />
//             )}
//           </div>
//         ))}

//         {isLoading && (
//           <div className="flex items-center gap-2 text-slate-400">
//             <Loader2 className="animate-spin" size={18} />
//             <span className="text-sm font-medium">Thinking...</span>
//           </div>
//         )}
//         <div ref={chatEndRef} />
//       </div>

//       {/* Input Area */}
//       <div className="border-t bg-white p-4">
//         <SuggestionBar />

//         <div className="mt-3 flex gap-3 items-center">
//           <button
//             onClick={handlePlusClick}
//             className="p-3 bg-slate-100 rounded-xl hover:bg-slate-200 transition-colors"
//           >
//             <Plus size={18} />
//           </button>

//           <input
//             ref={fileInputRef}
//             type="file"
//             style={{ display: "none" }}
//             onChange={handleFileChange}
//             accept=".pdf,.doc,.docx,.txt"
//           />

//           <input
//             value={inputValue}
//             onChange={(e) => setInputValue(e.target.value)}
//             onKeyDown={(e) =>
//               e.key === "Enter" && !e.shiftKey && handleSendMessage(inputValue)
//             }
//             placeholder="Type a message or /command..."
//             className="flex-1 p-3 bg-slate-100 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500/20 transition-all"
//           />

//           <button
//             onClick={() => handleSendMessage(inputValue)}
//             disabled={!inputValue.trim() || isLoading}
//             className="p-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 disabled:opacity-50 transition-colors"
//           >
//             <Send size={18} />
//           </button>
//         </div>

//         <div className="text-xs text-slate-400 mt-2 flex justify-between px-1">
//           <span>
//             Mode:{" "}
//             <span className="font-semibold text-slate-600">{currentMode}</span>
//           </span>
//           <span>AI can make mistakes. Check generated goals.</span>
//         </div>
//       </div>
//     </div>
//   );
// }
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

  

