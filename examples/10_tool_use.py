"""
Example 10: Function Calling / Tool Use
=======================================
Use Claude's tool use capabilities to extend its abilities with custom functions.

This example shows:
- Defining tools/functions for Claude
- Function calling workflow
- Handling tool results
- Multi-step tool usage

Sample output:
---------------
Claude wants to use: get_weather
Arguments: {"location": "San Francisco", "unit": "celsius"}

Weather: 18°C, Partly cloudy

Claude: The weather in San Francisco is currently 18°C and partly cloudy...
"""

import os
import json
from anthropic import Anthropic

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Please set ANTHROPIC_API_KEY environment variable")

client = Anthropic(api_key=api_key)

# Example 1: Simple tool use
print("=== Example 1: Weather Tool ===\n")

# Define available tools
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a location. Returns temperature and conditions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit"
                }
            },
            "required": ["location"]
        }
    }
]

# Simulated weather function (in real app, this would call an API)
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Simulated weather API - replace with real API call."""
    # In a real app, you'd call a weather API here
    mock_data = {
        "San Francisco": {"temp": 18, "condition": "Partly cloudy"},
        "New York": {"temp": 22, "condition": "Sunny"},
        "London": {"temp": 12, "condition": "Rainy"}
    }
    
    city = location.split(",")[0]
    data = mock_data.get(city, {"temp": 20, "condition": "Unknown"})
    
    if unit == "fahrenheit":
        data["temp"] = round(data["temp"] * 9/5 + 32)
        
    return {
        "location": location,
        "temperature": data["temp"],
        "unit": unit,
        "condition": data["condition"]
    }

# Initial request with tool definition
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[
        {
            "role": "user",
            "content": "What's the weather like in San Francisco?"
        }
    ]
)

print(f"Stop reason: {message.stop_reason}")

# Check if Claude wants to use a tool
if message.stop_reason == "tool_use":
    # Extract the tool use request
    tool_use = next(block for block in message.content if block.type == "tool_use")
    tool_name = tool_use.name
    tool_input = tool_use.input
    
    print(f"Claude wants to use: {tool_name}")
    print(f"Arguments: {json.dumps(tool_input, indent=2)}\n")
    
    # Execute the function
    if tool_name == "get_weather":
        result = get_weather(**tool_input)
        print(f"Weather: {result['temperature']}°{result['unit'][0].upper()}, {result['condition']}\n")
        
        # Send the result back to Claude
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=tools,
            messages=[
                {
                    "role": "user",
                    "content": "What's the weather like in San Francisco?"
                },
                {
                    "role": "assistant",
                    "content": message.content
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": json.dumps(result)
                        }
                    ]
                }
            ]
        )
        
        print(f"Claude: {response.content[0].text}")

# Example 2: Multiple tools
print("\n\n=== Example 2: Calculator Tools ===\n")

calculator_tools = [
    {
        "name": "add",
        "description": "Add two numbers together",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "multiply",
        "description": "Multiply two numbers",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            "required": ["a", "b"]
        }
    }
]

def add(a: float, b: float) -> float:
    return a + b

def multiply(a: float, b: float) -> float:
    return a * b

# Function registry
function_map = {
    "add": add,
    "multiply": multiply
}

def process_tool_call(user_query: str, tools: list, function_map: dict) -> str:
    """
    Process a user query that may require tool calls.
    
    Args:
        user_query: The user's question
        tools: List of available tools
        function_map: Dict mapping tool names to functions
        
    Returns:
        Claude's final response
    """
    messages = [{"role": "user", "content": user_query}]
    
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        if response.stop_reason == "tool_use":
            # Add assistant's response to messages
            messages.append({"role": "assistant", "content": response.content})
            
            # Process all tool calls
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    
                    print(f"🔧 Using tool: {tool_name}({tool_input})")
                    
                    # Execute the function
                    func = function_map[tool_name]
                    result = func(**tool_input)
                    
                    print(f"   Result: {result}\n")
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result)
                    })
            
            # Add tool results to messages
            messages.append({"role": "user", "content": tool_results})
            
        else:
            # No more tool calls, return final response
            return response.content[0].text

# Test the calculator
result = process_tool_call(
    "If I have 15 apples and I buy 7 more, then multiply that by 3, how many do I have?",
    calculator_tools,
    function_map
)

print(f"Claude: {result}")

# Example 3: Database query tool
print("\n\n=== Example 3: Database Query Tool ===\n")

database_tools = [
    {
        "name": "query_customers",
        "description": "Query customer database. Returns customer information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID to look up"
                }
            },
            "required": ["customer_id"]
        }
    }
]

def query_customers(customer_id: str) -> dict:
    """Simulated database query."""
    mock_db = {
        "C001": {"name": "John Smith", "email": "john@example.com", "plan": "Premium"},
        "C002": {"name": "Sarah Johnson", "email": "sarah@example.com", "plan": "Basic"},
        "C003": {"name": "Mike Chen", "email": "mike@example.com", "plan": "Enterprise"}
    }
    return mock_db.get(customer_id, {"error": "Customer not found"})

result = process_tool_call(
    "What is the email address for customer C001?",
    database_tools,
    {"query_customers": query_customers}
)

print(f"Claude: {result}")

# Pro tips for tool use:
# - Define clear, specific tool descriptions
# - Use JSON schema to validate inputs
# - Handle tool errors gracefully
# - Claude can chain multiple tool calls
# - Can mix tool use with regular conversation
# - Use tools for: API calls, database queries, calculations, file operations
# - Return structured data from tools (JSON preferred)
# - Consider rate limits when tools call external APIs
