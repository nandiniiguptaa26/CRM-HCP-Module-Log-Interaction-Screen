import "./App.css";
import React from "react";
import axios from "axios";

import { useSelector, useDispatch } from "react-redux";
import {
  updateForm,
  setAIResponse,
  resetForm,
} from "./redux/interactionSlice";

import InteractionForm from "./components/InteractionForm";
import AIAssistant from "./components/AIAssistant";

function App() {
  const dispatch = useDispatch();

  const formData = useSelector(
    (state) => state.interaction.formData
  );

  const chat = useSelector(
    (state) => state.interaction.chat
  );

  const aiResponse = useSelector(
    (state) => state.interaction.aiResponse
  );

  // ============================
  // Handle Form Change
  // ============================

  const handleChange = (e) => {
    dispatch(
      updateForm({
        [e.target.name]: e.target.value,
      })
    );
  };

  // ============================
  // Save Interaction
  // ============================

  const saveInteraction = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:8000/interactions",
        formData
      );

      alert("Interaction Saved Successfully");

      dispatch(resetForm());
    } catch (err) {
      console.error(err);
      alert("Unable to save interaction");
    }
  };

  // ============================
  // Format Time
  // ============================

  const formatTime = (time) => {
    if (!time) return "";

    if (/^\d{2}:\d{2}$/.test(time)) {
      return time;
    }

    const match = time.match(/(\d+):(\d+)\s?(AM|PM)/i);

    if (!match) return "";

    let hour = parseInt(match[1]);
    let minute = match[2];
    let period = match[3].toUpperCase();

    if (period === "PM" && hour !== 12) {
      hour += 12;
    }

    if (period === "AM" && hour === 12) {
      hour = 0;
    }

    return `${hour.toString().padStart(2, "0")}:${minute}`;
  };
// ============================
// Voice Recording
// ============================

const startVoiceRecording = () => {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    alert("Speech Recognition is not supported.");
    return;
  }

  const recognition = new SpeechRecognition();

  recognition.lang = "en-IN";
  recognition.continuous = true;
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  console.log("Requesting microphone...");

  recognition.start();

  recognition.onstart = () => {
    console.log("🎤 Listening...");
  };

  recognition.onspeechstart = () => {
    console.log("🗣 Speech detected");
  };

  recognition.onresult = (event) => {
    let transcript = "";

    for (let i = event.resultIndex; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript + " ";
    }

    transcript = transcript.trim();

    console.log("Transcript:", transcript);

    dispatch(
      updateForm({
        discussion: transcript,
      })
    );

    recognition.stop();

    sendToAIWithText(transcript);
  };

  recognition.onerror = (event) => {
    console.log("Speech Error:", event.error);
  };

  recognition.onend = () => {
    console.log("Recording stopped.");
  };
};
const sendToAIWithText = async (inputText) => {
  try {
    const res = await axios.post(
      "http://127.0.0.1:8000/ai/extract",
      {
        query: inputText,
      }
    );

    const data = res.data;

    dispatch(
      updateForm({
        hcp_name: data.hcp_name || "",
        meeting_type: data.meeting_type || "Meeting",
        date: data.date || "",
        time: formatTime(data.time),
        attendees: data.attendees || "",
        discussion: data.discussion || inputText,
        materials_shared: Array.isArray(data.materials_shared)
          ? data.materials_shared.join(", ")
          : data.materials_shared || "",
        samples_distributed: Array.isArray(data.samples_distributed)
          ? data.samples_distributed.join(", ")
          : data.samples_distributed || "",
        sentiment: data.sentiment || "",
        outcomes: data.outcomes || "",
        follow_up_actions: data.follow_up_actions || "",
        summary: data.summary || "",
        follow_up: data.follow_up || "",
      })
    );

    dispatch(setAIResponse(data.summary || ""));
  } catch (err) {
    console.error(err);
    alert("AI extraction failed");
  }
};

  // ============================
  // AI Extraction
  // ============================

const sendToAI = async () => {
  const inputText =
    chat.trim() !== ""
      ? chat
      : formData.discussion;

  if (!inputText) {
    alert("Please enter interaction details.");
    return;
  }

  sendToAIWithText(inputText);
};
  return (
    <div className="app">
      <div className="left-panel">
        <InteractionForm
          formData={formData}
          handleChange={handleChange}
          saveInteraction={saveInteraction}
          sendToAI={sendToAI}
          startVoiceRecording={startVoiceRecording}
        />
      </div>

      <div className="divider"></div>

      <div className="right-panel">
        <AIAssistant
          chat={chat}
          sendToAI={sendToAI}
          aiResponse={aiResponse}
        />
      </div>
    </div>
  );
}

export default App;