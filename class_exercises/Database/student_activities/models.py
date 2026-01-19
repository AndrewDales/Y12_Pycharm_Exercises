from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so

# Base is called an Abstract Base Class - our SQL Alchemy models will inherit from this class
class Base(so.DeclarativeBase):
    pass

# Sets up a Person table, this references "activities" via the person_activities table.
# In this case we allow the first_name to be optional, so it may be Null in the database table.
# first_name and last_name do not have additional column requirements, so the type hint is sufficient
class Person(Base):
    __tablename__ = 'persons'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    first_name: so.Mapped[Optional[str]]
    last_name: so.Mapped[str]


    # Gives a representation of a Person (for printing out)
    def __repr__(self) -> str:
        return f"Person(first_name='{self.first_name}', last_name='{self.last_name}')"

    # Include a method:
    def greeting(self) -> None:
        print(f'{self.first_name} says "hello"!')
