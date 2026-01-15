import { createSlice } from "@reduxjs/toolkit";

const appSlice = createSlice({
  name: "app",
  initialState: {
    currentMode: "planner",
    fileContext: null,
  },
  reducers: {
    setMode: (state, action) => {
      state.currentMode = action.payload;
    },
    setFileContext: (state, action) => {
      state.fileContext = action.payload;
    },
  },
});

export const { setMode, setFileContext } = appSlice.actions;
export default appSlice.reducer;
