#!/usr/bin/env python3
"""
ACME Intelligence Slack Bot
Simple, production-ready Slack integration for Snowflake Cortex Agents.
"""

import os
import requests
import json
import re
import logging
import time
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import Slack only if needed (progressive disclosure!)
try:
    from slack_bolt import App
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False
    logger.info("Slack Bolt not installed - core functionality still works!")

# ─── Configuration ────────────────────────────────────────────────────────────
# The ONLY things you need to configure

ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "trb65519")
PAT_TOKEN = os.getenv("SNOWFLAKE_PAT", "your-pat-here")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# The main agent - it has access to everything!
MAIN_AGENT = "ACME_INTELLIGENCE_AGENT"

# Optional: You can still use specific agents if needed
AGENTS = {
    "intelligence": "ACME_INTELLIGENCE_AGENT",
    "contracts": "ACME_CONTRACTS_AGENT",
    "perf": "DATA_ENGINEER_ASSISTANT",
}

# Thread context storage for multi-turn conversations
# Maps Slack thread_ts -> list of conversation messages
# Format: [{"role": "user", "content": [...]}, {"role": "assistant", "content": [...]}]
thread_context = {}

# ─── Core Function: Ask an Agent ──────────────────────────────────────────────
# This is the whole API. One function. That's it.

def format_for_slack(answer: str, question: str = "") -> str:
    """
    Format agent response for better Slack readability.
    
    Makes responses:
    - More concise and scannable
    - Better formatted with Slack markdown
    - Visual with emojis
    - Structured with clear sections
    """
    # Remove excessive context and focus on the answer
    lines = answer.split('\n')
    
    # Look for key data points
    formatted_parts = []
    current_section = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_section:
                formatted_parts.append('\n'.join(current_section))
                current_section = []
            continue
        
        # Clean up verbose explanations
        if line.startswith('**') and line.endswith('**:'):
            # Section headers - make them stand out
            formatted_parts.append(f"\n{line}")
            current_section = []
        elif line.startswith('**') and ':' in line:
            # Key-value pairs - keep concise
            current_section.append(line)
        elif line.startswith('•') or line.startswith('-'):
            # Bullet points - keep as is
            current_section.append(line)
        elif any(keyword in line.lower() for keyword in ['recommend', 'insight', 'key']):
            # Important insights - keep
            current_section.append(f"💡 {line}")
        else:
            # Regular text - be selective
            if len(line) < 200 and not any(skip in line.lower() for skip in ['suggests we have', 'this count comes from', 'data spans']):
                current_section.append(line)
    
    if current_section:
        formatted_parts.append('\n'.join(current_section))
    
    result = '\n'.join(formatted_parts)
    
    # Trim if still too long
    if len(result) > 2000:
        result = result[:1950] + "\n\n_... (response truncated for clarity)_"
    
    return result


