# Deep Agent Quickstart with Gemini 2.5 Flash

A comprehensive guide and working example for building deep agents using Google's Gemini 2.5 Flash model with the deepagents framework.

## Overview

This project demonstrates how to build intelligent research agents that can:
- Plan complex tasks using built-in planning tools
- Search the internet for information
- Manage file systems to handle large datasets
- Delegate subtasks to specialized subagents
- Synthesize research into polished reports

All powered by Google's fast and cost-efficient **Gemini 2.5 Flash** model.

## Quick Start


### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Or with uv:
```bash
uv add -r requirements.txt
```

### 2. Set Up API Keys
Create a `.env` file from the template:
```bash
cp .env.example .env
```

Then add your API keys:
- **GOOGLE_API_KEY**: Get from [Google AI Studio](https://aistudio.google.com/apikey)
- **TAVILY_API_KEY**: Get from [Tavily](https://tavily.com)

### 3. Run the Agent
```bash
python gemini_quickstart.py
```

## Files in This Project

| File | Purpose |
|------|---------|
| `GEMINI_QUICKSTART.md` | Comprehensive guide to using Gemini with deep agents |
| `gemini_quickstart.py` | Ready-to-run example script |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for environment variables |
| `README.md` | This file |

## What Makes This Different From Anthropic?

### Model Integration
```python
# Anthropic (Claude)
from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Google (Gemini) - This project
from langchain_google_genai import ChatGoogleGenerativeAI
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
```

### Key Benefits of Gemini 2.5 Flash
- ⚡ **Speed**: Optimized for fast inference
- 💰 **Cost**: More economical pricing
- 📊 **Context**: 1 million token window
- 🎯 **Quality**: Excellent performance-to-latency ratio

## Agent Architecture

```
┌─────────────────────────────────────────────┐
│      User Query (Research Task)             │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│  Gemini 2.5 Flash Deep Agent                │
│  ┌────────────────────────────────────────┐ │
│  │  System Prompt (Research Expert)       │ │
│  └────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────┘
               │
        ┌──────┼──────┬──────────┬──────────┐
        ▼      ▼      ▼          ▼          ▼
    ┌─────┐ ┌──────┐ ┌────────┐ ┌──────┐ ┌─────┐
    │Plan │ │Search│ │Organize│ │Write │ │Report│
    │Work │ │Web   │ │Files   │ │File  │ │Synth │
    │Todos│ │      │ │        │ │      │ │      │
    └─────┘ └──────┘ └────────┘ └──────┘ └─────┘
        │      │        │         │        │
        └──────┼────────┼─────────┼────────┘
               │        │         │
               ▼        ▼         ▼
        ┌──────────────────────────────┐
        │  Built-in Tools              │
        │  • write_todos               │
        │  • internet_search           │
        │  • read_file/write_file      │
        │  • grep/glob                 │
        │  • execute                   │
        │  • task (subagents)          │
        └──────────────────────────────┘
               │
               ▼
        ┌──────────────────────────────┐
        │  Final Report                │
        │  • Structured findings       │
        │  • Citations                 │
        │  • Analysis & conclusions    │
        └──────────────────────────────┘
```

## Example Usage

### Basic Research Agent
```python
from gemini_quickstart import agent

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "What are the latest developments in AI agents?"
    }]
})

print(result["messages"][-1].content)
```

### Research with Specific Parameters
```python
# Research with more search results
system_prompt = """You are an expert researcher...
Use up to 10 search results per query for comprehensive coverage."""

agent = create_deep_agent(
    tools=[internet_search],
    system_prompt=system_prompt,
    model=model,
)
```

## Common Tasks

### Change the Search Topic
Modify the `internet_search` call in your agent's instructions:
```python
# For finance-specific research
topic = "finance"

# For current news
topic = "news"

# For general topics
topic = "general"
```

### Add More Tools
Extend the agent with additional tools:
```python
def calculator(expression: str) -> float:
    """Evaluate mathematical expressions"""
    return eval(expression)

agent = create_deep_agent(
    tools=[internet_search, calculator],
    system_prompt=research_instructions,
    model=model,
)
```

### Create Specialized Subagents
Delegate specific tasks to specialized agents:
```python
# Define system prompts for specialized agents
data_analyst_prompt = "You are an expert data analyst..."
summarizer_prompt = "You are an expert at summarizing content..."

# Agents will automatically handle delegation
```

## Troubleshooting

### Issue: "GOOGLE_API_KEY not found"
**Solution**: Make sure you've set the environment variable:
```bash
export GOOGLE_API_KEY="your-key-here"
```

Or use a `.env` file with `python-dotenv`:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Issue: Rate limiting errors
**Solution**: Reduce request frequency or add delays:
```python
import time
time.sleep(1)  # 1 second delay between searches
```

### Issue: Large search results causing context issues
**Solution**: Use the built-in `write_file` tool to save results:
```python
# Agent automatically manages this with FilesystemMiddleware
# No additional configuration needed
```

## Performance Tips

1. **Use Flash model**: It's faster and cheaper than Pro/Ultra models
2. **Limit search results**: Set `max_results=3-5` for focused searches
3. **Cache API keys**: Set environment variables once, reuse across sessions
4. **Enable LangSmith**: Monitor agent behavior and optimize
5. **Use file management**: Let the agent offload context to files

## Resources

- **Deepagents**: https://github.com/langchain-ai/deepagents
- **Google Gemini API**: https://ai.google.dev
- **Tavily Search**: https://tavily.com
- **LangChain**: https://python.langchain.com
- **LangGraph**: https://langgraph.dev

## License

This project is provided as an educational example.

## Support

For issues with:
- **Deep agents**: Check [deepagents docs](https://github.com/langchain-ai/deepagents)
- **Gemini API**: Visit [Google AI Support](https://support.google.com/ai/)
- **Tavily**: Contact [Tavily Support](https://tavily.com/support)
