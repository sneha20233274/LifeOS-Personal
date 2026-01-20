import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, ChevronDown } from 'lucide-react';

// --- Helpers ---
const getDaysInMonth = (year, month) => new Date(year, month + 1, 0).getDate();
const getFirstDayOfMonth = (year, month) => new Date(year, month, 1).getDay();
const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

export default function CalendarPicker({ selectedDate, onDateChange, onClose }) {
  const [pickerView, setPickerView] = useState('calendar'); // 'calendar' or 'years'
  const [pickerDate, setPickerDate] = useState(new Date(selectedDate));

  // Sync internal state if external prop changes
  useEffect(() => {
    setPickerDate(new Date(selectedDate));
  }, [selectedDate]);

  const handleDateClick = (day) => {
    const newDate = new Date(pickerDate.getFullYear(), pickerDate.getMonth(), day);
    onDateChange(newDate);
    if (onClose) onClose();
  };

  const handleMonthNav = (direction) => {
    const newDate = new Date(pickerDate);
    newDate.setMonth(newDate.getMonth() + direction);
    setPickerDate(newDate);
  };

  const handleYearClick = (year) => {
    const newDate = new Date(pickerDate);
    newDate.setFullYear(year);
    setPickerDate(newDate);
    setPickerView('calendar');
  };

  const renderCalendar = () => {
    const daysInMonth = getDaysInMonth(pickerDate.getFullYear(), pickerDate.getMonth());
    const startDay = getFirstDayOfMonth(pickerDate.getFullYear(), pickerDate.getMonth());
    const blanks = Array(startDay).fill(null);
    const days = Array.from({ length: daysInMonth }, (_, i) => i + 1);

    return (
      <div className="p-4 w-[320px] bg-white rounded-2xl shadow-xl border border-gray-100">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-1">
            <span className="text-lg font-bold text-gray-900">{monthNames[pickerDate.getMonth()]}</span>
            <button 
              onClick={() => setPickerView('years')}
              className="text-lg font-bold hover:underline decoration-[#F49F99] underline-offset-4 text-[#F49F99] flex items-center"
            >
              {pickerDate.getFullYear()}
              <ChevronDown className="w-5 h-5 ml-1 text-gray-400" />
            </button>
          </div>
          <div className="flex gap-1">
            <button onClick={() => handleMonthNav(-1)} className="p-1 hover:bg-gray-100 rounded-full"><ChevronLeft className="w-5 h-5" /></button>
            <button onClick={() => handleMonthNav(1)} className="p-1 hover:bg-gray-100 rounded-full"><ChevronRight className="w-5 h-5" /></button>
          </div>
        </div>

        {/* Week Days */}
        <div className="grid grid-cols-7 mb-2">
          {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(d => (
            <div key={d} className="text-center text-xs font-medium text-gray-400 uppercase">{d}</div>
          ))}
        </div>

        {/* Days Grid */}
        <div className="grid grid-cols-7 gap-y-2">
          {blanks.map((_, i) => <div key={`blank-${i}`} />)}
          {days.map(day => {
            const isSelected = selectedDate.getDate() === day && 
                               selectedDate.getMonth() === pickerDate.getMonth() && 
                               selectedDate.getFullYear() === pickerDate.getFullYear();
            return (
              <button
                key={day}
                onClick={() => handleDateClick(day)}
                className={`h-9 w-9 mx-auto rounded-full flex flex-col items-center justify-center text-sm transition-colors relative group
                  ${isSelected ? 'bg-[#F49F99] text-white shadow-md' : 'text-gray-900 hover:bg-gray-100'}
                `}
              >
                <span>{day}</span>
              </button>
            );
          })}
        </div>
      </div>
    );
  };

  const renderYearPicker = () => {
    const currentYear = new Date().getFullYear();
    const years = Array.from({ length: 12 }, (_, i) => currentYear - 5 + i);

    return (
      <div className="p-4 w-[320px] max-h-[350px] overflow-y-auto bg-white rounded-2xl shadow-xl border border-gray-100">
        <div className="flex items-center justify-between mb-4 sticky top-0 bg-white z-10">
          <button onClick={() => setPickerView('calendar')} className="flex items-center text-sm text-gray-500 hover:text-gray-900">
            <ChevronLeft className="w-4 h-4 mr-1" /> Back
          </button>
          <span className="font-bold text-gray-900">Select Year</span>
        </div>
        <div className="flex flex-col gap-1">
          {years.map(year => (
            <button
              key={year}
              onClick={() => handleYearClick(year)}
              className={`py-3 px-4 rounded-lg text-left text-lg font-medium transition-colors
                ${pickerDate.getFullYear() === year ? 'bg-gray-50 text-[#F49F99]' : 'text-gray-600 hover:bg-gray-50'}
              `}
            >
              {year}
            </button>
          ))}
        </div>
      </div>
    );
  };

  return pickerView === 'calendar' ? renderCalendar() : renderYearPicker();
}