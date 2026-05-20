# Sample AutoGen Research Team

A multi-agent research and content pipeline built with [AutoGen v0.4](https://github.com/microsoft/autogen) (`autogen-agentchat`). Three progressively complex examples demonstrate the core AutoGen patterns. Serves as a canonical example and test fixture for the AI Workflow Visualizer.

## Examples

### Example 1 — Two-Agent Chat (`RoundRobinGroupChat`)

```
[Writer] ◀──▶ [Critic]
```

A writer and critic alternate turns. The writer revises based on feedback; the loop ends when the writer says `APPROVED`.

### Example 2 — Three-Agent Pipeline (`RoundRobinGroupChat`)

```
[Planner] ──▶ [Coder] ──▶ [Reviewer]
```

Agents take strictly ordered turns: the Planner produces a spec, the Coder implements it, and the Reviewer checks it. Ends when the Reviewer says `LGTM`.

### Example 3 — Research Pipeline (`SelectorGroupChat` + Tools)

```
                  [Selector LLM]
                 /    |    |    \
        [Researcher] [FactChecker] [Writer] [Editor]
             │              │                  │
        (web_search,    (web_search)       (save_report)
         fetch_url)
```

Four specialized agents collaborate on a full research-to-publication workflow. A lightweight `gpt-4o-mini` selector decides who speaks next based on pipeline stage. Ends when the Editor saves the final article and says `DONE`.

## Features Demonstrated

| AutoGen Feature | Location |
|---|---|
| `AssistantAgent(name, model_client, system_message)` | `src/agents/`, `examples/02_round_robin.py` |
| `RoundRobinGroupChat` | `src/agents/critic_pair.py`, `examples/02_round_robin.py` |
| `SelectorGroupChat` with custom `selector_prompt` | `src/agents/research_team.py` |
| `TextMentionTermination` | `src/agents/critic_pair.py`, `research_team.py` |
| `MaxMessageTermination` | `src/agents/research_team.py` |
| OR-termination (`condition1 \| condition2`) | `src/agents/research_team.py` |
| Async Python functions as tools | `src/tools/` |
| Multiple model tiers (`gpt-4o` + `gpt-4o-mini`) | `src/agents/research_team.py` |
| `Console` streaming output | All examples + `main.py` |
| `team.run_stream(task=...)` | All examples + `main.py` |

## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set credentials
cp .env.example .env
# Fill in OPENAI_API_KEY

# 3. Run the full research pipeline
python main.py "the future of nuclear fusion energy"

# Or run individual examples
python examples/01_two_agent_chat.py
python examples/02_round_robin.py
python examples/03_selector_chat.py
```

Output articles are saved to `outputs/` as Markdown files.

## Tests

```bash
pytest tests/ -v
```

Tool tests are pure async unit tests with no LLM calls. Agent tests mock the LLM client and verify team topology.

## Project Structure

```
src/
├── config.py              # OpenAIChatCompletionClient factory
├── agents/
│   ├── critic_pair.py     # Two-agent writer–critic (RoundRobinGroupChat)
│   └── research_team.py   # Four-agent research pipeline (SelectorGroupChat)
└── tools/
    ├── web_search.py      # web_search, fetch_url (stub — swap in Tavily)
    └── file_tools.py      # save_report, read_report
examples/
├── 01_two_agent_chat.py   # Simplest pattern
├── 02_round_robin.py      # Fixed-order multi-agent
└── 03_selector_chat.py    # Dynamic orchestration + tools
outputs/                   # Generated articles (gitignored)
main.py                    # Entry point
```

## Swapping In Real Tools

Both tool modules are stubs designed to be replaced:

- **`web_search`** → Use [`TavilyClient`](https://docs.tavily.com) or `langchain_community.tools.TavilySearchResults`
- **`fetch_url`** → Use `httpx` + `BeautifulSoup` for real HTML extraction

No other code needs to change — the agent and team configuration stays the same.
