# Deploying Agno Agents to Modal

This repository demonstrates how to easily deploy any Agno agent to Modal cloud platform using generic deployment scripts. Choose between FastAPI deployment for custom integrations or AG-UI deployment for standardized front-end integration.

## 📊 Deployment Overview

This repository provides **two deployment options**:

### 🔄 **FastAPI Deployment** (`agno_modal_deploy.py`)
- **Multi-agent support** with agent selection via `agent_id`
- **Custom API endpoints** (`/runs?agent_id=your-agent`)  
- **Authentication support** with token-based security
- **Best for**: API integrations, custom applications, multi-agent systems

### 🎨 **AG-UI Deployment** (`agno_modal_deploy_agui.py`) 
- **Standardized AG-UI protocol** for front-end integration
- **Single agent/team deployment** with `/agui` endpoint
- **No authentication** (optimized for front-end use)
- **Best for**: Web applications, UI frameworks like Dojo, standardized interfaces

Both options package your agent with dependencies and deploy to Modal's cloud platform, making your agent instantly available via REST API.


![Agno Modal Deployment Process](media/agno_modal_deploy.png)

## 🎥 See It In Action

Check out this quick demo of deploying a financial analysis agent to Modal. The deployment takes just seconds, and you can start making API calls right away!

![Agno Modal Deployment Demo](media/agno_modal_deploy.gif)

## 🎯 What You'll Learn

- **Two deployment options**: FastAPI vs AG-UI protocols
- How to deploy Agno agents to Modal in minutes
- Multiple supported agent patterns for maximum flexibility
- How to manage dependencies and secrets automatically
- How to interact with your deployed agent via API
- **NEW**: How to deploy for front-end integration with AG-UI

## 🔧 Supported Agno Agent Patterns

The deployment script supports **4 different Agno agent patterns** with automatic detection. This gives you maximum flexibility in how you structure your Agno agent code:

### Pattern 1: Function returning FastAPIApp (Highest Priority)
```python
def create_fastapi_app() -> FastAPIApp:
    """Create a complete FastAPI app with agent"""
    agent = Agent(name="My Agent", model=OpenAIChat(id="gpt-4o"))
    return FastAPIApp(agents=[agent])
```

### Pattern 2: Function returning Agent (Second Priority)
```python
def create_agent() -> Agent:
    """Create an agent - will be auto-wrapped in FastAPIApp"""
    return Agent(name="My Agent", model=OpenAIChat(id="gpt-4o"))
```

### Pattern 3: Direct FastAPIApp variable (Third Priority)
```python
# Direct FastAPIApp instance
agent = Agent(name="My Agent", model=OpenAIChat(id="gpt-4o"))
app = FastAPIApp(agents=[agent])
```

### Pattern 4: Direct Agent variable (Lowest Priority)
```python
# Direct Agent instance - will be auto-wrapped in FastAPIApp
agent = Agent(name="My Agent", model=OpenAIChat(id="gpt-4o"))
```

### Resolving Ambiguity with `__all__`

If your file has multiple patterns, use Python's `__all__` to specify which one to use:

```python
def create_fastapi_app() -> FastAPIApp: ...
def create_agent() -> Agent: ...
agent = Agent(...)
app = FastAPIApp(agents=[agent])

# Explicitly specify which pattern to use
__all__ = ['create_agent']  # Use the function returning Agent
```

## 🚀 Multi-Agent Support (NEW!)

Agno's latest version supports **multiple agents** in a single FastAPIApp instance! This allows you to deploy specialized agents that work together, each with their own `agent_id`.

### Multi-Agent Benefits

- **Specialized Expertise**: Different agents for different tasks (analysis vs. trading)
- **Single Deployment**: Deploy multiple agents together in one API
- **Shared Resources**: Common authentication, monitoring, and infrastructure
- **Agent Selection**: Choose which agent to use via the `agent_id` parameter

### Multi-Agent Patterns Supported

Currently, **Pattern 1** (Function returning FastAPIApp) and **Pattern 3** (Direct FastAPIApp variable) support multiple agents:

