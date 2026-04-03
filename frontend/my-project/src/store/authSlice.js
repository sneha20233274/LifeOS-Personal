import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  user: null,
  accessToken: null,
  refreshToken: null,
  isAuthenticated: false,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setCredentials: (state, action) => {
      const { user, access, refresh } = action.payload;

      // ✅ DO NOT overwrite user if not provided
      state.user = user ?? state.user;
      state.accessToken = access;
      state.refreshToken = refresh;
      state.isAuthenticated = true;

      // ✅ ALWAYS store consistent structure
      localStorage.setItem(
        "auth",
        JSON.stringify({
          user: state.user,
          access,
          refresh,
        })
      );
    },

    logout: (state) => {
      state.user = null;
      state.accessToken = null;
      state.refreshToken = null;
      state.isAuthenticated = false;

      localStorage.removeItem("auth");
    },

    loadFromStorage: (state, action) => {
      const { user, access, refresh } = action.payload || {};

      state.user = user || null;
      state.accessToken = access || null;
      state.refreshToken = refresh || null;
      state.isAuthenticated = !!access;
    },
  },
});

export const { setCredentials, logout, loadFromStorage } = authSlice.actions;
export default authSlice.reducer;