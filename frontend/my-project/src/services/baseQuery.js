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
  let result = await rawBaseQuery(args, api, extraOptions);

  if (result.error && [401, 403].includes(result.error.status)) {
    const auth = JSON.parse(localStorage.getItem("auth"));
    const refreshToken = auth?.refresh;

    if (!refreshToken) {
      api.dispatch(logout());
      return result;
    }

    const refreshResult = await rawBaseQuery(
      {
        url: "/auth/refresh",
        method: "POST",
        body: { refresh_token: refreshToken },
      },
      api,
      extraOptions
    );

    if (refreshResult.data?.access_token) {
      const currentAuth = JSON.parse(localStorage.getItem("auth"));

      api.dispatch(
        setCredentials({
          access: refreshResult.data.access_token,
          refresh: refreshToken,
          user: currentAuth?.user, // ✅ preserve user
        })
      );

      // retry original request
      result = await rawBaseQuery(args, api, extraOptions);
    } else {
      api.dispatch(logout());
    }
  }

  return result;
};