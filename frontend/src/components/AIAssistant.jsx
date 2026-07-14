import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  TextField,
  IconButton,
  Divider,
} from "@mui/material";

import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import SendIcon from "@mui/icons-material/Send";

import { useSelector, useDispatch } from "react-redux";
import {
  setChat,
} from "../redux/interactionSlice";

function AIAssistant({
  sendToAI,
  aiResponse,
}) {

  const dispatch = useDispatch();

  const chat = useSelector(
    (state) => state.interaction.chat
  );

  const [messages, setMessages] = useState([
    {
      from: "ai",
      text:
        "Hi! Describe your HCP interaction in natural language and I'll automatically fill the CRM form.",
    },
  ]);

  const handleSend = async () => {

    if (!chat.trim()) return;

    const userMessage = chat;

    setMessages((prev) => [
      ...prev,
      {
        from: "user",
        text: userMessage,
      },
    ]);

    await sendToAI();

    dispatch(setChat(""));
  };

  useEffect(() => {

    if (aiResponse) {

      setMessages((prev) => [
        ...prev,
        {
          from: "ai",
          text: aiResponse,
        },
      ]);

    }

  }, [aiResponse]);

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        background: "#fff",
      }}
    >

      {/* Header */}

      <Box
        sx={{
          px: 3,
          py: 2.5,
          borderBottom: "1px solid #E5E7EB",
        }}
      >

        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 1,
          }}
        >

          <AutoAwesomeIcon
            sx={{
              color: "#1976d2",
            }}
          />

          <Typography fontWeight={700}>
            AI Assistant
          </Typography>

        </Box>

        <Typography
          fontSize={13}
          color="#666"
          mt={1}
        >
          Tell me about your doctor interaction. I will automatically fill the CRM form.
        </Typography>

      </Box>

      {/* Messages */}

      <Box
        sx={{
          flex: 1,
          overflowY: "auto",
          p: 2,
        }}
      >

        {messages.map((msg, index) => (

          <Box
            key={index}
            sx={{
              display: "flex",
              justifyContent:
                msg.from === "user"
                  ? "flex-end"
                  : "flex-start",
              mb: 2,
            }}
          >

            <Box
              sx={{
                maxWidth: "90%",
                background:
                  msg.from === "ai"
                    ? "#EAF3FF"
                    : "#F3F4F6",
                borderRadius: 2,
                px: 2,
                py: 1.5,
              }}
            >
              {msg.text}
            </Box>

          </Box>

        ))}

      </Box>

      <Divider />

      {/* Chat */}

      <Box
        sx={{
          display: "flex",
          gap: 1,
          p: 2,
        }}
      >

        <TextField
          fullWidth
          size="small"
          placeholder="Example: Met Dr Sharma today at 3 PM. Discussed diabetes medicine..."
          value={chat}
          onChange={(e) =>
            dispatch(setChat(e.target.value))
          }
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSend();
            }
          }}
        />

        <IconButton
          onClick={handleSend}
          sx={{
            background: "#1976d2",
            color: "#fff",
            "&:hover": {
              background: "#1565c0",
            },
          }}
        >
          <SendIcon />
        </IconButton>

      </Box>

    </Box>
  );
}

export default AIAssistant;