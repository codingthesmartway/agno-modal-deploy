"""
Financial Agent - AG-UI Example

This file demonstrates how to create an Agno agent optimized for AG-UI
protocol deployment. AG-UI provides standardized front-end integration
for AI agents, perfect for web applications and UI frameworks like Dojo.

This example can be deployed using agno_modal_deploy_agui.py
"""

import argparse
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools

try:
    from agno.app.agui.app import AGUIApp
except ImportError:
    print("❌ AG-UI not available. Install with: pip install ag-ui-protocol")
    AGUIApp = None


def create_financial_agent() -> Agent:
    """Create a financial analysis agent optimized for AG-UI integration"""
    financial_agent = Agent(
        name="Financial Analysis Agent",
        agent_id="financial-analysis-agent",  # Explicit ID for consistency
        description="Expert financial advisor providing stock analysis, market insights, and investment recommendations via AG-UI protocol",
        
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
        
        # Agent configuration optimized for interactive UI
        add_history_to_messages=True,       # Remember conversation context (important for UI)
        num_history_responses=5,            # Keep last 5 exchanges
        add_datetime_to_instructions=True,  # Include current date/time
        markdown=True,                      # Format responses in markdown (great for UI)
        
        # Detailed instructions optimized for conversational UI
        instructions=[
            "You are an expert financial advisor and market analyst accessible through a web interface.",
            "Always provide clear, well-formatted responses suitable for display in a user interface.",
            "Use markdown formatting for better readability in web applications.",
            "When analyzing stocks, provide structured information including:",
            "  • Current price and recent performance",
            "  • Key financial metrics and ratios", 
            "  • Analyst recommendations and price targets",
            "  • Recent news and developments",
            "  • Risk assessment and market context",
            "Keep responses conversational but informative.",
            "Use bullet points, tables, and clear sections for better UI presentation.",
            "Always include timestamps and data sources when available.",
            "Be objective and mention both opportunities and risks.",
            "Ask clarifying questions when the user's request needs more specificity.",
        ],
        
        # Enable debugging for development
        debug_mode=True,
    )
    
    return financial_agent


def create_agui_app() -> AGUIApp:
    """
    Create an AG-UI app with the financial agent.
    
    AG-UI Pattern: Function returning AGUIApp (Highest Priority)
    This function creates an AGUIApp instance optimized for front-end integration.
    The AG-UI protocol provides standardized communication for web interfaces.
    """
    if AGUIApp is None:
        raise ImportError("AG-UI not available. Install with: pip install ag-ui-protocol")
    
    # Create the financial agent
    agent = create_financial_agent()
    
    # Create AG-UI app with the agent
    app = AGUIApp(agent=agent)
    return app


def main():
    """Local development server for AG-UI app"""
    try:
        if AGUIApp is None:
            print("❌ AG-UI not available. Install with: pip install ag-ui-protocol")
            return 1
        
        # Create AG-UI app
        agui_app = create_agui_app()
        
        print("🚀 Starting Financial Agent with AG-UI Protocol")
        print("   🎨 Protocol: AG-UI standardized")
        print("   🤖 Agent: Financial Analysis Agent")
        print("   🌐 Server: http://localhost:7777")
        print("   📖 Docs: http://localhost:7777/docs")
        print("   🎯 Endpoint: POST /agui (AG-UI standardized)")
        print("")
        print("💡 This agent is optimized for front-end integration!")
        print("   Connect with Dojo or other AG-UI compatible front-ends.")
        
        # Start the AG-UI server using AGUIApp's built-in serve method
        agui_app.serve(
            app=agui_app.get_app(),
            host="localhost",
            port=7777,
            reload=False
        )
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 