# Architecture Decision: @sproc vs Snowpark Project

## The Problem
We need to decide how to deploy our agent tools:

1. **Current approach**: Embed Python code in @sproc stored procedures
2. **Alternative**: Create a proper Snowpark project and deploy as packages

## Analysis

### Current @sproc Approach

**Pros:**
- Simple deployment - one SQL command creates the procedure
- Self-contained - all code embedded in the database
- Easy to version control as SQL files
- Direct agent integration - procedures are callable by agents

**Cons:**
- **Complex string escaping** - embedding Python in SQL strings is error-prone
- **Limited debugging** - hard to debug Python code inside SQL strings  
- **No proper IDE support** - Python code in strings lacks syntax highlighting
- **Dependency management** - limited to PACKAGES parameter
- **Code reuse** - can't easily share code between procedures

### Snowpark Project Approach

**Pros:**
- **Proper Python development** - real .py files with IDE support
- **Better dependency management** - requirements.txt, proper imports
- **Code reuse** - shared modules between different functions
- **Easier debugging** - proper Python stack traces
- **CI/CD friendly** - standard Python packaging and deployment

**Cons:**
- **More complex deployment** - need to package and upload
- **Additional infrastructure** - need staging for code packages
- **Learning curve** - new deployment process

## Decision

Given your feedback about code quality and the complexity we're seeing with string escaping, I recommend:

### **Hybrid Approach: Snowpark Project with Procedure Wrappers**

1. **Main logic in Snowpark project**:
   ```
   agent_tools/
   ├── src/
   │   ├── email_tools/
   │   │   └── sender.py       # Clean Python code
   │   └── web_tools/
   │       ├── scraper.py      # Core scraping
   │       └── analyzer.py     # AI analysis
   ├── requirements.txt        # Dependencies
   └── setup.py               # Package definition
   ```

2. **Simple @sproc wrappers**:
   ```sql
   CREATE PROCEDURE send_mail(recipient TEXT, subject TEXT, text TEXT)
   RETURNS TEXT
   LANGUAGE PYTHON
   RUNTIME_VERSION = '3.11'
   IMPORTS = ('@agent_tools_stage/agent_tools.zip')
   HANDLER = 'email_tools.sender.send_email_for_agent'
   ```

## Benefits of This Approach

✅ **Clean Python code** - no more string escaping hell  
✅ **Proper IDE support** - full IntelliSense, debugging  
✅ **Better testing** - proper unit tests, mocking  
✅ **Code reuse** - shared utilities across tools  
✅ **Easy AI integration** - proper SDK imports  
✅ **Simple agent integration** - still just call procedures  
✅ **Version control** - clean Python files in git  

## Implementation Plan

1. **Create Snowpark project structure**
2. **Move Python logic to proper modules**  
3. **Create simple @sproc wrappers**
4. **Update deployment to upload packages**
5. **Keep same agent interface** - procedures still callable

This gives us the best of both worlds - clean Python development with simple agent integration.

What do you think? Should we refactor to this approach?
