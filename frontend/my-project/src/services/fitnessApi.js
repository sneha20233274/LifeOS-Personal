import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery";

export const fitnessApi = createApi({
  reducerPath: "fitnessApi",
  baseQuery, // ✅ reuse shared baseQuery
  endpoints: (builder) => ({
    getWeeklyFitnessRoutine: builder.query({
      query: (userId) => ({
        url: "/fitness/weekly-routine",
        params: { user_id: userId },
      }),
    }),
  }),
});

export const {
  useGetWeeklyFitnessRoutineQuery,
} = fitnessApi;
