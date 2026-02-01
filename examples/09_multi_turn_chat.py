"""
Example 09: Multi-Turn Chat with Memory
=======================================
Build conversations that maintain context across multiple turns.

This example shows:
- Managing conversation history
- Context retention
- Building interactive chat interfaces
- Memory management for long conversations

Sample output:
---------------
User: What's the capital of France?
Assistant: The capital of France is Paris.

User: What's the population?
Assistant: Paris has approximately 2.2 million people...
"""

import os
from anthropic import Anthropic

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Please set ANTHROPIC_API_KEY environment variable")

client = Anthropic(api_key=api_key)

# Conversation history - stores all messages
conversation_history = []

def chat(user_message: str, system_prompt: str = None) -> str:
    """
    Send a message and get a response while maintaining conversation context.
    
    Args:
        user_message: The user's message
        system_prompt: Optional system prompt (only used on first message)
        
    Returns:
        Claude's response
    """
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # Create the API request
    params = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 2048,
        "messages": conversation_history
    }
    
    if system_prompt:
        params["system"] = system_prompt
    
    # Get response
    message = client.messages.create(**params)
    assistant_response = message.content[0].text
    
    # Add assistant response to history
    conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })
    
    return assistant_response

# Example 1: Basic multi-turn conversation
print("=== Example 1: Multi-Turn Conversation ===\n")

response = chat("What is the capital of France?")
print(f"User: What is the capital of France?")
print(f"Assistant: {response}\n")

# Claude remembers the context
response = chat("What's the population of that city?")
print(f"User: What's the population of that city?")
print(f"Assistant: {response}\n")

# Continue the conversation
response = chat("What are the top 3 tourist attractions there?")
print(f"User: What are the top 3 tourist attractions there?")
print(f"Assistant: {response}\n")

# Example 2: Clear and start a new conversation with a system prompt
print("\n=== Example 2: New Conversation with System Prompt ===\n")

conversation_history.clear()  # Reset conversation

system_prompt = """You are a helpful Python programming tutor. 
Explain concepts clearly with code examples. 
Always ask if the student has questions before moving on."""

response = chat(
    "I'm new to Python. Can you explain what a list is?",
    system_prompt=system_prompt
)
print(f"User: I'm new to Python. Can you explain what a list is?")
print(f"Assistant: {response}\n")

response = chat("How do I add items to a list?")
print(f"User: How do I add items to a list?")
print(f"Assistant: {response}\n")

# Example 3: Interactive chat loop
print("\n=== Example 3: Interactive Chat Session ===")
print("(Type 'quit' to exit, 'clear' to reset conversation)\n")

conversation_history.clear()  # Reset for interactive session

# Uncomment to run interactive mode:
"""
while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    
    if user_input.lower() == 'clear':
        conversation_history.clear()
        print("🔄 Conversation cleared.\n")
        continue
    
    if not user_input:
        continue
    
    try:
        response = chat(user_input)
        print(f"\nAssistant: {response}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
"""

print("(Interactive mode disabled in this example - uncomment code to enable)\n")

# Example 4: Conversation with memory management
print("\n=== Example 4: Managing Long Conversations ===\n")

def chat_with_memory_limit(user_message: str, max_history: int = 10) -> str:
    """
    Chat with automatic memory management.
    Keeps only the last N message pairs to avoid token limits.
    
    Args:
        user_message: The user's message
        max_history: Maximum number of messages to keep in history
        
    Returns:
        Claude's response
    """
    # Add user message
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # Trim history if too long (keep pairs of user/assistant messages)
    if len(conversation_history) > max_history:
        # Keep the system context if it exists, trim old messages
        conversation_history[:] = conversation_history[-max_history:]
    
    # Get response
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=conversation_history
    )
    
    assistant_response = message.content[0].text
    
    # Add assistant response
    conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })
    
    return assistant_response

conversation_history.clear()

print(f"Conversation size: {len(conversation_history)} messages")
response = chat_with_memory_limit("Tell me about machine learning", max_history=6)
print(f"After message 1: {len(conversation_history)} messages\n")

response = chat_with_memory_limit("What are neural networks?", max_history=6)
print(f"After message 2: {len(conversation_history)} messages\n")

response = chat_with_memory_limit("How does training work?", max_history=6)
print(f"After message 3: {len(conversation_history)} messages\n")

# After max_history is exceeded, oldest messages are removed
response = chat_with_memory_limit("What are some applications?", max_history=6)
print(f"After message 4: {len(conversation_history)} messages (trimmed to max_history)")

# Pro tips for multi-turn conversations:
# - Store conversation history in a list of message dicts
# - Each message has "role" (user/assistant) and "content"
# - System prompts can only be set at the conversation start
# - Monitor message count to avoid hitting token limits
# - Consider summarizing old messages for very long conversations
# - Save conversation history to disk for persistence
# - Can implement "forgot" commands to remove context
# - Use temperature control for consistent personalities
