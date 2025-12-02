#!/usr/bin/env python3
"""
Deep Agent Quickstart with Gemini 2.5 Flash

This script demonstrates building your first deep agent using Google Gemini 2.5 Flash.
The agent conducts research and writes reports using planning, file system tools, and subagent capabilities.
"""

import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent
from langchain_google_genai import ChatGoogleGenerativeAI


# ============================================================================
# Step 1: Initialize API Clients
# ============================================================================

# Initialize Tavily client for web search
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

# Initialize Google Gemini 2.5 Flash model
# Make sure you have GOOGLE_API_KEY set in your environment
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GOOGLE_API_KEY"),
    temperature=0.7,  # Controls randomness in responses
)


# ============================================================================
# Step 2: Define Custom Tools
# ============================================================================

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
) -> dict:
    """
    Run a web search using Tavily API.

    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 5)
        topic: Search topic category - "general", "news", or "finance" (default: "general")
        include_raw_content: Whether to include raw HTML content (default: False)

    Returns:
        Dictionary containing search results with titles, URLs, and content snippets
    """
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


# ============================================================================
# Step 3: Create System Prompt for the Agent
# ============================================================================

research_instructions = """You are an expert researcher powered by Google's Gemini 2.5 Flash model.
Your job is to conduct thorough research and then write a polished, well-structured report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify:
- max_results: The maximum number of results to return
- topic: The search topic ("general", "news", or "finance")
- include_raw_content: Whether to include raw content

## How to work effectively:

1. **Plan your research**: Use the built-in `write_todos` tool to break down complex research tasks
2. **Gather information**: Use `internet_search` to find relevant sources and information
3. **Manage context**: Use file system tools (`write_file`, `read_file`) to store and organize large amounts of research data
4. **Synthesize findings**: Compile your research into a coherent, well-organized report
5. **Be thorough**: Don't settle for surface-level answers - dig deeper to understand the topic fully

## Report Format:

When writing your final report, structure it as follows:
- **Title**: Clear, descriptive title
- **Executive Summary**: 2-3 sentence overview of key findings
- **Key Findings**: Main discoveries organized by theme or importance
- **Details**: In-depth information about each finding
- **Conclusion**: Summary of insights and implications
- **Sources**: List of sources consulted

Remember: You have access to built-in tools for planning (write_todos), file management (write_file, read_file),
and task delegation (task). Use these strategically to organize your work and produce high-quality reports."""


# ============================================================================
# Step 4: Create the Deep Agent
# ============================================================================

agent = create_deep_agent(
    tools=[internet_search],
    system_prompt=research_instructions,
    model=model,
)


# ============================================================================
# Step 5: Run the Agent
# ============================================================================

def main():
    """Main function to run the deep agent."""

    print("=" * 80)
    print("Deep Agent Quickstart with Gemini 2.5 Flash")
    print("=" * 80)
    print()

    # Example research query
    query = "Which are the top 3 Agentic Frameworks?"

    print(f"Researching: {query}")
    print("-" * 80)
    print()

    # Invoke the agent
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": query
        }]
    })

    # Extract and print the agent's response
    response = result["messages"][-1].content
    print("Agent's Research Report:")
    print("-" * 80)
    print(response)
    print()
    print("=" * 80)
    print("Research complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
