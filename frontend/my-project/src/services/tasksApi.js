import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery";

export const tasksApi = createApi({
  reducerPath: "tasksApi",
  baseQuery,

  endpoints: (builder) => ({

    /* -----------------------------
       GET ALL TASKS
    ------------------------------ */
    getTasks: builder.query({
      query: () => "/tasks",
    }),

    /* -----------------------------
       GET TASKS BY GOAL
    ------------------------------ */
    getTasksByGoal: builder.query({
      query: (goalId) => `/tasks/by-goal/${goalId}`,
    }),

    /* -----------------------------
       CREATE TASK
    ------------------------------ */
    createTask: builder.mutation({
      query: (payload) => ({
        url: "/tasks/",
        method: "POST",
        body: payload,
      }),
    }),

  }),
});

export const {
  useGetTasksQuery,
  useGetTasksByGoalQuery,
  useCreateTaskMutation,
} = tasksApi;
