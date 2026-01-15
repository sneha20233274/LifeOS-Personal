import { createSlice } from "@reduxjs/toolkit";

const proposalsSlice = createSlice({
  name: "proposals",
  initialState: {
    threadId: null,
    proposals: [],
  },
  reducers: {
    setProposals(state, action) {
      state.threadId = action.payload.threadId;
      state.proposals = action.payload.proposals;
    },
    clearProposals(state) {
      state.threadId = null;
      state.proposals = [];
    },
  },
});

export const { setProposals, clearProposals } = proposalsSlice.actions;
export default proposalsSlice.reducer;
