# wxo-api-example

FastAPI server for calling watsonx Orchestrate agents.

## Setup

1. Create a `.env` file:
```
INSTANCE_URL=https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/your-instance-id
AGENT_ID=your-agent-id
API_KEY=your-api-key
```

2. Install dependencies:
```bash
pip install fastapi uvicorn requests python-dotenv
```

3. Run:
```bash
python server.py
```

## Customization

Modify `generate_prompt()` to change how prompts are built for your use case.
