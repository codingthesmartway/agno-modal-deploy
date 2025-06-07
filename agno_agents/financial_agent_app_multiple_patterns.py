"""
Financial Agent - Multiple Patterns Demo

This file demonstrates what happens when multiple agent patterns exist
in the same file. The deployment script will detect ambiguity and 
require explicit selection using __all__.

This example shows all 4 patterns coexisting and uses __all__ to specify
which one to use for deployment.
"""

import argparse
from agno.agent import Agent
from agno.app.fastapi.app import FastAPIApp
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools


def _create_base_agent() -> Agent:
    """Helper function to create the base financial agent"""
    return Agent(
        name="Financial Analysis Agent",
        agent_id="financial-analysis-agent",  # Explicit ID for API calls
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


# Pattern 1: Function returning FastAPIApp (Highest Priority)
def create_fastapi_app() -> FastAPIApp:
    """Create a FastAPI app with the financial agent"""
    agent = _create_base_agent()
    return FastAPIApp(agents=[agent])  # Updated for new Agno version


# Pattern 2: Function returning Agent (Second Priority)  
def create_agent() -> Agent:
    """Create an agent - will be auto-wrapped in FastAPIApp"""
    return _create_base_agent()


# Pattern 3: Direct FastAPIApp variable (Third Priority)
financial_fastapi_app = FastAPIApp(agents=[_create_base_agent()])  # Updated for new Agno version


# Pattern 4: Direct Agent variable (Lowest Priority)
financial_agent = _create_base_agent()


# EXPLICIT SELECTION USING __all__
# Since multiple patterns exist, we use __all__ to specify which one to use.
# The deployment script will use this to resolve ambiguity.
#
# Try changing this to test different patterns:
# __all__ = ['create_fastapi_app']     # Pattern 1: Function returning FastAPIApp
# __all__ = ['create_agent']           # Pattern 2: Function returning Agent
# __all__ = ['financial_fastapi_app']  # Pattern 3: Direct FastAPIApp variable
# __all__ = ['financial_agent']        # Pattern 4: Direct Agent variable

__all__ = ['create_agent']  # Using Pattern 2 for this demo


def main():
    """Local development server - uses the pattern specified in __all__"""
    try:
        if 'create_fastapi_app' in __all__:
            # Pattern 1: Function returning FastAPIApp
            fastapi_app = create_fastapi_app()
        elif 'create_agent' in __all__:
            # Pattern 2: Function returning Agent (wrap in FastAPIApp)
            agent = create_agent()
            fastapi_app = FastAPIApp(agents=[agent])  # Updated for new Agno version
        elif 'financial_fastapi_app' in __all__:
            # Pattern 3: Direct FastAPIApp variable
            fastapi_app = financial_fastapi_app
        elif 'financial_agent' in __all__:
            # Pattern 4: Direct Agent variable (wrap in FastAPIApp)
            fastapi_app = FastAPIApp(agents=[financial_agent])  # Updated for new Agno version
        else:
            raise ValueError("Invalid __all__ specification")
        
        # Start the FastAPI server - Updated for new Agno version
        fastapi_app.serve(
            host="localhost",
            port=8005,
            reload=False
        )
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 