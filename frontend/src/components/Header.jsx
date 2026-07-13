import React from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
} from "@mui/material";

function Header() {
  return (
    <AppBar
      position="static"
      elevation={0}
      sx={{
        backgroundColor: "#ffffff",
        color: "#1f2937",
        borderBottom: "1px solid #e5e7eb",
      }}
    >
      <Toolbar
        sx={{
          minHeight: "72px !important",
          px: 4,
          display: "flex",
          alignItems: "center",
        }}
      >
        <Box>
          <Typography
            variant="h4"
            sx={{
              fontWeight: 700,
              fontSize: 30,
              lineHeight: 1.2,
            }}
          >
            AI First CRM
          </Typography>

          <Typography
            sx={{
              color: "#6b7280",
              fontSize: 15,
              mt: 0.5,
            }}
          >
            HCP Interaction Management Dashboard
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Header;