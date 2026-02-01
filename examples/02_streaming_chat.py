"""
Example 02: Streaming Chat Responses
====================================
Stream Claude's response token-by-token for a better user experience.

This example shows:
- Using streaming for real-time responses
- Handling stream events
- Printing tokens as they arrive

Sample output:
---------------
Claude: Let me tell you about quantum computing...
(Text appears progressively as Claude generates it)

Benefits of streaming:
- Better UX for long responses
- Lower perceived latency
- Ability to show "typing" indicators
"""

import os
from anthropic import Anthropic

# Initialize client
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Please set ANTHROPIC_API_KEY environment variable")

client = Anthropic(api_key=api_key)

print("Claude: ", end="", flush=True)

# Stream the response
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Explain quantum computing in simple terms."
        }
    ]
) as stream:
    # Print each text chunk as it arrives
    for text in stream.text_stream:
        print(text, end="", flush=True)

print("\n")  # New line after response completes

# You can also access the final message object
final_message = stream.get_final_message()
print(f"--- Metadata ---")
print(f"Total tokens used: {final_message.usage.input_tokens + final_message.usage.output_tokens}")
print(f"Stop reason: {final_message.stop_reason}")
