import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  formData: {
    hcp_name: "",
    meeting_type: "Meeting",
    date: "",
    time: "",
    attendees: "",
    discussion: "",
    summary: "",
    follow_up: "",
    materials_shared: "",
    samples_distributed: "",
    sentiment: "",
    outcomes: "",
    follow_up_actions: "",
  },
  chat: "",
  aiResponse: "",
};

const interactionSlice = createSlice({
  name: "interaction",
  initialState,
  reducers: {
    updateForm(state, action) {
      state.formData = {
        ...state.formData,
        ...action.payload,
      };
    },

    setChat(state, action) {
      state.chat = action.payload;
    },

    setAIResponse(state, action) {
      state.aiResponse = action.payload;
    },

    resetForm(state) {
      state.formData = initialState.formData;
      state.chat = "";
      state.aiResponse = "";
    },
  },
});

export const {
  updateForm,
  setChat,
  setAIResponse,
  resetForm,
} = interactionSlice.actions;

export default interactionSlice.reducer;