"""Two-agent writer–critic pattern using RoundRobinGroupChat."""
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from src.config import get_client


def build_critic_pair() -> RoundRobinGroupChat:
    """
    A writer and a critic alternate turns. The writer revises based on
    the critic's feedback; the loop terminates when the writer says APPROVED.
    Demonstrates: AssistantAgent, RoundRobinGroupChat, TextMentionTermination.
    """
    client = get_client("gpt-4o")

    writer = AssistantAgent(
        name="Writer",
        model_client=client,
        system_message=(
            "You are a content writer. Write clear, engaging prose on the given topic. "
            "Revise based on the critic's feedback. "
            "When the critic is satisfied, end your message with the single word APPROVED."
        ),
    )

    critic = AssistantAgent(
        name="Critic",
        model_client=client,
        system_message=(
            "You are a sharp but fair editor. Give specific, actionable feedback on the writing. "
            "Focus on clarity, structure, and factual accuracy. Keep feedback to 2-3 bullet points. "
            "When the writing meets publication standards, say 'This looks great — ready to finalize.'"
        ),
    )

    termination = TextMentionTermination("APPROVED")
    return RoundRobinGroupChat(
        participants=[writer, critic],
        termination_condition=termination,
        max_turns=10,
    )
