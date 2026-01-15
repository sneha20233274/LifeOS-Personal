import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const chatApi = createApi({
  reducerPath: "chatApi",
  baseQuery: fetchBaseQuery({ baseUrl: "http://127.0.0.1:8000" }),
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
