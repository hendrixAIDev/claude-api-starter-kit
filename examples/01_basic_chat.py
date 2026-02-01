"""
Example 01: Basic Chat Completion
==================================
The simplest way to send a message to Claude and get a response.

This example shows:
- Loading API key from environment
- Creating a basic chat request
- Getting a complete response

Sample output:
---------------
User: What is the capital of France?
Claude: The capital of France is Paris. It has been the capital since...
"""

import os
from anthropic import Anthropic

# Load API key from environment variable
# Make sure to set ANTHROPIC_API_KEY in your .env file
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Please set ANTHROPIC_API_KEY environment variable")

# Initialize the client
client = Anthropic(api_key=api_key)

# Send a message and get a response
message = client.messages.create(
    model="claude-sonnet-4-20250514",  # Latest Claude Sonnet model
    max_tokens=1024,                    # Maximum tokens in response
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ]
)

# Extract and print the response
response_text = message.content[0].text
print(f"Claude: {response_text}")

# The response object also contains useful metadata:
print(f"\n--- Metadata ---")
print(f"Model: {message.model}")
print(f"Input tokens: {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")
print(f"Stop reason: {message.stop_reason}")