#### Multi-Agent Pattern 1: Function returning FastAPIApp
```python
def create_fastapi_app() -> FastAPIApp:
    """Create FastAPIApp with multiple specialized agents"""
    analysis_agent = Agent(name="Analysis Agent", agent_id="analysis-agent", ...)
    trading_agent = Agent(name="Trading Agent", agent_id="trading-agent", ...)
    
    return FastAPIApp(agents=[analysis_agent, trading_agent])
```

#### Multi-Agent Pattern 3: Direct FastAPIApp variable
```python
# Create multiple agents
analysis_agent = Agent(name="Analysis Agent", agent_id="analysis-agent", ...)
trading_agent = Agent(name="Trading Agent", agent_id="trading-agent", ...)

# Direct FastAPIApp with multiple agents
app = FastAPIApp(agents=[analysis_agent, trading_agent])
```

### Multi-Agent API Usage

With multi-agent deployments, specify which agent to use:

```bash
# Use the financial analysis agent
curl -X POST 'https://your-url.modal.run/runs?agent_id=financial-analysis-agent' \
  -F "message=Analyze Apple's quarterly results"

# Use the trading strategy agent  
curl -X POST 'https://your-url.modal.run/runs?agent_id=trading-strategy-agent' \
  -F "message=What's a good entry strategy for Tesla?"
```

## 🎨 AG-UI Deployment (NEW!)

