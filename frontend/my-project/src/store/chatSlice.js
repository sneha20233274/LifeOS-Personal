// store/chatSlice.js
import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  activeSessionId: null,      // current session
  messages: [],               // messages for current session
  sessions: {},               // all sessions with messages
  history: [],                // session history for sidebar
};

const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    setSession: (state, action) => {
      state.activeSessionId = action.payload;
      // Load messages for this session if exists
      state.messages = state.sessions[action.payload] || [];
    },
    addMessage: (state, action) => {
      state.messages.push(action.payload);
      if (state.activeSessionId) {
        if (!state.sessions[state.activeSessionId]) state.sessions[state.activeSessionId] = [];
        state.sessions[state.activeSessionId].push(action.payload);
      }
    },
    addToHistory: (state, action) => {
      // Only add to history if it doesn't exist already
      const exists = state.history.find((h) => h.id === action.payload.id);
      if (!exists) state.history.push(action.payload);
    },
  },
});

export const { setSession, addMessage, addToHistory } = chatSlice.actions;
export default chatSlice.reducer;
