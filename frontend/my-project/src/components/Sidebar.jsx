// import { useDispatch, useSelector } from "react-redux";
// import { setSession, addToHistory } from "../store/chatSlice";
// import { MessageSquare, LayoutDashboard, Target, X, Plus } from "lucide-react";
// import { useNavigate } from "react-router-dom";
// import { useState, useEffect, useRef } from "react";

// const MIN_WIDTH = 80;
// const MAX_WIDTH = 340;

// export default function Sidebar() {
//   const { history, activeSessionId } = useSelector((s) => s.chat);
//   const dispatch = useDispatch();
//   const navigate = useNavigate();

//   const [collapsed, setCollapsed] = useState(false);
//   const [width, setWidth] = useState(300);

//   const sidebarRef = useRef(null);
//   const dragging = useRef(false);

//   const startDrag = () => {
//     dragging.current = true;
//   };

//   const stopDrag = () => {
//     dragging.current = false;
//   };

//   const onDrag = (e) => {
//     if (!dragging.current) return;

//     const sidebarLeft = sidebarRef.current.getBoundingClientRect().left;
//     let newWidth = e.clientX - sidebarLeft;

//     if (newWidth < MIN_WIDTH) newWidth = MIN_WIDTH;
//     if (newWidth > MAX_WIDTH) newWidth = MAX_WIDTH;

//     setWidth(newWidth);
//     setCollapsed(false);
//   };

//   useEffect(() => {
//     window.addEventListener("mousemove", onDrag);
//     window.addEventListener("mouseup", stopDrag);

//     return () => {
//       window.removeEventListener("mousemove", onDrag);
//       window.removeEventListener("mouseup", stopDrag);
//     };
//   }, []);

//   const createSession = () => {
//     const id = Date.now().toString();
//     dispatch(setSession(id));
//     dispatch(addToHistory({ id, title: "New Chat", date: "Just now" }));
//     navigate(`/session/${id}`);
//   };

//   return (
//     <div
//       ref={sidebarRef}
//       style={{
//         width: collapsed ? MIN_WIDTH : width,
//         minWidth: MIN_WIDTH,
//         maxWidth: MAX_WIDTH,
//       }}
//       className="relative bg-white border-r flex flex-col h-screen overflow-hidden shrink-0"
//     >
//       {/* Resize handle */}
//       <div
//         onMouseDown={startDrag}
//         className="absolute top-0 right-0 h-full w-[3px] cursor-ew-resize bg-slate-200 hover:bg-indigo-500"
//       />

//       {/* Header */}
//       <div className="p-5 border-b flex items-center justify-between">
//         {!collapsed && (
//           <h1 className="font-bold text-indigo-600 text-lg">⚡ ProdBot</h1>
//         )}
//         <button
//           onClick={() => setCollapsed(!collapsed)}
//           className="text-slate-400 hover:text-slate-600"
//         >
//           <X size={18} />
//         </button>
//       </div>

//       {/* New Session */}
//       <div className="p-4">
//         <button
//           onClick={createSession}
//           className="w-full bg-slate-900 text-white py-3 rounded-2xl font-medium shadow flex items-center justify-center gap-2"
//         >
//           <Plus size={18} />
//           {!collapsed && "New Session"}
//         </button>
//       </div>

//       {/* Tools */}
//       <div className="px-4">
//         {!collapsed && <p className="text-xs text-slate-400 mb-2">TOOLS</p>}
//         <Tool
//           icon={<MessageSquare size={18} />}
//           label="Chat"
//           collapsed={collapsed}
//         />
//         <Tool
//           icon={<LayoutDashboard size={18} />}
//           label="Dashboard"
//           collapsed={collapsed}
//         />
//         <Tool icon={<Target size={18} />} label="Goals" collapsed={collapsed} />
//       </div>

//       {/* History */}
//       <div className="flex-1 overflow-y-auto mt-4 px-4">
//         {!collapsed && <p className="text-xs text-slate-400 mb-2">HISTORY</p>}
//         {history.map((h) => (
//           <div
//             key={h.id}
//             onClick={() => {
//               dispatch(setSession(h.id));
//               navigate(`/session/${h.id}`);
//             }}
//             className={`p-3 rounded-xl cursor-pointer text-sm mb-1 flex items-center gap-2 ${
//               activeSessionId === h.id
//                 ? "bg-indigo-50 text-indigo-700 font-medium"
//                 : "hover:bg-slate-100 text-slate-600"
//             }`}
//           >
//             <MessageSquare size={16} />
//             {!collapsed && h.title}
//           </div>
//         ))}
//       </div>

//       {/* Footer */}
//       <div className="p-4 border-t flex items-center gap-3">
//         <div className="w-10 h-10 rounded-full bg-indigo-500 text-white flex items-center justify-center font-bold">
//           AD
//         </div>
//         {!collapsed && (
//           <div>
//             <p className="font-medium text-sm">Alex Developer</p>
//             <p className="text-xs text-slate-400">Pro Workspace</p>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }

