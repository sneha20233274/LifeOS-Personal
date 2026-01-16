// services/proposalsApi.js
import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery"; // ✅ shared baseQuery

export const proposalsApi = createApi({
  reducerPath: "proposalsApi",

  // 🔥 THIS IS THE FIX
  baseQuery: baseQuery,

  tagTypes: ["Proposals"],

  endpoints: (builder) => ({
    // 🔹 GET proposals
    getProposals: builder.query({
      query: () => ({
        url: "/chat/proposals",
        method: "GET",
      }),
      providesTags: ["Proposals"],
    }),

    // 🔹 SUBMIT proposals
    submitProposals: builder.mutation({
      query: ({ thread_id, proposals }) => ({
        url: "/chat/resume",
        method: "POST",
        body: {
          thread_id,
          proposals,
        },
      }),
      invalidatesTags: ["Proposals"],
    }),
  }),
});

export const {
  useGetProposalsQuery,
  useSubmitProposalsMutation,
} = proposalsApi;
