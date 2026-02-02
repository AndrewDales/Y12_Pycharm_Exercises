from sqlalchemy import create_engine
from models import Base

# Create an engine with the address of the
engine = create_engine('sqlite:///social_media.db', echo=True)

# Drop (delete) the existing tables so that they can be recreated reflecting any
# changes to the model
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
