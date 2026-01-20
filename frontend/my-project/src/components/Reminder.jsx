import React, { useState } from 'react';
import CalendarHeader from './CalendarHeader';
import Timeline from './Timeline';
// Import 'timelineEvents' as 'initialData' so we can load it into state
import { days, timelineEvents as initialData } from './data'; 

export const Remainder = () => {
  // 1. State for selected date (Defaults to Today)
  const [selectedDate, setSelectedDate] = useState(new Date());

  // 2. Master State for Events (allows adding/editing)
  const [allEvents, setAllEvents] = useState(initialData);

  // --- Handlers ---

  // Add a new event from the Dialog
  const handleAddNewEvent = (newEvent) => {
    // Create a new event object with a unique ID
    const eventWithId = { 
      ...newEvent, 
      id: Date.now(), 
      hasReminder: false // Default state
    };
    
    // Update the master list
    setAllEvents((prevEvents) => [...prevEvents, eventWithId]);
  };

  // Toggle the reminder bell
  const handleToggleReminder = (id) => {
    setAllEvents((prevEvents) => 
      prevEvents.map(ev => 
        ev.id === id ? { ...ev, hasReminder: !ev.hasReminder } : ev
      )
    );
  };

  // NEW: Handle Delete Event
  const handleDeleteEvent = (id) => {
    // Optional: Add a confirmation dialog
    if (window.confirm("Are you sure you want to delete this routine?")) {
      setAllEvents((prevEvents) => prevEvents.filter(ev => ev.id !== id));
    }
  };

  // NEW: Handle Toggle Status (Complete/Scheduled)
  const handleToggleStatus = (id) => {
    setAllEvents((prevEvents) => 
      prevEvents.map(ev => {
        if (ev.id === id) {
          // Toggle between 'Completed' and 'Scheduled'
          const newStatus = ev.status === 'Completed' ? 'Scheduled' : 'Completed';
          return { ...ev, status: newStatus };
        }
        return ev;
      })
    );
  };

  // --- Filter Logic ---
  const currentEvents = allEvents.filter(event => {
    if (!event.start_time) return false;
    
    const eventDate = new Date(event.start_time);
    
    // Compare Day, Month, and Year to ensure accuracy
    return eventDate.getDate() === selectedDate.getDate() &&
           eventDate.getMonth() === selectedDate.getMonth() &&
           eventDate.getFullYear() === selectedDate.getFullYear();
  });

  // --- Google Sync Logic ---
  const [isGoogleLinked, setIsGoogleLinked] = useState(false); 
  const [showGoogleEvents, setShowGoogleEvents] = useState(true);

  const handleGoogleClick = () => {
    if (!isGoogleLinked) {
      // Logic 1: Not connected? Redirect to OAuth
      console.log("Redirecting to Google OAuth...");
      // window.location.href = "http://localhost:8000/auth/google/login";
      
      // Simulating a successful login for now:
      setIsGoogleLinked(true); 
    } else {
        // Logic 2: Connected? Toggle Visibility
        setShowGoogleEvents(!showGoogleEvents);
    }
  };

  return (
    <div className="w-full min-h-screen bg-[#F8F8F8] font-sans flex flex-col">
       {/* Header */}
       <CalendarHeader 
        days={days} 
        selectedDate={selectedDate} 
        onDateSelect={setSelectedDate} 
        // Google Props
        isGoogleLinked={isGoogleLinked}
        isGoogleVisible={showGoogleEvents}
        onGoogleClick={handleGoogleClick}
      />
      
      {/* Timeline */}
      <div className="flex-1 w-full max-w-5xl mx-auto overflow-y-auto pb-20">
        <Timeline 
          events={currentEvents} 
          selectedDate={selectedDate}         // Pass selected date (for default in dialog)
          onAddNewEvent={handleAddNewEvent}   // Add handler
          onToggleReminder={handleToggleReminder} // Reminder handler
          
          // ▼▼▼ NEW PROPS PASSED HERE ▼▼▼
          onDeleteEvent={handleDeleteEvent}
          onToggleStatusEvent={handleToggleStatus}
        />
      </div>
    </div>
  );
};

export default Remainder;