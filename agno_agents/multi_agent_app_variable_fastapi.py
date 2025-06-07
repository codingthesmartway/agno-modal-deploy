"""
Multi-Agent Financial App - Pattern 3: Direct FastAPIApp variable export

This file demonstrates the third priority pattern with MULTIPLE AGENTS
where a FastAPIApp instance with multiple agents is directly exported
as a module variable.
"""

import argparse
from agno.agent import Agent
from agno.app.fastapi.app import FastAPIApp
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools


def _create_financial_analysis_agent() -> Agent:
    """Private helper function to create a financial analysis agent"""
    return Agent(
        name="Financial Analysis Agent",
        agent_id="financial-analysis-agent",  # Explicit ID for API calls
        description="Expert financial advisor providing comprehensive stock analysis, market insights, and investment research",
        
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
            "You are an expert financial advisor and market analyst specializing in research and analysis.",
            "Your role is to provide comprehensive stock analysis, market insights, and investment research.",
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
            "Focus on thorough analysis rather than specific trading recommendations.",
        ],
        
        # Enable debugging for development
        debug_mode=True,
    )


def _create_trading_strategy_agent() -> Agent:
    """Private helper function to create a trading strategy agent"""
    return Agent(
        name="Trading Strategy Agent",
        agent_id="trading-strategy-agent",  # Explicit ID for API calls
        description="Expert trading strategist providing tactical trading advice, portfolio management, and market timing insights",
        
        # Use GPT-4 for sophisticated trading strategy
        model=OpenAIChat(id="gpt-4o"),
        
        # YFinance tools focused on trading data
        tools=[
            YFinanceTools(
                stock_price=True,              # Real-time stock prices
                analyst_recommendations=True,   # Professional analyst ratings
                company_info=True,             # Company fundamentals
                stock_fundamentals=True,       # Financial metrics
            )
        ],
        
        # Agent configuration for better conversations
        add_history_to_messages=True,       # Remember conversation context
        num_history_responses=5,            # Keep last 5 exchanges
        add_datetime_to_instructions=True,  # Include current date/time
        markdown=True,                      # Format responses in markdown
        
        # Detailed instructions for trading strategy
        instructions=[
            "You are an expert trading strategist and portfolio manager.",
            "Your role is to provide tactical trading advice, portfolio management strategies, and market timing insights.",
            "Focus on actionable trading strategies and portfolio optimization.",
            "When providing trading advice, include:",
            "  • Entry and exit strategies",
            "  • Risk management techniques",
            "  • Position sizing recommendations",
            "  • Market timing considerations",
            "  • Portfolio diversification strategies",
            "Always emphasize risk management and proper position sizing.",
            "Provide specific trading setups when appropriate.",
            "Include stop-loss and take-profit levels when relevant.",
            "Consider market conditions and volatility in your recommendations.",
            "Always remind users that trading involves risk and past performance doesn't guarantee future results.",
        ],
        
        # Enable debugging for development
        debug_mode=True,
    )


# Pattern 3: Direct FastAPIApp variable export with Multiple Agents (Third Priority)
# This FastAPIApp instance contains multiple agents and will be automatically 
# detected and used by the deployment script. Updated for new Agno version.
multi_agent_financial_app = FastAPIApp(agents=[
    _create_financial_analysis_agent(),
    _create_trading_strategy_agent()
])

# Optional: Export list to explicitly specify what should be used
# This helps avoid ambiguity if multiple variables exist
__all__ = ['multi_agent_financial_app']


def main():
    """Local development server"""
    try:
        print("🚀 Starting Multi-Agent Financial App with:")
        print("   📊 Financial Analysis Agent (agent_id: financial-analysis-agent)")
        print("   📈 Trading Strategy Agent (agent_id: trading-strategy-agent)")
        print("   🌐 Server: http://localhost:8007")
        print("   📖 Docs: http://localhost:8007/docs")
        
        # Start the FastAPI server - Updated for new Agno version
        multi_agent_financial_app.serve(
            host="localhost",
            port=8007,
            reload=False
        )
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 