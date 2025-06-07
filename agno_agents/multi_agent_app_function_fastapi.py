"""
Multi-Agent Financial App - Pattern 1: Function returning FastAPIApp

This file demonstrates the highest priority pattern with MULTIPLE AGENTS
where a function returns a complete FastAPIApp instance containing both
a financial analysis agent and a trading strategy agent.
"""

import argparse
from agno.agent import Agent
from agno.app.fastapi.app import FastAPIApp
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools


def create_financial_analysis_agent() -> Agent:
    """Create a financial analysis agent for market research and stock analysis"""
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


def create_trading_strategy_agent() -> Agent:
    """Create a trading strategy agent for tactical trading advice and portfolio management"""
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


def create_fastapi_app() -> FastAPIApp:
    """
    Create a FastAPI app with multiple financial agents.
    
    Pattern 1: Function returning FastAPIApp with Multiple Agents (Highest Priority)
    This function creates both a financial analysis agent and a trading strategy agent,
    providing comprehensive financial services through a single API.
    """
    # Create both agents
    analysis_agent = create_financial_analysis_agent()
    trading_agent = create_trading_strategy_agent()
    
    # Create FastAPIApp with multiple agents - Updated for new Agno version
    app = FastAPIApp(agents=[analysis_agent, trading_agent])
    return app


def main():
    """Local development server"""
    try:
        # Create FastAPI app with multiple agents
        fastapi_app = create_fastapi_app()
        
        print("🚀 Starting Multi-Agent Financial App with:")
        print("   📊 Financial Analysis Agent (agent_id: financial-analysis-agent)")
        print("   📈 Trading Strategy Agent (agent_id: trading-strategy-agent)")
        print("   🌐 Server: http://localhost:8006")
        print("   📖 Docs: http://localhost:8006/docs")
        
        # Start the FastAPI server - Updated for new Agno version
        fastapi_app.serve(
            host="localhost",
            port=8006,
            reload=False
        )
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 