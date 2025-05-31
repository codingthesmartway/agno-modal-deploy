"""
Financial Agent - Multiple Patterns with __all__ Resolution

This file demonstrates a scenario where multiple patterns exist in the same file
and how __all__ can be used to explicitly specify which one should be used
by the deployment script, avoiding ambiguity.
"""

import argparse
from agno.agent import Agent
from agno.app.fastapi.app import FastAPIApp
from agno.app.fastapi.serve import serve_fastapi_app
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools


def _create_base_agent() -> Agent:
    """Helper function to create the base financial agent"""
    return Agent(
        name="Financial Analysis Agent",
        description="Expert financial advisor providing stock analysis, market insights, and investment recommendations",
        
        # Use GPT-4 for sophisticated financial analysis
        model=OpenAIChat(id="gpt-4o"),
        
        # YFinance tools for comprehensive market data
        tools=[
            YFinanceTools(
                stock_price=True,              # Real-time stock prices
                analyst_recommendations=True,   # Professional analyst ratings
                company_info=True,             # Company fundamentals
                company_news=True,             # Latest company news
                stock_fundamentals=True,       # Financial metrics
                income_statements=True,        # Revenue and profit data
                key_financial_ratios=True,     # Important financial ratios
            )
        ],
        
        # Agent configuration for better conversations
        add_history_to_messages=True,       # Remember conversation context
        num_history_responses=5,            # Keep last 5 exchanges
        add_datetime_to_instructions=True,  # Include current date/time
        markdown=True,                      # Format responses in markdown
        
        # Detailed instructions for financial analysis
        instructions=[
            "You are an expert financial advisor and market analyst.",
            "Always provide data-driven insights using the latest available information.",
            "When analyzing stocks, include:",
            "  • Current price and recent performance",
            "  • Key financial metrics and ratios", 
            "  • Analyst recommendations and price targets",
            "  • Recent news and developments",
            "  • Risk assessment and market context",
            "Use tables and structured formatting for data presentation.",
            "Provide clear, actionable insights while noting any limitations.",
            "Always include timestamps and data sources when available.",
            "Be objective and mention both opportunities and risks.",
        ],
        
        # Enable debugging for development
        debug_mode=True,
    )


# Pattern 1: Function returning FastAPIApp (normally highest priority)
def create_fastapi_app() -> FastAPIApp:
    """Create a FastAPI app with the financial agent"""
    agent = _create_base_agent()
    return FastAPIApp(agent=agent)


# Pattern 2: Function returning Agent (normally second priority)  
def create_financial_agent() -> Agent:
    """Create a financial analysis agent"""
    return _create_base_agent()


# Pattern 3: Direct FastAPIApp variable (normally third priority)
financial_app = FastAPIApp(agent=_create_base_agent())


# Pattern 4: Direct Agent variable (normally lowest priority)
financial_agent = _create_base_agent()


# IMPORTANT: Use __all__ to explicitly specify which pattern to use
# This resolves ambiguity when multiple patterns exist in the same file
# Comment/uncomment different lines to test different patterns

# Choose Pattern 1: Function returning FastAPIApp
# __all__ = ['create_fastapi_app']

# Choose Pattern 2: Function returning Agent
# __all__ = ['create_financial_agent']

# Choose Pattern 3: Direct FastAPIApp variable
# __all__ = ['financial_app']

# Choose Pattern 4: Direct Agent variable (currently selected)
__all__ = ['financial_agent']

# Without __all__, the deployment would fail with an error like:
# "❌ Multiple Agent functions found: ['create_financial_agent', ...]. 
#  Please export only one using __all__ = ['create_financial_agent']"


def main():
    """Local development server using the explicitly exported pattern"""
    try:
        # This example uses the __all__ selected pattern (financial_agent)
        # In practice, you'd adapt this based on your __all__ selection
        if 'financial_agent' in __all__:
            fastapi_app = FastAPIApp(agent=financial_agent)
        elif 'financial_app' in __all__:
            fastapi_app = financial_app
        elif 'create_fastapi_app' in __all__:
            fastapi_app = create_fastapi_app()
        elif 'create_financial_agent' in __all__:
            agent = create_financial_agent()
            fastapi_app = FastAPIApp(agent=agent)
        else:
            raise ValueError("No valid pattern specified in __all__")
        
        app = fastapi_app.get_app()
        
        # Start the FastAPI server
        serve_fastapi_app(
            app=app,
            host="localhost",
            port=8005,
            reload=False
        )
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 