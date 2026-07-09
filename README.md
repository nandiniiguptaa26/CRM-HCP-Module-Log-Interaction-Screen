# AI HCP CRM (Healthcare Professional CRM)

## Project Overview

AI HCP CRM is an intelligent customer relationship management system designed for healthcare sales teams to efficiently manage Healthcare Professional (HCP) interactions.

The application uses Generative AI and LangGraph agents to automatically extract important details from sales conversations, generate professional summaries, analyze sentiment, and suggest follow-up actions.

The system helps medical representatives maintain accurate interaction records and improve customer engagement through AI-powered automation.

## Key Features

- AI-based HCP interaction extraction
- Automatic identification of:
  - HCP name
  - Meeting type
  - Date and time
  - Attendees
  - Discussion points
  - Materials shared
  - Samples distributed
  - Sentiment analysis
  - Outcomes
  - Follow-up actions

- Interaction management:
  - Create and save HCP interactions
  - Edit interaction details
  - Search HCP interaction history

- AI capabilities:
  - Conversation summarization
  - Follow-up recommendation generation
  - AI CRM assistant

## Technology Stack

### Frontend
- React.js
- Material UI
- Axios
- JavaScript

### Backend
- FastAPI
- Python
- SQLAlchemy
- SQLite

### AI / Agent Framework
- LangGraph
- LangChain
- Groq LLM

## Architecture

Frontend (React)
↓
FastAPI Backend
↓
LangGraph AI Agent
↓
Groq LLM
↓
SQLite Database


## How to Run the Project

### Backend Setup

Navigate to backend folder:

```bash
cd backend