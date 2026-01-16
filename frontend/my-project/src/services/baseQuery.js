// services/baseQuery.js
import { fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const baseQuery = fetchBaseQuery({
  baseUrl: "http://127.0.0.1:8000",
  prepareHeaders: (headers) => {
    const auth = JSON.parse(localStorage.getItem("auth"));
    if (auth?.access) {
      headers.set("Authorization", `Bearer ${auth.access}`);
    }
    return headers;
  },
});
