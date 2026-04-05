import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQuery } from "./baseQuery";

export const googleAuthApi = createApi({
  reducerPath: "googleAuthApi",
  baseQuery,
  endpoints: (builder) => ({
    getGoogleAuthUrl: builder.query({
      query: () => "/integrations/google/auth/login",
    }),
  }),
});

export const {
  useLazyGetGoogleAuthUrlQuery,
} = googleAuthApi;