// function Tool({ icon, label, collapsed }) {
//   return (
//     <div className="flex items-center gap-3 p-3 text-slate-600 hover:bg-slate-100 rounded-xl justify-center md:justify-start">
//       {icon}
//       {!collapsed && <span>{label}</span>}
//     </div>
//   );
// }

import { useDispatch, useSelector } from "react-redux";
import { setSession, addToHistory } from "../store/chatSlice";
import { MessageSquare, LayoutDashboard, Target, X, Plus } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import { useCreateNewChatMutation } from "../services/chatApi"; // 👈 NEW

const MIN_WIDTH = 80;
const MAX_WIDTH = 340;

export default function Sidebar() {
  const { history, activeSessionId } = useSelector((s) => s.chat);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [collapsed, setCollapsed] = useState(false);
  const [width, setWidth] = useState(300);

  const sidebarRef = useRef(null);
  const dragging = useRef(false);

  const [createNewChat] = useCreateNewChatMutation(); // 👈 NEW

  const startDrag = () => {
    dragging.current = true;
  };

  const stopDrag = () => {
    dragging.current = false;
  };

  const onDrag = (e) => {
    if (!dragging.current) return;

    const sidebarLeft = sidebarRef.current.getBoundingClientRect().left;
    let newWidth = e.clientX - sidebarLeft;

    if (newWidth < MIN_WIDTH) newWidth = MIN_WIDTH;
    if (newWidth > MAX_WIDTH) newWidth = MAX_WIDTH;

    setWidth(newWidth);
    setCollapsed(false);
  };

  useEffect(() => {
    window.addEventListener("mousemove", onDrag);
    window.addEventListener("mouseup", stopDrag);

    return () => {
      window.removeEventListener("mousemove", onDrag);
      window.removeEventListener("mouseup", stopDrag);
    };
  }, []);

  // 🔑 UPDATED: backend-driven session creation
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
      console.error("Failed to create new chat", err);
    }
  };

  return (
    <div
      ref={sidebarRef}
      style={{
        width: collapsed ? MIN_WIDTH : width,
        minWidth: MIN_WIDTH,
        maxWidth: MAX_WIDTH,
      }}
      className="relative bg-white border-r flex flex-col h-screen overflow-hidden shrink-0"
    >
      {/* Resize handle */}
      <div
        onMouseDown={startDrag}
        className="absolute top-0 right-0 h-full w-[3px] cursor-ew-resize bg-slate-200 hover:bg-indigo-500"
      />

      {/* Header */}
      <div className="p-5 border-b flex items-center justify-between">
        {!collapsed && (
          <h1 className="font-bold text-indigo-600 text-lg">⚡ ProdBot</h1>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="text-slate-400 hover:text-slate-600"
        >
          <X size={18} />
        </button>
      </div>

      {/* New Session */}
      <div className="p-4">
        <button
          onClick={createSession}
          className="w-full bg-slate-900 text-white py-3 rounded-2xl font-medium shadow flex items-center justify-center gap-2"
        >
          <Plus size={18} />
          {!collapsed && "New Session"}
        </button>
      </div>

      {/* Tools */}
      <div className="px-4">
        {!collapsed && <p className="text-xs text-slate-400 mb-2">TOOLS</p>}
        <Tool
          icon={<MessageSquare size={18} />}
          label="Chat"
          collapsed={collapsed}
        />
        <Tool
          icon={<LayoutDashboard size={18} />}
          label="Dashboard"
          collapsed={collapsed}
        />
        <Tool icon={<Target size={18} />} label="Goals" collapsed={collapsed} />
      </div>

      {/* History */}
      <div className="flex-1 overflow-y-auto mt-4 px-4">
        {!collapsed && <p className="text-xs text-slate-400 mb-2">HISTORY</p>}
        {history.map((h) => (
          <div
            key={h.id}
            onClick={() => {
              dispatch(setSession(h.id));
              navigate(`/session/${h.id}`);
            }}
            className={`p-3 rounded-xl cursor-pointer text-sm mb-1 flex items-center gap-2 ${
              activeSessionId === h.id
                ? "bg-indigo-50 text-indigo-700 font-medium"
                : "hover:bg-slate-100 text-slate-600"
            }`}
          >
            <MessageSquare size={16} />
            {!collapsed && h.title}
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="p-4 border-t flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-indigo-500 text-white flex items-center justify-center font-bold">
          AD
        </div>
        {!collapsed && (
          <div>
            <p className="font-medium text-sm">Alex Developer</p>
            <p className="text-xs text-slate-400">Pro Workspace</p>
          </div>
        )}
      </div>
    </div>
  );
}

function Tool({ icon, label, collapsed }) {
  return (
    <div className="flex items-center gap-3 p-3 text-slate-600 hover:bg-slate-100 rounded-xl justify-center md:justify-start">
      {icon}
      {!collapsed && <span>{label}</span>}
    </div>
  );
}
