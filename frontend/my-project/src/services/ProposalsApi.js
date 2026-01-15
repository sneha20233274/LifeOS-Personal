import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const proposalsApi = createApi({
  reducerPath: "proposalsApi",

  baseQuery: fetchBaseQuery({
    baseUrl: "http://127.0.0.1:8000", // adjust if needed
    prepareHeaders: (headers, { getState }) => {
      const token = getState().auth?.token;
      if (token) {
        headers.set("authorization", `Bearer ${token}`);
      }
      return headers;
    },
  }),

  tagTypes: ["Proposals"],

  endpoints: (builder) => ({
    // 🔹 GET proposals after interrupt
    getProposals: builder.query({
      query: () => ({
        url: "/chat/proposals",
        method: "GET",
      }),
      providesTags: ["Proposals"],
    }),

    // 🔹 SUBMIT final proposal state (approve/reject/update)
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

// 🔥 Auto-generated hooks
export const {
  useGetProposalsQuery,
  useSubmitProposalsMutation,
} = proposalsApi;
