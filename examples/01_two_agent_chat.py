"""
Example 1: Two-Agent Chat (RoundRobinGroupChat)
------------------------------------------------
The simplest AutoGen pattern: a Writer and a Critic alternate turns.
The Writer revises based on feedback; the loop ends when it says APPROVED.

Demonstrates:
  - AssistantAgent
  - RoundRobinGroupChat
  - TextMentionTermination
  - Console streaming output
"""
import asyncio
from dotenv import load_dotenv
load_dotenv()

from autogen_agentchat.ui import Console
from src.agents.critic_pair import build_critic_pair


async def main() -> None:
    team = build_critic_pair()
    stream = team.run_stream(
        task="Write a 3-sentence elevator pitch for a meditation app targeting busy professionals."
    )
    await Console(stream)


if __name__ == "__main__":
    asyncio.run(main())
