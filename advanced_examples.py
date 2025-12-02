#!/usr/bin/env python3
"""
Advanced Deep Agent Examples with Gemini 2.5 Flash

This file contains advanced examples of deep agents:
1. Multi-step research with file management
2. News analysis agent with topic filtering
3. Finance research agent
4. Custom tool integration
5. Subagent delegation patterns
"""

import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Initialize model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GOOGLE_API_KEY"),
    temperature=0.7,
)

# Initialize Tavily client
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))


# ============================================================================
# Example 1: Multi-topic Research Agent
# ============================================================================

def create_comprehensive_researcher():
    """Create a deep agent that can research multiple topics simultaneously."""

    def internet_search(
        query: str,
        max_results: int = 5,
        topic: Literal["general", "news", "finance"] = "general",
        include_raw_content: bool = False,
    ) -> dict:
        """Run a web search with flexible parameters"""
        return tavily_client.search(
            query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic,
        )

    research_prompt = """You are an expert multi-disciplinary researcher powered by Gemini 2.5 Flash.

Your task is to conduct thorough research on multiple topics and compile findings.

## Available Tools:
- internet_search: Search across general, news, or finance topics
- write_todos: Plan your research approach
- read_file/write_file: Manage research data
- task: Delegate to subagents for parallel research

## Research Strategy:
1. Break down the request into subtopics using write_todos
2. Research each topic thoroughly with 5-10 search results
3. Organize findings by topic in separate files
4. Synthesize into a comprehensive report with citations

## Output Format:
Provide a well-structured report with:
- Executive Summary
- Topic-by-topic findings
- Cross-topic insights
- Recommendations based on research
"""

    agent = create_deep_agent(
        tools=[internet_search],
        system_prompt=research_prompt,
        model=model,
    )

    return agent


# ============================================================================
# Example 2: News Analysis Agent
# ============================================================================

def create_news_analyst():
    """Create a deep agent specialized in analyzing current news."""

    def news_search(
        query: str,
        max_results: int = 10,
    ) -> dict:
        """Specialized search for current news"""
        return tavily_client.search(
            query,
            max_results=max_results,
            topic="news",
            include_raw_content=True,
        )

    news_prompt = """You are a professional news analyst powered by Gemini 2.5 Flash.

Your expertise: Analyzing current news, identifying trends, and providing insights.

## Tools Available:
- news_search: Get the latest news on any topic
- write_file/read_file: Store and organize articles
- write_todos: Plan analysis workflow

## Analysis Process:
1. Search for recent news on the given topic
2. Read and analyze multiple sources
3. Identify key themes and patterns
4. Assess impact and implications
5. Provide forward-looking insights

## Output Style:
- Professional journalism standards
- Clear headline-style formatting
- Attribution to sources
- Balanced, objective analysis
- Key takeaways section
"""

    agent = create_deep_agent(
        tools=[news_search],
        system_prompt=news_prompt,
        model=model,
    )

    return agent


# ============================================================================
# Example 3: Finance Research Agent
# ============================================================================

def create_finance_researcher():
    """Create a deep agent for financial research and analysis."""

    def finance_search(
        query: str,
        max_results: int = 10,
    ) -> dict:
        """Specialized financial search"""
        return tavily_client.search(
            query,
            max_results=max_results,
            topic="finance",
            include_raw_content=True,
        )

    def calculate_metrics(metric_type: str, values: list) -> dict:
        """Calculate financial metrics"""
        if metric_type == "average":
            return {"result": sum(values) / len(values) if values else 0}
        elif metric_type == "growth":
            if len(values) >= 2:
                return {"result": ((values[-1] - values[0]) / values[0]) * 100}
        return {"result": None}

    finance_prompt = """You are a professional financial analyst powered by Gemini 2.5 Flash.

Your expertise: Financial analysis, market research, investment insights.

## Tools Available:
- finance_search: Search financial news and data
- calculate_metrics: Perform financial calculations
- write_file/read_file: Manage financial data
- write_todos: Plan analysis workflow

## Analysis Framework:
1. Gather financial data and recent news
2. Analyze company/market fundamentals
3. Review recent performance trends
4. Calculate key financial metrics
5. Provide investment perspective

## Report Structure:
- Company/Market Overview
- Financial Performance Analysis
- Risk Assessment
- Market Opportunities
- Investment Recommendation
- Data Sources & Disclaimers

IMPORTANT: Always include appropriate financial disclaimers.
"""

    agent = create_deep_agent(
        tools=[finance_search, calculate_metrics],
        system_prompt=finance_prompt,
        model=model,
    )

    return agent


# ============================================================================
# Example 4: Custom Tool Integration
# ============================================================================

