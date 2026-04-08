import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery";

export const analyticsApi = createApi({
  reducerPath: "analyticsApi",
  baseQuery,

  endpoints: (builder) => ({
    getAnalytics: builder.query({
      query: (body) => ({
        url: "/analytics/aggregate",
        method: "POST",
        body,
      }),
    }),

    getProductivity: builder.query({
      query: (body) => ({
        url: "/analytics/productivity",
        method: "POST",
        body,
      }),
    }),

    getWeekly: builder.query({
      query: (body) => ({
        url: "/analytics/weekly",
        method: "POST",
        body,
      }),
    }),

    getTrend: builder.query({
      query: (body) => ({
        url: "/analytics/trend",
        method: "POST",
        body,
      }),
    }),

    getProductivityAverage: builder.query({
      query: (body) => ({
        url: "/analytics/productivity-average",
        method: "POST",
        body,
      }),
    }),

    getInsights: builder.query({
      query: (body) => ({
        url: "/analytics/insights",
        method: "POST",
        body,
      }),
    }),
  }),
});

export const {
  useGetAnalyticsQuery,
  useGetProductivityQuery,
  useGetWeeklyQuery,
  useGetTrendQuery,
  useGetProductivityAverageQuery,
  useGetInsightsQuery,
} = analyticsApi;