from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn

app = FastAPI()

# Pydantic models to parse the webhook structure
class ExtractedVariables(BaseModel):
    budget: Optional[str]
    event: Optional[str]
    item: Optional[str]
    style_hint: Optional[str]

class CallReport(BaseModel):
    summary: Optional[str]
    sentiment: Optional[str]
    extracted_variables: Optional[ExtractedVariables]

class WebhookPayload(BaseModel):
    call_id: int
    bot_id: int
    bot_name: str
    phone_number: str
    call_date: str
    user_email: Optional[str]
    call_report: Optional[CallReport]

@app.post("/receive")
async def receive_data(payload: WebhookPayload):
    # Extract summary
    summary: Optional[str] = payload.call_report.summary if payload.call_report else None

    # Extract details as a dictionary (not model)
    details: Dict[str, Any] = {}
    if payload.call_report and payload.call_report.extracted_variables:
        ev = payload.call_report.extracted_variables
        details = {
            "event": ev.event,
            "item": ev.item,
            "budget": ev.budget,
            "style_hint": ev.style_hint
        }

    # Print for logs (optional)
    print("Webhook Received!")
    print("Summary:", summary)
    print("Details:", details)

    # Return response
    return {
        "summary": summary,
        "details": details,
        "raw_payload": payload.model_dump()
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
