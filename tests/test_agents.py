"""Smoke tests for agent and team construction — no LLM calls made."""
import pytest
from unittest.mock import patch, MagicMock
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination


@pytest.fixture
def mock_client():
    with patch("src.config.get_client") as m:
        m.return_value = MagicMock()
        yield m


def test_critic_pair_returns_round_robin(mock_client):
    from src.agents.critic_pair import build_critic_pair
    team = build_critic_pair()
    assert isinstance(team, RoundRobinGroupChat)


def test_critic_pair_has_two_participants(mock_client):
    from src.agents.critic_pair import build_critic_pair
    team = build_critic_pair()
    assert len(team._participants) == 2


def test_critic_pair_participant_names(mock_client):
    from src.agents.critic_pair import build_critic_pair
    team = build_critic_pair()
    names = [p.name for p in team._participants]
    assert "Writer" in names
    assert "Critic" in names


def test_research_team_returns_selector_chat(mock_client):
    from src.agents.research_team import build_research_team
    team = build_research_team()
    assert isinstance(team, SelectorGroupChat)


def test_research_team_has_four_participants(mock_client):
    from src.agents.research_team import build_research_team
    team = build_research_team()
    assert len(team._participants) == 4


def test_research_team_participant_names(mock_client):
    from src.agents.research_team import build_research_team
    team = build_research_team()
    names = [p.name for p in team._participants]
    assert names == ["Researcher", "FactChecker", "Writer", "Editor"]


def test_researcher_has_tools(mock_client):
    from src.agents.research_team import build_research_team
    team = build_research_team()
    researcher = next(p for p in team._participants if p.name == "Researcher")
    assert len(researcher._tools) == 2


def test_editor_has_save_tool(mock_client):
    from src.agents.research_team import build_research_team
    team = build_research_team()
    editor = next(p for p in team._participants if p.name == "Editor")
    assert len(editor._tools) == 1
    assert "save_report" in editor._tools[0].name
