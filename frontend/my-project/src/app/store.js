import { configureStore } from "@reduxjs/toolkit";

import chatReducer from "../store/chatSlice";
import appReducer from "../store/appSlice";
import authReducer, { loadFromStorage } from "../store/authSlice";
import { analyticsApi } from "../services/analyticsApi";

import { authApi } from "../services/authApi";
import { proposalsApi } from "../services/proposalsApi";
import { chatApi } from "../services/chatApi";
import { goalsApi } from "../services/goalsApi";
import { tasksApi } from "../services/tasksApi";
import { subtasksApi } from "../services/subtasksApi";
import { activitiesApi } from "../services/activitiesApi";
import { fitnessApi } from "../services/fitnessApi"; 
import {userApi}  from "../services/userApi"

export const store = configureStore({
  reducer: {
    chat: chatReducer,
    app: appReducer,
    auth: authReducer,

    [authApi.reducerPath]: authApi.reducer,
    [proposalsApi.reducerPath]: proposalsApi.reducer,
    [chatApi.reducerPath]: chatApi.reducer,
    [goalsApi.reducerPath]: goalsApi.reducer,
    [tasksApi.reducerPath]: tasksApi.reducer,
    [subtasksApi.reducerPath]: subtasksApi.reducer,
    [activitiesApi.reducerPath]: activitiesApi.reducer, // ✅ ADD
    [fitnessApi.reducerPath]: fitnessApi.reducer,
    [userApi.reducerPath]: userApi.reducer,
    [analyticsApi.reducerPath]: analyticsApi.reducer,
  },

  middleware: (defaultMiddleware) =>
    defaultMiddleware().concat(
      authApi.middleware,
      proposalsApi.middleware,
      chatApi.middleware,
      goalsApi.middleware,
      tasksApi.middleware,
      subtasksApi.middleware,
      activitiesApi.middleware,
      fitnessApi.middleware,
      analyticsApi.middleware,
      userApi.middleware// ✅ ADD
    ),
});



let initialized = false;

const initialiseApp = () => {
  if (initialized) return;
  initialized = true;

  const auth = localStorage.getItem("auth");
  if (!auth) return;

  // 1️⃣ Hydrate Redux instantly
  store.dispatch(loadFromStorage(JSON.parse(auth)));

  // 2️⃣ Validate token in background
  store.dispatch(authApi.endpoints.loadUser.initiate());
};

initialiseApp();
