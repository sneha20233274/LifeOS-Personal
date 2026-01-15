import { configureStore } from "@reduxjs/toolkit";

import chatReducer from "../store/chatSlice";
import appReducer from "../store/appSlice";
import authReducer from "../store/authSlice";

import { authApi } from "../services/authApi";
import { proposalsApi } from "../services/proposalsApi";
import { chatApi } from "../services/chatApi"; // 👈 NEW

export const store = configureStore({
  reducer: {
    chat: chatReducer,
    app: appReducer,
    auth: authReducer,

    // 🔑 RTK Query reducers
    [authApi.reducerPath]: authApi.reducer,
    [proposalsApi.reducerPath]: proposalsApi.reducer,
    [chatApi.reducerPath]: chatApi.reducer, // 👈 NEW
  },

  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(
      authApi.middleware,
      proposalsApi.middleware,
      chatApi.middleware // 👈 NEW
    ),
});
