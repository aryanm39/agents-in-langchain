from fastapi import FastAPI, Depends, HTTPException, status
from schemas import AgentRequest, AgentResponse
from agent import run_agent

app = FastAPI()

@app.post("/agent", response_model=AgentResponse)
async def call_agent(request: AgentRequest):
    try:
        result = run_agent(request.query)
        return AgentResponse(response=result["output"], sources=result["sources"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))