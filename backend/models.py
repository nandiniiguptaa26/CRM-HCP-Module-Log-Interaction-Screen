from sqlalchemy import Column, Integer, String, Text, Date, Time
from database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # HCP Details
    hcp_name = Column(String, nullable=False)
    meeting_type = Column(String)

    # Interaction Details
    date = Column(String)
    time = Column(String)
    attendees = Column(String)
    discussion = Column(String)

 

    # AI Generated
    summary = Column(String)
    follow_up = Column(String)
    materials_shared = Column(Text, nullable=True)

    samples_distributed = Column(Text, nullable=True)

    sentiment = Column(String, nullable=True)

    outcomes = Column(Text, nullable=True)

    follow_up_actions = Column(Text, nullable=True)