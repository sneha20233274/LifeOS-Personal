// services/analyticsApi.js

import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery";

export const analyticsApi = createApi({
  reducerPath: "analyticsApi",
  baseQuery,

  endpoints: (builder) => ({

    // ✅ 1. CATEGORY AGGREGATION (Pie Chart)
    getAnalytics: builder.mutation({
      query: (body) => ({
        url: "/analytics/aggregate",
        method: "POST",
        body,
      }),
    }),

    // ✅ 2. PRODUCTIVITY SCORE
    getProductivity: builder.mutation({
      query: (body) => ({
        url: "/analytics/productivity",
        method: "POST",
        body,
      }),
    }),

    // ✅ 3. WEEKLY DISTRIBUTION (Bar Chart)
    getWeekly: builder.mutation({
      query: (body) => ({
        url: "/analytics/weekly",
        method: "POST",
        body,
      }),
    }),

    // ✅ 4. PRODUCTIVITY TREND (Line Chart)
    getTrend: builder.mutation({
      query: (body) => ({
        url: "/analytics/trend",
        method: "POST",
        body,
      }),
    }),

    // ✅ 5. PRODUCTIVITY AVERAGE (Optional)
    getProductivityAverage: builder.mutation({
      query: (body) => ({
        url: "/analytics/productivity-average",
        method: "POST",
        body,
      }),
    }),

  }),
});

// ✅ EXPORT HOOKS
export const {
  useGetAnalyticsMutation,
  useGetProductivityMutation,
  useGetWeeklyMutation,
  useGetTrendMutation,
  useGetProductivityAverageMutation,
} = analyticsApi;