def ask_agent(question: str, agent: str = "intelligence", conversation_history: list = None, progress_callback=None) -> dict:
    """
    Ask a Snowflake Intelligence agent a question.
    
    Args:
        question: Natural language question
        agent: Which agent to use ("intelligence", "contracts", "perf")
        conversation_history: List of previous messages for multi-turn context
    
    Returns:
        dict with 'answer' (str), 'thinking' (str), 'tools_used' (list)
    """
    agent_name = AGENTS.get(agent, AGENTS["intelligence"])
    
    url = f"https://{ACCOUNT}.snowflakecomputing.com/api/v2/databases/SNOWFLAKE_INTELLIGENCE/schemas/AGENTS/agents/{agent_name}:run"
    
    # Build messages with conversation history for multi-turn
    messages = []
    
    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history)
        logger.info(f"📚 Including {len(conversation_history)} previous messages for context")
    
    # Add current question
    messages.append({
        "role": "user",
        "content": [{"type": "text", "text": question}]
    })
    
    payload = {"messages": messages}
    
    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "X-Snowflake-Authorization-Token-Type": "PROGRAMMATIC_ACCESS_TOKEN",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, stream=True, timeout=60)
        response.raise_for_status()
        
        # Parse streaming response with progress updates
        result = {"answer": "", "thinking": "", "tools_used": [], "raw_events": [], "sql": None, "thread_id": None, "message_id": None}
        last_status = None
        
        for line in response.iter_lines(decode_unicode=True):
            if line.startswith('event: '):
                event_type = line[7:].strip()
            elif line.startswith('data: '):
                try:
                    data = json.loads(line[6:])
                    result["raw_events"].append(data)
                    
                    # Extract thread info for multi-turn
                    if event_type == 'metadata':
                        if 'message_id' in data:
                            result["message_id"] = data['message_id']
                            logger.info(f"Got message_id: {data['message_id']}")
                        if 'thread_id' in data:
                            result["thread_id"] = data['thread_id']
                            logger.info(f"Got thread_id: {data['thread_id']}")
                    
                    # Extract SQL from execution_trace event - this is where the real SQL is!
                    if event_type == 'execution_trace':
                        # The execution trace contains the actual SQL
                        if isinstance(data, list):
                            for trace_item in data:
                                if isinstance(trace_item, str):
                                    try:
                                        trace_json = json.loads(trace_item)
                                        # Look for SQL in attributes
                                        for attr in trace_json.get('attributes', []):
                                            if attr.get('key') == 'snow.ai.observability.agent.tool.cortex_analyst.sql_query':
                                                sql = attr.get('value', {}).get('stringValue')
                                                if sql and not result.get("sql"):
                                                    result["sql"] = sql
                                                    logger.info(f"Found SQL in execution trace: {sql[:100]}...")
                                    except:
                                        pass
                    
                    # Send progress updates
                    if 'status' in data and 'message' in data:
                        status_msg = data['message']
                        if status_msg != last_status and progress_callback:
                            progress_callback(status_msg)
                            last_status = status_msg
                    
                    # Extract the good stuff
                    if 'text' in data and event_type == 'response.text.delta':
                        result["answer"] += data['text']
                    elif 'text' in data and event_type == 'response.thinking.delta':
                        result["thinking"] += data['text']
                    elif 'type' in data and 'cortex' in str(data.get('type', '')).lower():
                        tool_name = data.get('type', 'unknown')
                        if tool_name not in result["tools_used"]:
                            result["tools_used"].append(tool_name)
                        
                except: pass
        
        return result
        
    except Exception as e:
        logger.error(f"Agent call failed: {e}")
        return {"answer": f"Sorry, I encountered an error: {e}", "thinking": "", "tools_used": []}

# ─── Simple API ──────────────────────────────────────────────────────────────
# The simplest possible interface - just ask!

def ask(question: str, agent: Optional[str] = None) -> str:
    """
    Ask a question. That's it.
    
    The main ACME_INTELLIGENCE_AGENT has access to all your data and tools.
    Snowflake's orchestration layer picks the right semantic model and tools.
    
    Args:
        question: Your natural language question
        agent: Optional - specify a different agent ("contracts", "perf")
    
    Returns:
        The answer from the agent
    
    Examples:
        ask("How many customers do we have?")
        ask("Which contracts are at risk?") 
        ask("What are the slowest queries?")
    """
    # Use the main agent unless specified otherwise
    agent_key = agent if agent else "intelligence"
    result = ask_agent(question, agent_key)
    return result["answer"]

# ─── Slack Integration ────────────────────────────────────────────────────────
# Connect to Slack when you're ready

