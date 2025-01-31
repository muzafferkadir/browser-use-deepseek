from langchain_openai import ChatOpenAI
from browser_use import Agent
from pydantic import SecretStr
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    # Initialize the model
    llm = ChatOpenAI(
        base_url='https://api.deepseek.com/v1',
        model='deepseek-reasoner',
        api_key=SecretStr(api_key)
    )

    # Create agent with the model
    agent = Agent(
        task="Go to Reddit, search for 'browser-use' in the search bar, click on the first post and return the first comment.",
        llm=llm,
        use_vision=False
    )

    # Run the agent
    result = await agent.run()
    print(result)

if __name__ == "__main__":
    asyncio.run(main()) 