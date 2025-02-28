from fastapi import FastAPI, Form, HTTPException
import re

# ✅ Import for handling form data
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Allow all origins for API access (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_QUERY_LENGTH = 200  # Strict input length limit

# ✅ Predefined Security & Medical Responses
responses = {
    # Security Incidents
    "fire": "🔥 Fire department alerted.",
    "intruder": "🚨 Security team alerted.",
    "suspicious activity": "🔍 Security team monitoring the area.",
    "theft": "🚔 Security team investigating reported theft.",
    "vandalism": "🚧 Incident logged: Property damage detected.",
    "lost item": "🛠️ Lost item reported. Security will assist in locating it.",
    "unauthorized vehicle": "🚗 Security team alerted about an unauthorized vehicle.",
    "harassment": "⚠️ Incident reported. Security and HR teams have been notified.",
    "active shooter": "⚠️ Active shooter alert. Lockdown procedures activated. Call 911 immediately.",

    # Medical Emergencies
    "heart attack": "🩺 Medical team alerted for a possible heart attack. Perform CPR if necessary.",
    "stroke": "🚑 Emergency response team dispatched for possible stroke symptoms.",
    "seizure": "⚕️ Medical assistance is on the way for seizure response.",
    "choking": "🚑 Heimlich maneuver may be required. Emergency responders notified.",
    "unconscious": "🚑 Medical team alerted. Check for breathing and pulse.",
    "bleeding": "🩸 Apply direct pressure to the wound. Medical help is on the way.",
    "fracture": "🦴 Medical assistance dispatched for possible fracture.",
    "burn": "🔥 Emergency responders alerted for burn injury.",
    "allergic reaction": "⚕️ Medical team dispatched for severe allergic reaction.",
    "slip and fall": "⚠️ Medical response team alerted. Do not move the injured person."
}

# ✅ Root endpoint to prevent 404 error
@app.get("/")
def home():
    return {"message": "Welcome to the Security Chatbot API! Use the /chatbot endpoint to send messages."}

@app.post("/chatbot")
def handle_chatbot(query: str = Form(...)):
    query = query.strip()  # Remove leading/trailing spaces

    # ✅ IMMEDIATELY block oversized inputs BEFORE doing anything else
    if len(query) > MAX_QUERY_LENGTH:
        raise HTTPException(status_code=413, detail="Input too long. Maximum allowed is 200 characters.")

    query_lower = query.lower()  # Convert to lowercase
    cleaned_query = re.sub(r'\s+', ' ', query_lower).strip()  # Normalize spaces

    # ✅ Check keywords in the order they appear in the input
    words = cleaned_query.split()
    
    for i in range(len(words)):
        # Check single-word matches
        if words[i] in responses:
            return {"response": responses[words[i]]}
        
        # ✅ Fixing "Heart Attack" & "Active Shooter" detection (two-word matches)
        if i < len(words) - 1:
            two_word_phrase = f"{words[i]} {words[i+1]}"
            if two_word_phrase in responses:
                return {"response": responses[two_word_phrase]}

    # ❌ Default response if no match found
    return {"response": "❓ Please specify the type of incident clearly."}

# ✅ Ensure Gunicorn can find the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)













