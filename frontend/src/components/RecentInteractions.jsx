import React from "react";
import {
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  Divider,
  Button,
} from "@mui/material";

function RecentInteractions({
  interactions,
  fetchInteractions,
}) {
  return (
    <Paper sx={{ p: 3, borderRadius: 3 }}>
      <Typography variant="h6" fontWeight="bold">
        Recent Interactions
      </Typography>

      <Button
        variant="contained"
        fullWidth
        sx={{ mt: 2, mb: 2 }}
        onClick={fetchInteractions}
      >
        Refresh
      </Button>

      <List>
        {interactions.length === 0 ? (
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ mt: 2 }}
          >
            No interactions found.
          </Typography>
        ) : (
          interactions.map((item) => (
            <React.Fragment key={item.id}>
              <ListItem alignItems="flex-start">
                <ListItemText
                  primary={item.hcp_name}
                  secondary={
                    <>
                      <strong>Meeting:</strong> {item.meeting_type}
                      <br />
                      <strong>Date:</strong> {item.date}
                      <br />
                      <strong>Summary:</strong> {item.summary}
                    </>
                  }
                />
              </ListItem>
              <Divider />
            </React.Fragment>
          ))
        )}
      </List>
    </Paper>
  );
}

export default RecentInteractions;