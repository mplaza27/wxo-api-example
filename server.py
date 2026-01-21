"""
watsonx Orchestrate API Boilerplate
"""

import os
from typing import Optional
import requests
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import uvicorn

load_dotenv()

# Configuration
INSTANCE_URL = os.getenv("INSTANCE_URL")
AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("API_KEY")
IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"

# Default prompt - customize this for your use case or expand on the generate_prompt function
PROMPT=f"Hello, what can you do?"

app = FastAPI()


def generate_prompt(input: Optional[str] = None) -> str:
    """Generate the prompt for the Orchestrate agent. Modify this for your use case."""
    if input:
        prompt = f"do something with {input}"
    else:
        prompt = PROMPT
    return prompt


def get_bearer_token() -> str:
    """Authenticate with IBM Cloud IAM to get a bearer token."""
    response = requests.post(
        IAM_TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": API_KEY}
    )
    response.raise_for_status()
    return response.json().get("access_token")


def call_orchestrate_agent(prompt: str, bearer_token: str) -> str:
    """Call watsonx Orchestrate agent with the given prompt."""
    response = requests.post(
        f"{INSTANCE_URL}/v1/orchestrate/{AGENT_ID}/chat/completions",
        headers={"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"},
        json={"messages": [{"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": 1000, "stream": False}
    )
    response.raise_for_status()
    result = response.json()
    
    if "choices" in result and len(result["choices"]) > 0:
        return result["choices"][0].get("message", {}).get("content", "")
    return "No content returned."


@app.post("/call_orchestrate")
def call_orchestrate():
    """Call the watsonx Orchestrate agent."""
    if not all([INSTANCE_URL, AGENT_ID, API_KEY]):
        raise HTTPException(status_code=500, detail="Missing environment variables")
    
    try:
        prompt = generate_prompt()
        bearer_token = get_bearer_token()
        response = call_orchestrate_agent(prompt, bearer_token)
        return {"success": True, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    if not all([INSTANCE_URL, AGENT_ID, API_KEY]):
        print("ERROR: Missing required environment variables (INSTANCE_URL, AGENT_ID, API_KEY)")
        exit(1)
    
    print(f"Starting server... Instance: {INSTANCE_URL}, Agent: {AGENT_ID}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
