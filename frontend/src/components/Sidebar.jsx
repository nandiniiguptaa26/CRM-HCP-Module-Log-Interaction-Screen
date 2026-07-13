import React from "react";
import {
  Drawer,
  Toolbar,
  Typography,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
} from "@mui/material";

import DashboardIcon from "@mui/icons-material/Dashboard";
import DescriptionIcon from "@mui/icons-material/Description";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import LocalHospitalIcon from "@mui/icons-material/LocalHospital";
import AssessmentIcon from "@mui/icons-material/Assessment";

const drawerWidth = 250;

const menuItems = [
  {
    text: "Dashboard",
    icon: <DashboardIcon />,
  },
  {
    text: "Interactions",
    icon: <DescriptionIcon />,
    active: true,
  },
  {
    text: "AI Assistant",
    icon: <AutoAwesomeIcon />,
  },
  {
    text: "Doctors",
    icon: <LocalHospitalIcon />,
  },
  {
    text: "Reports",
    icon: <AssessmentIcon />,
  },
];

function Sidebar() {
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,

        "& .MuiDrawer-paper": {
          width: drawerWidth,
          boxSizing: "border-box",
          background: "#1565C0",
          color: "#fff",
          borderRight: "none",
        },
      }}
    >
      <Toolbar
        sx={{
          minHeight: 72,
          px: 3,
          borderBottom: "1px solid rgba(255,255,255,.15)",
        }}
      >
        <Typography
          variant="h5"
          sx={{
            fontWeight: 700,
          }}
        >
          AI CRM
        </Typography>
      </Toolbar>

      <Box sx={{ mt: 2 }}>
        <List>
          {menuItems.map((item) => (
            <ListItem
              disablePadding
              key={item.text}
              sx={{ mb: 1 }}
            >
              <ListItemButton
                sx={{
                  mx: 2,
                  borderRadius: 2,

                  backgroundColor: item.active
                    ? "rgba(255,255,255,.15)"
                    : "transparent",

                  "&:hover": {
                    backgroundColor: "rgba(255,255,255,.12)",
                  },
                }}
              >
                <ListItemIcon
                  sx={{
                    color: "#fff",
                    minWidth: 40,
                  }}
                >
                  {item.icon}
                </ListItemIcon>

                <ListItemText
                  primary={item.text}
                  primaryTypographyProps={{
                    fontSize: 15,
                    fontWeight: item.active ? 700 : 500,
                  }}
                />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>
    </Drawer>
  );
}

export default Sidebar;