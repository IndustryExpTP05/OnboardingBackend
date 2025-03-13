from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class DataEntry(Base):
    __tablename__ = "data_table"  # ✅ Make sure this matches your queries
    ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String, index=True)
