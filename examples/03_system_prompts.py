"""
Example 03: Using System Prompts Effectively
============================================
System prompts set the context, role, and behavior for Claude.

This example shows:
- Setting a system prompt to define Claude's role
- Using system prompts to control output format
- Different system prompt strategies

Sample output:
---------------
Pirate Claude: Ahoy there, matey! Ye be askin' about the seven seas...
Professional Claude: Thank you for your inquiry. The world's oceans include...
"""

import os
from anthropic import Anthropic

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Please set ANTHROPIC_API_KEY environment variable")

client = Anthropic(api_key=api_key)

# Example 1: Role-playing system prompt
print("=== Example 1: Pirate Assistant ===\n")
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a helpful assistant who speaks like a pirate. Use pirate slang and expressions in all your responses.",
    messages=[
        {
            "role": "user",
            "content": "Tell me about the ocean."
        }
    ]
)
print(f"Pirate Claude: {message.content[0].text}\n")

# Example 2: Professional tone
print("\n=== Example 2: Professional Assistant ===\n")
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a professional business consultant. Provide concise, formal responses with clear structure.",
    messages=[
        {
            "role": "user",
            "content": "Tell me about the ocean."
        }
    ]
)
print(f"Professional Claude: {message.content[0].text}\n")

# Example 3: Output format control
print("\n=== Example 3: Controlled Output Format ===\n")
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="""You are an expert summarizer. For every response:
1. Start with a one-sentence summary
2. Follow with 3-5 key points as bullet points
3. End with a practical takeaway
Keep responses concise and actionable.""",
    messages=[
        {
            "role": "user",
            "content": "Explain machine learning."
        }
    ]
)
print(f"Structured Claude: {message.content[0].text}\n")

# Pro tip: System prompts are great for:
# - Setting expertise level (expert vs. beginner-friendly)
# - Controlling verbosity (concise vs. detailed)
# - Defining output format (markdown, JSON, bullet points)
# - Establishing personality or brand voice
# - Adding task-specific instructions that apply to all messages