def create_specialized_agent_with_custom_tools():
    """Create an agent with specialized custom tools."""

    def internet_search(query: str, max_results: int = 5) -> dict:
        return tavily_client.search(query, max_results=max_results)

    def url_fetcher(url: str) -> str:
        """Fetch and process content from a specific URL"""
        try:
            import httpx
            response = httpx.get(url, follow_redirects=True, timeout=10)
            return response.text[:2000]  # Return first 2000 chars
        except Exception as e:
            return f"Error fetching URL: {str(e)}"

    def text_summarizer(text: str, max_length: int = 100) -> str:
        """Summarize text to specified length"""
        sentences = text.split(".")
        summary = ""
        for sentence in sentences:
            if len(summary) < max_length:
                summary += sentence + ". "
            else:
                break
        return summary

    custom_prompt = """You are an advanced research agent with specialized tools.

## Available Tools:
- internet_search: Search the web
- url_fetcher: Get content from specific URLs
- text_summarizer: Condense long text
- write_file/read_file: Manage data
- write_todos: Plan research

## Research Methodology:
1. Use internet_search to find relevant sources
2. Fetch full content from promising URLs
3. Summarize key findings
4. Organize in files
5. Synthesize comprehensive report
"""

    agent = create_deep_agent(
        tools=[internet_search, url_fetcher, text_summarizer],
        system_prompt=custom_prompt,
        model=model,
    )

    return agent


# ============================================================================
# Example 5: Comparative Analysis Agent
# ============================================================================

def create_comparative_analyst():
    """Create an agent specialized in comparing different entities."""

    def internet_search(query: str, max_results: int = 5) -> dict:
        return tavily_client.search(query, max_results=max_results)

    comparative_prompt = """You are a comparative analysis expert powered by Gemini 2.5 Flash.

Your specialty: In-depth comparison of companies, products, technologies, etc.

## Comparison Framework:
1. Search for each entity being compared
2. Gather information on key dimensions
3. Create detailed comparison matrix
4. Highlight advantages/disadvantages
5. Provide recommendation or conclusion

## Key Dimensions to Compare:
- Features and capabilities
- Performance metrics
- Cost/Value proposition
- User experience
- Market position
- Pros and cons

## Output Format:
- Comparison table
- Detailed analysis per dimension
- Summary matrix
- Recommendation
- Supporting data

## Tips:
- Be comprehensive and fair
- Use objective criteria
- Source all claims
- Highlight trade-offs
"""

    agent = create_deep_agent(
        tools=[internet_search],
        system_prompt=comparative_prompt,
        model=model,
    )

    return agent


# ============================================================================
# Example 6: Tutorial/Guide Creator Agent
# ============================================================================

def create_tutorial_writer():
    """Create an agent that writes detailed tutorials and guides."""

    def internet_search(query: str, max_results: int = 5) -> dict:
        return tavily_client.search(query, max_results=max_results)

    tutorial_prompt = """You are an expert tutorial and guide writer powered by Gemini 2.5 Flash.

Your specialty: Creating clear, comprehensive tutorials and step-by-step guides.

## Tutorial Structure:
1. Overview/Introduction
2. Prerequisites and setup
3. Step-by-step instructions
4. Code examples (if applicable)
5. Troubleshooting section
6. Next steps/advanced topics
7. Resources and references

## Writing Guidelines:
- Use clear, accessible language
- Number steps clearly
- Provide code examples with syntax highlighting
- Include screenshots/diagrams when relevant
- Add troubleshooting common issues
- Link to related resources

## Tools Available:
- internet_search: Find latest tutorials and best practices
- write_file: Save guide content
- write_todos: Organize tutorial structure

## Process:
1. Research current best practices
2. Plan tutorial structure with write_todos
3. Write each section with examples
4. Save to files
5. Create comprehensive guide
"""

    agent = create_deep_agent(
        tools=[internet_search],
        system_prompt=tutorial_prompt,
        model=model,
    )

    return agent


# ============================================================================
# Example 7: Demo Functions
# ============================================================================

def demo_comprehensive_research():
    """Demo: Run comprehensive research on multiple topics."""
    agent = create_comprehensive_researcher()

    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": "Research the current state of AI agents, including their applications, limitations, and future trends."
        }]
    })

    print("=" * 80)
    print("COMPREHENSIVE RESEARCH RESULTS")
    print("=" * 80)
    print(result["messages"][-1].content)
    print()


def demo_news_analysis():
    """Demo: Analyze current news."""
    agent = create_news_analyst()

    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": "Analyze recent developments in artificial intelligence and their implications for the tech industry."
        }]
    })

    print("=" * 80)
    print("NEWS ANALYSIS RESULTS")
    print("=" * 80)
    print(result["messages"][-1].content)
    print()


def demo_finance_research():
    """Demo: Analyze financial information."""
    agent = create_finance_researcher()

    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": "Research the AI/ML sector trends and identify promising investment opportunities."
        }]
    })

    print("=" * 80)
    print("FINANCE RESEARCH RESULTS")
    print("=" * 80)
    print(result["messages"][-1].content)
    print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        example = sys.argv[1]

        if example == "research":
            demo_comprehensive_research()
        elif example == "news":
            demo_news_analysis()
        elif example == "finance":
            demo_finance_research()
        else:
            print("Usage: python advanced_examples.py [research|news|finance]")
    else:
        print("Available examples:")
        print("  python advanced_examples.py research   - Run comprehensive research")
        print("  python advanced_examples.py news       - Run news analysis")
        print("  python advanced_examples.py finance    - Run finance research")
