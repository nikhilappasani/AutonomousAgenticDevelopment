from fastapi import FastAPI, Request, HTTPException
import uvicorn
import httpx
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("JiraShim")

app = FastAPI()

# Configuration
LANGGRAPH_SERVER = "http://127.0.0.1:2025"
TARGET_ENDPOINT = f"{LANGGRAPH_SERVER}/runs"

@app.post("/jira-webhook")
async def handle_jira_webhook(request: Request):
    try:
        payload = await request.json()
        logger.info("📩 Received Jira Webhook Payload")
        
        # 1. Validation (Is this a real issue event?)
        if "issue" not in payload:
            logger.warning("Ignoring non-issue payload")
            return {"status": "ignored", "reason": "no_issue_key"}
            
        story_id = payload["issue"]["key"]
        event_type = payload.get("webhookEvent", "unknown")
        
        logger.info(f"⚡ Triggering Agent for {story_id} (Event: {event_type})")
        
        # 2. Transform Payload for LangGraph
        # LangGraph Dev Server expects standard run request
        # We wrap the Jira payload into "input" so our State schema can read it
        graph_payload = {
            "assistant_id": "agent", # Must match graph name in langgraph.json
            "input": {
                # Pass the raw payload so "issue" and "webhookEvent" are top-level in State
                "issue": payload["issue"],
                "webhookEvent": event_type,
                "jira_story_id": story_id, # Redundant but helpful
                "user": payload.get("user", {})
            },
            "config": {
                "configurable": {
                    "thread_id": story_id # Use Story ID as thread ID for persistence
                }
            }
        }
        
        logger.info(f"📤 Sending to LangGraph: {json.dumps(graph_payload, indent=2)}")
        
        # 3. Forward to LangGraph
        async with httpx.AsyncClient() as client:
            response = await client.post(TARGET_ENDPOINT, json=graph_payload, timeout=10.0)
            
            if response.status_code >= 400:
                logger.error(f"❌ LangGraph Server Error: {response.text}")
                raise HTTPException(status_code=500, detail=f"Agent Server failed: {response.text}")
                
            logger.info(f"✅ Agent Started! Run ID: {response.json().get('run_id')}")
            
        return {"status": "triggered", "story_id": story_id}
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting Jira Webhook Shim on port 8000...")
    print(f"👉 Point Ngrok here: ngrok http 8000")
    print(f"👉 Jira Webhook URL: https://<ngrok>/jira-webhook")
    uvicorn.run(app, host="0.0.0.0", port=8000)
