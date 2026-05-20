"""
Example 2: Three-Agent RoundRobinGroupChat — Plan → Code → Review
------------------------------------------------------------------
Three agents take strictly ordered turns: a Planner breaks down the task,
a Coder implements it, and a Reviewer checks it. The loop ends when the
Reviewer is satisfied and says LGTM.

Demonstrates:
  - Multiple AssistantAgents with specialized system prompts
  - RoundRobinGroupChat with fixed turn order
  - TextMentionTermination + max_turns safety bound
"""
import asyncio
from dotenv import load_dotenv
load_dotenv()

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from src.config import get_client


async def main() -> None:
    client = get_client("gpt-4o")

    planner = AssistantAgent(
        name="Planner",
        model_client=client,
        system_message=(
            "You are a software architect. Break the task into a clear, numbered "
            "implementation plan. Be concise — no more than 5 steps."
        ),
    )

    coder = AssistantAgent(
        name="Coder",
        model_client=client,
        system_message=(
            "You are a Python developer. Implement the Planner's steps as clean, "
            "idiomatic Python with type hints. Output only the code block."
        ),
    )

    reviewer = AssistantAgent(
        name="Reviewer",
        model_client=client,
        system_message=(
            "You are a senior engineer doing code review. Check for bugs, missing edge cases, "
            "and style issues. If everything looks good, end your message with LGTM."
        ),
    )

    termination = TextMentionTermination("LGTM")
    team = RoundRobinGroupChat(
        participants=[planner, coder, reviewer],
        termination_condition=termination,
        max_turns=9,
    )

    stream = team.run_stream(task="Write a Python function that validates an email address using a regex.")
    await Console(stream)


if __name__ == "__main__":
    asyncio.run(main())
