import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")  # This should be set in Render

# Create the async database engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Dependency to get database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
