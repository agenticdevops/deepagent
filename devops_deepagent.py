import re
from typing import List, Dict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage


# 1) Configure Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    max_output_tokens=4096,
)

# 2) System prompt for planning phase (plan + TODOs + sub-agents + FS)
PLANNING_PROMPT = """
You are a senior DevOps engineer and CI/CD architect.

Your ONLY job in this phase is to produce a clear internal plan
for how you would answer the user's question.

IMPORTANT:
- Do NOT answer the question itself.
- Do NOT design the full CI/CD pipeline yet.
- Just output a step-by-step plan for your reasoning and execution.
- Imagine you are a "deep agent" that:
  - creates TODO lists,
  - delegates work to different internal roles,
  - and writes intermediate notes into files.
  But here, you ONLY DESCRIBE these things as text for visualization.

Output format (follow this structure exactly):

## Reasoning Plan
- Step 1: ...
- Step 2: ...
- Step 3: ...
- etc.

## Reasoning Plan Table
Represent the same steps as a Markdown table:

| Step | Description | Owner (Role)       | Status |
| ---  | ----------- | ------------------ | ------ |
| 1    | ...         | main-agent         | todo   |
| 2    | ...         | requirements-analyst | todo |
| 3    | ...         | pipeline-architect | todo   |

Guidelines:
- Use 4–8 steps.
- Owner names can be:
  - main-agent
  - requirements-analyst
  - pipeline-architect
  - risk-reviewer
- Status should be "todo" for all rows in this planning phase.

## TODO List
Represent your tasks as a Markdown table with these columns:

| ID | Task | Owner (Role)           | Depends On | Status | Notes |
| --- | --- | ---------------------- | ---------- | ------ | ----- |
| T1  | ... | main-agent or sub-role | -          | todo   | ...  |
| T2  | ... | requirements-analyst   | T1         | todo   | ...  |

Guidelines:
- Use 4–8 TODO items.
- Use Owner names like:
  - main-agent
  - requirements-analyst
  - pipeline-architect
  - risk-reviewer
- Set Status initially to "todo" for all items.



## Sub-Agent Plan
Explain in 3–6 bullet points:
- Which TODOs you would conceptually delegate to which roles
  (requirements-analyst, pipeline-architect, risk-reviewer).
- What each role is responsible for.

## Filesystem Plan
Explain in 3–6 bullet points:
- What intermediate artifacts you would create as files, e.g.:
  - /notes/requirements.md
  - /design/pipeline_design.md
  - /notes/risk_review.md
- What you would store in each file.
- You are only describing this; you are NOT actually writing files.
"""

# 3) System prompt for answer phase (ONLY the sections, no TODO table)
ANSWER_PROMPT = """
You are a senior DevOps engineer and CI/CD architect.

You will receive:
- The user's original question.
- A "Reasoning Plan" and TODO list that you created earlier.
- A conceptual sub-agent plan and filesystem plan.

Your job:
- Follow that plan.
- Think carefully at each step.
- Produce a structured, clear CI/CD design.

The host application will render the TODO Progress table itself,
so you do NOT need to print it again.

Output format (ONLY these sections):

## Context
- Short restatement of the team & problem.

## Key Factors
- Bulleted list of constraints, risks, and goals.

## Option 1
- Description
- Pros
- Cons

## Option 2
- Description
- Pros
- Cons

## Recommendation
- Which option you recommend and why.

## Next 2–4 Weeks Plan
- 4–7 concrete action items the team can execute.

IMPORTANT:
- Do NOT mention tools, APIs, or function-calls.
- Do NOT say "filesystem" or "deep agent" in the user-facing sections.
- Do NOT print any TODO table; the host will show TODO progress separately.
"""


# ---------- Helpers ----------

def get_text_from_llm(messages) -> str:
    """Call Gemini and normalize content to plain text."""
    resp = llm.invoke(messages)
    content = resp.content
    if isinstance(content, str):
        return content
    parts = []
    for ch in content:
        if isinstance(ch, dict) and "text" in ch:
            parts.append(ch["text"])
        else:
            parts.append(str(ch))
    return "\n".join(parts)


