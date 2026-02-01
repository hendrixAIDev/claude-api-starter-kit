# Claude API Starter Kit 🚀

A comprehensive Python starter kit for building applications with the Claude API. Get started in minutes with 10 ready-to-use examples covering everything from basic chat to advanced tool use.

## ✨ Features

- **10 Production-Ready Examples** - Copy, paste, and customize for your needs
- **Utility Library** - Reusable API client with error handling and retry logic
- **Best Practices** - Learn proper error handling, streaming, and token management
- **Well Documented** - Every example includes detailed comments and sample output
- **Modern Python** - Uses the latest Anthropic SDK with type hints
- **Zero to Hero** - Progress from simple chat to advanced function calling

## 📦 What's Included

### Examples Directory

1. **01_basic_chat.py** - Simple chat completion with Claude
2. **02_streaming_chat.py** - Real-time streaming responses
3. **03_system_prompts.py** - Control Claude's behavior and personality
4. **04_structured_output.py** - Get JSON and structured data responses
5. **05_code_review.py** - AI-powered code analysis and security audits
6. **06_email_writer.py** - Generate professional emails for any scenario
7. **07_content_summarizer.py** - Summarize articles and long-form content
8. **08_data_extractor.py** - Extract structured data from unstructured text
9. **09_multi_turn_chat.py** - Build conversational interfaces with memory
10. **10_tool_use.py** - Function calling and tool integration

### Utilities

- **ClaudeClient** - Simplified API wrapper with convenience methods
- **Error Handling** - Graceful handling of rate limits and API errors
- **Retry Logic** - Automatic retry with exponential backoff

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

4. Run any example:
```bash
cd examples
python 01_basic_chat.py
```

## 💡 Usage Examples

### Basic Chat

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "What is the capital of France?"
    }]
)

print(message.content[0].text)
```

### Using the Utility Library

```python
from utils import ClaudeClient

client = ClaudeClient()  # Uses ANTHROPIC_API_KEY from environment

# Simple chat
response = client.chat("Explain quantum computing in simple terms")
print(response)

# Streaming chat
for chunk in client.chat_stream("Write me a poem"):
    print(chunk, end="", flush=True)
```

### Structured Data Extraction

```python
import json
from utils import ClaudeClient

client = ClaudeClient()

response = client.chat(
    "Extract contact info from this email: ...",
    system="Return only valid JSON with name, email, and phone fields"
)

data = json.loads(response)
print(f"Name: {data['name']}")
print(f"Email: {data['email']}")
```

## 📚 Examples Breakdown

### Beginner Level
- **01-04**: Core fundamentals (chat, streaming, prompts, structured output)

### Intermediate Level
- **05-07**: Practical applications (code review, email writing, summarization)

### Advanced Level
- **08-10**: Complex patterns (data extraction, multi-turn chat, tool use)

## 🎯 Use Cases

This starter kit is perfect for building:

- **AI Chatbots** - Customer support, internal tools, virtual assistants
- **Content Generation** - Emails, summaries, articles, social posts
- **Code Tools** - Code review, documentation, refactoring suggestions
- **Data Processing** - Extract structured data from documents and text
- **Workflow Automation** - Integrate AI into your existing pipelines

## 🛠️ Best Practices

### Error Handling

All examples include proper error handling:

```python
from utils import handle_api_errors, retry_with_backoff

@retry_with_backoff(max_retries=3)
@handle_api_errors
def make_api_call():
    # Your code here
    pass
```

### Token Management

Monitor token usage to control costs:

```python
message = client.messages.create(...)
print(f"Input tokens: {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")
```

### Model Selection

Choose the right model for your needs:

- **Claude Sonnet 4** (default) - Best balance of intelligence and speed
- **Claude Opus** - Maximum capability for complex tasks
- **Claude Haiku** - Fastest, most cost-effective

## 📖 Documentation

### API Reference

- [Anthropic API Docs](https://docs.anthropic.com/)
- [Python SDK Reference](https://github.com/anthropics/anthropic-sdk-python)
- [Model Comparison](https://docs.anthropic.com/claude/docs/models-overview)

### Helpful Resources

- [Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Tool Use Documentation](https://docs.anthropic.com/claude/docs/tool-use)
- [Rate Limits & Billing](https://docs.anthropic.com/claude/reference/rate-limits)

## 💰 Pricing

The Claude API uses token-based pricing. Approximate costs:

- **Claude Sonnet 4**: $3 per million input tokens, $15 per million output tokens
- **Claude Opus**: $15 per million input tokens, $75 per million output tokens
- **Claude Haiku**: $0.25 per million input tokens, $1.25 per million output tokens

*Prices subject to change - check [Anthropic's pricing page](https://www.anthropic.com/pricing) for current rates*

## 🔐 Security Best Practices

- **Never commit your API key** - Use environment variables
- **Use .gitignore** - Exclude `.env` files from version control
- **Rotate keys regularly** - Generate new keys periodically
- **Monitor usage** - Set up billing alerts in the Anthropic Console
- **Validate inputs** - Sanitize user inputs before sending to the API

## 🤝 Contributing

Found a bug or have a suggestion? Feel free to:

1. Fork this repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - feel free to use this in your projects!

## 🆘 Support

- **Documentation**: See individual example files for detailed comments
- **Issues**: Open an issue on GitHub
- **Anthropic Support**: [support@anthropic.com](mailto:support@anthropic.com)

## 🎓 Learning Path

Recommended order for learning:

1. Start with `01_basic_chat.py` to understand the fundamentals
2. Move to `02_streaming_chat.py` for better UX
3. Learn `03_system_prompts.py` to control Claude's behavior
4. Master `04_structured_output.py` for data extraction
5. Explore `05-07` for practical applications
6. Tackle `08-10` for advanced patterns

## 🚢 What to Build Next

Ideas to extend this starter kit:

- **RAG System** - Add document retrieval for knowledge-based chat
- **Voice Integration** - Combine with speech-to-text/text-to-speech
- **Web Interface** - Build a Streamlit or Flask UI
- **Database Integration** - Store conversations and user data
- **Multi-Agent Systems** - Coordinate multiple Claude instances
- **API Service** - Deploy as a REST API with FastAPI

## ⭐ Show Your Support

If this starter kit helped you, please:
- Star this repository
- Share it with other developers
- Build something awesome and tag us!

---

**Built with ❤️ for the AI developer community**

*Ready to build something amazing with Claude? Start with example 01 and level up from there!*
