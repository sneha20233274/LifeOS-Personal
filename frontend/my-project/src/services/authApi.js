import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { setCredentials } from "../store/authSlice";

export const authApi = createApi({
  reducerPath: "authApi",

  baseQuery: fetchBaseQuery({
    baseUrl: "http://localhost:8000",
    prepareHeaders: (headers) => {
      const auth = JSON.parse(localStorage.getItem("auth"));
      if (auth?.access) {
        headers.set("Authorization", `Bearer ${auth.access}`);
      }
      return headers;
    },
  }),

  endpoints: (builder) => ({
    login: builder.mutation({
      query: (body) => ({
        url: "/auth/login",
        method: "POST",
        body,
      }),
      async onQueryStarted(_, { queryFulfilled, dispatch }) {
        const { data } = await queryFulfilled;
        dispatch(setCredentials(data));
      },
    }),

    signup: builder.mutation({
      query: (body) => ({
        url: "/auth/register",
        method: "POST",
        body,
      }),
    }),

    loadUser: builder.query({
      query: () => ({
        url: "/auth/profile",
        method: "GET",
      }),

      async onQueryStarted(_, { queryFulfilled, dispatch }) {
        try {
          const { data } = await queryFulfilled;

          // ✅ Update user only, keep tokens
          dispatch(
            setCredentials({
              user: data.user,
              access: JSON.parse(localStorage.getItem("auth"))?.access,
              refresh: JSON.parse(localStorage.getItem("auth"))?.refresh,
            })
          );
        } catch {
          // ❌ DO NOTHING HERE
          // logout should happen ONLY on explicit 401 handling elsewhere
        }
      },
    }),
  }),
});

export const {
  useLoginMutation,
  useSignupMutation,
  useLoadUserQuery,
} = authApi;
