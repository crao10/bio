"""Main agent logic for the story discovery scout."""

import json
import os
import sys

import anthropic
from dotenv import load_dotenv

from prompt import SYSTEM_PROMPT, USER_PROMPT
from mailer import format_briefing_html, send_email

load_dotenv()


def run_scout() -> list[dict]:
    """Run the story discovery agent and return parsed story candidates."""
    client = anthropic.Anthropic()

    print("Running story scout with web search...")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        tools=[{"type": "web_search_20250305"}],
        messages=[{"role": "user", "content": USER_PROMPT}],
    )

    # Extract the final text block from the response — the model may produce
    # multiple content blocks (tool_use, tool_result, text) when using web
    # search.  We need to continue the conversation until we get a text block
    # containing our JSON.
    messages = [{"role": "user", "content": USER_PROMPT}]
    while response.stop_reason == "tool_use":
        # Append assistant message with all content blocks
        messages.append({"role": "assistant", "content": response.content})

        # Build tool results for every tool_use block
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": "Search complete.",
                    }
                )
        messages.append({"role": "user", "content": tool_results})

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=[{"type": "web_search_20250305"}],
            messages=messages,
        )

    # Pull the JSON from the final text block
    text = ""
    for block in response.content:
        if hasattr(block, "text"):
            text = block.text
            break

    if not text:
        raise RuntimeError("No text response from Claude")

    # Strip markdown fencing if present
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0]
    cleaned = cleaned.strip()

    data = json.loads(cleaned)
    stories = data["stories"]

    if len(stories) != 3:
        raise ValueError(f"Expected 3 stories, got {len(stories)}")

    return stories


def main():
    """Run scout and optionally send email."""
    stories = run_scout()

    # Pretty-print to stdout
    print(json.dumps(stories, indent=2))

    # Send email if configured
    to_email = os.environ.get("TO_EMAIL")
    if to_email and os.environ.get("SENDGRID_API_KEY"):
        html = format_briefing_html(stories)
        send_email(html, to_email)
        print(f"\nBriefing sent to {to_email}")
    else:
        # Write HTML to file for preview
        html = format_briefing_html(stories)
        with open("briefing.html", "w") as f:
            f.write(html)
        print("\nNo email configured. HTML written to briefing.html")


if __name__ == "__main__":
    main()
