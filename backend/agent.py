import os
import langchain
from langchain import hub
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from tools import search_with_sources, get_weather_data
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=os.getenv("GEMINI_API_KEY"), 
    temperature=0,
)

search_tool =   Tool(
        name="google_search",
        func=search_with_sources,
        description="Search for real-time news from trusted sources only."
    )
get_weather_data = Tool(
        name="Weather",
        func=get_weather_data,
        description="Get current weather for a city."
    )

prompt = hub.pull("hwchase17/react")
tools = [search_tool, get_weather_data]

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_tool_error=True,
    handle_parsing_errors=True,
    verbose=True,
    return_intermediate_steps=True,
)

import re

def run_agent(user_input: str):
    response = agent_executor.invoke({"input": user_input})

    # Extract sources from intermediate steps
    sources = []
    for action, observation in response.get("intermediate_steps", []):
        if action.tool == "google_search":
            if "SOURCES:" in observation:
                sources_section = observation.split("SOURCES:")[-1].strip()
                sources = [s.strip() for s in sources_section.splitlines() if s.strip()]

    return {
        "output": response["output"],
        "sources": sources,
    }