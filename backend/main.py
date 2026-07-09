from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Interaction
from schemas import InteractionCreate

from ai_agent.graph import graph

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# Database
# ==========================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================================
# Home
# ==========================================================

@app.get("/")
def home():
    return {"message": "Backend Running"}


# ==========================================================
# Save Interaction
# ==========================================================

@app.post("/interactions")
def create_interaction(
    data: InteractionCreate,
    db: Session = Depends(get_db)
):

    interaction = Interaction(**data.model_dump())

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return interaction


# ==========================================================
# Get All
# ==========================================================

@app.get("/interactions")
def get_interactions(
    db: Session = Depends(get_db)
):
    return db.query(Interaction).all()


# ==========================================================
# Update
# ==========================================================

@app.put("/interactions/{interaction_id}")
def update_interaction(
    interaction_id: int,
    data: InteractionCreate,
    db: Session = Depends(get_db)
):

    interaction = (
        db.query(Interaction)
        .filter(Interaction.id == interaction_id)
        .first()
    )

    if interaction is None:
        return {
            "message": "Interaction not found"
        }

    interaction.hcp_name = data.hcp_name
    interaction.meeting_type = data.meeting_type
    interaction.date = data.date
    interaction.time = data.time
    interaction.attendees = data.attendees
    interaction.discussion = data.discussion
    interaction.summary = data.summary
    interaction.follow_up = data.follow_up
    interaction.materials_shared = data.materials_shared
    interaction.samples_distributed = data.samples_distributed
    interaction.materials_shared = data.materials_shared

    interaction.samples_distributed = data.samples_distributed

    interaction.sentiment = data.sentiment

    interaction.outcomes = data.outcomes

    interaction.follow_up_actions = data.follow_up_actions


    db.commit()
    db.refresh(interaction)

    return interaction


# ==========================================================
# Search
# ==========================================================

@app.get("/interactions/search/{hcp_name}")
def search_hcp(
    hcp_name: str,
    db: Session = Depends(get_db)
):

    results = (
        db.query(Interaction)
        .filter(Interaction.hcp_name.contains(hcp_name))
        .all()
    )

    return results


# ==========================================================
# AI EXTRACT (NEW)
# ==========================================================

@app.post("/ai/extract")
def ai_extract(data: dict):

    result = graph.invoke({
        "action": "extract",
        "input": {
            "query": data["query"]
        }
    })

    return result["output"]


# ==========================================================
# AI SUMMARY
# ==========================================================

@app.post("/ai/summary")
def ai_summary(data: dict):

    result = graph.invoke({
        "action": "summary",
        "input": {
            "discussion": data["discussion"]
        }
    })

    return result["output"]


# ==========================================================
# AI FOLLOWUP
# ==========================================================

@app.post("/ai/followup")
def ai_followup(data: dict):

    result = graph.invoke({
        "action": "followup",
        "input": {
            "discussion": data["discussion"]
        }
    })

    return result["output"]


# ==========================================================
# AI CHAT
# ==========================================================

@app.post("/ai/chat")
def ai_chat(data: dict):

    result = graph.invoke({
        "action": "chat",
        "input": {
            "query": data["query"]
        }
    })

    return result["output"]