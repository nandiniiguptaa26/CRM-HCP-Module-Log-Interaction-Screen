import os
import json
import re

from datetime import datetime

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from database import SessionLocal
from models import Interaction

from ai_agent.prompts import (
    EXTRACT_PROMPT,
    SUMMARY_PROMPT,
    FOLLOWUP_PROMPT,
    CHAT_PROMPT,
    VALIDATION_PROMPT,
)

load_dotenv()

# =====================================================
# LLM CONFIGURATION
# =====================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)

# =====================================================
# DATABASE
# =====================================================

def get_db():
    return SessionLocal()


# =====================================================
# JSON CLEANER
# =====================================================

def clean_json_response(text):

    text = text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if match:
        return match.group()

    return text


# =====================================================
# TOOL 1 : VALIDATE INTERACTION
# =====================================================

def validate_interaction(data: dict):

    errors = []

    required = [
        "hcp_name",
        "discussion",
        "meeting_type",
        "date",
        "time"
    ]

    for field in required:

        value = data.get(field)

        if value is None or str(value).strip() == "":
            errors.append(f"{field} is missing")

    if errors:

        return {
            "status": "error",
            "errors": errors
        }

    try:

        prompt = VALIDATION_PROMPT.format(
            interaction=json.dumps(data, indent=2)
        )

        result = llm.invoke(prompt)

        answer = result.content.strip().lower()

        if "invalid" in answer:

            return {
                "status": "error",
                "errors": [
                    "AI validation failed."
                ]
            }

    except Exception as e:

        print("Validation Warning:", e)

    return {
        "status": "success"
    }


# =====================================================
# TOOL 2 : EXTRACT INTERACTION
# =====================================================

def extract_interaction(user_input: str):

    now = datetime.now()

    today = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")

    prompt = EXTRACT_PROMPT.format(
        today=today,
        current_time=current_time,
        discussion=user_input
    )

    try:

        result = llm.invoke(prompt)

        cleaned = clean_json_response(result.content)

        data = json.loads(cleaned)

    except Exception as e:

        print("Extraction Error:", e)

        data = {}

    defaults = {

        "hcp_name": "",

        "meeting_type": "Meeting",

        "date": today,

        "time": current_time,

        "attendees": "",

        "discussion": user_input,

        "materials_shared": "",

        "samples_distributed": "",

        "sentiment": "Neutral",

        "outcomes": "",

        "follow_up_actions": "",

        "summary": "",

        "follow_up": ""

    }

    for key, value in defaults.items():

        if key not in data or data[key] is None:

            data[key] = value

    if isinstance(data["materials_shared"], list):

        data["materials_shared"] = ", ".join(
            data["materials_shared"]
        )

    if isinstance(data["samples_distributed"], list):

        data["samples_distributed"] = ", ".join(
            data["samples_distributed"]
        )


    return data
# =====================================================
# TOOL 3 : SAVE INTERACTION
# =====================================================

def log_interaction(data: dict):

    db = get_db()

    try:

        interaction = Interaction(**data)

        db.add(interaction)
        db.commit()
        db.refresh(interaction)

        return {

            "status": "success",

            "interaction_id": interaction.id,

            "message": "Interaction saved successfully"

        }

    except Exception as e:

        db.rollback()

        print("DATABASE ERROR:", e)

        return {

            "status": "error",

            "message": str(e)

        }

    finally:

        db.close()


# =====================================================
# TOOL 4 : EDIT INTERACTION
# =====================================================

def edit_interaction(
    interaction_id: int,
    updates: dict
):

    db = get_db()

    try:

        interaction = (

            db.query(Interaction)

            .filter(
                Interaction.id == interaction_id
            )

            .first()

        )

        if not interaction:

            return {

                "status": "error",

                "message": "Interaction not found"

            }

        for key, value in updates.items():

            if hasattr(interaction, key):

                setattr(
                    interaction,
                    key,
                    value
                )

        db.commit()
        db.refresh(interaction)

        return {

            "status": "success",

            "message": "Interaction updated successfully",

            "interaction_id": interaction.id

        }

    except Exception as e:

        db.rollback()

        return {

            "status": "error",

            "message": str(e)

        }

    finally:

        db.close()


# =====================================================
# TOOL 5 : SEARCH HCP HISTORY
# =====================================================

def search_hcp(name: str):

    db = get_db()

    try:

        results = (

            db.query(Interaction)

            .filter(
                Interaction.hcp_name.ilike(f"%{name}%")
            )

            .order_by(
                Interaction.id.desc()
            )

            .all()

        )

        history = []

        for item in results:

            history.append({

                "id": item.id,

                "hcp_name": item.hcp_name,

                "meeting_type": item.meeting_type,

                "date": item.date,

                "time": item.time,

                "attendees": item.attendees,

                "discussion": item.discussion,

                "summary": item.summary,

                "follow_up": item.follow_up,

                "sentiment": item.sentiment,

                "outcomes": item.outcomes

            })

        return history

    except Exception as e:

        print("SEARCH ERROR:", e)

        return []

    finally:

        db.close()
# =====================================================
# TOOL 6 : AI SUMMARY
# =====================================================

def summarize_interaction(
    notes: str,
    history: list = None
):

    history_text = ""

    if history:

        history_text = "\n\nPrevious HCP Interactions:\n"

        for index, visit in enumerate(history[:3], start=1):

            history_text += f"""

Visit {index}

Date: {visit.get('date')}

Meeting Type: {visit.get('meeting_type')}

Discussion: {visit.get('discussion')}

Summary: {visit.get('summary')}

Follow-up: {visit.get('follow_up')}

"""

    prompt = SUMMARY_PROMPT.format(

        discussion=notes + history_text

    )

    try:

        result = llm.invoke(prompt)

        return result.content.strip()

    except Exception as e:

        print("SUMMARY ERROR:", e)

        return ""


# =====================================================
# TOOL 7 : AI FOLLOW-UP
# =====================================================

def suggest_followup(
    notes: str,
    history: list = None
):

    history_text = ""

    if history:

        history_text = "\n\nPrevious HCP Interactions:\n"

        for index, visit in enumerate(history[:3], start=1):

            history_text += f"""

Visit {index}

Date: {visit.get('date')}

Discussion: {visit.get('discussion')}

Follow-up: {visit.get('follow_up')}

"""

    prompt = FOLLOWUP_PROMPT.format(

        discussion=notes + history_text

    )

    try:

        result = llm.invoke(prompt)

        return result.content.strip()

    except Exception as e:

        print("FOLLOWUP ERROR:", e)

        return ""


# =====================================================
# TOOL 8 : AI CHAT ASSISTANT
# =====================================================

def chat_assistant(query: str):

    prompt = CHAT_PROMPT.format(

        query=query

    )

    try:

        result = llm.invoke(prompt)

        return result.content.strip()

    except Exception as e:

        print("CHAT ERROR:", e)

        return "Unable to process request."