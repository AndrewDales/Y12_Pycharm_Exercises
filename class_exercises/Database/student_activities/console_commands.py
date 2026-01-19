from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session
from models import Person

# Connect to the activities database
engine = create_engine('sqlite:///activities.sqlite', echo=True)
