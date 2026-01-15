import React, { useState, useEffect, useRef, useCallback } from 'react';
import { 
  MessageSquare, 
  LayoutDashboard, 
  Target, 
  Settings, 
  Send, 
  Menu, 
  X, 
  Clock, 
  CheckCircle, 
  Edit2, 
  Save, 
  BarChart2, 
  Calendar,
  Activity,
  Zap,
  Sparkles,
  Loader2,
  Plus,
  FileText,
  History,
  UploadCloud,
  Trash2,
  MoreHorizontal,
  File,
  BrainCircuit,
  User,
  GripVertical
} from 'lucide-react';

// ==========================================
// 1. DATA MODELS & MOCK DATA (Schema Definition)
// ==========================================

const DUMMY_USER = {
  id: 'u_8823',
  name: 'Alex Developer',
  role: 'Pro Workspace',
  avatar_initials: 'AD',
  preferences: { theme: 'light', notifications: true }
};

const DUMMY_STATS = {
  weekly_breakdown: [
    { category: 'Coding', hours: 25, color: 'bg-blue-500' },
    { category: 'Meetings', hours: 8, color: 'bg-yellow-500' },
    { category: 'Research', hours: 12, color: 'bg-purple-500' },
    { category: 'Breaks', hours: 5, color: 'bg-green-500' },
  ],
  total_hours: 50,
  productivity_trend: 'up' // up, down, neutral
};

const DUMMY_SESSIONS = [
  { id: 's_1', title: 'Q3 Goal Planning', date: '2 hrs ago' },
  { id: 's_2', title: 'React Study Schedule', date: 'Yesterday' },
  { id: 's_3', title: 'Project Beta Sync', date: 'Oct 24' },
];

const SUGGESTED_QUERIES = [
  "Analyze my coding vs meetings balance",
  "Create a goal to read 50 pages daily",
  "Summarize my week's productivity",
  "Suggest a way to reduce meeting time"
];

const MODES = [
  { id: 'planner', label: 'Planner', icon: Calendar, desc: 'Structured & detailed' },
  { id: 'analyst', label: 'Analyst', icon: BarChart2, desc: 'Data-driven insights' },
  { id: 'motivator', label: 'Motivator', icon: Zap, desc: 'Energetic & encouraging' },
];

// ==========================================
// 2. MOCK BACKEND SERVICE
// ==========================================

const MockBackend = {
  fetchUser: async () => {
    return new Promise(resolve => setTimeout(() => resolve(DUMMY_USER), 500));
  },
  
  fetchStats: async () => {
    return new Promise(resolve => setTimeout(() => resolve(DUMMY_STATS), 800));
  },

  fetchSessions: async () => {
    return new Promise(resolve => setTimeout(() => resolve(DUMMY_SESSIONS), 600));
  },

  createGoal: async (goalData) => {
    console.log("[POST] /api/goals", goalData);
    return new Promise(resolve => setTimeout(() => resolve({ success: true, id: Date.now() }), 1200));
  }
};

// ==========================================
// 3. EXTERNAL API INTEGRATION (Gemini)
// ==========================================

