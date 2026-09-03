"""FollowThrough — a human-in-the-loop proposal agent for freelancers.

Uses the AWS Strands Agents SDK and Amazon Bedrock's Amazon Nova Lite model.
The workflow is deliberately explicit and reliable for a demo:
    parse inquiry -> retrieve portfolio matches -> draft with Nova ->
    propose slots -> require human approval.

Nothing is ever sent automatically.

Run:
    python -m pip install -r requirements.txt
    python agent.py sample_inquiries/01_clear.txt

Before running, configure AWS credentials for the account that has Bedrock
access in us-east-1. See README.md.
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

from strands import Agent, tool
from strands.models import BedrockModel

PORTFOLIO_PATH = Path(__file__).parent / "portfolio.json"
AWS_REGION = "us-east-1"
# Amazon-owned model: does not require the Anthropic first-time use-case form.
MODEL_ID = "amazon.nova-lite-v1:0"

SYSTEM_PROMPT = """
You are FollowThrough, an assistant that helps independent consultants and
freelancers respond to client inquiries quickly and well.

Write only the proposal email draft requested by the user. Be warm,
professional, concise, and specific. Address the inquiry directly, only cite
past projects supplied in the context, never invent a price or a capability,
and do not claim to send an email. End by saying that three possible call
times are provided separately for the human reviewer.

If the inquiry is vague, write a short reply that asks the minimum necessary
clarifying questions rather than guessing the client intent.
"""


@tool
def parse_inquiry(text: str) -> dict:
    """Extract deterministic signals from a raw client inquiry."""
    lower = text.lower()
    budget_match = re.search(r"\$[\d,]+(?:\s*-\s*\$?[\d,]+)?", text)
    budget_signal = budget_match.group(0) if budget_match else "not stated"

    if any(word in lower for word in ["urgent", "asap", "this week", "immediately", "right away"]):
        urgency = "high"
    elif any(word in lower for word in ["soon", "few weeks", "this month"]):
        urgency = "medium"
    else:
        urgency = "low/unspecified"

    tz_match = re.search(
        r"\b(eastern|pacific|central|mountain|utc|gmt|est|pst|cst|mst)\b", lower
    )
    timezone_hint = tz_match.group(0).upper() if tz_match else "not stated"

    return {
        "need": text.strip(),
        "budget_signal": budget_signal,
        "urgency": urgency,
        "timezone_hint": timezone_hint,
    }


@tool
def search_portfolio(query: str) -> list[dict]:
    """Return up to two genuinely relevant portfolio records by keyword overlap."""
    if not PORTFOLIO_PATH.exists():
        return []

    projects = json.loads(PORTFOLIO_PATH.read_text(encoding="utf-8"))
    query_words = set(re.findall(r"[a-z0-9]+", query.lower()))
    scored: list[tuple[int, dict]] = []

    for project in projects:
        title = project.get("title", "")
        summary = project.get("summary", "")
        tags = project.get("tags", [])
        all_words = set(re.findall(r"[a-z0-9]+", " ".join([title, summary, *tags]).lower()))
        tag_words = set(re.findall(r"[a-z0-9]+", " ".join(tags).lower()))
        score = len(query_words & all_words) + 2 * len(query_words & tag_words)
        if score:
            scored.append((score, project))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [project for _, project in scored[:2]]


@tool
def check_calendar(days_ahead: int = 7) -> list[str]:
    """Return three demo-stable available call slots.

    This is intentionally mocked so the recorded demo never depends on an
    OAuth session. It can be replaced with Google Calendar freebusy later.
    """
    today = datetime.now()
    offsets_and_hours = [(1, 10), (2, 14), (4, 15)]
    return [
        (today + timedelta(days=offset)).strftime(f"%A, %b %d at {hour}:00")
        for offset, hour in offsets_and_hours
    ][:3]


@tool
def request_approval(draft: str, slots: list[str]) -> dict:
    """Human approval gate. The workflow stops here and never sends email."""
    print("\n" + "=" * 72)
    print("DRAFT PROPOSAL — HUMAN APPROVAL REQUIRED")
    print("=" * 72)
    print(draft)
    print("\nSuggested intro-call times:")
    for number, slot in enumerate(slots, start=1):
        print(f"  {number}. {slot}")
    print("=" * 72)

    decision = input("Approve this draft? [approve/revise]: ").strip().lower()
    if decision.startswith("a"):
        return {"status": "approved"}
    return {"status": "revise", "feedback": input("What should change? ").strip()}


def build_agent() -> Agent:
    """Create a Strands Agent backed by Amazon Nova Lite on Bedrock."""
    model = BedrockModel(
        model_id=MODEL_ID,
        region_name=AWS_REGION,
        temperature=0.3,
    )
    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        # Registered tools make the available capabilities explicit in the
        # Strands agent; the demo workflow below invokes them deterministically.
        tools=[parse_inquiry, search_portfolio, check_calendar, request_approval],
    )


def draft_with_nova(agent: Agent, inquiry: dict, matches: list[dict], revision: str = "") -> str:
    """Ask Nova for the proposal text grounded only in the prepared context."""
    matches_text = "\n".join(
        f"- {match['title']}: {match['summary']}" for match in matches
    ) or "No relevant past-project match was found. Do not fabricate one."

    prompt = f"""Create the proposal email draft for this inquiry.

RAW INQUIRY:
{inquiry['need']}

EXTRACTED SIGNALS:
- Budget: {inquiry['budget_signal']}
- Urgency: {inquiry['urgency']}
- Timezone hint: {inquiry['timezone_hint']}

RELEVANT PAST PROJECTS:
{matches_text}

{('REVISION REQUEST: ' + revision) if revision else ''}

Return only the email draft, with no preamble and no invented facts."""
    return str(agent(prompt))


def run_on_file(path: str) -> None:
    """Run the complete proposal workflow against a sample inquiry file."""
    inquiry_text = Path(path).read_text(encoding="utf-8")
    print(f"\n>>> New inquiry loaded: {path}")

    # Explicit multi-tool orchestration keeps the demo repeatable.
    inquiry = parse_inquiry(inquiry_text)
    matches = search_portfolio(inquiry_text)
    slots = check_calendar()
    print(f">>> Parsed urgency: {inquiry['urgency']} | budget: {inquiry['budget_signal']}")
    print(">>> Portfolio matches: " + (", ".join(match["title"] for match in matches) or "none"))
    print(">>> Asking Amazon Nova to draft the proposal...")

    agent = build_agent()
    revision = ""
    while True:
        draft = draft_with_nova(agent, inquiry, matches, revision)
        approval = request_approval(draft, slots)
        if approval["status"] == "approved":
            print("\n>>> Approved. FollowThrough has prepared the final draft; it has NOT sent anything.")
            break
        revision = approval["feedback"]
        print("\n>>> Revising only the requested parts...\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python agent.py <path-to-inquiry.txt>")
        raise SystemExit(1)
    run_on_file(sys.argv[1])
