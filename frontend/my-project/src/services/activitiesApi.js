// services/activitiesApi.js
import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery";

export const activitiesApi = createApi({
  reducerPath: "activitiesApi",
  baseQuery,

  endpoints: (builder) => ({
    getActivities: builder.query({
      query: () => ({
        url: "/activities/",
        method: "GET",
      }),
    }),
  }),
});

export const { useGetActivitiesQuery } = activitiesApi;
