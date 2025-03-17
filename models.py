from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class DataEntry(Base):
    __tablename__ = "data_table"  # ✅ Matches your database table name

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # 🔹 Change "ID" → "id"
    name = Column(String, index=True)  # 🔹 Change "Name" → "name"
