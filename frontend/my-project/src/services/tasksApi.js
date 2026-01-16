import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery";

export const tasksApi = createApi({
  reducerPath: "tasksApi",
  baseQuery,

  endpoints: (builder) => ({
    // 🔹 all tasks
    getTasks: builder.query({
      query: () => "/tasks",
    }),

    // 🔹 tasks for a specific goal
    getTasksByGoal: builder.query({
      query: (goalId) => `/tasks/by-goal/${goalId}`,
    }),
  }),
});

export const {
  useGetTasksQuery,
  useGetTasksByGoalQuery,
} = tasksApi;
