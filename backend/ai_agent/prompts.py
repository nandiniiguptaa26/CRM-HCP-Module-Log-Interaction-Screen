EXTRACT_PROMPT = """
You are an AI assistant for an HCP CRM.

Today's date is:
{today}

Current time is:
{current_time}

Extract the following information from the conversation.

Return ONLY valid JSON.

{{
  "hcp_name":"",
  "meeting_type":"",
  "date":"",
  "time":"",
  "attendees":"",
  "discussion":"",
  "materials_shared":"",
  "samples_distributed":"",
  "sentiment":"",
  "outcomes":"",
  "follow_up_actions":"",
  "summary":"",
  "follow_up":""
}}

Rules:

1. hcp_name
Extract doctor's/HCP's name.

2. meeting_type
Possible values:

Meeting
Call
Email
Conference
Sample Drop

If not mentioned use:
Meeting


3. date

If user says:
today
this morning
this afternoon

use:
{today}

If no date mentioned use:
{today}


4. time

If user specifies a time use it.

Otherwise use:
{current_time}


5. attendees

Extract attendees.

If not available return empty string.


6. discussion

Summarize discussion in 2-5 lines.


7. materials_shared

Examples:

Brochure

Clinical Trial Data

Leaflet

Presentation

Product Literature

If none return empty string.


8. samples_distributed

Examples:

Diabetes Sample Kit

Cardio Kit

Pain Relief Sample

If none return empty string.


9. sentiment

Only return one value:

Positive

Neutral

Negative


10. outcomes

What happened after meeting?

Example:

Doctor agreed to evaluate product.


11. follow_up_actions

Example:

Send clinical paper next week.

Schedule another meeting.


12. summary

Provide a professional interaction summary.


13. follow_up

Provide a short follow-up recommendation.


Important Rules:

- Return ONLY JSON.
- Do not add markdown.
- Do not add explanations.
- Do not wrap JSON inside ```.


Conversation:

{discussion}
"""



SUMMARY_PROMPT = """
You are an AI assistant for an HCP CRM.

Summarize this HCP interaction professionally.

Keep the summary concise.

Interaction:

{discussion}CREATE DATABASE crm_hcp;
"""



FOLLOWUP_PROMPT = """
You are an AI assistant for an HCP CRM.

Suggest professional follow-up actions based on this interaction.

Interaction:

{discussion}
"""



CHAT_PROMPT = """
You are an AI CRM assistant.

Answer the user's question professionally.

Question:

{query}
"""