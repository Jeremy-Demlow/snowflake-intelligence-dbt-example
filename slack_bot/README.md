# ACME Intelligence Slack Bot 🤖

A simple, production-ready Slack bot that connects your team to Snowflake Cortex Agents.

## Quick Start

```python
from simple_bot import ask

# That's it. Just ask.
print(ask("How many customers do we have?"))
# → "Based on our financial metrics data, we currently have 14 customers..."
```

## Features

- ✅ **Multi-turn conversations** - Ask follow-up questions with full context
- ✅ **SQL transparency** - See the generated queries
- ✅ **Smart progress updates** - Know what's happening without spam
- ✅ **Clean formatting** - Optimized for Slack readability
- ✅ **Response timing** - See how long queries take
- ✅ **Three slash commands** - `/ask-acme`, `/contracts`, `/perf`
- ✅ **Works with @mentions** - Natural conversation in threads
- ✅ **📊 Chart visualization** - Automatic chart rendering from Agent responses (NEW!)

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

**Optional - Enable Chart Visualization:**
```bash
pip install altair vl-convert-python
```

This enables automatic chart rendering when the Agent returns Vega-Lite specifications. See `CHART_FEATURE.md` for details.

### 2. Configure Environment Variables

```bash
# Set these in your environment or .zshrc
export SNOWFLAKE_ACCOUNT="your-account"
export SNOWFLAKE_PAT="your-personal-access-token"
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export SLACK_APP_TOKEN="xapp-your-app-token"
```

### 3. Create Slack App (One-Time Setup)

**Use the manifest for instant setup:**

1. Go to https://api.slack.com/apps
2. Click **"Create New App"** → **"From an app manifest"**
3. Choose your workspace (e.g., TESTWORKSPACE)
4. Select **YAML** format
5. Copy and paste the entire contents of `slack_app_manifest.yml`
6. Click **"Next"** → **"Create"**

**Get your tokens:**
- **Bot Token**: OAuth & Permissions → Install to Workspace → Copy "Bot User OAuth Token"
- **App Token**: Basic Information → App-Level Tokens → Copy token (or generate with `connections:write` scope)

**The manifest automatically configures:**
- All 3 slash commands (`/ask-acme`, `/contracts`, `/perf`)
- Socket Mode for easy development
- All required bot permissions
- Event subscriptions for @mentions and DMs

### 4. Test Before Running

```bash
python test_bot.py  # Health check
```

### 5. Run the Bot

```bash
python simple_bot.py
```

## Usage

### Slack Commands

**Slash Commands** (start a new thread):
```
/ask-acme How many customers do we have?
/contracts Which contracts are at risk?
/perf What are the slowest queries today?
```

**Follow-up Questions** (in threads):
```
@ACME Intelligence Bot Who are those customers?
@ACME Intelligence Bot Which one has highest revenue?
```

**You'll see:**
- Question posted visibly
- Smart progress updates (every 5s + key milestones)
- Clean answer with proper Slack formatting
- SQL query in code block
- Response timing and tools used
- Tip about asking follow-ups

### Python Module (Without Slack)

```python
from simple_bot import ask

# Just ask questions
answer = ask("What's our revenue this quarter?")
answer = ask("Which contracts need attention?")
answer = ask("Show me slow queries from today")
```

## Testing

### Health Check
```bash
python test_bot.py  # Verifies imports, config, dependencies
```

### Test API Directly
```bash
cd testing_ground
export SNOWFLAKE_PAT="your-token"
python test_with_pat.py  # Calls real agent, shows streaming events
```

### Interactive Testing
```bash
jupyter notebook quick_start.ipynb  # Test without Slack
```

## How It Works

### Multi-Turn Conversations

The bot maintains conversation context so you can ask follow-ups:

```
You: /ask-acme How many customers do we have?
Bot: Based on our financial data, we have 14 customers...
     [Shows SQL and timing]

You: @bot Who are those customers?  (in the thread)
Bot: Our 14 customers are:
     1. PARENT_001
     2. PARENT_002
     ...
     [Shows SQL and timing]

You: @bot Which one has highest revenue?  (in the thread)
Bot: PARENT_005 with $30.7M ARR...
```

The agent **remembers the context** from previous questions!

### What You See

**Question Posted:**
```
@User asked:
How many customers do we have?
```

**Progress (every 5s + milestones):**
```
🤔 Analyzing...
🧠 Planning the next steps...
⚡ Executing SQL...
✨ Generating SQL...
```

**Answer with Metadata:**
```
Based on our financial data, we have *14 customers* in total.

```sql
SELECT COUNT(DISTINCT ndr_parent)...
```

⏱️ 15.7s • Tools: cortex_analyst_text_to_sql

💡 Tip: Ask follow-ups by @mentioning me in this thread
```

**Chart (when appropriate):**
```
📊 Generated chart visualization:
[PNG image of chart appears in thread]
```

The Agent automatically creates charts for time-series, comparisons, and distributions!

## Technical Details

### Available Agents

- **ACME_INTELLIGENCE_AGENT** - Main agent with access to all semantic models
- **ACME_CONTRACTS_AGENT** - Specialized for contract analysis
- **DATA_ENGINEER_ASSISTANT** - Query performance optimization

**Pro tip:** The intelligence agent can handle most questions since it has access to all data!

### API Endpoint
```
POST https://{account}.snowflakecomputing.com/api/v2/databases/SNOWFLAKE_INTELLIGENCE/schemas/AGENTS/agents/{agent_name}:run
```

### Multi-Turn Implementation
Conversation history is passed in the `messages` array:
```json
{
  "messages": [
    {"role": "user", "content": [{"text": "How many customers?"}]},
    {"role": "assistant", "content": [{"text": "14 customers"}]},
    {"role": "user", "content": [{"text": "Who are they?"}]}
  ]
}
```

The agent uses this history to understand context like "they" refers to the "14 customers" from before.

## Troubleshooting

### Bot doesn't respond
1. Check logs in terminal where bot is running
2. Verify environment variables are set
3. Run `python test_bot.py` to check health

### "dispatch_failed" error
- Bot took too long to acknowledge
- Already fixed with immediate `ack()` call

### Multi-turn not working
- Make sure to @mention the bot in the thread (not slash command)
- Check logs for "Multi-turn: X previous messages"

### SQL not displaying
- Check logs for "Found SQL in execution trace"
- Verify `cortex_analyst_text_to_sql` tool was used

## Future Improvements

See `notes_to_self.md` for detailed improvement roadmap including:
- Update progress in place (not separate messages)
- Rich Slack blocks with sections
- Interactive buttons for "Show SQL", "Export Data"
- Thread context expiry (memory management)
- Usage analytics and monitoring

## Learn More

- **`CHART_FEATURE.md`** - **NEW!** Complete guide to automatic chart visualization
- **`notes_to_self.md`** - Detailed technical documentation and improvement roadmap
- **`testing_ground/examples.md`** - Real API response examples
- **`testing_ground/test_with_pat.py`** - Working API test
- **`quick_start.ipynb`** - Interactive notebook

---

**Simple by design** - Leverages Snowflake's Intelligence layers to provide enterprise AI in Slack.
