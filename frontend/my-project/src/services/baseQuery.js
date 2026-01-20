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
  // 1️⃣ First request
  let result = await rawBaseQuery(args, api, extraOptions);

  // 2️⃣ If access token expired
  if (
  result.error &&
  [401, 403].includes(result.error.status)
) {
    const auth = JSON.parse(localStorage.getItem("auth"));
    const refreshToken = auth?.refresh;

    // ❌ No refresh token → logout
    if (!refreshToken) {
      api.dispatch(logout());
      return result;
    }

    // 3️⃣ Call refresh endpoint
    const refreshResult = await rawBaseQuery(
      {
        url: "/auth/refresh",
        method: "POST",
        body: { refresh_token: refreshToken },
      },
      api,
      extraOptions
    );

    // 4️⃣ If refresh succeeded
    if (refreshResult.data?.access_token) {
      api.dispatch(
        setCredentials({
          access: refreshResult.data.access_token,
          refresh: refreshToken, // keep same refresh
        })
      );

      // 5️⃣ Retry original request with NEW access token
      result = await rawBaseQuery(args, api, extraOptions);
    } else {
      // refresh failed → logout
      api.dispatch(logout());
    }
  }

  return result;
};
