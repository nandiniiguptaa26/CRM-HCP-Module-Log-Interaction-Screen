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
)


load_dotenv()


# =====================================================
# LLM CONFIGURATION
# =====================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
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

    """
    Remove markdown and extract JSON
    """

    text = text.strip()

    text = text.replace(
        "```json",
        ""
    )

    text = text.replace(
        "```",
        ""
    )


    # find JSON object

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )


    if match:

        return match.group()


    return text
    # =====================================================
# Tool 1 : Extract Interaction
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


        text = result.content


        print("========== AI RAW RESPONSE ==========")
        print(text)
        print("=====================================")


        cleaned_text = clean_json_response(text)


        data = json.loads(cleaned_text)



    except Exception as e:


        print(
            "AI EXTRACTION ERROR:",
            e
        )


        data = {

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



    # ============================
    # DEFAULT VALUES
    # ============================


    default_values = {


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



    for key, value in default_values.items():

        if key not in data or data[key] is None:

            data[key] = value



    # convert list response to string

    if isinstance(
        data.get("materials_shared"),
        list
    ):

        data["materials_shared"] = ", ".join(
            data["materials_shared"]
        )


    if isinstance(
        data.get("samples_distributed"),
        list
    ):

        data["samples_distributed"] = ", ".join(
            data["samples_distributed"]
        )


    return data
    # =====================================================
# Tool 2 : Save Interaction
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

        print(
            "DATABASE ERROR:",
            e
        )


        return {

            "status": "error",

            "message": str(e)

        }


    finally:

        db.close()



# =====================================================
# Tool 3 : Edit Interaction
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


            if hasattr(
                interaction,
                key
            ):

                setattr(
                    interaction,
                    key,
                    value
                )


        db.commit()

        db.refresh(interaction)


        return {

            "status": "success",

            "message": "Interaction updated successfully"

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
# Tool 4 : Search HCP
# =====================================================

def search_hcp(name: str):

    db = get_db()


    try:


        results = (

            db.query(Interaction)

            .filter(
                Interaction.hcp_name.contains(name)
            )

            .all()

        )


        response = []


        for item in results:


            response.append({

                "id": item.id,

                "hcp_name": item.hcp_name,

                "meeting_type": item.meeting_type,

                "date": item.date,

                "time": item.time,

                "attendees": item.attendees,

                "discussion": item.discussion,

                "summary": item.summary,

                "follow_up": item.follow_up

            })


        return response



    finally:

        db.close()




# =====================================================
# Tool 5 : AI Summary
# =====================================================

def summarize_interaction(notes: str):


    prompt = SUMMARY_PROMPT.format(
        discussion=notes
    )


    try:

        result = llm.invoke(prompt)

        return result.content.strip()


    except Exception as e:

        print(
            "SUMMARY ERROR:",
            e
        )

        return ""




# =====================================================
# Tool 6 : AI Follow-up
# =====================================================

def suggest_followup(notes: str):


    prompt = FOLLOWUP_PROMPT.format(
        discussion=notes
    )


    try:

        result = llm.invoke(prompt)

        return result.content.strip()


    except Exception as e:

        print(
            "FOLLOWUP ERROR:",
            e
        )

        return ""




# =====================================================
# Tool 7 : AI Chat Assistant
# =====================================================

def chat_assistant(query: str):


    prompt = CHAT_PROMPT.format(
        query=query
    )


    try:

        result = llm.invoke(prompt)

        return result.content.strip()


    except Exception as e:


        print(
            "CHAT ERROR:",
            e
        )


        return "Unable to process request."