if SLACK_AVAILABLE and SLACK_BOT_TOKEN and SLACK_APP_TOKEN:
    app = App(token=SLACK_BOT_TOKEN)
    
    @app.message(re.compile(".*"))  # Listen to all messages
    def handle_message(message, say):
        """Handle any message to the bot - includes thread follow-ups"""
        # Ignore bot messages
        if message.get("bot_id"):
            return
        
        question = message['text']
        channel_type = message.get('channel_type', '')
        thread_ts = message.get('thread_ts') or message.get('ts')
        is_in_thread = message.get('thread_ts') is not None
        
        # Only respond in: DMs, @mentions, or threads we're participating in
        bot_user_id = app.client.auth_test()['user_id']
        
        # Check if this is in a thread we created/participated in
        in_our_thread = is_in_thread and thread_ts in thread_context
        
        if channel_type != 'im' and f"<@{bot_user_id}>" not in question and not in_our_thread:
            return
        
        # Clean up @mention from question
        question = question.replace(f"<@{bot_user_id}>", "").strip()
        
        logger.info(f"Message received: '{question}' (in_thread={is_in_thread}, has_context={in_our_thread})")
        
        # Show smart progress - updates every 5s or on key milestones
        start_time = time.time()
        last_update = start_time
        progress_msg = None
        seen_statuses = set()
        
        # Smart progress callback - only show important/unique updates
        def show_smart_progress(status):
            nonlocal last_update, progress_msg, seen_statuses
            
            now = time.time()
            status_key = status.lower().split()[0]  # First word
            
            # Key milestones to always show
            key_milestones = ["planning", "executing", "generating", "forming"]
            is_milestone = any(m in status_key for m in key_milestones)
            
            # Show if: (1) Key milestone OR (2) 5+ seconds since last update
            should_update = is_milestone or (now - last_update >= 5.0)
            
            # Don't repeat same status
            if status_key in seen_statuses and not should_update:
                return
            
            if should_update:
                seen_statuses.add(status_key)
                last_update = now
                
                # Map to friendly emoji
                emoji_map = {
                    "planning": "🧠",
                    "executing": "⚡",
                    "generating": "✨",
                    "forming": "📝",
                    "running": "🔧",
                    "streaming": "📊"
                }
                emoji = emoji_map.get(status_key, "⏳")
                
                say(f"{emoji} {status}...", thread_ts=thread_ts)
        
        try:
            # Get conversation history for multi-turn
            conversation_history = thread_context.get(thread_ts, [])
            
            if conversation_history:
                logger.info(f"🔄 Multi-turn: {len(conversation_history)} previous messages in context")
            else:
                logger.info(f"🆕 New conversation starting")
            
            # Call agent with smart progress
            result = ask_agent(
                question,
                "intelligence",
                conversation_history=conversation_history,
                progress_callback=show_smart_progress
            )
            
            elapsed = time.time() - start_time
            
            # Build clean response with proper Slack formatting
            answer = result["answer"]
            if len(answer) > 2500:
                answer = answer[:2400] + "\n\n_... (truncated)_"
            
            # Fix Markdown formatting for Slack
            # Slack uses *text* for bold, not **text**
            answer = answer.replace('**', '*')
            
            # Clean up verbose sections
            lines = answer.split('\n')
            cleaned_lines = []
            for line in lines:
                # Skip overly verbose explanatory text
                if any(skip in line.lower() for skip in [
                    'this count comes from',
                    'data spans from',
                    'suggests we have',
                    'this customer count is derived'
                ]):
                    continue
                cleaned_lines.append(line)
            
            answer = '\n'.join(cleaned_lines)
            
            # Add SQL in code block if available
            if result.get("sql") and result["sql"] != "SQL query executed":
                sql_preview = result["sql"][:500]
                answer += f"\n\n```sql\n{sql_preview}\n```"
            
            # Add metadata footer
            tools_used = ', '.join(set(result["tools_used"])) if result["tools_used"] else "None"
            answer += f"\n\n_⏱️ {elapsed:.1f}s • Tools: {tools_used}_"
            
            say(answer, thread_ts=thread_ts)
            
            # Save conversation history for multi-turn follow-ups
            # Add user question
            conversation_history.append({
                "role": "user",
                "content": [{"type": "text", "text": question}]
            })
            
            # Add assistant response  
            conversation_history.append({
                "role": "assistant",
                "content": [{"type": "text", "text": result["answer"]}]
            })
            
            # Keep last 10 messages to avoid token limits
            thread_context[thread_ts] = conversation_history[-10:]
            
            logger.info(f"💾 Saved conversation history: {len(thread_context[thread_ts])} messages")
            
            # Only show tip on first message in thread
            if len(conversation_history) == 2:  # First Q&A pair
                say("💡 _Tip: Ask follow-up questions by @mentioning me in this thread_", thread_ts=thread_ts)
            
        except Exception as e:
            logger.exception("Error handling message")
            say(f"❌ Sorry, I encountered an error: {e}", thread_ts=thread_ts)
    
    @app.command("/ask-acme")
    def handle_ask_acme(ack, command, say, respond):
        """Handle /ask-acme slash command"""
        ack()  # Acknowledge immediately
        
        question = command.get("text", "").strip()
        user_id = command.get("user_id")
        channel_id = command.get("channel_id")
        
        if not question:
            return respond("Usage: `/ask-acme <your question>`")
        
        try:
            logger.info(f"Slash command: /ask-acme '{question}'")
            start_time = time.time()  # Track timing
            
            # Post the question publicly with proper Slack formatting
            question_msg = say(
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"<@{user_id}> asked:"
                        }
                    },
                    {
                        "type": "section", 
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{question}*"
                        }
                    }
                ],
                text=f"<@{user_id}> asked: {question}",  # Fallback
                channel=channel_id
            )
            thread_ts = question_msg['ts']
            
            # Show thinking in thread
            say("🤔 Analyzing...", thread_ts=thread_ts)
            
            # Get conversation history (empty for first message)
            conversation_history = thread_context.get(thread_ts, [])
            
            # Call agent with conversation history for multi-turn
            result = ask_agent(
                question, 
                "intelligence",
                conversation_history=conversation_history
            )
            
            if not result["answer"]:
                logger.error(f"Empty response. Raw events: {len(result['raw_events'])}")
                return say("❌ No response received. Please try again.", thread_ts=thread_ts)
            
            # Calculate elapsed time
            elapsed = time.time() - start_time
            
            # Build the response with proper Slack formatting
            answer = result["answer"]
            if len(answer) > 2500:
                answer = answer[:2400] + "\n\n_... (truncated)_"
            
            # Fix Markdown: Slack uses *text* not **text**
            answer = answer.replace('**', '*')
            
            # Clean up verbose sections
            lines = answer.split('\n')
            cleaned_lines = []
            for line in lines:
                if any(skip in line.lower() for skip in [
                    'this count comes from',
                    'data spans from', 
                    'this customer count is derived'
                ]):
                    continue
                cleaned_lines.append(line)
            answer = '\n'.join(cleaned_lines)
            
            # Add SQL in code block if available
            if result.get("sql") and result["sql"] != "SQL query executed":
                sql_preview = result["sql"][:500]
                answer += f"\n\n```sql\n{sql_preview}\n```"
            
            # Add metadata footer with tools and timing
            tools_used = ', '.join(set(result["tools_used"])) if result["tools_used"] else "None"
            answer += f"\n\n_⏱️ {elapsed:.1f}s • Tools: {tools_used}_"
            
            say(answer, thread_ts=thread_ts)
            
            # Save conversation history for follow-ups
            conversation_history.append({
                "role": "user",
                "content": [{"type": "text", "text": question}]
            })
            conversation_history.append({
                "role": "assistant",
                "content": [{"type": "text", "text": result["answer"]}]
            })
            
            thread_context[thread_ts] = conversation_history[-10:]  # Keep last 10 messages
            logger.info(f"💾 Saved conversation: {len(thread_context[thread_ts])} messages")
            
            # Add helpful tip about follow-ups (only on first message)
            if len(conversation_history) == 2:
                say("💡 _Tip: Ask follow-up questions by @mentioning me in this thread_", thread_ts=thread_ts)
            
        except Exception as e:
            logger.error(f"Command failed: {e}", exc_info=True)
            respond(f"❌ Error: {e}", response_type="ephemeral")
    
    @app.command("/contracts")
    def handle_contracts(ack, command, respond):
        """Handle /contracts slash command"""
        ack()  # Acknowledge immediately
        
        question = command.get("text", "").strip()
        
        if not question:
            return respond("Usage: `/contracts <your question>`")
        
        # Show immediate feedback
        respond("📋 Analyzing contracts...", response_type="ephemeral")
        
        try:
            logger.info(f"Slash command: /contracts '{question}'")
            result = ask_agent(question, "contracts")
            
            if not result["answer"]:
                return respond("❌ No response received. Please try again.", response_type="ephemeral")
            
            # Keep it simple and clean
            answer = result["answer"][:800] if len(result["answer"]) > 800 else result["answer"]
            
            respond(answer, response_type="in_channel")
        except Exception as e:
            logger.error(f"Command failed: {e}", exc_info=True)
            respond(f"❌ Error: {e}", response_type="ephemeral")
    
    @app.command("/perf")
    def handle_perf(ack, command, respond):
        """Handle /perf slash command"""
        ack()  # Acknowledge immediately
        
        question = command.get("text", "").strip()
        
        if not question:
            return respond("Usage: `/perf <your question>`")
        
        # Show immediate feedback
        respond("⚡ Analyzing performance...", response_type="ephemeral")
        
        try:
            logger.info(f"Slash command: /perf '{question}'")
            result = ask_agent(question, "perf")
            
            if not result["answer"]:
                return respond("❌ No response received. Please try again.", response_type="ephemeral")
            
            # Keep it simple and clean  
            answer = result["answer"][:800] if len(result["answer"]) > 800 else result["answer"]
            
            respond(answer, response_type="in_channel")
        except Exception as e:
            logger.error(f"Command failed: {e}", exc_info=True)
            respond(f"❌ Error: {e}", response_type="ephemeral")
    
    def start():
        """Start the bot"""
        print("🚀 Starting ACME Intelligence Slack Bot...")
        print(f"   Account: {ACCOUNT}")
        print(f"   Agents: {', '.join(AGENTS.values())}")
        print()
        SocketModeHandler(app, SLACK_APP_TOKEN).start()

    
    def start():
        """Start the Slack bot"""
        print("🚀 Starting ACME Intelligence Slack Bot...")
        print(f"   Account: {ACCOUNT}")
        print(f"   Agents: {', '.join(AGENTS.values())}")
        print()
        SocketModeHandler(app, SLACK_APP_TOKEN).start()

else:
    if not SLACK_AVAILABLE:
        logger.info("Slack Bolt not installed - install with: pip install slack-bolt")
    else:
        logger.info("Slack tokens not configured - core ask() function still works")
    
    def start():
        """Dummy start function when Slack not available"""
        print("⚠️  Slack integration not available.")
        print("Install with: pip install slack-bolt")
        print("Or test the core functionality: from simple_bot import ask")

# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if SLACK_AVAILABLE and SLACK_BOT_TOKEN and SLACK_APP_TOKEN:
        start()
    else:
        # Interactive testing mode
        print("🧪 Testing Mode - Core Functionality")
        print()
        print("The core ask() function works without Slack!")
        print()
        print("Try it out:")
        print('>>> from simple_bot import ask')
        print('>>> print(ask("How many customers do we have?"))')
        print()
        
        # Run a quick test if PAT is available
        if PAT_TOKEN and PAT_TOKEN != "your-pat-here":
            print("Running quick test...")
            try:
                answer = ask("Hello, are you working?")
                print(f"✅ Agent responded!")
                print(f"📝 Preview: {answer[:200]}...")
            except Exception as e:
                print(f"❌ Test failed: {e}")
                print("💡 Check your PAT token and Snowflake account")
