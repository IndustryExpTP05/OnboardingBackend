from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import DataEntry

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# ✅ Health check route
@app.get("/")
async def root():
    return {"message": "FastAPI is running on Render 🚀"}

# ✅ Check PostgreSQL connection
@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(1))  # SQLAlchemy async SELECT 1
        return {"database_status": "Connected"}
    except Exception as e:
        return {"error": str(e)}

# ✅ Fetch data from PostgreSQL instead of CSV
@app.get("/data")
async def fetch_data(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(DataEntry))  # Fetch from DB
        data = result.scalars().all()  # Convert query result to list
        return [{"ID": entry.ID, "Name": entry.Name} for entry in data]
    except Exception as e:
        return {"error": str(e)}