def extract_todo_table_block(text: str) -> str:
    """
    Extract the Markdown table under '## TODO List' from the planning output.
    Returns the raw table string (header + rows).
    """
    # Find the TODO List section
    m = re.search(r"## TODO List(.*?)(## |\Z)", text, flags=re.DOTALL)
    if not m:
        return ""

    section = m.group(1)

    # Find the table lines (lines starting with '|')
    lines = section.strip().splitlines()
    table_lines = [line for line in lines if line.strip().startswith("|")]

    return "\n".join(table_lines)


def parse_todo_table(table_md: str) -> List[Dict[str, str]]:
    """
    Parse a simple Markdown table into a list of dicts.
    Assumes first row is header, second row is separator, rest are data.
    """
    rows = [line.strip() for line in table_md.splitlines() if line.strip()]
    if len(rows) < 3:
        return []

    header_cells = [c.strip() for c in rows[0].strip("|").split("|")]
    data_rows = rows[2:]  # skip header and separator

    todos: List[Dict[str, str]] = []
    for row in data_rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) != len(header_cells):
            continue
        item = {header_cells[i]: cells[i] for i in range(len(header_cells))}
        todos.append(item)
    return todos


def render_todo_table(todos: List[Dict[str, str]], status_override: str = None) -> str:
    """
    Render a TODO table as Markdown.
    If status_override is given, all Status cells are set to that value.
    """
    if not todos:
        return "*(No TODOs found)*"

    headers = list(todos[0].keys())
    header_row = "| " + " | ".join(headers) + " |"
    sep_row = "| " + " | ".join("---" for _ in headers) + " |"

    data_lines = []
    for todo in todos:
        row_cells = []
        for h in headers:
            if h.lower() == "status" and status_override is not None:
                row_cells.append(status_override)
            else:
                row_cells.append(todo.get(h, ""))
        data_lines.append("| " + " | ".join(row_cells) + " |")

    return "\n".join([header_row, sep_row, *data_lines])


if __name__ == "__main__":
    user_question = """
We are a 10-person SaaS team running ~20 microservices on EKS (AWS).
Most services are Node.js and Python, each in separate GitHub repos.
We currently build Docker images manually on laptops and deploy via `kubectl apply`.

Design a CI/CD approach for us that:
- Uses GitHub as the source of truth.
- Builds and pushes Docker images to a registry.
- Deploys to staging and production on EKS.
- Includes basic automated tests and some safety checks.
- Stays realistic for a small team.

Compare at least:
- A simple, single-pipeline-per-service approach.
- A more standardized, shared workflow approach.
"""

    # ============ PHASE 1: PLANNING + TODOs ============
    planning_messages = [
        SystemMessage(content=PLANNING_PROMPT),
        HumanMessage(content=user_question),
    ]
    reasoning_plan = get_text_from_llm(planning_messages)

    print("\n=== PHASE 1: REASONING PLAN + TODOs ===\n")
    print(reasoning_plan)
    print("\n=== END PLAN ===\n")

    # Extract TODO table and parse it
    raw_todo_table = extract_todo_table_block(reasoning_plan)
    todos = parse_todo_table(raw_todo_table)

    # Compute TODO Progress table (all marked as done)
    todo_progress_table = render_todo_table(todos, status_override="done")

    # ============ PHASE 2: FINAL ANSWER ============
    combined_prompt = f"""
User question:
{user_question}

Reasoning Plan and TODOs from Phase 1:
{reasoning_plan}
"""

    answer_messages = [
        SystemMessage(content=ANSWER_PROMPT),
        HumanMessage(content=combined_prompt),
    ]
    final_answer = get_text_from_llm(answer_messages)

    # Print Phase 2 with TODO Progress + sections
    print("\n=== PHASE 2: FINAL ANSWER (WITH TODO PROGRESS) ===\n")

    print("## TODO Progress\n")
    print(todo_progress_table)
    print("\n")
    print(final_answer)

    print("\n=== END ANSWER ===")
