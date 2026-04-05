import React, { useState } from "react";
import CalendarHeader from "./CalendarHeader";
import Timeline from "./Timeline";
import { days } from "./data";
import toast from "react-hot-toast";

import {
  useGetEventsByDateQuery,
  useCreateEventMutation,
  useToggleEventReminderMutation,
  useToggleEventStatusMutation,
  useDeleteEventMutation,
} from "../services/eventsApi";
import { useLazyGetGoogleAuthUrlQuery } from "../services/googleAuthApi";

export function ConnectGoogleButton() {
  const [getAuthUrl, { isFetching, error }] =
    useLazyGetGoogleAuthUrlQuery();

  const handleConnect = async () => {
    try {
      const res = await getAuthUrl().unwrap();
      window.location.href = res.auth_url;
    } catch (err) {
      console.error("Google connect failed", err);
    }
  };

  return (
    <button onClick={handleConnect} disabled={isFetching}>
      {isFetching ? "Connecting..." : "Connect Google Calendar"}
    </button>
  );
}
const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

export const Remainder = () => {
  /* -----------------------------
     DATE STATE (UI STATE)
  ------------------------------ */
  const [selectedDate, setSelectedDate] = useState(new Date());
  const dateISO = new Date(
   selectedDate.getFullYear(),
   selectedDate.getMonth(),
   selectedDate.getDate(),
   0, 0, 0
 ).toISOString()
 console.log(dateISO);

  /* -----------------------------
     RTK QUERY (BACKEND STATE)
  ------------------------------ */
  const {
    data: events = [],
    isLoading,
  } = useGetEventsByDateQuery({
        date: dateISO,
        tz: userTimezone,
      });
;

  const [createEvent] = useCreateEventMutation();
  const [toggleReminder] = useToggleEventReminderMutation();
  const [toggleStatus] = useToggleEventStatusMutation();
  const [deleteEvent] = useDeleteEventMutation();

  /* -----------------------------
     GOOGLE SYNC (UI STATE)
  ------------------------------ */
  const [isGoogleLinked, setIsGoogleLinked] = useState(false);
  const [showGoogleEvents, setShowGoogleEvents] = useState(true);

  const [getGoogleAuthUrl, { isFetching }] =
    useLazyGetGoogleAuthUrlQuery();

  const handleGoogleClick = async () => {
    if (!isGoogleLinked) {
      console.log("Redirecting to Google OAuth...");
      try {
        const res = await getGoogleAuthUrl().unwrap();
        window.location.href = res.auth_url;
        setIsGoogleLinked(true);
      } catch (err) {
        console.error("Google connect failed", err);
      }
    } else {
      setShowGoogleEvents(!showGoogleEvents);
    }
  };

  /* -----------------------------
     EVENT HANDLERS (ASYNC + TOAST)
  ------------------------------ */

  const handleAddEvent = async (newEvent) => {
    const toastId = toast.loading("Creating event...");
    try {
      await createEvent(newEvent).unwrap();
      toast.success("Event created 🎉", { id: toastId });
    } catch (err) {
      toast.error("Failed to create event", { id: toastId });
    }
  };

  const handleToggleReminder = async (id, hasReminder) => {
    try {
      await toggleReminder({ id, hasReminder: !hasReminder }).unwrap();
      toast.success(
        !hasReminder ? "Reminder enabled 🔔" : "Reminder disabled 🔕"
      );
    } catch (err) {
      toast.error("Failed to update reminder");
    }
  };

  const handleToggleStatus = async (id, currentStatus) => {
    const nextStatus =
      currentStatus === "Completed" ? "Scheduled" : "Completed";

    try {
      await toggleStatus({ id, status: nextStatus }).unwrap();
      toast.success(
        nextStatus === "Completed"
          ? "Marked as completed ✅"
          : "Marked as incomplete ↩️"
      );
    } catch (err) {
      toast.error("Failed to update status");
    }
  };

  const handleDeleteEvent = async (id) => {
    if (!window.confirm("Are you sure you want to delete this routine?")) return;

    const toastId = toast.loading("Deleting event...");
    try {
      await deleteEvent(id).unwrap();
      toast.success("Event deleted 🗑️", { id: toastId });
    } catch (err) {
      toast.error("Failed to delete event", { id: toastId });
    }
  };

  /* -----------------------------
     RENDER
  ------------------------------ */
  return (
    <div className="w-full min-h-screen bg-[#F8F8F8] font-sans flex flex-col">
      
      {/* Header */}
      <CalendarHeader
        days={days}
        selectedDate={selectedDate}
        onDateSelect={setSelectedDate}
        isGoogleLinked={isGoogleLinked}
        isGoogleVisible={showGoogleEvents}
        onGoogleClick={handleGoogleClick}
      />

      {/* Timeline */}
      <div className="flex-1 w-full max-w-5xl mx-auto overflow-y-auto pb-20">
        {isLoading && (
          <p className="text-center text-gray-500 mt-4">
            Loading events...
          </p>
        )}

        <Timeline
          events={events}
          selectedDate={selectedDate}
          onAddNewEvent={handleAddEvent}
          onToggleReminder={handleToggleReminder}
          onToggleStatusEvent={handleToggleStatus}
          onDeleteEvent={handleDeleteEvent}
        />
      </div>
    </div>
  );
};

export default Remainder;
