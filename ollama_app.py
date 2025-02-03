import os

# Optional: Disable telemetry
# os.environ["ANONYMIZED_TELEMETRY"] = "false"

# Optional: Set the OLLAMA host to a remote server
# os.environ["OLLAMA_HOST"] = "http://x.x.x.x:11434"

import asyncio
from browser_use import Agent
from browser_use.agent.views import AgentHistoryList
from langchain_ollama import ChatOllama


async def run_search() -> AgentHistoryList:
    agent = Agent(
        task="Search for the cheapest flight from Samsun to Ankara on 4 February on Google",
        llm=ChatOllama(
            model="qwen2.5:7b",
            num_ctx=32000,
        ),
        retry_delay=3,
        max_failures=5,
    )

    result = await agent.run()
    return result


async def main():
    result = await run_search()
    print("\n\n", result)


if __name__ == "__main__":
    asyncio.run(main()) 