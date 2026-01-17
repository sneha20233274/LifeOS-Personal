import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery";

export const subtasksApi = createApi({
  reducerPath: "subtasksApi",
  baseQuery,

  endpoints: (builder) => ({

    /* -----------------------------
       GET SUBTASKS BY TASK
    ------------------------------ */
    getSubtasksByTask: builder.query({
      query: (taskId) => `/subtasks/by-task/${taskId}`,
    }),

    /* -----------------------------
       CREATE SUBTASK
    ------------------------------ */
    createSubtask: builder.mutation({
      query: (payload) => ({
        url: "/subtasks/",
        method: "POST",
        body: payload,
      }),
    }),

  }),
});

export const {
  useGetSubtasksByTaskQuery,
  useCreateSubtaskMutation,
} = subtasksApi;
