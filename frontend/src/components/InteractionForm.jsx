import React from "react";

import {
  Box,
  Paper,
  Typography,
  TextField,
  MenuItem,
  Button,
  Divider,
  Link,
  Radio,
  RadioGroup,
  FormControlLabel,
  InputAdornment,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";
import MicIcon from "@mui/icons-material/Mic";
import AddIcon from "@mui/icons-material/Add";

const interactionTypes = [
  "Meeting",
  "Call",
  "Email",
  "Conference",
  "Sample Drop",
];

function InteractionForm({
  formData,
  handleChange,
  saveInteraction,
  sendToAI,
}) {

  return (

    <Paper
      elevation={0}
      sx={{
        height: "100%",
        overflowY: "auto",
        borderRadius: 0,
        p: 4,
      }}
    >

      {/* Heading */}

      <Typography
        sx={{
          fontSize: 34,
          fontWeight: 700,
          mb: 4,
        }}
      >
        Log HCP Interaction
      </Typography>

      <Typography
        sx={{
          fontWeight: 700,
          color: "#777",
          fontSize: 12,
          letterSpacing: 1,
          mb: 3,
        }}
      >
        INTERACTION DETAILS
      </Typography>

      {/* HCP + Interaction Type */}

      <Box
        sx={{
          display: "flex",
          gap: 2,
          mb: 3,
        }}
      >

        <Box flex={1}>

          <Typography sx={{ mb: 1, fontWeight: 600 }}>
            HCP Name
          </Typography>

          <TextField
            fullWidth
            size="small"
            name="hcp_name"
            value={formData.hcp_name}
            onChange={handleChange}
            placeholder="Search or select HCP..."
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon fontSize="small" />
                </InputAdornment>
              ),
            }}
          />

        </Box>

        <Box flex={1}>

          <Typography sx={{ mb: 1, fontWeight: 600 }}>
            Interaction Type
          </Typography>

          <TextField
            select
            fullWidth
            size="small"
            name="meeting_type"
            value={formData.meeting_type}
            onChange={handleChange}
          >
            {interactionTypes.map((item) => (
              <MenuItem
                key={item}
                value={item}
              >
                {item}
              </MenuItem>
            ))}
          </TextField>

        </Box>

      </Box>

      {/* Date + Time */}

      <Box
        sx={{
          display: "flex",
          gap: 2,
          mb: 3,
        }}
      >

        <Box flex={1}>

          <Typography sx={{ mb: 1, fontWeight: 600 }}>
            Date
          </Typography>

          <TextField
            fullWidth
            size="small"
            type="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
          />

        </Box>

        <Box flex={1}>

          <Typography sx={{ mb: 1, fontWeight: 600 }}>
            Time
          </Typography>

          <TextField
            fullWidth
            size="small"
            type="time"
            name="time"
            value={formData.time}
            onChange={handleChange}
          />

        </Box>

      </Box>

      {/* Attendees */}

      <Typography
        sx={{
          fontWeight: 600,
          mb: 1,
        }}
      >
        Attendees
      </Typography>

      <TextField
        fullWidth
        size="small"
        name="attendees"
        value={formData.attendees}
        onChange={handleChange}
        placeholder="Enter names or search..."
        sx={{ mb: 3 }}
      />
            {/* Topics Discussed */}

      <Typography
        sx={{
          fontWeight: 600,
          mb: 1,
        }}
      >
        Topics Discussed
      </Typography>

      <TextField
        fullWidth
        multiline
        rows={5}
        name="discussion"
        value={formData.discussion}
        onChange={handleChange}
        placeholder="Enter key discussion points..."
      />

      <Link
        component="button"
        underline="none"
        onClick={sendToAI}
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1,
          mt: 2,
          mb: 4,
          fontSize: 13,
          color: "#1976d2",
        }}
      >
        <MicIcon sx={{ fontSize: 18 }} />
        Summarize from Voice Note (Requires Consent)
      </Link>

      <Divider sx={{ mb: 4 }} />

      {/* ========================================== */}
      {/* Materials Shared / Samples Distributed */}
      {/* ========================================== */}

      <Typography
        sx={{
          fontSize: 20,
          fontWeight: 700,
          mb: 3,
        }}
      >
        Materials Shared / Samples Distributed
      </Typography>

      {/* Materials Shared */}

      <Typography
        sx={{
          fontWeight: 600,
          mb: 1,
        }}
      >
        Materials Shared
      </Typography>

      <Box
        sx={{
          display: "flex",
          gap: 2,
          mb: 2,
        }}
      >
        <TextField
          fullWidth
          size="small"
          name="materials_shared"
          value={formData.materials_shared}
          onChange={handleChange}
          placeholder="Search / Add"
        />

        <Button
          variant="outlined"
          startIcon={<AddIcon />}
        >
          Add
        </Button>
      </Box>

      {!formData.materials_shared && (
        <Typography
          sx={{
            color: "#777",
            mb: 3,
            fontSize: 14,
          }}
        >
          No materials added.
        </Typography>
      )}

      {/* Samples Distributed */}

      <Typography
        sx={{
          fontWeight: 600,
          mb: 1,
        }}
      >
        Samples Distributed
      </Typography>

      <Box
        sx={{
          display: "flex",
          gap: 2,
          mb: 2,
        }}
      >
        <TextField
          fullWidth
          size="small"
          name="samples_distributed"
          value={formData.samples_distributed}
          onChange={handleChange}
          placeholder="Search / Add"
        />

        <Button
          variant="outlined"
          startIcon={<AddIcon />}
        >
          Add Sample
        </Button>
      </Box>

      {!formData.samples_distributed && (
        <Typography
          sx={{
            color: "#777",
            mb: 4,
            fontSize: 14,
          }}
        >
          No samples added.
        </Typography>
      )}

      <Divider sx={{ mb: 4 }} />
            {/* ========================================== */}
      {/* Observed / Inferred HCP Sentiment */}
      {/* ========================================== */}

      <Typography
        sx={{
          fontWeight: 700,
          fontSize: 18,
          mb: 2,
        }}
      >
        Observed / Inferred HCP Sentiment
      </Typography>

      <RadioGroup
        row
        name="sentiment"
        value={formData.sentiment}
        onChange={handleChange}
        sx={{ mb: 4 }}
      >
        <FormControlLabel
          value="Positive"
          control={<Radio />}
          label="😊 Positive"
        />

        <FormControlLabel
          value="Neutral"
          control={<Radio />}
          label="😐 Neutral"
        />

        <FormControlLabel
          value="Negative"
          control={<Radio />}
          label="☹ Negative"
        />
      </RadioGroup>

      {/* Outcomes */}

      <Typography
        sx={{
          fontWeight: 600,
          mb: 1,
        }}
      >
        Outcomes
      </Typography>

      <TextField
        fullWidth
        multiline
        rows={3}
        name="outcomes"
        value={formData.outcomes}
        onChange={handleChange}
        placeholder="Enter meeting outcomes..."
        sx={{ mb: 3 }}
      />

      {/* Follow-up Actions */}

      <Typography
        sx={{
          fontWeight: 600,
          mb: 1,
        }}
      >
        Follow-up Actions
      </Typography>

      <TextField
        fullWidth
        multiline
        rows={3}
        name="follow_up_actions"
        value={formData.follow_up_actions}
        onChange={handleChange}
        placeholder="Enter follow-up actions..."
        sx={{ mb: 4 }}
      />

      <Divider sx={{ mb: 4 }} />

      {/* Bottom Buttons */}

      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <Button
          variant="outlined"
          onClick={() => window.location.reload()}
          sx={{
            textTransform: "none",
            px: 4,
          }}
        >
          Cancel
        </Button>

        <Button
          variant="contained"
          onClick={saveInteraction}
          sx={{
            textTransform: "none",
            px: 4,
            backgroundColor: "#1976d2",

            "&:hover": {
              backgroundColor: "#1565c0",
            },
          }}
        >
          Save Interaction
        </Button>
      </Box>

    </Paper>

  );
}

export default InteractionForm;