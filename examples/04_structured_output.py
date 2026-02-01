"""
Example 04: Getting Structured JSON Responses
=============================================
Extract structured data from Claude's responses for programmatic use.

This example shows:
- Prompting for JSON output
- Parsing JSON responses
- Error handling for malformed JSON
- Using structured data in your application

Sample output:
---------------
{
  "summary": "Paris is the capital of France...",
  "key_facts": ["Population: 2.2M", "Founded: 3rd century BC"],
  "sentiment": "positive"
}
"""

import os
import json
from anthropic import Anthropic

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Please set ANTHROPIC_API_KEY environment variable")

client = Anthropic(api_key=api_key)

# Example 1: Extract structured data from text
print("=== Example 1: Extract Structured Data ===\n")

text_to_analyze = """
The new iPhone 15 Pro was released yesterday. It features a titanium design,
USB-C charging, and an improved A17 Pro chip. The starting price is $999.
Early reviews are overwhelmingly positive, praising the camera quality.
"""

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="""You are a data extraction assistant. Always respond with valid JSON only, no additional text.
Extract information in this exact format:
{
  "product": "product name",
  "price": numeric_value,
  "key_features": ["feature1", "feature2"],
  "sentiment": "positive/negative/neutral"
}""",
    messages=[
        {
            "role": "user",
            "content": f"Extract structured data from this text:\n\n{text_to_analyze}"
        }
    ]
)

# Parse the JSON response
try:
    structured_data = json.loads(message.content[0].text)
    print("Extracted data:")
    print(json.dumps(structured_data, indent=2))
    
    # Use the structured data programmatically
    print(f"\n✓ Product: {structured_data['product']}")
    print(f"✓ Price: ${structured_data['price']}")
    print(f"✓ Features: {', '.join(structured_data['key_features'])}")
    print(f"✓ Sentiment: {structured_data['sentiment']}")
    
except json.JSONDecodeError as e:
    print(f"❌ Failed to parse JSON: {e}")
    print(f"Raw response: {message.content[0].text}")


# Example 2: Generate structured data for multiple items
print("\n\n=== Example 2: Batch Data Extraction ===\n")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2048,
    system="""You are a data extraction assistant. Always respond with valid JSON only.
Return an array of objects with this structure:
[
  {
    "name": "person name",
    "role": "their role",
    "email": "email if mentioned, else null"
  }
]""",
    messages=[
        {
            "role": "user",
            "content": """Extract contact information:
            
John Smith is the CEO of Acme Corp. You can reach him at john@acme.com.
Sarah Johnson serves as the CTO and handles technical partnerships.
Mike Chen is the Head of Sales."""
        }
    ]
)

try:
    contacts = json.loads(message.content[0].text)
    print("Extracted contacts:")
    print(json.dumps(contacts, indent=2))
    
    # Use in your application
    for contact in contacts:
        print(f"\n📧 {contact['name']} ({contact['role']})")
        if contact.get('email'):
            print(f"   Email: {contact['email']}")
            
except json.JSONDecodeError as e:
    print(f"❌ Failed to parse JSON: {e}")

# Pro tips for structured output:
# 1. Be explicit about the JSON format in the system prompt
# 2. Request "valid JSON only, no additional text"
# 3. Always handle JSON parsing errors
# 4. Use temperature=0 for more consistent formatting
# 5. Validate the structure matches your expectations
