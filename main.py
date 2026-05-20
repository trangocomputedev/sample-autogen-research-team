"""
Entry point — runs the full four-agent research pipeline.
Usage: python main.py [topic]
"""
import asyncio
import sys
from dotenv import load_dotenv
load_dotenv()

from autogen_agentchat.ui import Console
from src.agents.research_team import build_research_team


async def main() -> None:
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "recent advances in renewable energy"
    team = build_research_team()
    stream = team.run_stream(task=f"Research and write an article about: {topic}")
    await Console(stream)


if __name__ == "__main__":
    asyncio.run(main())
