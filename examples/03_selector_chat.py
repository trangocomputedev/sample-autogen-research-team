"""
Example 3: SelectorGroupChat with Tools
----------------------------------------
Four specialized agents collaborate on a research-to-publication pipeline.
A lightweight gpt-4o-mini model acts as the selector, deciding who speaks
next based on pipeline stage. Tools give agents the ability to search the
web and save files.

Demonstrates:
  - SelectorGroupChat with a custom selector_prompt
  - Tool use (async functions as tools)
  - OR-termination: TextMentionTermination | MaxMessageTermination
  - Multiple model tiers (gpt-4o for agents, gpt-4o-mini for selector)
"""
import asyncio
from dotenv import load_dotenv
load_dotenv()

from autogen_agentchat.ui import Console
from src.agents.research_team import build_research_team


async def main() -> None:
    team = build_research_team()
    stream = team.run_stream(
        task="Research and write an article about recent advances in solid-state battery technology."
    )
    await Console(stream)


if __name__ == "__main__":
    asyncio.run(main())
