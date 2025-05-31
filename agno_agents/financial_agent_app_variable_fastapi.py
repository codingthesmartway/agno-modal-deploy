"""
Financial Agent - Pattern 3: Direct FastAPIApp variable export

This file demonstrates the third priority pattern where a FastAPIApp 
instance is directly exported as a module variable.
"""

import argparse
from agno.agent import Agent
from agno.app.fastapi.app import FastAPIApp
from agno.app.fastapi.serve import serve_fastapi_app
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools


def _create_financial_agent() -> Agent:
    """Private helper function to create the financial agent"""
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


# Pattern 3: Direct FastAPIApp variable export (Third Priority)
# This FastAPIApp instance will be automatically detected and used
# by the deployment script.
financial_app = FastAPIApp(agent=_create_financial_agent())

# Optional: Export list to explicitly specify what should be used
# This helps avoid ambiguity if multiple variables exist
__all__ = ['financial_app']


def main():
    """Local development server"""
    try:
        # Use the module-level FastAPIApp instance
        app = financial_app.get_app()
        
        # Start the FastAPI server
        serve_fastapi_app(
            app=app,
            host="localhost",
            port=8003,
            reload=False
        )
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 