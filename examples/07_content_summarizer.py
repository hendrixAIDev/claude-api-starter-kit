"""
Example 07: Content Summarizer
==============================
Summarize articles, documents, and web content.

This example shows:
- Text summarization
- Key points extraction
- Different summary lengths
- Summary formatting options

Sample output:
---------------
📝 SUMMARY
A new study shows that regular exercise improves cognitive function...

🔑 KEY POINTS
• 30 minutes of daily exercise recommended
• Benefits visible within 6 weeks
• Applicable to all age groups

💡 TAKEAWAY
Start with just 15 minutes daily and gradually increase.
"""

import os
from anthropic import Anthropic

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Please set ANTHROPIC_API_KEY environment variable")

client = Anthropic(api_key=api_key)

# Sample article to summarize
long_article = """
The Impact of Artificial Intelligence on Modern Healthcare

Artificial intelligence (AI) is revolutionizing healthcare in ways that were unimaginable just a decade ago. From diagnostic tools to personalized treatment plans, AI is enhancing the capabilities of healthcare professionals and improving patient outcomes across the globe.

One of the most significant applications of AI in healthcare is in medical imaging. Machine learning algorithms can now analyze X-rays, MRIs, and CT scans with accuracy that rivals or even surpasses human radiologists. A recent study published in Nature Medicine found that AI systems could detect breast cancer in mammograms with 94.5% accuracy, compared to 88% for human radiologists. This technology is particularly valuable in areas with a shortage of medical specialists.

AI is also transforming drug discovery and development. Traditional drug development can take 10-15 years and cost billions of dollars. AI algorithms can analyze vast databases of molecular structures and predict which compounds are most likely to be effective against specific diseases. This has already led to faster identification of potential treatments for conditions ranging from cancer to rare genetic disorders.

Personalized medicine is another area where AI is making substantial contributions. By analyzing a patient's genetic information, lifestyle factors, and medical history, AI systems can help doctors create tailored treatment plans that are more effective and have fewer side effects than one-size-fits-all approaches.

However, the integration of AI in healthcare also raises important questions about data privacy, algorithmic bias, and the changing role of healthcare professionals. As these technologies become more prevalent, it's crucial that we address these challenges to ensure AI serves all patients equitably.

Despite these challenges, the future of AI in healthcare looks promising. Experts predict that AI will become an indispensable tool for healthcare providers, helping them make better decisions, reduce errors, and ultimately save more lives.
"""

# Example 1: Standard summary
print("=== Example 1: Standard Summary ===\n")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0.3,
    system="""You are a professional summarizer. Create clear, accurate summaries that:
- Capture the main points
- Maintain the original tone
- Are concise but complete
- Use simple, accessible language""",
    messages=[
        {
            "role": "user",
            "content": f"Summarize this article in 3-4 sentences:\n\n{long_article}"
        }
    ]
)

print(message.content[0].text)

# Example 2: Structured summary with key points
print("\n\n=== Example 2: Structured Summary ===\n")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0.3,
    system="""You are a professional summarizer. Create structured summaries with:
1. A one-paragraph summary (2-3 sentences)
2. Key points as bullet points
3. One practical takeaway

Use clear formatting with headers.""",
    messages=[
        {
            "role": "user",
            "content": f"Create a structured summary of this article:\n\n{long_article}"
        }
    ]
)

print(message.content[0].text)

# Example 3: Executive summary (very brief)
print("\n\n=== Example 3: Executive Summary ===\n")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=512,
    temperature=0.3,
    system="""You are a professional summarizer for busy executives. Create ultra-concise summaries:
- Maximum 2 sentences
- Focus on the single most important point
- Use clear, decisive language""",
    messages=[
        {
            "role": "user",
            "content": f"Create an executive summary:\n\n{long_article}"
        }
    ]
)

print(message.content[0].text)

# Example 4: Summary for specific audience
print("\n\n=== Example 4: Summary for Non-Technical Audience ===\n")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0.4,
    system="""You are a science communicator who explains complex topics to general audiences.
Create summaries that:
- Avoid jargon and technical terms
- Use analogies and examples
- Are engaging and easy to understand
- Highlight why it matters to everyday people""",
    messages=[
        {
            "role": "user",
            "content": f"Explain this article to someone with no technical background:\n\n{long_article}"
        }
    ]
)

print(message.content[0].text)

# Pro tips for content summarization:
# - Use temperature 0.3-0.4 for factual accuracy
# - Specify the desired length (sentences, words, paragraphs)
# - Tailor the summary to the audience (executives, technical, general)
# - Can ask for specific formats (bullet points, paragraphs, tables)
# - For very long content, consider chunking and summarizing sections
# - Can extract specific information (dates, names, numbers) separately
