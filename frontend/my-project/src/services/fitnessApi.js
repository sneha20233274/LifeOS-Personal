import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery";

export const fitnessApi = createApi({
  reducerPath: "fitnessApi",
  baseQuery, 
  endpoints: (builder) => ({
    getWeeklyFitnessRoutine: builder.query({
      query: () => ({
        url: "/fitness/weekly-routine",
      }),
    }),
  }),
});

export const {
  useGetWeeklyFitnessRoutineQuery,
} = fitnessApi;
