"""
Example 06: Professional Email Generator
========================================
Generate professional emails for different scenarios.

This example shows:
- Context-aware email generation
- Tone and formality control
- Different email types (cold outreach, follow-up, etc.)
- Personalization

Sample output:
---------------
Subject: Partnership Opportunity with Acme Corp

Dear Sarah,

I hope this email finds you well. I'm reaching out to explore...

[Professional, well-structured email follows]
"""

import os
from anthropic import Anthropic

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Please set ANTHROPIC_API_KEY environment variable")

client = Anthropic(api_key=api_key)

# Example 1: Cold outreach email
print("=== Example 1: Cold Outreach Email ===\n")

email_context = {
    "recipient_name": "Sarah Johnson",
    "recipient_company": "TechCorp",
    "sender_name": "Alex Chen",
    "sender_company": "Acme Solutions",
    "purpose": "propose a partnership for AI integration",
    "value_proposition": "our AI platform has helped 50+ companies reduce costs by 30%"
}

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0.7,
    system="""You are a professional email writer. Generate emails that are:
- Professional but warm
- Concise and scannable
- Include a clear call-to-action
- Personalized based on context provided
- Include both subject line and body""",
    messages=[
        {
            "role": "user",
            "content": f"""Write a cold outreach email with these details:

Recipient: {email_context['recipient_name']} at {email_context['recipient_company']}
Sender: {email_context['sender_name']} at {email_context['sender_company']}
Purpose: {email_context['purpose']}
Value: {email_context['value_proposition']}

Keep it under 150 words."""
        }
    ]
)

print(message.content[0].text)

# Example 2: Follow-up email
print("\n\n=== Example 2: Follow-up Email ===\n")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0.7,
    system="""You are a professional email writer. Generate emails that are:
- Polite and non-pushy
- Reference previous conversation
- Provide value, not just "checking in"
- Include a specific next step""",
    messages=[
        {
            "role": "user",
            "content": """Write a follow-up email to a prospect I met at a conference last week.

Context:
- Met Sarah at TechConf 2024
- Discussed their need for better data analytics
- She seemed interested but wanted to think about it
- It's been 5 days since the conversation
- I want to share a relevant case study and schedule a demo

Keep it friendly and under 100 words."""
        }
    ]
)

print(message.content[0].text)

# Example 3: Customer support response
print("\n\n=== Example 3: Customer Support Email ===\n")

customer_issue = """
Customer: John Smith
Issue: Product stopped working after recent update
Tone: Frustrated (mentioned in ticket: "This is unacceptable")
Resolution: Engineering team identified the bug, fix deployed, offering 1 month credit
"""

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0.6,
    system="""You are a customer support specialist. Generate emails that:
- Acknowledge the customer's frustration with empathy
- Explain what happened clearly
- Describe the solution and next steps
- Offer compensation when appropriate
- End on a positive, relationship-building note""",
    messages=[
        {
            "role": "user",
            "content": f"Write a customer support response email:\n\n{customer_issue}"
        }
    ]
)

print(message.content[0].text)

# Pro tips for email generation:
# - Adjust temperature based on formality (0.6-0.7 for business, 0.8-0.9 for creative)
# - Provide context about the relationship and previous interactions
# - Specify tone (formal, casual, empathetic, etc.)
# - Set word limits to keep emails concise
# - Ask for subject lines when needed
# - Can generate multiple variations and choose the best one
