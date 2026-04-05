import { configureStore } from "@reduxjs/toolkit";

/* ---------------------------
   NORMAL REDUX SLICES
---------------------------- */
import chatReducer from "../store/chatSlice";
import appReducer from "../store/appSlice";
import authReducer, { loadFromStorage } from "../store/authSlice";
import { analyticsApi } from "../services/analyticsApi";

/* ---------------------------
   RTK QUERY APIS
---------------------------- */
import { authApi } from "../services/authApi";
import { proposalsApi } from "../services/proposalsApi";
import { chatApi } from "../services/chatApi";
import { goalsApi } from "../services/goalsApi";
import { tasksApi } from "../services/tasksApi";
import { subtasksApi } from "../services/subtasksApi";
import { activitiesApi } from "../services/activitiesApi";


import { eventsApi } from "../services/eventsApi";
import { googleAuthApi } from "../services/googleAuthApi"
/* ---------------------------
   STORE CONFIG
---------------------------- */
import { analyticsApi } from "../services/analyticsApi";
import { fitnessApi } from "../services/fitnessApi"; 
import {userApi}  from "../services/userApi"

export const store = configureStore({
  reducer: {
    // Classic slices
    chat: chatReducer,
    app: appReducer,
    auth: authReducer,

    // RTK Query reducers
    [authApi.reducerPath]: authApi.reducer,
    [proposalsApi.reducerPath]: proposalsApi.reducer,
    [chatApi.reducerPath]: chatApi.reducer,
    [goalsApi.reducerPath]: goalsApi.reducer,
    [tasksApi.reducerPath]: tasksApi.reducer,
    [subtasksApi.reducerPath]: subtasksApi.reducer,
    [activitiesApi.reducerPath]: activitiesApi.reducer,
    [fitnessApi.reducerPath]: fitnessApi.reducer,

    [eventsApi.reducerPath]: eventsApi.reducer,
    [googleAuthApi.reducerPath]: googleAuthApi.reducer,

    [userApi.reducerPath]: userApi.reducer,
    [analyticsApi.reducerPath]: analyticsApi.reducer,

  },
  

  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false, // ✅ important (dates, tokens, etc.)
    }).concat(
      authApi.middleware,
      proposalsApi.middleware,
      chatApi.middleware,
      goalsApi.middleware,
      tasksApi.middleware,
      subtasksApi.middleware,
      activitiesApi.middleware,
      fitnessApi.middleware,

      eventsApi.middleware,
      googleAuthApi.middleware,

      analyticsApi.middleware,
      userApi.middleware// ✅ ADD
    ),

  devTools: import.meta.env.DEV,
});

/* ---------------------------
   APP INITIALIZATION
---------------------------- */

let initialized = false;

const initialiseApp = () => {
  if (initialized) return;
  initialized = true;

  const auth = localStorage.getItem("auth");
  if (!auth) return;

  // 1️⃣ Hydrate auth slice instantly
  store.dispatch(loadFromStorage(JSON.parse(auth)));

  // 2️⃣ Validate token silently in background
  store.dispatch(authApi.endpoints.loadUser.initiate());
};

initialiseApp();
