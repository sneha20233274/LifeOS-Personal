import React, { useState, useRef, useEffect } from 'react';
import { Inbox, ChevronLeft, ChevronRight, ChevronDown, Sparkles, LayoutGrid, List } from 'lucide-react';
// standard colored Google icon
import { FcGoogle } from "react-icons/fc"; 
import CalendarPicker from './CalendarPicker'; 

const CalendarHeader = ({ 
  days = [], 
  selectedDate, 
  onDateSelect,
  // New Props for Google Logic
  isGoogleLinked = false,   // Does the user have an account connected in DB?
  isGoogleVisible = false,  // Are we currently showing the google events?
  onGoogleClick             // Function to handle the click
}) => {
  const [isDatePickerOpen, setIsDatePickerOpen] = useState(false);
  const datePickerRef = useRef(null);

  // --- SAFETY ---
  const safeDate = (selectedDate instanceof Date && !isNaN(selectedDate)) 
    ? selectedDate 
    : new Date();

  // --- 1. Close Popover on Click Outside ---
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (datePickerRef.current && !datePickerRef.current.contains(event.target)) {
        setIsDatePickerOpen(false);
      }
    };
    if (isDatePickerOpen) document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isDatePickerOpen]);

  // --- 2. Navigation Handlers ---
  const handlePreviousDay = () => {
    const newDate = new Date(safeDate);
    newDate.setDate(newDate.getDate() - 1);
    onDateSelect(newDate);
  };

  const handleNextDay = () => {
    const newDate = new Date(safeDate);
    newDate.setDate(newDate.getDate() + 1);
    onDateSelect(newDate);
  };

  // --- 3. Week Days Logic ---
  const getWeekDays = () => {
    const weekDaysArr = [];
    const startOfWeek = new Date(safeDate);
    const day = startOfWeek.getDay(); 
    startOfWeek.setDate(startOfWeek.getDate() - day); 

    for (let i = 0; i < 7; i++) {
      const d = new Date(startOfWeek);
      d.setDate(d.getDate() + i);
      weekDaysArr.push(d);
    }
    return weekDaysArr;
  };

  const weekDays = getWeekDays();
  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  // --- 4. Render Dots ---
  const renderTaskIndicator = (category) => {
    switch(category) {
      case 'Work':      return <div className="w-1.5 h-1.5 bg-purple-500 rounded-full shadow-sm" title="Work"></div>;
      case 'Personal':  return <div className="w-1.5 h-1.5 bg-amber-400 rounded-full shadow-sm" title="Personal"></div>;
      case 'Health':    return <div className="w-1.5 h-1.5 bg-rose-400 rounded-full shadow-sm" title="Health"></div>;
      default:          return <div className="w-1.5 h-1.5 bg-gray-300 rounded-full"></div>;
    }
  };

  return (
    <div className="w-full bg-[#F8F8F8] pt-4 pb-4 px-4 md:px-8 z-20 relative shadow-sm border-b border-gray-100">
      
      {/* --- TOP CONTROL BAR --- */}
      <div className="flex justify-between items-center mb-6">
        
        <div className="flex items-center gap-4">
          
          {/* Navigation Arrows */}
          <div className="flex gap-1">
             <button onClick={handlePreviousDay} className="p-1.5 hover:bg-white hover:shadow-sm rounded-full text-gray-600 transition-all"><ChevronLeft className="w-5 h-5" /></button>
             <button onClick={handleNextDay} className="p-1.5 hover:bg-white hover:shadow-sm rounded-full text-gray-600 transition-all"><ChevronRight className="w-5 h-5" /></button>
          </div>

          {/* Date Title & Picker Trigger */}
          <div className="relative" ref={datePickerRef}>
            <div 
               onClick={() => setIsDatePickerOpen(!isDatePickerOpen)}
               className="flex items-baseline gap-2 cursor-pointer select-none group"
            >
              <h1 className="text-2xl font-bold text-gray-800 tracking-tight">{safeDate.toLocaleString('default', { month: 'long' })}</h1>
              <span className="text-2xl font-bold text-[#F49F99]">{safeDate.getFullYear()}</span>
              <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform duration-200 ${isDatePickerOpen ? 'rotate-180' : 'group-hover:rotate-180'}`} />
            </div>

            {/* POPOVER */}
            {isDatePickerOpen && (
              <div className="absolute top-12 left-0 z-50 animate-in fade-in zoom-in-95 duration-200">
                <CalendarPicker 
                  selectedDate={safeDate} 
                  onDateChange={(d) => {
                    onDateSelect(d);
                    setIsDatePickerOpen(false);
                  }} 
                  onClose={() => setIsDatePickerOpen(false)}
                />
              </div>
            )}
          </div>
        </div>

        {/* Right Side Controls */}
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all shadow-md hover:shadow-lg transform active:scale-95">
            <Sparkles className="w-4 h-4" />
            <span className="hidden sm:inline font-medium">AI Planner</span>
          </button>
          
          <div className="bg-white p-1 rounded-lg shadow-sm flex gap-1 border border-gray-100 items-center">
             
             {/* ▼▼▼ GOOGLE TOGGLE ▼▼▼ */}
             <button 
               onClick={onGoogleClick}
               className={`
                 p-2 rounded-md transition-all duration-200 flex items-center gap-2
                 ${!isGoogleLinked 
                    ? 'opacity-50 hover:opacity-100 grayscale hover:grayscale-0' // Not Linked Style
                    : isGoogleVisible 
                        ? 'bg-blue-50 ring-1 ring-blue-100' // Linked & Visible
                        : 'hover:bg-gray-50' // Linked & Hidden
                 }
               `}
               title={!isGoogleLinked ? "Connect Google Calendar" : "Toggle Google Events"}
             >
               <FcGoogle className="w-5 h-5" />
               {/* Optional: Show label only if not linked */}
               {!isGoogleLinked && <span className="text-xs font-medium text-gray-500 pr-1">Sync</span>}
             </button>
             
             {/* Divider */}
             <div className="w-[1px] h-5 bg-gray-200 mx-1"></div>

             
          </div>
        </div>
      </div>

      {/* --- DAYS STRIP --- */}
      <div className="flex justify-between items-start w-full mt-2">
        {weekDays.map((dateObj, index) => {
          const isActive = dateObj.toDateString() === safeDate.toDateString();
          const matchedDayData = days.find(d => d.date === dateObj.getDate());
          
          return (
            <div 
              key={index} 
              onClick={() => onDateSelect(dateObj)}
              className="flex-1 flex flex-col items-center cursor-pointer group select-none"
            >
              <span className={`text-xs font-semibold mb-3 transition-colors ${isActive ? 'text-[#F49F99]' : 'text-gray-400 group-hover:text-gray-600'}`}>
                {dayNames[index]}
              </span>
              
              <div className={`
                w-10 h-10 flex items-center justify-center rounded-full text-sm font-bold mb-3 transition-all duration-300
                ${isActive 
                  ? 'bg-[#F49F99] text-white shadow-lg shadow-red-100 scale-110' 
                  : 'text-gray-700 hover:bg-white hover:shadow-md'
                }
              `}>
                {dateObj.getDate()}
              </div>
              
              <div className="flex gap-1 h-2 items-center justify-center">
                {matchedDayData?.tasks?.slice(0, 3).map((taskCategory, i) => (
                   <React.Fragment key={i}>
                     {renderTaskIndicator(taskCategory)}
                   </React.Fragment>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CalendarHeader;