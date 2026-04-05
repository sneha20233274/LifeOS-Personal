import { useState } from 'react';
import { FiPlus } from "react-icons/fi"; 
import { 
  Sun, Moon, CheckSquare, Briefcase, Heart, 
  MapPin, Bell, BellOff, Trash2, CheckCircle2, Circle, Undo2
} from 'lucide-react';
import { CreateTaskDialog } from './CreateTaskDialog'; 

// --- TimelineItem ---
const TimelineItem = ({ event, isLast, onToggleReminder, onDelete, onToggleStatus }) => {
  
  const isCompleted = event.status === 'Completed';

  // 1. Format Time
  const formatTime = (isoString) => {
    if (!isoString) return '';
    const date = new Date(isoString.endsWith("Z") ? isoString : isoString + "Z");

    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const timeStart = formatTime(event.start_time);
  const timeEnd = formatTime(event.end_time);

  // 2. Icon Mapping
  const renderIcon = (category) => {
    switch(category) {
      case 'Work': return <Briefcase className="w-4 h-4" />;
      case 'Health': return <Heart className="w-4 h-4" />;
      case 'Personal': return <Sun className="w-4 h-4" />;
      case 'General': return <CheckSquare className="w-4 h-4" />;
      default: return <div className="w-2 h-2 rounded-full bg-gray-400" />;
    }
  };

  // 3. Priority Color (Dimmed if completed)
  const getPriorityColor = (priority) => {
    if (isCompleted) return 'border-l-4 border-l-gray-300'; // Gray out priority when done
    switch(priority) {
      case 'High': return 'border-l-4 border-l-red-400';
      case 'Medium': return 'border-l-4 border-l-[#F49F99]';
      default: return 'border-l-4 border-l-gray-300';
    }
  };
  console.log(event.has_reminder
, event.has_reminder);

  return (
    <div className={`flex w-full min-h-[90px] group ${isCompleted ? 'opacity-70' : ''}`}>
      
      {/* Time Column */}
      <div className="w-24 text-right pr-4 pt-1 flex flex-col items-end">
        <span className={`text-sm font-bold ${isCompleted ? 'text-gray-400 line-through' : 'text-gray-700'}`}>
          {timeStart}
        </span>
        <span className="text-xs font-medium text-gray-400 mt-1">{timeEnd}</span>
      </div>

      {/* Line & Icon Column */}
      <div className="relative flex flex-col items-center w-8">
        {!isLast && <div className="absolute top-4 bottom-[-10px] w-[2px] bg-gray-100"></div>}
        <div className={`
          relative z-10 w-9 h-9 rounded-full flex items-center justify-center border-2 bg-white transition-colors
          ${isCompleted 
            ? 'border-gray-200 text-gray-300' // Dimmed icon
            : event.is_all_day ? 'border-[#F49F99] text-[#F49F99]' : 'border-gray-200 text-gray-400'
          }
        `}>
          {isCompleted ? <CheckCircle2 className="w-4 h-4" /> : renderIcon(event.category)}
        </div>
      </div>

      {/* Content Card */}
      <div className="flex-1 pl-6 pb-6">
        <div className={`
          relative rounded-xl p-5 bg-white shadow-sm transition-all border border-gray-100 
          ${getPriorityColor(event.priority)}
          ${isCompleted ? 'bg-gray-50' : 'hover:shadow-md'} 
        `}>
            
            <div className="flex justify-between items-start">
              <div className="flex-1 pr-4">
                {/* Title with Strikethrough */}
                <h3 className={`font-semibold text-lg transition-all ${isCompleted ? 'text-gray-400 line-through' : 'text-gray-800'}`}>
                  {event.title}
                </h3>
                
                {/* Description with Strikethrough */}
                {event.description && (
                  <p className={`text-sm mt-1 ${isCompleted ? 'text-gray-300 line-through' : 'text-gray-500'}`}>
                    {event.description}
                  </p>
                )}
                
                {event.location_or_link && !isCompleted && (
                  <div className="flex items-center gap-1 mt-2 text-xs text-blue-500 bg-blue-50 w-fit px-2 py-1 rounded">
                    <MapPin className="w-3 h-3" /> {event.location_or_link}
                  </div>
                )}
              </div>

              {/* --- ACTION ICONS (Top Right) --- */}
              <div className="flex items-center gap-1">
                
                {/* 1. Complete / Undo Button */}
                <button 
                  onClick={() => onToggleStatus && onToggleStatus(event.id, event.status)
}
                  className={`p-1.5 rounded-full transition-colors ${
                    isCompleted 
                      ? 'text-green-500 hover:bg-green-50' 
                      : 'text-gray-300 hover:text-green-500 hover:bg-green-50'
                  }`}
                  title={isCompleted ? "Mark as Incomplete" : "Mark as Completed"}
                >
                  {isCompleted ? <Undo2 className="w-4 h-4" /> : <Circle className="w-4 h-4" />}
                </button>

                {/* 2. Reminder Button */}
                <button 
                  onClick={() => onToggleReminder && onToggleReminder(event.id, event.has_reminder
)}
                  className={`p-1.5 rounded-full transition-colors ${
                    event.has_reminder
 
                      ? 'text-[#F49F99] hover:bg-red-50' 
                      : 'text-gray-300 hover:text-[#F49F99] hover:bg-red-50'
                  }`}
                  title="Toggle Reminder"
                >
                  {event.has_reminder
 ? <Bell className="w-4 h-4 fill-current" /> : <BellOff className="w-4 h-4" />}
                </button>

                {/* 3. Delete Button */}
                <button 
                  onClick={() => onDelete && onDelete(event.id)}
                  className="p-1.5 rounded-full text-gray-300 hover:text-red-500 hover:bg-red-50 transition-colors"
                  title="Delete Routine"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
            
            {/* Footer tags (Hidden if completed to reduce noise, or keep simple) */}
            <div className={`mt-3 flex gap-2 ${isCompleted ? 'opacity-50' : ''}`}>
                <span className="text-[10px] uppercase font-bold tracking-wider text-gray-400 bg-gray-50 px-2 py-1 rounded">
                  {event.category}
                </span>
                {event.is_all_day && (
                  <span className="text-[10px] uppercase font-bold tracking-wider text-white bg-[#F49F99] px-2 py-1 rounded">
                    All Day
                  </span>
                )}
                 {/* Status Badge */}
                 {isCompleted && (
                  <span className="text-[10px] uppercase font-bold tracking-wider text-green-600 bg-green-100 px-2 py-1 rounded">
                    Done
                  </span>
                 )}
            </div>

        </div>
      </div>
    </div>
  );
};


// --- Main Timeline ---
export default function Timeline({ 
  events = [], 
  onAddNewEvent, 
  selectedDate,
  onToggleReminder,
  onDeleteEvent,     // <--- New Prop
  onToggleStatusEvent // <--- New Prop
}) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleSaveTask = (newRoutineEvent) => {
    if (onAddNewEvent) onAddNewEvent(newRoutineEvent);
    setIsModalOpen(false);
  };

  return (
    <div className="relative min-h-screen p-6 pb-32">
       
       <div className="max-w-3xl mx-auto mt-6">
         {events && events.length > 0 ? (
          [...events]
             .sort((a, b) => new Date(a.start_time) - new Date(b.start_time))
             .map((event, index) => (
                <TimelineItem 
                  key={event.id || index} 
                  event={event} 
                  isLast={index === events.length - 1} 
                  onToggleReminder={onToggleReminder}
                  onDelete={onDeleteEvent}         // Pass down
                  onToggleStatus={onToggleStatusEvent} // Pass down
                />
           ))
         ) : (
           <div className="text-center mt-20 text-gray-400 flex flex-col items-center">
             <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
               <Sun className="w-8 h-8 text-gray-300" />
             </div>
             <p className="font-medium">No routine planned.</p>
             <p className="text-sm">Enjoy your free time!</p>
           </div>
         )}
       </div>

       {/* Floating Action Button */}
       <button 
         onClick={() => setIsModalOpen(true)} 
         className="fixed bottom-10 right-10 w-16 h-16 bg-[#F49F99] text-white rounded-full shadow-xl flex items-center justify-center hover:bg-[#e08e88] transition-all hover:scale-105 z-50 cursor-pointer"
       >
         <FiPlus className="w-8 h-8" />
       </button>

       {/* Modal */}
       <CreateTaskDialog 
         isOpen={isModalOpen} 
         onClose={() => setIsModalOpen(false)} 
         onSave={handleSaveTask}
         initialDate={selectedDate} 
       />
    </div>
  );
}