AG-UI provides a **standardized protocol** for front-end integration. Perfect for web applications and UI frameworks like [Dojo](https://github.com/ag-ui-protocol/ag-ui).

### AG-UI vs FastAPI Comparison

| Feature | FastAPI Deployment | AG-UI Deployment |
|---------|-------------------|------------------|
| **Protocol** | Custom Agno API | Standardized AG-UI |
| **Agents** | Multiple agents | Single agent/team |
| **Endpoint** | `/runs?agent_id=X` | `/agui` |
| **Authentication** | Optional token auth | None (front-end optimized) |
| **Best for** | API integrations | Web UIs, front-ends |

### AG-UI Deployment Script

Use `agno_modal_deploy_agui.py` for AG-UI deployments:

```python
# agno_modal_deploy_agui.py - CONFIGURATION
AGENT_FILE = "agno_agents/financial_agent_agui_app.py"
```

### AG-UI Supported Patterns

1. **Function returning AGUIApp** (Highest Priority)
2. **Function returning Agent** (Auto-wrapped in AGUIApp)
3. **Function returning Team** (Auto-wrapped in AGUIApp)
4. **Direct AGUIApp variable**
5. **Direct Agent variable** (Auto-wrapped)
6. **Direct Team variable** (Auto-wrapped)

### AG-UI Example Usage

```bash
# Deploy with AG-UI protocol
modal serve agno_modal_deploy_agui.py
modal deploy agno_modal_deploy_agui.py

# Interact with AG-UI endpoint
curl -X POST 'https://your-agui-deployment.modal.run/agui' \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze Apple stock performance"}'
```

### AG-UI Front-End Integration

AG-UI deployments work seamlessly with front-end frameworks:

- **[Dojo](https://github.com/ag-ui-protocol/ag-ui)**: Advanced UI for AG-UI agents
- **Custom front-ends**: Any AG-UI compatible interface
- **Web applications**: Direct integration with standardized protocol

## 📁 Pattern Examples

This repository includes complete working examples for all patterns in the [`agno_agents/`](agno_agents/) directory:

**Single-Agent Examples:**
- `agno_agents/financial_agent_app.py` - Original example (Pattern 1)
- `agno_agents/financial_agent_app_function_fastapi.py` - Pattern 1 demo
- `agno_agents/financial_agent_app_function_agent.py` - Pattern 2 demo  
- `agno_agents/financial_agent_app_variable_fastapi.py` - Pattern 3 demo
- `agno_agents/financial_agent_app_variable_agent.py` - Pattern 4 demo
- `agno_agents/financial_agent_app_multiple_patterns.py` - Ambiguity resolution demo

**Multi-Agent Examples (NEW!):**
- `agno_agents/multi_agent_app_function_fastapi.py` - Pattern 1 with multiple agents
- `agno_agents/multi_agent_app_variable_fastapi.py` - Pattern 3 with multiple agents

**AG-UI Examples (NEW!):**
- `agno_agents/financial_agent_agui_app.py` - AG-UI protocol example

See the [agno_agents README](agno_agents/README.md) for detailed information about each example.

## 📋 Prerequisites

1. **Modal Account**: Create a free account at [modal.com](https://modal.com)
2. **Modal CLI**: Install and authenticate Modal
3. **Python Environment**: Python 3.8+ with your Agno agent dependencies
4. **Agno Version**: This deployment script is compatible with the latest Agno version (updated for FastAPIApp changes)

### Setting Up Modal

```bash
# Install Modal
pip install modal

# Authenticate with Modal (creates account if needed)
modal setup
```

## 🚀 Quick Start

### Step 1: Prepare Your Agent

Choose any of the 4 supported patterns. Here are examples for each:

#### Pattern 1: Function returning FastAPIApp (Recommended)
```python
# your_agent.py
from agno.agent import Agent
from agno.app.fastapi.app import FastAPIApp
from agno.models.openai import OpenAIChat

def create_fastapi_app() -> FastAPIApp:
    """
    Create a FastAPI app with your agent.
    This is the most flexible pattern with full control.
    """
    agent = Agent(
        name="Your Agent",
        agent_id="your-agent-id",  # Explicit ID for API calls
        model=OpenAIChat(id="gpt-4o"),
        # ... your agent configuration
    )
    
    return FastAPIApp(agents=[agent])
```

#### Pattern 2: Function returning Agent (Simplest)
```python
# your_agent.py  
from agno.agent import Agent
from agno.models.openai import OpenAIChat

def create_agent() -> Agent:
    """
    Create an agent - will be automatically wrapped in FastAPIApp.
    This is the simplest pattern for basic deployments.
    """
    return Agent(
        name="Your Agent",
        agent_id="your-agent-id",  # Explicit ID for API calls
        model=OpenAIChat(id="gpt-4o"),
        # ... your agent configuration
    )
```

#### Pattern 3: Direct FastAPIApp variable
```python
# your_agent.py
from agno.agent import Agent
from agno.app.fastapi.app import FastAPIApp
from agno.models.openai import OpenAIChat

# Create agent
agent = Agent(
    name="Your Agent",
    agent_id="your-agent-id",  # Explicit ID for API calls
    model=OpenAIChat(id="gpt-4o"),
    # ... your agent configuration  
)

# Direct FastAPIApp instance
app = FastAPIApp(agents=[agent])

# Optional: Explicit export
__all__ = ['app']
```

#### Pattern 4: Direct Agent variable
```python
# your_agent.py
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Direct Agent instance - will be auto-wrapped in FastAPIApp
agent = Agent(
    name="Your Agent",
    agent_id="your-agent-id",  # Explicit ID for API calls
    model=OpenAIChat(id="gpt-4o"),
    # ... your agent configuration
)

# Optional: Explicit export
__all__ = ['agent']
```

### Step 2: Create Dependencies File

Create a `requirements.txt` file with all your dependencies:

```bash
# Generate requirements.txt from your current environment
pip freeze > requirements.txt

# Or manually create with your dependencies
echo "agno>=1.5.0" > requirements.txt
echo "openai>=1.82.0" >> requirements.txt
echo "fastapi>=0.115.0" >> requirements.txt
# ... add other dependencies
```

### Step 3: Configure API Keys (Optional)

Set up your API keys for automatic secret management:

```bash
# Copy the example environment file
cp .example.env .env

# Edit .env and replace placeholder values with your actual API keys
# .env
OPENAI_API_KEY=sk-your-actual-openai-key
ANTHROPIC_API_KEY=your-actual-anthropic-key
GROQ_API_KEY=your-actual-groq-key
# ... add other API keys as needed
```

**Note**: The `.example.env` file contains placeholder values and is safe to commit to git. Your actual `.env` file with real API keys should never be committed (it's already in `.gitignore`).

### Step 3.5: Configure Authentication (Optional)

For production deployments, you can enable token-based authentication to protect your API:

**1. Enable authentication in the deployment script:**
```python
# In agno_modal_deploy.py - CONFIGURATION section
ENABLE_AUTH = True   # Set to False to disable authentication
PROTECT_DOCS = True  # Set to False to make /docs publicly accessible
```

**2. Add your authentication token to .env:**
```bash
# Add to your .env file
AUTH_TOKEN=your-super-secret-deployment-token-here
```

**Important**: The deployment script validates your authentication configuration at deployment time. If you enable authentication but forget to add the token, the deployment will fail immediately with a helpful error message.

**Authentication Features:**
- ✅ **Bearer Token Authentication** - Standard HTTP authentication
- ✅ **Configurable Docs Protection** - Optionally protect /docs and /redoc
- ✅ **Health Check Always Public** - /health endpoint remains unprotected for monitoring
- ✅ **Zero Agent Changes** - Authentication is handled at deployment level
- ✅ **Secure Configuration** - Only sensitive token stored as secret

**Usage with Authentication:**
```bash
# Making authenticated requests
curl -X POST 'https://your-deployment-url.modal.run/runs?agent_id=financial-analysis-agent' \
  -H "Authorization: Bearer your-super-secret-deployment-token-here" \
  -F "message=What is the current stock price of AAPL?" \
  -F "stream=false"

# Health check (always public)
curl https://your-deployment-url.modal.run/health
```

### Step 4: Configure Deployment Script

Edit the `AGENT_FILE` variable in `agno_modal_deploy.py`:

```python
# ============================================================================
# CONFIGURATION - Edit this to point to your agent implementation file
# ============================================================================
AGENT_FILE = "your_agent.py"  # Change this to your agent file
# Or use one of the examples:
# AGENT_FILE = "agno_agents/financial_agent_app.py"
# ============================================================================
```

### Step 5: Deploy to Modal

```bash
# Development deployment (with hot reloading)
modal serve agno_modal_deploy.py

# Production deployment
modal deploy agno_modal_deploy.py
```

That's it! Your agent is now deployed and accessible via a public URL.

## 📖 Detailed Walkthrough

### Understanding the Deployment Script

The `agno_modal_deploy.py` script is a generic deployment solution that:

1. **Auto-detects your agent** from the `AGENT_FILE` configuration using priority-based pattern detection
2. **Loads dependencies** dynamically from `requirements.txt`
3. **Manages secrets** automatically from `.env` file
4. **Configures Modal** with optimal settings for Agno agents
5. **Deploys your agent** as a scalable web service

### How Agent Detection Works

The script uses a sophisticated detection system with the following priority order:

#### 1. Function returning FastAPIApp (Highest Priority)
- Looks for functions with names containing "fastapi" and "app"
- Specifically recognizes `create_fastapi_app()`
- Provides full control over FastAPI configuration

#### 2. Function returning Agent (Second Priority)  
- Looks for functions with names containing "agent" or starting with "create_"
- Automatically wraps the returned Agent in FastAPIApp
- Simplest pattern for basic deployments

#### 3. Direct FastAPIApp variable (Third Priority)
- Looks for module-level variables that are FastAPIApp instances
- Uses the instance directly without modification

#### 4. Direct Agent variable (Lowest Priority)
- Looks for module-level variables that are Agent instances  
- Automatically wraps the Agent in FastAPIApp

#### Ambiguity Resolution
When multiple patterns exist in the same file, the deployment fails with a helpful error message:

```
❌ Multiple Agent functions found: ['create_agent', 'create_financial_agent']. 
   Please export only one using __all__ = ['create_agent']
```

Use Python's `__all__` to explicitly specify which pattern to use:

```python
def create_agent() -> Agent: ...
def create_financial_agent() -> Agent: ...

# Explicitly choose which function to use
__all__ = ['create_agent']
```

### How It Works

#### 1. Agent Detection and Validation

```python
# The script reads your agent file name
AGENT_FILE = "agno_agents/financial_agent_app.py"
agent_file_path = Path(AGENT_FILE)

# Validates the file exists
if not agent_file_path.exists():
    raise FileNotFoundError(f"Agent file not found: {agent_file_path}")

# Uses filename as Modal app name
APP_NAME = agent_file_path.stem  # "financial_agent_app"
```

#### 2. Pattern Detection

```python
def detect_agent_pattern(agent_module):
    # Checks for __all__ exports first
    if hasattr(agent_module, '__all__'):
        available_names = agent_module.__all__
    else:
        available_names = [name for name in dir(agent_module) if not name.startswith('_')]
    
    # Collects candidates for each pattern
    # Applies priority-based selection
    # Returns (pattern_type, callable_or_object, pattern_name)
```

#### 3. Dependency Management

The script automatically reads your `requirements.txt` file:

```python
def load_requirements():
    # Ensures GitPython is always included (required by Agno)
    dependencies.add("GitPython")
    
    # Reads and parses requirements.txt
    with open(requirements_file, 'r') as f:
        for line in f:
            # Handles comments, editable installs, etc.
            # Adds valid dependencies to the list
```

**Key Features:**
- ✅ **Mandatory requirements.txt** - No fallback dependencies
- ✅ **GitPython auto-included** - Always ensures Agno compatibility
- ✅ **Smart parsing** - Handles comments, editable installs, recursive requirements
- ✅ **Error handling** - Clear messages if file is missing or invalid

#### 4. Secret Management

The script uses Modal's built-in `.env` file support:

```python
# Checks if .env file exists
has_env_file = load_env_file()

# Uses Modal's from_dotenv() for automatic secret injection
secrets=[modal.Secret.from_dotenv()] if has_env_file else []
```

**Benefits:**
- ✅ **Automatic** - No manual secret creation needed
- ✅ **Secure** - Secrets are encrypted and managed by Modal
- ✅ **Simple** - Just create a `.env` file with your API keys
- ✅ **Optional** - Works without secrets (with warnings)

#### 5. Modal Configuration

The script configures Modal with optimal settings for Agno agents:

```python
@app.function(
    image=image,
    max_containers=10,        # Scale up to 10 containers
    min_containers=1,         # Keep 1 container warm
    timeout=300,              # 5-minute timeout
    secrets=[...],            # Auto-injected from .env
)
```

#### 6. Dynamic Import and Deployment

```python
def fastapi_app():
    # Dynamically imports your agent module
    agent_module = importlib.import_module(AGENT_MODULE)
    
    # Detects the agent pattern
    pattern_type, pattern_object, pattern_name = detect_agent_pattern(agent_module)
    
    # Handles different patterns appropriately
    if pattern_type == 'fastapi_function':
        fastapi_app_instance = pattern_object()
    elif pattern_type == 'agent_function':
        agent_instance = pattern_object()
        fastapi_app_instance = FastAPIApp(agents=[agent_instance])
    # ... handles all 4 patterns
    
    return fastapi_app_instance.get_app()
```

## 🛠 Customization Options

### Environment Variables

You can customize deployment behavior with environment variables:

```bash
# Deployment configuration
MAX_CONTAINERS=20 modal deploy agno_modal_deploy.py    # Scale to 20 containers
MIN_CONTAINERS=2 modal deploy agno_modal_deploy.py     # Keep 2 containers warm
TIMEOUT=600 modal deploy agno_modal_deploy.py          # 10-minute timeout
MAX_CONCURRENT=200 modal deploy agno_modal_deploy.py   # 200 concurrent requests
```

### Multiple Agents

Deploy different agents by changing the `AGENT_FILE`:

```python
# For a trading bot (Pattern 2: Function returning Agent)
AGENT_FILE = "trading_bot.py"

# For a research assistant (Pattern 1: Function returning FastAPIApp) 
AGENT_FILE = "research_assistant.py"

# For a financial advisor (Pattern 4: Direct Agent variable)
AGENT_FILE = "agno_agents/financial_agent_app_variable_agent.py"
```

## 🌐 Using Your Deployed Agent

Once deployed, Modal provides you with a public URL. You can interact with your agent using:

### API Endpoints

- **POST `/runs`** - Main agent interaction endpoint
- **GET `/health`** - Health check
- **GET `/docs`** - Interactive API documentation
- **GET `/redoc`** - Alternative API documentation

**Important**: Agno now **requires** the `agent_id` parameter for all requests to `/runs` endpoint, even for single-agent deployments. Use `/runs?agent_id=your-agent-id` format.

**Agent IDs in Examples:**
- Single-agent examples: `agent_id=financial-analysis-agent`
- Multi-agent examples: 
  - Financial analysis: `agent_id=financial-analysis-agent`
  - Trading strategy: `agent_id=trading-strategy-agent`

### Example API Usage

```bash
# Basic chat request (add -H "Authorization: Bearer your-token" if auth is enabled)
curl -X POST 'https://your-deployment-url.modal.run/runs?agent_id=financial-analysis-agent' \
  -F "message=What is the current stock price of AAPL?" \
  -F "stream=false"

# Streaming response
curl -X POST 'https://your-deployment-url.modal.run/runs?agent_id=financial-analysis-agent' \
  -F "message=Analyze the market trends" \
  -F "stream=true"

# With session for conversation continuity
curl -X POST 'https://your-deployment-url.modal.run/runs?agent_id=financial-analysis-agent' \
  -F "message=Hello, I need investment advice" \
  -F "stream=false" \
  -F "session_id=my-session-123"
```

**Note**: If you enabled authentication (`ENABLE_AUTH=True`), add the authorization header to all requests:
```bash
-H "Authorization: Bearer your-super-secret-deployment-token-here"
```

### Python Client Example

```python
import requests

# Your Modal deployment URL
BASE_URL = "https://your-deployment-url.modal.run"

# Headers for authentication (if enabled)
headers = {"Authorization": "Bearer your-super-secret-deployment-token-here"}

# Send a message to your agent
response = requests.post(
    f"{BASE_URL}/runs?agent_id=financial-analysis-agent",
    headers=headers,  # Add this if authentication is enabled
    files={
        "message": (None, "What are the top tech stocks to watch?"),
        "stream": (None, "false")
    }
)

print(response.json())
```

## 📊 Pattern Examples

This repository includes complete examples for all 4 supported patterns in the [`agno_agents/`](agno_agents/) directory:

### Testing Different Patterns

To test different patterns, simply update the `AGENT_FILE` in `agno_modal_deploy.py`:

```python
# Single-Agent Examples
# Test Pattern 1: Function returning FastAPIApp
AGENT_FILE = "agno_agents/financial_agent_app_function_fastapi.py"

# Test Pattern 2: Function returning Agent  
AGENT_FILE = "agno_agents/financial_agent_app_function_agent.py"

# Test Pattern 3: Direct FastAPIApp variable
AGENT_FILE = "agno_agents/financial_agent_app_variable_fastapi.py"

# Test Pattern 4: Direct Agent variable
AGENT_FILE = "agno_agents/financial_agent_app_variable_agent.py"

# Test Ambiguity Resolution
AGENT_FILE = "agno_agents/financial_agent_app_multiple_patterns.py"

# Multi-Agent Examples (NEW!)
# Test Multi-Agent Pattern 1: Function returning FastAPIApp with multiple agents
AGENT_FILE = "agno_agents/multi_agent_app_function_fastapi.py"

# Test Multi-Agent Pattern 3: Direct FastAPIApp variable with multiple agents
AGENT_FILE = "agno_agents/multi_agent_app_variable_fastapi.py"
```

### Agent Features (All Examples)

**Single-Agent Examples:**
- **Real-time stock prices** using YFinance
- **Company fundamentals** and financial ratios
- **Analyst recommendations** and price targets
- **Recent company news** and market developments
- **GPT-4o powered analysis** for sophisticated insights

**Multi-Agent Examples:**
- **Financial Analysis Agent** (`agent_id: financial-analysis-agent`):
  - Comprehensive stock analysis and market research
  - Company fundamentals and financial ratios
  - Investment research and risk assessment
- **Trading Strategy Agent** (`agent_id: trading-strategy-agent`):
  - Tactical trading advice and portfolio management
  - Entry/exit strategies and risk management
  - Market timing and position sizing recommendations

### Usage Examples

**Single-Agent Examples:**
```bash
# Stock analysis
curl -X POST 'https://your-url.modal.run/runs?agent_id=financial-analysis-agent' \
  -F "message=Analyze Tesla (TSLA) stock performance" \
  -F "stream=false"

# Market comparison
curl -X POST 'https://your-url.modal.run/runs?agent_id=financial-analysis-agent' \
  -F "message=Compare Apple vs Microsoft for investment" \
  -F "stream=false"

# Portfolio advice
curl -X POST 'https://your-url.modal.run/runs?agent_id=financial-analysis-agent' \
  -F "message=Should I invest in NVIDIA right now?" \
  -F "stream=false"
```

**Multi-Agent Examples:**
```bash
# Financial analysis (using analysis agent)
curl -X POST 'https://your-url.modal.run/runs?agent_id=financial-analysis-agent' \
  -F "message=Analyze Apple's financial statements and provide investment research" \
  -F "stream=false"

# Trading strategy (using trading agent)
curl -X POST 'https://your-url.modal.run/runs?agent_id=trading-strategy-agent' \
  -F "message=What's a good trading strategy for Tesla this week?" \
  -F "stream=false"

# Portfolio management (using trading agent)
curl -X POST 'https://your-url.modal.run/runs?agent_id=trading-strategy-agent' \
  -F "message=Help me create a diversified tech portfolio with risk management" \
  -F "stream=false"
```

## 🔧 Troubleshooting

### Common Issues

1. **Agent file not found**
   ```
   ❌ Agent file not found: your_agent.py
   ```
   **Solution**: Ensure your agent file exists and `AGENT_FILE` is correct

2. **Missing requirements.txt**
   ```
   ❌ requirements.txt not found
   ```
   **Solution**: Create requirements.txt with `pip freeze > requirements.txt`

3. **No valid agent pattern found**
   ```
   ❌ No valid agent pattern found in 'your_agent'. Supported patterns:
      1. Function returning FastAPIApp (e.g., def create_fastapi_app() -> FastAPIApp)
      2. Function returning Agent (e.g., def create_agent() -> Agent)
      3. Direct FastAPIApp variable (e.g., app = FastAPIApp(agents=[agent]))
      4. Direct Agent variable (e.g., agent = Agent(...))
   ```
   **Solution**: Implement one of the 4 supported patterns in your agent file

4. **Multiple patterns detected**
   ```
   ❌ Multiple Agent functions found: ['create_agent', 'create_financial_agent']. 
      Please export only one using __all__ = ['create_agent']
   ```
   **Solution**: Add `__all__ = ['function_or_variable_name']` to specify which pattern to use

5. **API key errors**
   ```
   ⚠️ Warning: No .env file found during deployment
   ```
   **Solution**: Create `.env` file with your API keys

6. **Authentication configuration errors**
   ```
   ❌ Authentication is enabled but no .env file found
   ```
   **Solution**: Create `.env` file with `AUTH_TOKEN=your-token` or set `ENABLE_AUTH=False`

7. **Missing authentication token**
   ```
   ❌ AUTH_TOKEN not found in .env file
   ```
   **Solution**: Add `AUTH_TOKEN=your-secret-token` to your `.env` file

8. **Commented authentication token**
   ```
   ❌ AUTH_TOKEN is commented out in .env file
   ```
   **Solution**: Uncomment the `AUTH_TOKEN` line in your `.env` file

### Pattern Selection Guidelines

- **Use Pattern 1** (Function returning FastAPIApp) for maximum control and complex setups
- **Use Pattern 2** (Function returning Agent) for simple deployments and clean code
- **Use Pattern 3** (Direct FastAPIApp variable) for module-level initialization 
- **Use Pattern 4** (Direct Agent variable) for the simplest possible setup
- **Use `__all__`** when you have multiple patterns in the same file

## 🤝 Contributing

Feel free to improve this deployment script or add more examples! The goal is to make Agno agent deployment as simple as possible for everyone.

## 📄 License

This project is open source and available under the MIT License.
