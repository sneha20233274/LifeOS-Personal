import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery";

export const goalsApi = createApi({
  reducerPath: "goalsApi",

  baseQuery,
  

  endpoints: (builder) => ({
    getGoals: builder.query({
      query: () => "/goals",
    }),
  }),
});

export const { useGetGoalsQuery } = goalsApi;