const callGeminiAPI = async (prompt, systemContext = "", isJson = false) => {
  const apiKey = ""; // Injected at runtime
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`;
  
  const fullPrompt = systemContext ? `${systemContext}\n\nUser Query: ${prompt}` : prompt;

  const payload = {
    contents: [{ parts: [{ text: fullPrompt }] }],
    generationConfig: isJson ? { responseMimeType: "application/json" } : {}
  };

  const delays = [1000, 2000, 4000];
  for (let i = 0; i <= delays.length; i++) {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (!response.ok) throw new Error(`API call failed: ${response.statusText}`);

      const data = await response.json();
      const textResponse = data.candidates?.[0]?.content?.parts?.[0]?.text;
      
      if (!textResponse) throw new Error("No response content");

      return isJson ? JSON.parse(textResponse) : textResponse;
    } catch (error) {
      if (i === delays.length) {
        console.error("Gemini API Error:", error);
        throw error;
      }
      await new Promise(resolve => setTimeout(resolve, delays[i]));
    }
  }
};

// ==========================================
// 4. PRESENTATIONAL COMPONENTS
// ==========================================

const ActivityChart = ({ data }) => {
  const maxHours = Math.max(...data.map(d => d.hours));
  
  return (
    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm mt-2 w-full max-w-md animate-in fade-in zoom-in-95 duration-300">
      <h3 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
        <Activity size={16} className="text-blue-600" />
        Weekly Activity Breakdown
      </h3>
      <div className="space-y-3">
        {data.map((item) => (
          <div key={item.category} className="space-y-1">
            <div className="flex justify-between text-xs text-slate-500">
              <span>{item.category}</span>
              <span>{item.hours}h</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${item.color} transition-all duration-500`} 
                style={{ width: `${(item.hours / maxHours) * 100}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const GoalSchemaCard = ({ initialData, onSave, onCancel }) => {
  const [formData, setFormData] = useState(initialData);
  const [isEditing, setIsEditing] = useState(true);
  const [isSaved, setIsSaved] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSave = async () => {
    setIsSaving(true);
    await MockBackend.createGoal(formData);
    setIsSaving(false);
    setIsEditing(false);
    setIsSaved(true);
    onSave(formData);
  };

  if (isSaved) {
    return (
      <div className="bg-green-50 border border-green-200 p-4 rounded-xl mt-2 w-full max-w-md flex items-center gap-3 animate-in fade-in slide-in-from-bottom-2 duration-500">
        <div className="bg-green-100 p-2 rounded-full text-green-600">
          <CheckCircle size={24} />
        </div>
        <div>
          <h4 className="font-semibold text-green-900">Goal Created Successfully</h4>
          <p className="text-sm text-green-700">
            {formData.title} • {formData.target} {formData.unit}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-sm mt-2 w-full max-w-md overflow-hidden animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="bg-gradient-to-r from-purple-50 to-indigo-50 px-4 py-3 border-b border-slate-200 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Sparkles size={16} className="text-purple-600" />
          <span className="font-semibold text-slate-700 text-sm">New Goal Schema</span>
        </div>
        <span className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full">Draft</span>
      </div>
      
      <div className="p-4 space-y-4">
        <div className="space-y-1">
          <label className="text-xs font-medium text-slate-500 uppercase tracking-wide">Goal Title</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            disabled={!isEditing || isSaving}
            className="w-full text-sm font-medium text-slate-900 border-b border-slate-200 focus:border-purple-500 outline-none py-1 bg-transparent transition-colors placeholder:text-slate-300"
            placeholder="e.g., Learn React"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-500 uppercase tracking-wide">Target</label>
            <input
              type="number"
              name="target"
              value={formData.target}
              onChange={handleChange}
              disabled={!isEditing || isSaving}
              className="w-full text-sm text-slate-900 border-b border-slate-200 focus:border-purple-500 outline-none py-1 bg-transparent"
            />
          </div>
          
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-500 uppercase tracking-wide">Unit</label>
            <select
              name="unit"
              value={formData.unit}
              onChange={handleChange}
              disabled={!isEditing || isSaving}
              className="w-full text-sm text-slate-900 border-b border-slate-200 focus:border-purple-500 outline-none py-1 bg-transparent cursor-pointer"
            >
              <option value="hours">Hours</option>
              <option value="minutes">Minutes</option>
              <option value="tasks">Tasks</option>
              <option value="pages">Pages</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-500 uppercase tracking-wide">Frequency</label>
            <select
              name="frequency"
              value={formData.frequency}
              onChange={handleChange}
              disabled={!isEditing || isSaving}
              className="w-full text-sm text-slate-900 border-b border-slate-200 focus:border-purple-500 outline-none py-1 bg-transparent cursor-pointer"
            >
              <option value="Daily">Daily</option>
              <option value="Weekly">Weekly</option>
              <option value="Monthly">Monthly</option>
            </select>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-500 uppercase tracking-wide">Priority</label>
            <select
              name="priority"
              value={formData.priority}
              onChange={handleChange}
              disabled={!isEditing || isSaving}
              className="w-full text-sm text-slate-900 border-b border-slate-200 focus:border-purple-500 outline-none py-1 bg-transparent cursor-pointer"
            >
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>
        </div>
      </div>

      <div className="px-4 py-3 bg-slate-50 border-t border-slate-200 flex justify-end gap-2">
        <button 
          onClick={onCancel}
          disabled={isSaving}
          className="text-xs font-medium text-slate-500 hover:text-slate-800 px-3 py-2 transition-colors disabled:opacity-50"
        >
          Cancel
        </button>
        <button 
          onClick={handleSave}
          disabled={isSaving}
          className="bg-slate-900 hover:bg-slate-800 text-white text-xs font-medium px-4 py-2 rounded-lg flex items-center gap-2 transition-colors shadow-sm disabled:opacity-70 disabled:cursor-not-allowed"
        >
          {isSaving ? <Loader2 size={14} className="animate-spin" /> : <Save size={14} />}
          {isSaving ? 'Saving...' : 'Create Goal'}
        </button>
      </div>
    </div>
  );
};

const MessageBubble = ({ message, isBot }) => {
  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-6 group`}>
      <div className={`flex max-w-[90%] md:max-w-[75%] gap-3 ${isBot ? 'flex-row' : 'flex-row-reverse'}`}>
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${isBot ? 'bg-indigo-100 text-indigo-600' : 'bg-slate-200 text-slate-600'}`}>
          {isBot ? <Zap size={16} /> : <div className="text-xs font-bold">ME</div>}
        </div>

        <div className={`flex flex-col ${isBot ? 'items-start' : 'items-end'}`}>
          {message.text && (
            <div className={`py-3 px-4 rounded-2xl text-sm leading-relaxed shadow-sm relative break-words max-w-full ${
              isBot 
                ? 'bg-white text-slate-700 border border-slate-100 rounded-tl-none' 
                : 'bg-indigo-600 text-white rounded-tr-none'
            }`}>
              {message.text}
              {message.fileAttachment && (
                 <div className="mt-2 pt-2 border-t border-indigo-500/30 flex items-center gap-2 text-xs opacity-90">
                   <FileText size={12} />
                   Analyzed: {message.fileAttachment}
                 </div>
              )}
            </div>
          )}
          
          {message.type === 'activity-chart' && (
            <ActivityChart data={message.data} />
          )}
          
          {message.type === 'goal-schema' && (
            <GoalSchemaCard 
              initialData={message.data} 
              onSave={(data) => console.log('Goal Saved:', data)}
              onCancel={() => console.log('Goal Cancelled')}
            />
          )}
          
          <span className="text-[10px] text-slate-400 mt-1 px-1 opacity-0 group-hover:opacity-100 transition-opacity">
            {message.timestamp}
          </span>
        </div>
      </div>
    </div>
  );
};

const SidebarItem = ({ icon: Icon, label, active, onClick, collapsed, badge }) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center gap-3 p-3 rounded-xl transition-all duration-200 group relative ${
      active 
        ? 'bg-indigo-50 text-indigo-700 font-medium' 
        : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
    }`}
  >
    <Icon size={20} className={active ? 'text-indigo-600' : 'text-slate-400 group-hover:text-slate-600'} />
    {!collapsed && (
      <div className="flex-1 flex justify-between items-center text-left min-w-0">
        <span className="truncate">{label}</span>
        {badge && <span className="text-[10px] bg-indigo-100 text-indigo-600 px-1.5 py-0.5 rounded-md font-medium flex-shrink-0 ml-2">{badge}</span>}
      </div>
    )}
  </button>
);

