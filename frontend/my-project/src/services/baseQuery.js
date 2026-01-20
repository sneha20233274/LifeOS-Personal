import { fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { setCredentials, logout } from "../store/authSlice";

const rawBaseQuery = fetchBaseQuery({
  baseUrl: "http://localhost:8000",
  prepareHeaders: (headers) => {
    const auth = JSON.parse(localStorage.getItem("auth"));
    if (auth?.access) {
      headers.set("Authorization", `Bearer ${auth.access}`);
    }
    return headers;
  },
});

export const baseQuery = async (args, api, extraOptions) => {
  // 1️⃣ First attempt
  let result = await rawBaseQuery(args, api, extraOptions);

  // 2️⃣ Access token expired
  if (result.error?.status === 401) {
    const auth = JSON.parse(localStorage.getItem("auth"));
    const refreshToken = auth?.refresh;

    // no refresh token → force logout
    if (!refreshToken) {
      api.dispatch(logout());
      return result;
    }

    // 3️⃣ Call refresh
    const refreshResult = await rawBaseQuery(
      {
        url: "/auth/refresh",
        method: "POST",
        body: { refresh_token: refreshToken },
      },
      api,
      extraOptions
    );

    // 4️⃣ Refresh success → save new tokens
    if (refreshResult.data) {
      api.dispatch(setCredentials(refreshResult.data));

      // 5️⃣ Retry original request
      result = await rawBaseQuery(args, api, extraOptions);
    } else {
      // refresh failed (revoked / expired)
      api.dispatch(logout());
    }
  }

  return result;
};
