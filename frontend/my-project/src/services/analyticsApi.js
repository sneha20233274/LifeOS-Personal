import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery";

export const analyticsApi = createApi({
  reducerPath: "analyticsApi",
  baseQuery,

  endpoints: (builder) => ({
    getAnalytics: builder.mutation({
      query: (body) => ({
        url: "/analytics/aggregate",
        method: "POST",
        body,
      }),
    }),

    getProductivity: builder.mutation({
      query: (body) => ({
        url: "/analytics/productivity",
        method: "POST",
        body,
      }),
    }),

    getWeekly: builder.mutation({
      query: (body) => ({
        url: "/analytics/weekly",
        method: "POST",
        body,
      }),
    }),

    getTrend: builder.mutation({
      query: (body) => ({
        url: "/analytics/trend",
        method: "POST",
        body,
      }),
    }),

    getProductivityAverage: builder.mutation({
      query: (body) => ({
        url: "/analytics/productivity-average",
        method: "POST",
        body,
      }),
    }),

    // 🔥 NEW INSIGHTS API
    getInsights: builder.mutation({
      query: (body) => ({
        url: "/analytics/insights",
        method: "POST",
        body,
      }),
    }),
  }),
});

export const {
  useGetAnalyticsMutation,
  useGetProductivityMutation,
  useGetWeeklyMutation,
  useGetTrendMutation,
  useGetProductivityAverageMutation,
  useGetInsightsMutation, // ✅ NEW EXPORT
} = analyticsApi;