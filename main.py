import sqlite3
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Vaastu Next API Service")

# ----------------------------------------------------
# CORS Config: Allows your HTML frontend to communicate
# ----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your actual deployed URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# 1. Database Initialization
# ----------------------------------------------------
def init_db():
    conn = sqlite3.connect("vaastu_next.db")
    cursor = conn.cursor()
    # Create Bookings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone_string TEXT NOT NULL,
            consultation_class TEXT NOT NULL,
            target_zone TEXT NOT NULL,
            objectives TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ----------------------------------------------------
# 2. Data Transfer Objects (Pydantic Schemas)
# ----------------------------------------------------
class ConsultationRequest(BaseModel):
    full_name: str = Field(..., description="Client legal or corporate name")
    phone_string: str = Field(..., description="Contact telephone string")
    consultation_class: str = Field(..., description="Residential, Commercial, Industrial")
    target_zone: str = Field(..., description="Target footprint zone parameters")
    objectives: Optional[str] = Field(None, description="Detailed optimization criteria")

class ChatMessage(BaseModel):
    message: str

# ----------------------------------------------------
# 3. API Endpoints
# ----------------------------------------------------

@app.post("/api/schedule-consultation")
async def schedule_consultation(request: ConsultationRequest):
    """
    Receives frontend booking payloads and logs requests safely to SQLite
    """
    try:
        conn = sqlite3.connect("vaastu_next.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO consultations (full_name, phone_string, consultation_class, target_zone, objectives, timestamp)
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
        return {"status": "success", "message": "Blueprint routing request successfully logged."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database write execution failed: {str(e)}")


@app.post("/api/chat")
async def process_chatbot_message(payload: ChatMessage):
    """
    Processes incoming engineering or spatial requests via your chat interface
    """
    user_query = payload.message.strip().lower()
    
    if not user_query:
        raise HTTPException(status_code=400, detail="Empty query string processed.")

    # Engineering baseline or LLM wrapper routing context
    # You can easily plug your custom OpenAI / Anthropic API layer right here
    if "office" in user_query or "work" in user_query:
        ai_reply = "For corporate and designer workspaces, it is vital to balance lighting and desk orientations to eliminate friction. I recommend looking into optimizing entry thresholds and seating alignments to maximize clarity and stable cash flows."
    elif "basement" in user_query:
        ai_reply = "Basement layout footprints typically suffer from subdued energetic flows. By executing logical layout modifications—without tearing down walls—we can transform it into a vibrant workspace where clients feel comfortable and motivated."
    else:
        ai_reply = "Namaste! I am your advanced logical spatial assistant. Please tell me more about your floor layout, structural entries, or corporate environment so we can calculate a high-impact optimization blueprint."

    return {
        "status": "success",
        "reply": ai_reply,
        "processed_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    # Changed from 0.0.0.0 to 127.0.0.1 to prevent the network address error
    uvicorn.run(app, host="127.0.0.1", port=8000)