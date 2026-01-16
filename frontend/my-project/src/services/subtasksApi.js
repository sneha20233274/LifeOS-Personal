import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery";

export const subtasksApi = createApi({
  reducerPath: "subtasksApi",
  baseQuery,

  endpoints: (builder) => ({
    getSubtasksByTask: builder.query({
      query: (taskId) => `/subtasks/by-task/${taskId}`,
    }),
  }),
});

export const { useGetSubtasksByTaskQuery } = subtasksApi;
