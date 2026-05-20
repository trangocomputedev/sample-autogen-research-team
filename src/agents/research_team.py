"""Four-agent research pipeline using SelectorGroupChat."""
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from src.config import get_client
from src.tools.web_search import web_search, fetch_url
from src.tools.file_tools import save_report

_SELECTOR_PROMPT = """\
You are managing a content production pipeline with four specialists:
- Researcher: gathers information using search tools
- FactChecker: verifies claims from the research
- Writer: drafts the article from verified facts
- Editor: polishes the draft and saves the final output

Participants: {participants}

Conversation so far:
{history}

Select the most appropriate next speaker based on the pipeline stage.
Only move to the next stage when the current stage signals completion.
Reply with only the speaker's name."""


def build_research_team() -> SelectorGroupChat:
    """
    Four specialized agents collaborate to research, verify, write, and edit
    an article. A gpt-4o-mini selector decides who speaks next based on
    workflow stage. Demonstrates: SelectorGroupChat, tool use, OrTermination.
    """
    client = get_client("gpt-4o")
    selector_client = get_client("gpt-4o-mini")

    researcher = AssistantAgent(
        name="Researcher",
        model_client=client,
        tools=[web_search, fetch_url],
        system_message=(
            "You are a Senior Research Analyst. Use web_search to gather information "
            "from multiple sources, and fetch_url to get article details. "
            "Summarize findings with clear source references. "
            "End your message with 'Research complete.' when you have enough material."
        ),
    )

    fact_checker = AssistantAgent(
        name="FactChecker",
        model_client=client,
        tools=[web_search],
        system_message=(
            "You are a meticulous fact-checker. Review the researcher's findings and "
            "verify each major claim using an independent web_search. "
            "Label each claim VERIFIED, UNVERIFIED, or DISPUTED with citation. "
            "End your message with 'Fact-check complete.' when done."
        ),
    )

    writer = AssistantAgent(
        name="Writer",
        model_client=client,
        system_message=(
            "You are a Senior Content Writer. Using only the verified research, write a "
            "well-structured 500-word article with an introduction, 2-3 body sections "
            "with subheadings, and a conclusion. Format in Markdown. "
            "End your message with 'Draft complete.' when finished."
        ),
    )

    editor = AssistantAgent(
        name="Editor",
        model_client=client,
        tools=[save_report],
        system_message=(
            "You are a Content Editor. Review the draft for clarity, flow, and accuracy. "
            "Improve sentence variety and fix any passive voice. "
            "Use save_report to persist the polished final article. "
            "End your final message with DONE."
        ),
    )

    # OR-termination: stop when Editor says DONE or after 20 messages
    termination = TextMentionTermination("DONE") | MaxMessageTermination(20)

    return SelectorGroupChat(
        participants=[researcher, fact_checker, writer, editor],
        model_client=selector_client,
        termination_condition=termination,
        selector_prompt=_SELECTOR_PROMPT,
    )
