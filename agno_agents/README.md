# Agno Agent Pattern Examples

This directory contains complete working examples demonstrating all supported agent patterns for deployment with the `agno_modal_deploy.py` script, including both single-agent and multi-agent implementations.

All agents in this directory are fully functional and ready to deploy!

## 📁 Pattern Examples

### Single-Agent Examples

#### `financial_agent_app.py` - Original Example
The original financial agent implementation using Pattern 1 (Function returning FastAPIApp).

#### `financial_agent_app_function_fastapi.py` - Pattern 1
**Function returning FastAPIApp** (Highest Priority)
- Shows the most flexible pattern with full control over FastAPI configuration
- Function: `create_fastapi_app() -> FastAPIApp`
- Best for: Complex setups requiring FastAPI customization

#### `financial_agent_app_function_agent.py` - Pattern 2  
**Function returning Agent** (Second Priority)
- Demonstrates the simplest deployment pattern
- Function: `create_financial_agent() -> Agent`
- Automatically wrapped in FastAPIApp by deployment script
- Best for: Simple deployments with minimal setup

#### `financial_agent_app_variable_fastapi.py` - Pattern 3
**Direct FastAPIApp variable export** (Third Priority)
- Shows module-level FastAPIApp instance
- Variable: `financial_app = FastAPIApp(agents=[agent])`
- Uses `__all__ = ['financial_app']` to specify export
- Best for: Module-level initialization patterns

#### `financial_agent_app_variable_agent.py` - Pattern 4
**Direct Agent variable export** (Lowest Priority)
- Shows the simplest possible setup
- Variable: `financial_agent = Agent(...)`
- Uses `__all__ = ['financial_agent']` to specify export
- Automatically wrapped in FastAPIApp by deployment script
- Best for: Minimal setup with direct agent definition

#### `financial_agent_app_multiple_patterns.py` - Ambiguity Resolution
**Multiple Patterns Demo**
- Shows what happens when multiple patterns exist in the same file
- Demonstrates how to use `__all__` to resolve ambiguity
- Contains all 4 patterns with `__all__` selection
- Shows error handling for ambiguous configurations

### Multi-Agent Examples (NEW!)

#### `multi_agent_app_function_fastapi.py` - Multi-Agent Pattern 1
**Function returning FastAPIApp with Multiple Agents** (Highest Priority)
- Demonstrates deploying multiple specialized agents in one FastAPIApp
- Function: `create_fastapi_app() -> FastAPIApp`
- Agents: Financial Analysis Agent + Trading Strategy Agent
- Agent IDs: `financial-analysis-agent`, `trading-strategy-agent`
- Best for: Complex multi-agent setups with specialized roles

#### `multi_agent_app_variable_fastapi.py` - Multi-Agent Pattern 3  
**Direct FastAPIApp variable with Multiple Agents** (Third Priority)
- Shows module-level FastAPIApp instance with multiple agents
- Variable: `multi_agent_financial_app = FastAPIApp(agents=[...])`
- Agents: Financial Analysis Agent + Trading Strategy Agent
- Agent IDs: `financial-analysis-agent`, `trading-strategy-agent`
- Best for: Module-level multi-agent initialization

## 🚀 Testing Different Patterns

To test any of these patterns, update the `AGENT_FILE` in `../agno_modal_deploy.py`:

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

## 🧪 Local Testing

Each example file can be run locally for development:

```bash
# Run any example locally (each uses a different port)
cd agno_agents

# Single-agent examples
python financial_agent_app.py                      # Port 8001
python financial_agent_app_function_fastapi.py     # Port 8001  
python financial_agent_app_function_agent.py       # Port 8002
python financial_agent_app_variable_fastapi.py     # Port 8003
python financial_agent_app_variable_agent.py       # Port 8004
python financial_agent_app_multiple_patterns.py    # Port 8005

# Multi-agent examples (NEW!)
python multi_agent_app_function_fastapi.py         # Port 8006
python multi_agent_app_variable_fastapi.py         # Port 8007
```

## 🎯 Financial Agent Features

**Single-Agent Examples:**
All single-agent examples implement the same sophisticated financial analysis agent:
- **Real-time stock prices** using YFinance
- **Company fundamentals** and financial ratios
- **Analyst recommendations** and price targets
- **Recent company news** and market developments
- **GPT-4o powered analysis** for sophisticated insights
- **Conversation memory** for context-aware responses
- **Markdown formatting** for beautiful output

**Multi-Agent Examples:**
Multi-agent examples include two specialized agents:

**Financial Analysis Agent** (`agent_id: financial-analysis-agent`):
- Comprehensive stock analysis and market research
- Company fundamentals and financial ratios
- Investment research and risk assessment
- Real-time stock prices and company news

**Trading Strategy Agent** (`agent_id: trading-strategy-agent`):
- Tactical trading advice and portfolio management
- Entry/exit strategies and risk management
- Market timing and position sizing recommendations
- Trading setup analysis

## 🔧 Pattern Selection Guidelines

- **Use Pattern 1** (Function returning FastAPIApp) for maximum control and complex setups
- **Use Pattern 2** (Function returning Agent) for simple deployments and clean code
- **Use Pattern 3** (Direct FastAPIApp variable) for module-level initialization 
- **Use Pattern 4** (Direct Agent variable) for the simplest possible setup
- **Use `__all__`** when you have multiple patterns in the same file

## 📚 More Information

See the main [README.md](../README.md) for complete documentation on:
- Deployment instructions
- Authentication setup
- API usage examples
- Troubleshooting guide 