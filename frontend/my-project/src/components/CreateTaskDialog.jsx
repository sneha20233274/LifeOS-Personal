import { useState, useRef, useEffect } from 'react';
import { 
  X, Calendar, AlignLeft, MapPin, Tag, Flag, Clock, ChevronDown, Check,
  Briefcase, Heart, Sun, CheckSquare ,AlertCircle// <--- Fixed: Added CheckSquare here
} from 'lucide-react';
import CalendarPicker from './CalendarPicker'; 

// --- CONFIG: Colors & Icons ---
const CATEGORIES = [
  { id: 'General', icon: CheckSquare, color: 'text-gray-500', bg: 'bg-gray-100' },
  { id: 'Work', icon: Briefcase, color: 'text-purple-500', bg: 'bg-purple-100' },
  { id: 'Personal', icon: Sun, color: 'text-amber-500', bg: 'bg-amber-100' },
  { id: 'Health', icon: Heart, color: 'text-rose-500', bg: 'bg-rose-100' },
];

const PRIORITIES = [
  { id: 'Low', color: 'bg-blue-400', label: 'Low Priority' },
  { id: 'Medium', color: 'bg-orange-400', label: 'Medium Priority' },
  { id: 'High', color: 'bg-red-500', label: 'High Priority' },
];

// --- SUB-COMPONENT 1: Custom Dropdown (Category & Priority) ---
const CustomSelect = ({ label, value, options, onChange, type = 'category' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    if (isOpen) document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen]);

  // Find currently selected option object
  const selectedOption = options.find(opt => opt.id === value) || options[0];

  return (
    <div className="flex-1 space-y-1" ref={containerRef}>
      <label className="flex items-center gap-2 text-xs font-semibold text-gray-500">
        {type === 'category' ? <Tag className="w-3 h-3" /> : <Flag className="w-3 h-3" />} 
        {label}
      </label>
      
      <div className="relative">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className={`
            w-full flex items-center justify-between p-2.5 rounded-xl border text-sm font-medium transition-all
            ${isOpen 
              ? 'border-[#F49F99] ring-2 ring-[#F49F99]/10 bg-white' 
              : 'border-transparent bg-gray-50 hover:bg-gray-100 hover:border-gray-200'
            }
          `}
        >
          <div className="flex items-center gap-2">
            {/* Render Selected Value */}
            {type === 'category' ? (
              <>
                <div className={`p-1 rounded-md ${selectedOption.bg}`}>
                  <selectedOption.icon className={`w-3.5 h-3.5 ${selectedOption.color}`} />
                </div>
                <span className="text-gray-700">{selectedOption.id}</span>
              </>
            ) : (
              <>
                <div className={`w-2.5 h-2.5 rounded-full ${selectedOption.color}`} />
                <span className="text-gray-700">{selectedOption.id}</span>
              </>
            )}
          </div>
          <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
        </button>

        {/* Dropdown Menu */}
        {isOpen && (
          <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden z-50 animate-in fade-in zoom-in-95 duration-100">
            {options.map((option) => (
              <button
                key={option.id}
                onClick={() => {
                  onChange(option.id);
                  setIsOpen(false);
                }}
                className={`
                  w-full flex items-center justify-between px-3 py-2.5 text-sm transition-colors
                  ${value === option.id ? 'bg-[#F49F99]/5' : 'hover:bg-gray-50'}
                `}
              >
                <div className="flex items-center gap-3">
                  {type === 'category' ? (
                    <>
                      <div className={`p-1.5 rounded-lg ${option.bg}`}>
                        <option.icon className={`w-4 h-4 ${option.color}`} />
                      </div>
                      <span className={`font-medium ${value === option.id ? 'text-[#F49F99]' : 'text-gray-700'}`}>
                        {option.id}
                      </span>
                    </>
                  ) : (
                    <>
                      <div className={`w-3 h-3 rounded-full ${option.color}`} />
                      <span className={`font-medium ${value === option.id ? 'text-[#F49F99]' : 'text-gray-700'}`}>
                        {option.id}
                      </span>
                    </>
                  )}
                </div>
                
                {value === option.id && <Check className="w-4 h-4 text-[#F49F99]" />}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};


// --- SUB-COMPONENT 2: Time Picker Popover ---
const TimePickerPopover = ({ time, onChange, onClose }) => {
  const [hours, minutes] = time.split(':');
  
  // Generate arrays for HH (00-23) and MM (00-55, step 5)
  const hourOptions = Array.from({ length: 24 }, (_, i) => i.toString().padStart(2, '0'));
  const minuteOptions = Array.from({ length: 12 }, (_, i) => (i * 5).toString().padStart(2, '0'));

  return (
    <div className="bg-white rounded-xl shadow-xl border border-gray-100 p-2 flex gap-2 w-48 animate-in fade-in zoom-in-95 duration-200">
      {/* Hours Column */}
      <div className="flex-1 h-48 overflow-y-auto no-scrollbar flex flex-col gap-1 border-r border-gray-50 pr-1">
        <span className="text-[10px] text-gray-400 text-center font-bold sticky top-0 bg-white pb-1">HR</span>
        {hourOptions.map((h) => (
          <button
            key={h}
            onClick={() => onChange(`${h}:${minutes}`)}
            className={`py-1.5 rounded-md text-sm font-medium transition-colors ${
              hours === h ? 'bg-[#F49F99] text-white' : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            {h}
          </button>
        ))}
      </div>

      {/* Minutes Column */}
      <div className="flex-1 h-48 overflow-y-auto no-scrollbar flex flex-col gap-1 pl-1">
        <span className="text-[10px] text-gray-400 text-center font-bold sticky top-0 bg-white pb-1">MIN</span>
        {minuteOptions.map((m) => (
          <button
            key={m}
            onClick={() => {
              onChange(`${hours}:${m}`);
              if(onClose) onClose(); // Optional: Close after selecting minute
            }}
            className={`py-1.5 rounded-md text-sm font-medium transition-colors ${
              minutes === m ? 'bg-[#F49F99] text-white' : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            {m}
          </button>
        ))}
      </div>
    </div>
  );
};

// --- SUB-COMPONENT 3: Custom Time Input Trigger ---
const CustomTimeInput = ({ value, onChange, isError }) => {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef(null);

  // Close on click outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    if (isOpen) document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen]);

  return (
    <div className="relative" ref={containerRef}>
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className={`
          flex items-center gap-2 px-3 py-2 rounded-lg border text-sm font-medium transition-all
          ${isError 
            ? 'border-red-300 text-red-500 bg-red-50 hover:border-red-400' 
            : isOpen 
              ? 'border-[#F49F99] text-[#F49F99] bg-[#F49F99]/5' 
              : 'border-transparent bg-gray-50 text-gray-700 hover:border-[#F49F99]/30 hover:text-[#F49F99]'
          }
        `}
      >
        <span>{value}</span>
        <ChevronDown className={`w-3 h-3 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute top-10 left-0 z-50">
          <TimePickerPopover 
            time={value} 
            onChange={onChange} 
          />
        </div>
      )}
    </div>
  );
};

// --- MAIN COMPONENT: Create Task Dialog ---
export function CreateTaskDialog({ isOpen, onClose, onSave, initialDate }) {
  const [title, setTitle] = useState('');
  const [startTimeStr, setStartTimeStr] = useState('09:00');
  const [endTimeStr, setEndTimeStr] = useState('10:00');
  const [isAllDay, setIsAllDay] = useState(false);
  const [description, setDescription] = useState('');
  const [locationOrLink, setLocationOrLink] = useState('');
  
  // Use the Config IDs for state
  const [category, setCategory] = useState('General');
  const [priority, setPriority] = useState('Medium');

  // Date Picker State
  const [dateObj, setDateObj] = useState(initialDate); 
  useEffect(() => {
    setDateObj(initialDate);
  }, [initialDate]);

  const [isDatePickerOpen, setIsDatePickerOpen] = useState(false);
  const datePickerRef = useRef(null);

  // Close popover when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (datePickerRef.current && !datePickerRef.current.contains(event.target)) {
        setIsDatePickerOpen(false);
      }
    };
    if (isDatePickerOpen) document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isDatePickerOpen]);

  // --- VALIDATION LOGIC ---
  const getMinutes = (timeStr) => {
    const [h, m] = timeStr.split(':').map(Number);
    return h * 60 + m;
  };
  
  // Check if End Time is strictly greater than Start Time (only if not All Day)
  const isTimeInvalid = !isAllDay && getMinutes(endTimeStr) <= getMinutes(startTimeStr);

  if (!isOpen) return null;
  
  const resetForm = () => {
      setTitle('');
      setDescription('');
      setLocationOrLink('');
      setStartTimeStr('09:00');
      setEndTimeStr('10:00');
      setCategory('General');
      setPriority('Medium');
      setIsAllDay(false);
  };
  
  const handleSave = () => {
    if (!title.trim()) return;
    if (isTimeInvalid) return; // Prevent save if time is invalid

    // Convert dateObj to string for constructing timestamps
    const dateStr = dateObj.toISOString().split('T')[0];
    const startDateTime = new Date(`${dateStr}T${startTimeStr}:00`);
    const endDateTime = new Date(`${dateStr}T${endTimeStr}:00`);

    const newRoutineEvent = {
      title,
      description,
      start_time: startDateTime.toISOString(),
      end_time: endDateTime.toISOString(),
      is_all_day: isAllDay,
      category,
      priority,
      status: "Scheduled",
      location_or_link: locationOrLink || null,
      source: "manual"
    };
    
    onSave(newRoutineEvent);
    onClose();
    resetForm();
  };

  const formatDateDisplay = (date) => {
    return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
  };

  return (
    <>
      {/* Overlay */}
      <div 
        className="fixed inset-0 bg-black/50 z-[1400] transition-opacity" 
        onClick={onClose} 
      />
      
      {/* Modal Content */}
      <div className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-[1401] w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-2xl m-4 overflow-visible"> 
          
          {/* Header */}
          <div className="p-6 relative bg-[#F49F99]/90 rounded-t-2xl">
             <button onClick={onClose} className="absolute right-4 top-4 w-8 h-8 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center text-white">
              <X className="w-5 h-5" />
            </button>
             <div className="pt-4">
              <input
                type="text"
                placeholder="What is your routine?"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full bg-transparent border-none outline-none text-white text-2xl font-bold placeholder-white/70"
                autoFocus
              />
            </div>
          </div>

          <div className="p-6 space-y-5">
            
            {/* --- SECTION 1: DATE & TIME --- */}
            <div className="space-y-4">
              
              {/* Row 1: Date & All Day Toggle */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3 relative" ref={datePickerRef}>
                   <Calendar className="w-5 h-5 text-[#F49F99]" />
                   
                   {/* Custom Date Trigger */}
                   <button 
                     onClick={() => setIsDatePickerOpen(!isDatePickerOpen)}
                     className="text-sm font-medium hover:text-[#F49F99] transition-colors bg-gray-50 px-3 py-1.5 rounded-lg border border-transparent hover:border-[#F49F99]/30"
                   >
                     {formatDateDisplay(dateObj)}
                   </button>

                   {/* External Calendar Component */}
                   {isDatePickerOpen && (
                     <div className="absolute top-10 left-0 z-50 animate-in fade-in zoom-in-95 duration-200">
                       <CalendarPicker 
                         selectedDate={dateObj} 
                         onDateChange={(d) => {
                           setDateObj(d);
                           setIsDatePickerOpen(false);
                         }}
                       />
                     </div>
                   )}
                </div>

                <label className="flex items-center gap-2 cursor-pointer bg-gray-50 px-3 py-1.5 rounded-lg border border-transparent hover:bg-gray-100 transition-colors">
                  <span className="text-xs font-medium text-gray-600">All Day</span>
                  <div className={`w-8 h-4 rounded-full p-0.5 transition-colors ${isAllDay ? 'bg-[#F49F99]' : 'bg-gray-300'}`}>
                    <div className={`w-3 h-3 bg-white rounded-full shadow-sm transition-transform ${isAllDay ? 'translate-x-4' : 'translate-x-0'}`} />
                  </div>
                  <input type="checkbox" checked={isAllDay} onChange={(e) => setIsAllDay(e.target.checked)} className="hidden" />
                </label>
              </div>

              {/* Row 2: Time Selection (Custom Pickers) */}
              {!isAllDay && (
                <div className="flex flex-col gap-2 animate-in slide-in-from-top-2 duration-200">
                  <div className="flex items-center gap-3 pl-8">
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4 text-gray-400" />
                      <CustomTimeInput value={startTimeStr} onChange={setStartTimeStr} />
                    </div>
                    <span className="text-gray-300 font-medium">-</span>
                    {/* Pass isError prop to highlight input if invalid */}
                    <CustomTimeInput 
                      value={endTimeStr} 
                      onChange={setEndTimeStr} 
                      isError={isTimeInvalid} 
                    />
                  </div>
                  
                  {/* Validation Error Message */}
                  {isTimeInvalid && (
                    <div className="flex items-center gap-2 pl-8 text-xs text-red-500 font-medium animate-in fade-in slide-in-from-left-2">
                      <AlertCircle className="w-3 h-3" />
                      <span>End time must be after start time</span>
                    </div>
                  )}
                </div>
              )}
            </div>

            <hr className="border-gray-100" />

            {/* --- SECTION 2: CATEGORY & PRIORITY --- */}
            <div className="flex gap-4">
               <CustomSelect 
                 label="Category" 
                 type="category" 
                 value={category} 
                 options={CATEGORIES} 
                 onChange={setCategory} 
               />
               <CustomSelect 
                 label="Priority" 
                 type="priority" 
                 value={priority} 
                 options={PRIORITIES} 
                 onChange={setPriority} 
               />
            </div>

            {/* --- SECTION 3: DETAILS --- */}
            <div className="space-y-2">
              <label className="flex items-center gap-2 text-sm font-medium text-gray-600">
                <AlignLeft className="w-4 h-4 text-[#F49F99]" /> Description
              </label>
              <textarea 
                value={description} 
                onChange={(e) => setDescription(e.target.value)} 
                placeholder="Add notes..." 
                rows={2} 
                className="w-full p-3 rounded-lg bg-gray-50 border-none outline-none text-sm resize-none focus:ring-1 focus:ring-[#F49F99]" 
              />
            </div>

            <div className="space-y-2">
               <div className="flex items-center gap-3 border-b border-gray-100 pb-2">
                 <MapPin className="w-4 h-4 text-[#F49F99]" />
                 <input 
                   type="text" 
                   value={locationOrLink} 
                   onChange={(e) => setLocationOrLink(e.target.value)} 
                   placeholder="Add location or link..." 
                   className="flex-1 outline-none text-sm placeholder-gray-400" 
                 />
               </div>
            </div>
          </div>

          {/* Footer */}
          <div className="p-6 bg-gray-50 rounded-b-2xl">
            <button 
              onClick={handleSave} 
              disabled={!title.trim() || isTimeInvalid} 
              className="w-full py-3 rounded-xl bg-[#F49F99] text-white font-semibold shadow-md hover:bg-[#e08e88] transition-all disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg transform active:scale-[0.98]"
            >
              Create Event
            </button>
          </div>
        </div>
      </div>
    </>
  );
}