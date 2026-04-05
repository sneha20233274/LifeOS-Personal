import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery";
export const eventsApi = createApi({
  reducerPath: "eventsApi",

  baseQuery: baseQuery,

  tagTypes: ["Events"],

  endpoints: (builder) => ({
    /* ---------------------------
       GET EVENTS BY DATE
    ---------------------------- */
    getEventsByDate: builder.query({
      query: ({ date, tz }) =>
        `/events?date=${encodeURIComponent(date)}&tz=${encodeURIComponent(tz)}`,
      providesTags: ["Events"],
    }),


    /* ---------------------------
       CREATE EVENT
    ---------------------------- */
    createEvent: builder.mutation({
      query: (data) => ({
        url: "/events",
        method: "POST",
        body: data,
      }),
      invalidatesTags: ["Events"],
    }),

    /* ---------------------------
       TOGGLE REMINDER
    ---------------------------- */
    toggleEventReminder: builder.mutation({
      query: ({ id, hasReminder }) => ({
        url: `/events/${id}/reminder`,
        method: "PATCH",
        body: { hasReminder },
      }),
      invalidatesTags: ["Events"],
    }),

    /* ---------------------------
       TOGGLE STATUS
    ---------------------------- */
    toggleEventStatus: builder.mutation({
      query: ({ id, status }) => ({
        url: `/events/${id}`,
        method: "PUT",
        body: { status },
      }),
      invalidatesTags: ["Events"],
    }),


    /* ---------------------------
       DELETE EVENT
    ---------------------------- */
    deleteEvent: builder.mutation({
      query: (id) => ({
        url: `/events/${id}`,
        method: "DELETE",
      }),
      invalidatesTags: ["Events"],
    })

  }),
});

export const {
  useGetEventsByDateQuery,
  useCreateEventMutation,
  useToggleEventReminderMutation,
  useToggleEventStatusMutation,
  useDeleteEventMutation,
} = eventsApi;