const HistoryItem = ({ title, date, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`w-full text-left p-3 rounded-xl transition-all duration-200 hover:bg-slate-50 group ${
      active ? 'bg-slate-50 ring-1 ring-slate-200' : ''
    }`}
  >
    <p className={`text-sm font-medium truncate ${active ? 'text-indigo-700' : 'text-slate-700'}`}>{title}</p>
    <div className="flex justify-between items-center mt-1">
      <p className="text-xs text-slate-400">{date}</p>
      <MoreHorizontal size={14} className="text-slate-300 opacity-0 group-hover:opacity-100 transition-opacity" />
    </div>
  </button>
);

// ==========================================
// 5. MAIN APPLICATION COMPONENT
// ==========================================

export default function App() {
  const [userData, setUserData] = useState(null); 
  const [sessionHistory, setSessionHistory] = useState([]); 
  
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  
  const [currentMode, setCurrentMode] = useState('planner');
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [fileContext, setFileContext] = useState(null);
  
  // Sidebar Resize State
  const [sidebarWidth, setSidebarWidth] = useState(288); // Default width (w-72)
  const [isResizing, setIsResizing] = useState(false);

  const chatEndRef = useRef(null);
  const fileInputRef = useRef(null);
  const sidebarRef = useRef(null);
  
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'text',
      text: "Hello! I'm your Productivity Assistant. I'm loading your latest stats...",
      timestamp: '10:00 AM',
      sender: 'bot'
    }
  ]);

  useEffect(() => {
    const initApp = async () => {
      try {
        const user = await MockBackend.fetchUser();
        setUserData(user);
        const history = await MockBackend.fetchSessions();
        setSessionHistory(history);
        setMessages(prev => [{
          id: 2,
          type: 'text',
          text: `Welcome back, ${user.name.split(' ')[0]}! I've loaded your profile. Ask me about your activity or to create a new goal.`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          sender: 'bot'
        }]);
      } catch (err) {
        console.error("Failed to load initial data", err);
      }
    };
    initApp();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);


  // --- Resize Handlers ---
  const startResizing = useCallback(() => {
    setIsResizing(true);
  }, []);

  const stopResizing = useCallback(() => {
    setIsResizing(false);
  }, []);

  const resize = useCallback((mouseMoveEvent) => {
    if (isResizing) {
      const newWidth = mouseMoveEvent.clientX;
      if (newWidth > 200 && newWidth < 500) { // Constraint sidebar width
        setSidebarWidth(newWidth);
      }
    }
  }, [isResizing]);

  useEffect(() => {
    window.addEventListener("mousemove", resize);
    window.addEventListener("mouseup", stopResizing);
    return () => {
      window.removeEventListener("mousemove", resize);
      window.removeEventListener("mouseup", stopResizing);
    };
  }, [resize, stopResizing]);

  // --- Other Handlers ---

  const handleNewChat = () => {
    setActiveSessionId(null);
    setMessages([{
      id: Date.now(),
      type: 'text',
      text: "New session started. How can I help you optimize your productivity today?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      sender: 'bot'
    }]);
    setFileContext(null);
    setMobileMenuOpen(false);
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const tempId = Date.now();
    setMessages(prev => [...prev, {
      id: tempId,
      type: 'text',
      text: `Uploading ${file.name}...`,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }]);

    setIsTyping(true);

    try {
      let content = "";
      if (file.type === "text/plain" || file.name.endsWith('.md') || file.name.endsWith('.json') || file.name.endsWith('.js')) {
        content = await new Promise((resolve) => {
          const reader = new FileReader();
          reader.onload = (e) => resolve(e.target.result);
          reader.readAsText(file);
        });
      } else {
        content = `[Simulated Content for ${file.name}]`;
      }

      setFileContext({ name: file.name, content: content });
      
      const analysisPrompt = `I just uploaded a file named "${file.name}". Context: ${content.substring(0, 1000)}... Summarize usage.`;
      const aiResponse = await callGeminiAPI(analysisPrompt, `You are in ${currentMode} mode.`);

      setMessages(prev => [
        ...prev.filter(m => m.id !== tempId),
        {
          id: tempId,
          type: 'text',
          text: `Uploaded ${file.name}`,
          sender: 'user',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        },
        {
          id: Date.now() + 1,
          type: 'text',
          text: aiResponse,
          sender: 'bot',
          fileAttachment: file.name,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
      
      if (!activeSessionId) {
        const newId = Date.now().toString();
        setSessionHistory(prev => [{ id: newId, title: `Analysis: ${file.name}`, date: 'Just now' }, ...prev]);
        setActiveSessionId(newId);
      }

    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, {
        id: Date.now(),
        type: 'text',
        text: "Error reading file.",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleSendMessage = async (text) => {
    if (!text.trim()) return;

    const userMsg = {
      id: Date.now(),
      type: 'text',
      text: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      sender: 'user'
    };
    setMessages(prev => [...prev, userMsg]);
    setInputValue('');
    setIsTyping(true);

    if (!activeSessionId) {
      const newId = Date.now().toString();
      setActiveSessionId(newId);
      setSessionHistory(prev => [{ id: newId, title: text.substring(0, 20) + '...', date: 'Just now' }, ...prev]);
    }

    try {
      const lowerText = text.toLowerCase();
      
      if ((lowerText.includes('create') || lowerText.includes('set')) && lowerText.includes('goal')) {
         const prompt = `Extract goal details from: "${text}". JSON keys: title, target (number), unit (string), frequency, priority.`;
         const schema = await callGeminiAPI(prompt, "You are a data extractor.", true);
         
         setMessages(prev => [...prev, {
           id: Date.now() + 1,
           type: 'goal-schema',
           text: "I've drafted a goal based on your request. You can refine it below.",
           data: schema,
           sender: 'bot',
           timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
         }]);
         setIsTyping(false);
         return;
      }
      
      if (lowerText.includes('chart') || lowerText.includes('graph') || lowerText.includes('visualize') || lowerText.includes('stats')) {
        const stats = await MockBackend.fetchStats();
        
        setMessages(prev => [...prev, {
          id: Date.now() + 1,
          type: 'activity-chart',
          text: `Here is your activity breakdown. Trend is ${stats.productivity_trend}.`,
          data: stats.weekly_breakdown,
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString()
        }]);
        setIsTyping(false);
        return;
      }

      const systemContext = `
        You are a productivity assistant in '${currentMode}' mode.
        ${MODES.find(m => m.id === currentMode)?.desc}.
        User: ${userData ? userData.name : 'User'}.
        ${fileContext ? `Active Document: ${fileContext.name}: ${fileContext.content}` : ''}
      `;

      const responseText = await callGeminiAPI(text, systemContext);
      
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        type: 'text',
        text: responseText,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);

    } catch (error) {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        type: 'text',
        text: "Connection error. Please try again.",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(inputValue);
    }
  };

  return (
    // FIX: Using fixed inset-0 is more robust than h-screen for full-screen apps
    <div className="fixed inset-0 flex bg-slate-50 text-slate-900 font-sans overflow-hidden">
      
      {mobileMenuOpen && (
        <div 
          className="fixed inset-0 bg-black/20 z-40 md:hidden backdrop-blur-sm"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside 
        ref={sidebarRef}
        className={`
          fixed md:static inset-y-0 left-0 z-50 bg-white border-r border-slate-200 
          flex flex-col shadow-xl md:shadow-none flex-shrink-0 relative group
          ${mobileMenuOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
        `}
        style={{ 
          width: sidebarOpen ? sidebarWidth : 80,
          transition: isResizing ? 'none' : 'width 300ms ease-in-out'
        }}
      >
        <div className="p-4 border-b border-slate-100 flex-shrink-0">
          <div className={`flex items-center ${sidebarOpen ? 'justify-between' : 'justify-center'} mb-6`}>
            {sidebarOpen ? (
              <div className="flex items-center gap-2 text-indigo-600 font-bold text-xl min-w-0">
                <Zap className="fill-current flex-shrink-0" />
                <span className="truncate">ProdBot</span>
              </div>
            ) : (
              <Zap className="text-indigo-600 fill-current" />
            )}
             <button 
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="hidden md:flex p-1.5 hover:bg-slate-100 rounded-lg text-slate-400 transition-colors"
              >
                {sidebarOpen ? <X size={18} /> : <Menu size={18} />}
              </button>
          </div>

          <button 
            onClick={handleNewChat}
            className={`
              w-full bg-slate-900 hover:bg-slate-800 text-white rounded-xl flex items-center justify-center transition-all duration-200 shadow-sm
              ${sidebarOpen ? 'py-3 px-4 gap-2' : 'p-3'}
            `}
          >
            <Plus size={20} />
            {sidebarOpen && <span className="font-medium text-sm truncate">New Session</span>}
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-6">
          <div className="space-y-1">
             {sidebarOpen && <p className="px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Tools</p>}
             <SidebarItem icon={MessageSquare} label="Chat" active={true} onClick={() => {}} collapsed={!sidebarOpen} />
             <SidebarItem icon={LayoutDashboard} label="Dashboard" active={false} onClick={() => {}} collapsed={!sidebarOpen} />
             <SidebarItem icon={Target} label="Goals" active={false} onClick={() => {}} collapsed={!sidebarOpen} badge="3" />
          </div>

          <div className="space-y-1">
             {sidebarOpen && <p className="px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Context & Mode</p>}
             <div className="relative">
                <input 
                  type="file" 
                  ref={fileInputRef}
                  className="hidden" 
                  onChange={handleFileUpload}
                  accept=".txt,.md,.json,.pdf,.docx"
                />
                <SidebarItem 
                  icon={UploadCloud} 
                  label={fileContext ? "File Active" : "Upload Docs"} 
                  active={!!fileContext}
                  onClick={() => fileInputRef.current?.click()} 
                  collapsed={!sidebarOpen} 
                />
                {fileContext && sidebarOpen && (
                   <div className="mx-3 mt-1 bg-indigo-50 text-indigo-700 text-[10px] p-2 rounded-lg flex justify-between items-center animate-in zoom-in">
                     <span className="truncate max-w-[120px]">{fileContext.name}</span>
                     <button onClick={(e) => { e.stopPropagation(); setFileContext(null); }}><X size={12} /></button>
                   </div>
                )}
             </div>

             {sidebarOpen ? (
                <div className="grid grid-cols-3 gap-1 px-1 mt-2">
                   {MODES.map(mode => (
                     <button
                       key={mode.id}
                       onClick={() => setCurrentMode(mode.id)}
                       title={mode.desc}
                       className={`flex flex-col items-center justify-center p-2 rounded-lg transition-all border ${
                         currentMode === mode.id 
                           ? 'bg-indigo-50 border-indigo-200 text-indigo-700' 
                           : 'bg-white border-slate-100 text-slate-400 hover:border-slate-200'
                       }`}
                     >
                       <mode.icon size={16} className="mb-1" />
                       <span className="text-[10px] font-medium">{mode.label}</span>
                     </button>
                   ))}
                </div>
             ) : (
                <button className="w-full flex justify-center p-3 text-indigo-500">
                  <BrainCircuit size={20} />
                </button>
             )}
          </div>

          {sidebarOpen && (
            <div className="space-y-1">
              <div className="flex items-center justify-between px-3 mb-2">
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">History</p>
                <History size={12} className="text-slate-300" />
              </div>
              <div className="space-y-1">
                {sessionHistory.map(chat => (
                  <HistoryItem 
                    key={chat.id}
                    title={chat.title}
                    date={chat.date}
                    active={activeSessionId === chat.id}
                    onClick={() => {
                       setActiveSessionId(chat.id);
                    }}
                  />
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="p-4 border-t border-slate-100 bg-slate-50/50 flex-shrink-0">
           {sidebarOpen ? (
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 border-2 border-white shadow-sm flex items-center justify-center text-white font-bold text-xs flex-shrink-0">
                {userData?.avatar_initials || <User size={14} />}
              </div>
              <div className="overflow-hidden flex-1 min-w-0">
                <p className="text-sm font-semibold text-slate-700 truncate">{userData?.name || 'Loading...'}</p>
                <p className="text-xs text-slate-400 truncate">{userData?.role || 'Guest'}</p>
              </div>
              <button className="text-slate-400 hover:text-slate-600 flex-shrink-0"><Settings size={16}/></button>
            </div>
           ) : (
             <div className="flex justify-center">
               <div className="w-8 h-8 rounded-full bg-indigo-500"></div>
             </div>
           )}
        </div>

        {/* Resize Handle (Desktop Only) */}
        <div 
          className={`
            hidden md:block absolute right-0 top-0 bottom-0 w-1 
            cursor-col-resize hover:bg-indigo-400 hover:w-1.5
            transition-all z-50
            ${isResizing ? 'bg-indigo-500 w-1.5' : 'bg-transparent'}
          `}
          onMouseDown={startResizing}
        />
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col h-full min-w-0 bg-slate-50/30 relative overflow-hidden">
        
        {/* Mobile Header */}
        <div className="md:hidden h-16 bg-white border-b border-slate-200 flex items-center px-4 justify-between sticky top-0 z-30 flex-shrink-0">
          <button onClick={() => setMobileMenuOpen(true)} className="p-2 -ml-2 text-slate-600">
            <Menu />
          </button>
          <span className="font-semibold text-slate-800">Chat Assistant</span>
          <div className="w-8" />
        </div>

        <div className="flex-1 overflow-y-auto p-4 md:p-8 scroll-smooth w-full">
          <div className="max-w-3xl mx-auto pb-6">
            {messages.map((msg) => (
              <MessageBubble 
                key={msg.id} 
                message={msg} 
                isBot={msg.sender === 'bot'} 
              />
            ))}
            
            {isTyping && (
              <div className="flex justify-start mb-6">
                 <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center">
                       <Zap size={16} />
                    </div>
                    <div className="bg-white border border-slate-100 px-4 py-3 rounded-2xl rounded-tl-none shadow-sm flex items-center gap-2">
                      <span className="text-xs font-medium text-slate-500">
                         {fileContext ? 'Analyzing document...' : 'Thinking...'}
                      </span>
                      <Loader2 size={12} className="animate-spin text-indigo-500" />
                    </div>
                 </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
        </div>

        {/* FIX: Add flex-shrink-0 so input area doesn't get squashed */}
        <div className="bg-white border-t border-slate-200 p-4 md:p-6 z-20 flex-shrink-0">
          <div className="max-w-3xl mx-auto space-y-4">
            
            {messages.length < 3 && (
              <div className="flex gap-2 overflow-x-auto pb-2 no-scrollbar mask-gradient">
                {SUGGESTED_QUERIES.map((q, i) => (
                  <button
                    key={i}
                    onClick={() => handleSendMessage(q)}
                    className="flex-shrink-0 text-xs bg-white hover:bg-indigo-50 text-slate-600 hover:text-indigo-600 border border-slate-200 hover:border-indigo-200 px-3 py-2 rounded-lg transition-all shadow-sm whitespace-nowrap"
                  >
                    {q}
                  </button>
                ))}
              </div>
            )}

            <div className="relative flex items-end gap-2 bg-slate-50 border border-slate-200 rounded-xl p-2 shadow-sm focus-within:ring-2 focus-within:ring-indigo-100 focus-within:border-indigo-300 transition-all">
              <button 
                onClick={() => fileInputRef.current?.click()}
                className="p-2 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors flex-shrink-0"
                title="Upload Context"
              >
                <Plus size={20} />
              </button>

              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={fileContext ? `Ask about "${fileContext.name}"...` : "Type a message or /command..."}
                className="w-full bg-transparent border-none text-slate-800 placeholder:text-slate-400 text-sm resize-none focus:ring-0 px-2 py-2 max-h-32 min-h-[44px]"
                rows={1}
              />
              
              <button 
                onClick={() => handleSendMessage(inputValue)}
                disabled={!inputValue.trim()}
                className={`p-2 rounded-lg flex-shrink-0 transition-all ${
                  inputValue.trim() 
                    ? 'bg-indigo-600 text-white shadow-md hover:bg-indigo-700 transform hover:scale-105' 
                    : 'bg-slate-200 text-slate-400 cursor-not-allowed'
                }`}
              >
                <Send size={18} className={inputValue.trim() ? "ml-0.5" : ""} />
              </button>
            </div>
            
            <div className="flex justify-between items-center px-1">
              <p className="text-[10px] text-slate-400">
                Mode: <span className="font-medium text-indigo-500 capitalize">{currentMode}</span>
              </p>
              <p className="text-[10px] text-slate-400">
                AI can make mistakes. Check generated goals.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}