"""
Example 08: Data Extractor
==========================
Extract structured data from unstructured text.

This example shows:
- Named entity recognition
- Data extraction patterns
- Validation and formatting
- Handling missing data

Sample output:
---------------
Extracted Information:
{
  "people": [
    {"name": "John Smith", "role": "CEO", "company": "Acme Corp"}
  ],
  "dates": ["2024-03-15", "2024-04-01"],
  "amounts": [{"value": 1000000, "currency": "USD"}]
}
"""

import os
import json
from anthropic import Anthropic

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Please set ANTHROPIC_API_KEY environment variable")

client = Anthropic(api_key=api_key)

# Example 1: Extract contact information
print("=== Example 1: Contact Information Extraction ===\n")

unstructured_text = """
Hey team,

After yesterday's meeting, here are the contacts you need:

1. John Smith is the new VP of Engineering at TechCorp. You can reach him at 
   john.smith@techcorp.com or call (555) 123-4567. His office is in Building 3.

2. Sarah Martinez, the Head of Sales, is based in our NYC office. Email her at
   s.martinez@company.com. She's available M-F, 9-5 EST.

3. For legal questions, contact Mike Chen (General Counsel). His assistant is 
   Jennifer Lee - jennifer.l@company.com, extension 1234.

Thanks!
"""

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0.2,
    system="""You are a data extraction specialist. Extract contact information and return ONLY valid JSON.

Format:
{
  "contacts": [
    {
      "name": "Full Name",
      "title": "Job Title (or null)",
      "company": "Company Name (or null)",
      "email": "email@domain.com (or null)",
      "phone": "Phone Number (or null)",
      "location": "Location (or null)"
    }
  ]
}

Include only information explicitly mentioned. Use null for missing data.""",
    messages=[
        {
            "role": "user",
            "content": f"Extract all contact information:\n\n{unstructured_text}"
        }
    ]
)

contacts_data = json.loads(message.content[0].text)
print(json.dumps(contacts_data, indent=2))

print("\n📇 Formatted Contacts:")
for contact in contacts_data['contacts']:
    print(f"\n• {contact['name']}")
    if contact.get('title'):
        print(f"  Role: {contact['title']}")
    if contact.get('email'):
        print(f"  Email: {contact['email']}")
    if contact.get('phone'):
        print(f"  Phone: {contact['phone']}")

# Example 2: Extract financial data
print("\n\n=== Example 2: Financial Data Extraction ===\n")

financial_text = """
Q3 2024 Financial Summary:

Revenue was $2.5M, up 35% YoY. Operating expenses came in at $1.8M, 
including $450K in R&D, $600K in sales & marketing, and $750K in G&A.

Net income: $700K (28% margin)
Cash on hand: $5.2M
ARR growth: 42%

Major deals closed:
- Acme Corp: $150K annual contract (3-year commitment)
- TechStart Inc: $85K annual contract
- Global Systems: $220K annual contract (enterprise tier)
"""

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0.1,  # Very low for precise number extraction
    system="""You are a financial data extraction specialist. Extract all financial metrics and return ONLY valid JSON.

Format:
{
  "period": "Q3 2024",
  "metrics": {
    "revenue": 2500000,
    "operating_expenses": 1800000,
    "net_income": 700000,
    "cash": 5200000
  },
  "growth": {
    "revenue_yoy": 35,
    "arr_growth": 42
  },
  "deals": [
    {
      "company": "Company Name",
      "amount": 150000,
      "type": "annual",
      "duration_years": 3
    }
  ]
}

All amounts in USD. Percentages as numbers (35, not 0.35).""",
    messages=[
        {
            "role": "user",
            "content": f"Extract financial data:\n\n{financial_text}"
        }
    ]
)

financial_data = json.loads(message.content[0].text)
print(json.dumps(financial_data, indent=2))

print("\n💰 Summary:")
print(f"Revenue: ${financial_data['metrics']['revenue']:,}")
print(f"Net Income: ${financial_data['metrics']['net_income']:,}")
print(f"Total Deals: ${sum(d['amount'] for d in financial_data['deals']):,}")

# Example 3: Extract events and dates
print("\n\n=== Example 3: Event Extraction ===\n")

event_text = """
Upcoming Schedule:

March 15, 2024 - Product launch webinar at 2pm EST. Sarah will present the 
new features. Register at launch.company.com

March 22-24 - TechConf 2024 in San Francisco. Our booth is #305. 
The team dinner is on March 23rd at 7pm.

April 1, 2024 - Q1 board meeting. Financial reports due March 28th.

Note: The April 10th customer advisory board meeting has been moved to April 17th.
"""

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0.2,
    system="""Extract all events with dates. Return ONLY valid JSON.

Format:
{
  "events": [
    {
      "date": "2024-03-15",
      "end_date": null,
      "title": "Event Title",
      "description": "Brief description",
      "location": "Location (or null)",
      "time": "2:00 PM EST (or null)"
    }
  ]
}

Use ISO date format (YYYY-MM-DD). Include all mentioned details.""",
    messages=[
        {
            "role": "user",
            "content": f"Extract all events:\n\n{event_text}"
        }
    ]
)

events_data = json.loads(message.content[0].text)
print(json.dumps(events_data, indent=2))

print("\n📅 Calendar Summary:")
for event in sorted(events_data['events'], key=lambda x: x['date']):
    print(f"\n{event['date']}: {event['title']}")
    if event.get('time'):
        print(f"  Time: {event['time']}")
    if event.get('location'):
        print(f"  Location: {event['location']}")

# Pro tips for data extraction:
# - Use very low temperature (0.1-0.2) for accuracy
# - Be explicit about the JSON schema you want
# - Handle null/missing values explicitly
# - Validate extracted data against expected formats
# - For large documents, consider chunking
# - Can combine with web scraping to extract from HTML/websites
# - Use regex post-processing for additional validation if needed
