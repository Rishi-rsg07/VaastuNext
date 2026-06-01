from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import sqlite3
from datetime import datetime

app = FastAPI(title="Vaastu Next Booking API")

# Enable CORS so your frontend can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your specific domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Database Setup (SQLite)
def init_db():
    conn = sqlite3.connect("consultations.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone_string TEXT NOT NULL,
            consultation_class TEXT,
            target_zone TEXT,
            objectives TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 2. Data Schema (Matching your UI exactly)
class ConsultationRequest(BaseModel):
    full_name: str = Field(..., alias="full_name")
    phone_string: str = Field(..., alias="phone_string")
    consultation_class: str = Field(..., alias="consultation_class")
    target_zone: str = Field(..., alias="target_zone")
    objectives: Optional[str] = Field(None, alias="objectives")

# 3. Endpoint for "Request Blueprint Routing"
@app.post("/api/schedule-consultation")
async def schedule_consultation(request: ConsultationRequest):
    try:
        conn = sqlite3.connect("consultations.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bookings (full_name, phone_string, consultation_class, target_zone, objectives, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            request.full_name,
            request.phone_string,
            request.consultation_class,
            request.target_zone,
            request.objectives,
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
        
        return {"status": "success", "message": "Blueprint routing request logged successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="[IP_ADDRESS]", port=8000)