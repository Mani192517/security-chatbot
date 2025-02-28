from fastapi import APIRouter, Query
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import datetime  # Import datetime to use datetime.now()

# Initialize FastAPI Router
router = APIRouter()

# Load environment variables
load_dotenv("config/.env")

# Email Configuration
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SECURITY_TEAM_EMAIL = os.getenv("SECURITY_TEAM_EMAIL")

# Predefined room locations
ROOM_LOCATIONS = {
    "bella ciao room": "B3 2nd Floor",
    "conference hall": "Building A, Ground Floor",
    "security office": "Main Entrance, First Floor"
}

def send_email_alert(subject, body):
    """Send an email notification for security incidents."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = SECURITY_TEAM_EMAIL

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, SECURITY_TEAM_EMAIL, msg.as_string())
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {e}"

@router.post("/chatbot")
def chatbot_response(query: str = Query(..., description="User query")):
    query_lower = query.lower()

    # Check if it's a room location request
    for room, location in ROOM_LOCATIONS.items():
        if room in query_lower:
            return {"response": f"The {room.title()} is located at {location}."}

    # Define incident keywords to watch for
    incident_keywords = ["incident", "report", "fire", "security breach", "unauthorized access", "intruder"]

    # Function to handle queries and check for incident keywords
    if any(word in query_lower for word in incident_keywords):
        email_subject = "🚨 Security Incident Reported!"
        email_body = f"A new security incident has been reported: {query}.\n\nPlease check immediately."
        email_status = send_email_alert(email_subject, email_body)

        # Log the incident to a file
        with open("logs/security_incidents.log", "a") as log_file:
            log_file.write(f"Incident: {query}\nDate and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        return {"response": "Incident reported! Security has been notified via email.", "email_status": email_status}

    return {"response": "Your query has been processed."}

