// services/chatApi.js
import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery"; // ✅ shared baseQuery

export const chatApi = createApi({
  reducerPath: "chatApi",

  // 🔥 THIS IS THE FIX
  baseQuery: baseQuery,

  endpoints: (builder) => ({
    createNewChat: builder.mutation({
      query: () => ({
        url: "/chat/new",
        method: "POST",
      }),
    }),

    runChat: builder.mutation({
      query: ({ thread_id, prompt }) => ({
        url: "/chat/run",
        method: "POST",
        body: {
          thread_id,
          prompt,
        },
      }),
    }),
  }),
});

export const {
  useCreateNewChatMutation,
  useRunChatMutation,
} = chatApi;
