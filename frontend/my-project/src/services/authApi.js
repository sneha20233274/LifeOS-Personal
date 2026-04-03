import { createApi } from "@reduxjs/toolkit/query/react";
import { setCredentials, logout } from "../store/authSlice";
import { baseQuery } from "./baseQuery";

export const authApi = createApi({
  reducerPath: "authApi",
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
        try {
          const { data } = await queryFulfilled;

          const access = data.access_token;
          const refresh = data.refresh_token;

          // ✅ temporarily store tokens
          localStorage.setItem(
            "auth",
            JSON.stringify({ access, refresh, user: null })
          );

          // ✅ fetch user
          const res = await fetch("http://localhost:8000/users/me", {
            headers: {
              Authorization: `Bearer ${access}`,
            },
          });

          const userData = await res.json();

          dispatch(
            setCredentials({
              access,
              refresh,
              user: userData,
            })
          );
        } catch (err) {
          console.error("Login failed", err);
        }
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

    /* ---------------- CHANGE PASSWORD ---------------- */
    changePassword: builder.mutation({
      query: (body) => ({
        url: "/auth/change-password",
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
          dispatch(logout());
        }
      },
    }),

    /* ---------------- LOAD USER ---------------- */
    loadUser: builder.query({
      query: () => ({
        url: "/users/me",
        method: "GET",
      }),

      async onQueryStarted(_, { queryFulfilled, dispatch }) {
        try {
          const { data } = await queryFulfilled;

          const auth = JSON.parse(localStorage.getItem("auth"));

          dispatch(
            setCredentials({
              user: data,
              access: auth?.access,
              refresh: auth?.refresh,
            })
          );
        } catch (err) {
          console.error("Load user failed", err);
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
  useChangePasswordMutation,
} = authApi;