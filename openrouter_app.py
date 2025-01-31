import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from browser_use import Agent

# dotenv
load_dotenv()

api_key = os.getenv('OPENROUTER_API_KEY', '')
if not api_key:
    raise ValueError('OPENROUTER_API_KEY is not set')


async def run_search():
    agent = Agent(
        task=('go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result'),
        llm=ChatOpenAI(
            base_url='https://openrouter.ai/api/v1',
            model='deepseek/deepseek-r1',  # You can change this to any model available on OpenRouter
            api_key=SecretStr(api_key)
        ),
        use_vision=False,
        max_failures=2,
        max_actions_per_step=1,
    )

    await agent.run()


if __name__ == '__main__':
    asyncio.run(run_search()) 