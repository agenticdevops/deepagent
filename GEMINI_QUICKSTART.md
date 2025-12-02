# Deep Agent Quickstart with Gemini 2.5 Flash

> Build your first deep agent using Google's Gemini 2.5 Flash model in minutes

This guide walks you through creating your first deep agent with planning, file system tools, and subagent capabilities using Google's Gemini 2.5 Flash model instead of Anthropic Claude. You'll build a research agent that can conduct research and write reports.

## Prerequisites

Before you begin, make sure you have:

1. A **Google AI API key** from [Google AI Studio](https://aistudio.google.com/apikey)
2. A **Tavily API key** for web search capabilities from [Tavily](https://tavily.com)
3. Python 3.8 or higher installed
4. Basic familiarity with Python

## Step 1: Install Dependencies

Install the required packages using your preferred package manager:

### Using pip
```bash
pip install deepagents tavily-python langchain-google-genai
```

### Using uv
```bash
uv add deepagents tavily-python langchain-google-genai
```

### Using poetry
```bash
poetry add deepagents tavily-python langchain-google-genai
```

## Step 2: Set Up Your API Keys

Set up your environment variables with your API keys:

```bash
export GOOGLE_API_KEY="your-google-api-key"
export TAVILY_API_KEY="your-tavily-api-key"
```

Or create a `.env` file in your project directory:

```
GOOGLE_API_KEY=your-google-api-key
TAVILY_API_KEY=your-tavily-api-key
```

Then load it in your Python script:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Step 3: Initialize the Gemini Model

```python
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize Google Gemini 2.5 Flash model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GOOGLE_API_KEY"),
    temperature=0.7,  # Controls randomness in responses (0.0 to 1.0)
)
```

### Key Gemini Model Parameters

- **model**: The model identifier (`gemini-2.5-flash` or `gemini-2.0-flash`)
- **temperature**: Controls randomness (0.0 = deterministic, 1.0 = very random)
- **api_key**: Your Google AI API key
- **max_tokens**: Maximum output length (optional)
- **top_p**: Nucleus sampling parameter (optional)
- **top_k**: Top-k sampling parameter (optional)

## Step 4: Create a Search Tool

```python
from typing import Literal
from tavily import TavilyClient

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )
```

## Step 5: Create a Deep Agent with Gemini 2.5 Flash

```python
from deepagents import create_deep_agent

# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher powered by Google's Gemini 2.5 Flash model.
Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return,
the topic, and whether raw content should be included.

Use the built-in tools strategically:
- `write_todos`: Break down complex tasks into steps
- `write_file`/`read_file`: Manage large amounts of research data
- `task`: Delegate sub-tasks to specialized subagents when needed
"""

agent = create_deep_agent(
    tools=[internet_search],
    system_prompt=research_instructions,
    model=model,  # Pass the Gemini model instance
)
```

## Step 6: Run the Agent

```python
# Invoke the agent with a research query
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "What is LangGraph and how is it used in AI applications?"
    }]
})

# Print the agent's response
print(result["messages"][-1].content)
```

## What Happened?

Your deep agent with Gemini 2.5 Flash automatically:

1. **Planned its approach**: Used the built-in `write_todos` tool to break down the research task into manageable steps
2. **Conducted research**: Called the `internet_search` tool to gather information from the web
3. **Managed context**: Used file system tools (`write_file`, `read_file`) to offload large search results and organize data
4. **Spawned subagents** (if needed): Delegated complex subtasks to specialized subagents for parallel processing
5. **Synthesized a report**: Compiled findings into a coherent, well-structured response

## Key Differences from Anthropic Version

| Aspect | Anthropic (Claude) | Google (Gemini) |
|--------|-------------------|-----------------|
| **Model Import** | `langchain-anthropic` | `langchain-google-genai` |
| **Class** | `ChatAnthropic` | `ChatGoogleGenerativeAI` |
| **Model ID** | `claude-3-5-sonnet-20241022` | `gemini-2.5-flash` |
| **API Key Var** | `ANTHROPIC_API_KEY` | `GOOGLE_API_KEY` |
| **Cost** | Higher (more capable models) | Lower (more cost-efficient) |
| **Speed** | Balanced | Very fast (Flash model) |
| **Context Window** | 200k tokens | 1 million tokens (Gemini 2.0) |

## Gemini 2.5 Flash Advantages

- **Speed**: Optimized for fast inference
- **Cost**: More economical than larger models
- **Efficiency**: Excellent quality-to-speed ratio
- **Large Context**: 1 million token context window
- **Multimodal**: Can handle images, audio, and video (with extended integration)

## Full Example Script

Here's a complete, ready-to-run example:

```python
#!/usr/bin/env python3
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize clients
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GOOGLE_API_KEY"),
    temperature=0.7,
)

# Define tools
def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

# System prompt
research_instructions = """You are an expert researcher. Your job is to conduct thorough research
and then write a polished report. You have access to an internet search tool."""

# Create agent
agent = create_deep_agent(
    tools=[internet_search],
    system_prompt=research_instructions,
    model=model,
)

# Run agent
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "What is LangGraph?"
    }]
})

print(result["messages"][-1].content)
```

## Next Steps

Now that you've built your first deep agent with Gemini 2.5 Flash:

- **Customize your agent**: Modify the system prompt and add more specialized tools for your use case
- **Add more tools**: Integrate additional APIs beyond Tavily (database tools, calculation tools, etc.)
- **Create subagents**: Delegate complex tasks to specialized sub-agents for better organization
- **Use middleware**: Explore the middleware architecture for features like human-in-the-loop, prompt caching, and conversation summarization
- **Add long-term memory**: Enable persistent memory across conversations for multi-session research
- **Deploy to production**: Learn about deployment options for LangGraph applications

## Troubleshooting

### API Key Not Found
```
KeyError: 'GOOGLE_API_KEY'
```
Make sure you've exported your Google API key:
```bash
export GOOGLE_API_KEY="your-key-here"
```

### Rate Limiting
If you hit rate limits on Tavily or Gemini API, consider:
- Reducing `max_results` in search calls
- Adding delays between requests
- Upgrading your API plan

### Model Not Found
```
ValueError: Unsupported model: gemini-2.5-flash
```
Make sure you're using a valid Gemini model ID. Available models:
- `gemini-2.5-flash` (recommended)
- `gemini-2.0-flash`
- `gemini-1.5-pro`
- `gemini-1.5-flash`

## Resources

- **Deepagents Documentation**: [deepagents.readthedocs.io](https://deepagents.readthedocs.io)
- **Google Gemini API**: [ai.google.dev](https://ai.google.dev)
- **Tavily Search API**: [tavily.com](https://tavily.com)
- **LangChain Google Integration**: [python.langchain.com/docs/integrations/llms/google_generative_ai](https://python.langchain.com/docs/integrations/llms/google_generative_ai)
