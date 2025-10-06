# ACME Intelligence Slack Bot 🤖

A simple, production-ready Slack bot that connects your team to Snowflake Cortex Agents.

## Quick Start

```python
from simple_bot import ask

# That's it. Just ask.
print(ask("How many customers do we have?"))
# → "Based on our financial metrics data, we currently have 14 customers..."
```

## Why Simple?

This bot leverages **Snowflake's Intelligence layers** to handle all complexity:
- ✅ One API call to Snowflake Cortex Agents
- ✅ Snowflake's orchestration picks the right semantic models
- ✅ Automatic tool selection (Cortex Analyst, Cortex Search)
- ✅ ~150 lines of actual code
- ✅ Easy to understand and extend

## Architecture

```
User Question → Snowflake Cortex Agent API → Streaming Response → Slack

Snowflake Agent Handles:
  • Question analysis
  • Semantic model selection (Operational/Financial/Contracts)
  • Tool orchestration (Cortex Analyst, Cortex Search)
  • SQL generation
  • Query execution
  • Response formatting

Our Bot Handles:
  • API authentication
  • Streaming response parsing
  • Slack message formatting
```

**Simple by design** - Snowflake's intelligence layers do the heavy lifting.

## Project Structure

```
slack_bot/
├── README.md                  # This file
├── simple_bot.py              # Main bot code (~600 lines)
├── quick_start.ipynb          # Interactive testing notebook
├── requirements.txt           # Python dependencies
├── slack_app_manifest.yml     # Slack app configuration
├── test_bot.py                # Health check script
└── testing_ground/            # API research and testing
```

## Setup

### 1. Install Dependencies

```bash
conda activate your_env
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Set these in your environment or .zshrc
export SNOWFLAKE_ACCOUNT="your-account"
export SNOWFLAKE_PAT="your-personal-access-token"
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export SLACK_APP_TOKEN="xapp-your-app-token"
```

### 3. Create Slack App (One-Time)

1. Go to https://api.slack.com/apps
2. Click **"Create New App"** → **"From an app manifest"**
3. Choose your workspace
4. Select **YAML** format
5. Paste contents of `slack_app_manifest.yml`
6. Click **"Create"**
7. Get your tokens from the app settings

### 4. Test Before Running

```bash
python test_bot.py  # Health check
```

### 5. Run the Bot

```bash
python simple_bot.py
```

## Usage

### Interactive Testing (Recommended to start)

```bash
jupyter notebook quick_start.ipynb
```

Test questions interactively and see real responses from your Snowflake agents.

### Python Module

```python
from simple_bot import ask

# Business intelligence
answer = ask("What's our revenue this quarter?")

# Contract analysis
answer = ask("Which contracts need attention?") 

# Performance analysis
answer = ask("Show me slow queries from today")
```

### Slack Bot (Production)

```bash
export SNOWFLAKE_ACCOUNT="your-account"
export SNOWFLAKE_PAT="your-pat-token"
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_APP_TOKEN="xapp-..."

python simple_bot.py
```

## Testing

### Test Core Functionality

```bash
cd testing_ground

# Test with real agent
export SNOWFLAKE_PAT="your-token"
python test_with_pat.py
```

This calls your real Snowflake Cortex Agent and captures the streaming response.

## Design Philosophy

### Single Agent Approach

This bot uses **one primary agent** (`ACME_INTELLIGENCE_AGENT`) for all questions. The agent automatically:

- Selects from multiple semantic models (Operational, Financial, Contracts)
- Chooses the right tool (Cortex Analyst for SQL, Cortex Search for documents)
- Generates and executes queries
- Formats executive-ready responses

**Result:** Snowflake's orchestration layer handles the intelligence, we just call the API.

### Tested Capabilities

```python
ask("What is our total revenue?")        # → "$208,046.73 across 25 technicians"
ask("How many customers do we have?")    # → "14 customers in total"
ask("How many active contracts?")        # → "77 active contracts"
```

All answered by the same agent, using different semantic models automatically.

## API Details

### Snowflake Agent Object API

**Endpoint:**
```
POST https://{account}.snowflakecomputing.com/api/v2/databases/SNOWFLAKE_INTELLIGENCE/schemas/AGENTS/agents/{agent_name}:run
```

**Authentication:**
```python
headers = {
    "Authorization": f"Bearer {PAT_TOKEN}",
    "X-Snowflake-Authorization-Token-Type": "PROGRAMMATIC_ACCESS_TOKEN",
}
```

**Request:**
```json
{
  "messages": [{
    "role": "user",
    "content": [{"type": "text", "text": "Your question here"}]
  }]
}
```

**Response:** Server-Sent Events stream with:
- `response.status` - Planning updates
- `response.thinking.delta` - Reasoning tokens
- `response.tool_use` - Tool invocations  
- `response.text.delta` - Answer tokens
- `response` - Final aggregated response

See `testing_ground/examples.md` for real response examples.

## Extending the Bot

The simple design makes extensions easy:

### Add Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Add Caching
```python
from functools import lru_cache
ask = lru_cache(maxsize=100)(ask)
```

### Add Rich Formatting
```python
def format_for_slack(answer):
    # Custom Slack block formatting
    return formatted_blocks
```

### Add Conversation Context
```python
thread_memory = {}

def ask_with_context(question, thread_id):
    context = thread_memory.get(thread_id, [])
    # Include context in question or use Snowflake's thread_id parameter
    return ask(question)
```

## Development Approach

This bot was built by:

1. **Testing the real API first** - Captured actual Snowflake agent responses
2. **Understanding the streaming format** - Server-Sent Events with specific event types
3. **Simplifying based on reality** - Let Snowflake handle orchestration
4. **Building incrementally** - Start with core, add features as needed

See `testing_ground/` for the research and testing process.

## Slack App Setup

To deploy to Slack:

1. **Create Slack App** at https://api.slack.com/apps
2. **Enable Socket Mode** (easiest for getting started)
3. **Add Bot Token Scopes:**
   - `chat:write`
   - `commands`
   - `app_mentions:read`
4. **Create Slash Commands** (optional):
   - `/ask-acme` - General questions
   - `/contracts` - Contract analysis
   - `/perf` - Performance analysis
5. **Install to Workspace**
6. **Get tokens** and set environment variables

## Production Considerations

For production deployment, consider adding:

- Secure token storage (not environment variables)
- Error handling and retries
- Rate limiting
- Usage analytics
- Logging and monitoring
- Conversation threading (using Snowflake's thread_id parameter)
- Interactive Slack components (buttons, modals)

## Available Agents

Your Snowflake Intelligence platform has:

- **ACME_INTELLIGENCE_AGENT** - Comprehensive business intelligence (default)
- **ACME_CONTRACTS_AGENT** - Contract analysis and churn prevention
- **DATA_ENGINEER_ASSISTANT** - Query performance and optimization

The intelligence agent has access to all semantic models and can handle most questions.

## Learn More

- **`testing_ground/examples.md`** - Real API response examples and patterns
- **`testing_ground/test_with_pat.py`** - Working test code
- **`quick_start.ipynb`** - Interactive experimentation

---

**Built with simplicity in mind** - Let Snowflake's intelligence do what it does best.
