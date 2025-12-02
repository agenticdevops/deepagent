# Quick Reference Card - Gemini Deep Agent

## Setup (2 minutes)

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

## Minimal Example

```python
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from deepagents import create_deep_agent
from tavily import TavilyClient

# Setup
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

# Tool
def search(query: str):
    return tavily.search(query)

# Agent
agent = create_deep_agent(
    tools=[search],
    system_prompt="You are a research expert.",
    model=model,
)

# Run
result = agent.invoke({
    "messages": [{"role": "user", "content": "Research AI agents"}]
})

print(result["messages"][-1].content)
```

## Key Differences from Anthropic

```python
# Anthropic (Original)
from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Google (This Project) ⭐
from langchain_google_genai import ChatGoogleGenerativeAI
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
```

## Configuration

```python
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",           # Model ID
    api_key=os.environ.get("GOOGLE_API_KEY"),
    temperature=0.7,                    # 0=deterministic, 1=creative
    max_tokens=2048,                    # Output limit (optional)
    top_p=0.9,                          # Nucleus sampling (optional)
    top_k=40,                           # Top-k sampling (optional)
)
```

## Built-in Agent Tools

Every deep agent automatically has:

```
write_todos(items)      # Plan tasks
read_file(path)         # Read files
write_file(path, content)
edit_file(path, old, new)
ls(dir)                 # List directory
grep(pattern, files)    # Search text
glob(pattern)           # Find files
execute(command)        # Run shell
task(prompt)            # Subagent
```

## Custom Tools Pattern

```python
def my_tool(param: str) -> str:
    """Tool description"""
    return "result"

agent = create_deep_agent(
    tools=[my_tool, search_tool],
    system_prompt="...",
    model=model,
)
```

## Agent Invocation

```python
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Your request here"
    }]
})

# Get response
response = result["messages"][-1].content
print(response)
```

## Model Comparison

| Factor | Claude | Gemini |
|--------|--------|--------|
| Speed | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Cost | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Reasoning | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Context | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## Typical Task Flow

```
User Request
    ↓
Agent Plans (write_todos)
    ↓
Search Information (search_tool)
    ↓
Organize Data (write_file)
    ↓
Analyze & Synthesize
    ↓
Generate Report
    ↓
Output
```

## Environment Variables

```bash
# Required
export GOOGLE_API_KEY="AIzaSy..."
export TAVILY_API_KEY="tvly-..."

# Optional
export LANGSMITH_API_KEY="..."
```

## File Examples

### Simple Research
See: `gemini_quickstart.py`

### Advanced Examples
See: `advanced_examples.py`
- Comprehensive Researcher
- News Analyst
- Finance Researcher
- Comparative Analyst
- Tutorial Writer

## Running Examples

```bash
# Basic research
python gemini_quickstart.py

# Advanced examples
python advanced_examples.py research
python advanced_examples.py news
python advanced_examples.py finance
```

## Customization Checklist

- [ ] Update system prompt for your domain
- [ ] Add custom tools relevant to your task
- [ ] Adjust temperature (0=deterministic, 1=creative)
- [ ] Set max_tokens appropriate for output size
- [ ] Test with sample inputs
- [ ] Monitor costs and performance
- [ ] Deploy when ready

## Common Patterns

### Research Task
```python
prompt = """You are a researcher.
1. Plan subtopics with write_todos
2. Search each topic thoroughly
3. Save findings to files
4. Synthesize report"""
```

### Analysis Task
```python
prompt = """You are an analyst.
1. Search for relevant data
2. Organize in files
3. Perform analysis
4. Generate insights"""
```

### Tutorial Creation
```python
prompt = """You are a tutorial writer.
1. Plan structure with write_todos
2. Research best practices
3. Write detailed steps
4. Add examples and troubleshooting"""
```

## Performance Tips

1. **Use Flash model** - fastest & cheapest
2. **Limit search results** - max_results=3-5
3. **Set appropriate temperature** - 0.3-0.7 for consistency
4. **Use file tools** - offload context
5. **Monitor with LangSmith** - (optional) debug performance

## Cost Estimation

For 1000 research tasks per month:
- **Claude**: ~$45
- **Gemini 2.5 Flash**: ~$1

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API key error | Check `export GOOGLE_API_KEY="..."`|
| Module not found | Run `pip install -r requirements.txt`|
| Rate limited | Reduce queries or upgrade plan |
| Slow response | Use Flash model, reduce results |
| Large context | Use write_file to offload data |

## Useful Urls

- Google AI: https://ai.google.dev
- Tavily: https://tavily.com
- Deepagents: https://github.com/langchain-ai/deepagents
- LangChain: https://python.langchain.com
- LangGraph: https://langgraph.dev

## Files in Project

```
deepagent2/
├── gemini_quickstart.py        # ⭐ Start here!
├── advanced_examples.py         # Advanced cases
├── GEMINI_QUICKSTART.md        # Full guide
├── COMPARISON.md               # Model comparison
├── README.md                   # Project overview
├── QUICK_REFERENCE.md          # This file
├── requirements.txt            # Dependencies
└── .env.example               # API key template
```

## Next Steps

1. **Read**: GEMINI_QUICKSTART.md
2. **Setup**: Create .env file
3. **Run**: `python gemini_quickstart.py`
4. **Explore**: `advanced_examples.py`
5. **Customize**: Modify for your use case
6. **Deploy**: Use LangGraph for production

---

**TL;DR**: Install deps → Set API keys → Run `gemini_quickstart.py` → Customize
