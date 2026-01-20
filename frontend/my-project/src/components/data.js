// data.js

// Helper to get ISO string for today/tomorrow
const getDateString = (offsetDays = 0) => {
  const d = new Date();
  d.setDate(d.getDate() + offsetDays);
  return d.toISOString().split('T')[0]; // Returns "2026-01-20"
};

const TODAY = getDateString(0);
const TOMORROW = getDateString(1);
const DAY_AFTER = getDateString(2);

// Data for the dots on the Calendar Header
export const days = [
  { day: "Today", date: new Date().getDate(), tasks: ['Work', 'Health'] },
  { day: "Tmrw", date: new Date(Date.now() + 86400000).getDate(), tasks: ['Personal'] },
];

// Data for the Timeline List
export const timelineEvents = [
  // --- TODAY'S EVENTS ---
  { 
    id: 1, 
    title: 'Morning Standup', 
    description: 'Sync with the dev team.',
    start_time: `${TODAY}T09:00:00`,
    end_time: `${TODAY}T09:30:00`,
    category: 'Work',
    priority: 'High',
    status: 'Scheduled',
    hasReminder: true
  },
  { 
    id: 2, 
    title: 'Gym Session', 
    start_time: `${TODAY}T18:00:00`,
    end_time: `${TODAY}T19:00:00`,
    category: 'Health',
    priority: 'Medium',
    status: 'Scheduled'
  },

  // --- TOMORROW'S EVENTS ---
  { 
    id: 3, 
    title: 'Grocery Shopping', 
    start_time: `${TOMORROW}T10:00:00`,
    end_time: `${TOMORROW}T11:00:00`,
    category: 'Personal',
    priority: 'Low',
    status: 'Scheduled'
  },
  
  // --- DAY AFTER EVENTS ---
  { 
    id: 4, 
    title: 'Deep Work', 
    start_time: `${DAY_AFTER}T08:00:00`,
    end_time: `${DAY_AFTER}T12:00:00`,
    category: 'Work',
    priority: 'High',
    status: 'Scheduled'
  },
];