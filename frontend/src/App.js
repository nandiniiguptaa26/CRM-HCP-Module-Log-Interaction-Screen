import "./App.css";
import React, { useState } from "react";
import axios from "axios";

import InteractionForm from "./components/InteractionForm";
import AIAssistant from "./components/AIAssistant";

function App() {

  const [formData, setFormData] = useState({
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

    follow_up_actions: ""
  });

  const [chat, setChat] = useState("");
  const [aiResponse, setAiResponse] = useState("");

  // ============================
  // Handle Form Change
  // ============================

  const handleChange = (e) => {

    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));

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

      setFormData({
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

        follow_up_actions: ""
      });

      setChat("");
      setAiResponse("");

    }

    catch (err) {

      console.error(err);
      alert("Unable to save interaction");

    }

  };

  // ============================
  // AI Extraction
  // ============================
const formatTime = (time) => {

  if (!time) return "";

  // already correct format
  if (/^\d{2}:\d{2}$/.test(time)) {
    return time;
  }

  const match = time.match(/(\d+):(\d+)\s?(AM|PM)/i);

  if (!match) {
    return "";
  }

  let hour = parseInt(match[1]);
  let minute = match[2];
  let period = match[3].toUpperCase();

  if (period === "PM" && hour !== 12) {
    hour += 12;
  }

  if (period === "AM" && hour === 12) {
    hour = 0;
  }

  return `${hour.toString().padStart(2,"0")}:${minute}`;

};
  const sendToAI = async () => {

    try {

      const inputText =
        chat.trim() !== ""
          ? chat
          : formData.discussion;

      if (!inputText) {

        alert("Please enter interaction details.");

        return;

      }

      const res = await axios.post(

        "http://127.0.0.1:8000/ai/extract",

        {
          query: inputText
        }

      );

      const data = res.data;

      console.log("AI Response:", data);
setFormData({

  hcp_name: data.hcp_name || "",

  meeting_type:
    data.meeting_type || "Meeting",

  date:
    data.date || "",

  time:
    formatTime(data.time),

  attendees:
    data.attendees || "",

  discussion:
    data.discussion || inputText,


  materials_shared:
    Array.isArray(data.materials_shared)
      ? data.materials_shared.join(", ")
      : data.materials_shared || "",


  samples_distributed:
    Array.isArray(data.samples_distributed)
      ? data.samples_distributed.join(", ")
      : data.samples_distributed || "",


  sentiment:
    data.sentiment || "",


  outcomes:
    data.outcomes || "",


  follow_up_actions:
    data.follow_up_actions || "",


  summary:
    data.summary || "",


  follow_up:
    data.follow_up || ""

});

setAiResponse(data.summary || "");

    }

    catch (err) {

  console.error(err);

  alert("AI extraction failed");

}

  };

return (

  <div className="app">

    <div className="left-panel">

      <InteractionForm

        formData={formData}

        handleChange={handleChange}

        saveInteraction={saveInteraction}

        sendToAI={sendToAI}

      />

    </div>

    <div className="divider"></div>

    <div className="right-panel">

      <AIAssistant

        chat={chat}

        setChat={setChat}

        sendToAI={sendToAI}

        aiResponse={aiResponse}

      />

    </div>

  </div>

);

}

export default App;