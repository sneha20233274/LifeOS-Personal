import { baseQuery } from "./baseQuery";
import { createApi } from "@reduxjs/toolkit/query/react";

export const userApi = createApi({
  reducerPath: "userApi",
  baseQuery,
  tagTypes: ["User"],

  endpoints: (builder) => ({
    getMyProfile: builder.query({
      query: () => "/users/me",
      providesTags: ["User"],
    }),

    updateProfile: builder.mutation({
      query: (body) => ({
        url: "/users/me",
        method: "PUT",
        body,
      }),
      invalidatesTags: ["User"],
    }),
  }),
});


export const {
  useGetMyProfileQuery,
  useUpdateProfileMutation,
} = userApi;
