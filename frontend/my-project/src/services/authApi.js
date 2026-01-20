import { createApi } from "@reduxjs/toolkit/query/react";
import { setCredentials,logout } from "../store/authSlice";
import { baseQuery } from "./baseQuery"; // ✅ shared baseQuery

export const authApi = createApi({
  reducerPath: "authApi",

  // 🔥 THIS WAS MISSING
  baseQuery: baseQuery,

  endpoints: (builder) => ({
    /* ---------------- LOGIN ---------------- */
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

    /* ---------------- SIGNUP ---------------- */
    signup: builder.mutation({
      query: (body) => ({
        url: "/auth/register",
        method: "POST",
        body,
      }),
    }),
    /* ---------------- LOGOUT ---------------- */
logout: builder.mutation({
  query: () => {
    const auth = JSON.parse(localStorage.getItem("auth"));
    return {
      url: "/auth/logout",
      method: "POST",
      body: {
        refresh_token: auth?.refresh,
      },
    };
  },
  async onQueryStarted(_, { dispatch, queryFulfilled }) {
    try {
      await queryFulfilled;
    } finally {
      // Always clear local state (even if API fails)
      dispatch(logout());
    }
  },
}),


    /* ---------------- LOAD USER ---------------- */
    loadUser: builder.query({
      query: () => ({
        url: "/auth/profile",
        method: "GET",
      }),

      async onQueryStarted(_, { queryFulfilled, dispatch }) {
        try {
          const { data } = await queryFulfilled;

          dispatch(
            setCredentials({
              user: data.user,
              access: JSON.parse(localStorage.getItem("auth"))?.access,
              refresh: JSON.parse(localStorage.getItem("auth"))?.refresh,
            })
          );
        } catch {
          // do nothing – explicit logout elsewhere
        }
      },
    }),
  }),
});

export const {
  useLoginMutation,
  useSignupMutation,
  useLoadUserQuery,
  useLogoutMutation,
} = authApi;
