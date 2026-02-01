"""
Example 05: AI Code Reviewer
============================
Use Claude to review code and provide suggestions.

This example shows:
- Code analysis and review
- Security vulnerability detection
- Best practice recommendations
- Actionable improvement suggestions

Sample output:
---------------
🔍 Code Review for example.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ STRENGTHS:
- Good error handling with try/except
- Clear function naming

⚠️  ISSUES FOUND:
1. [SECURITY] SQL injection vulnerability on line 12
2. [PERFORMANCE] Inefficient loop on line 25
3. [STYLE] Missing docstrings

💡 SUGGESTIONS:
- Use parameterized queries for database access
- Consider using list comprehension instead of loop
- Add type hints for better code clarity
"""

import os
from anthropic import Anthropic

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Please set ANTHROPIC_API_KEY environment variable")

client = Anthropic(api_key=api_key)

# Code to review (intentionally has issues for demonstration)
code_to_review = """
def get_user_data(user_id):
    import sqlite3
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Vulnerable to SQL injection!
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
    result = cursor.fetchall()
    conn.close()
    return result

def process_items(items):
    results = []
    # Inefficient loop
    for item in items:
        if item > 0:
            results.append(item * 2)
    return results
"""

print("🔍 Code Review Session")
print("=" * 50)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2048,
    temperature=0.3,  # Lower temperature for more consistent technical analysis
    system="""You are an expert code reviewer with deep knowledge of security, performance, and best practices.

Review code and provide:
1. A brief summary of what the code does
2. Security vulnerabilities (mark as [SECURITY])
3. Performance issues (mark as [PERFORMANCE])
4. Code quality issues (mark as [STYLE])
5. Specific, actionable suggestions for improvement

Format your review clearly with sections and bullet points.""",
    messages=[
        {
            "role": "user",
            "content": f"Please review this Python code:\n\n```python\n{code_to_review}\n```"
        }
    ]
)

print(message.content[0].text)

# Example 2: Get a specific security audit
print("\n\n🔒 Security-Focused Review")
print("=" * 50)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0.2,
    system="""You are a security auditor. Focus exclusively on security vulnerabilities.
For each issue found, provide:
- Severity level (Critical/High/Medium/Low)
- Description of the vulnerability
- Concrete code example showing the fix""",
    messages=[
        {
            "role": "user",
            "content": f"Security audit this code:\n\n```python\n{code_to_review}\n```"
        }
    ]
)

print(message.content[0].text)

# Pro tips for code review:
# - Use temperature 0.2-0.3 for more consistent technical analysis
# - Be specific about what aspects to focus on (security, performance, style)
# - Provide context about the codebase or framework when relevant
# - Ask for specific code examples in the suggestions
# - Can also ask for refactored versions of the code
