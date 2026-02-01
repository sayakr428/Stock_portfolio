
import streamlit as st
import pandas as pd
from openai import OpenAI
import os

# Configure the page
st.set_page_config(
    page_title="Trading Data Assistant",
    page_icon="📊",
    layout="wide"
)

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("⚠️ OpenAI API key not found!")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'trades_data' not in st.session_state:
    st.session_state.trades_data = None
if 'holdings_data' not in st.session_state:
    st.session_state.holdings_data = None
if 'data_context' not in st.session_state:
    st.session_state.data_context = ""

def create_enhanced_data_summary(trades_df, holdings_df):
    """Create comprehensive data summary with aggregations and statistics"""
    summary = "=== TRADING DATA SUMMARY ===\n\n"
    
    # TRADES DATA
    if trades_df is not None and not trades_df.empty:
        summary += "--- TRADES DATA ---\n"
        summary += f"Total number of trades: {len(trades_df)}\n"
        summary += f"Columns: {', '.join(trades_df.columns.tolist())}\n\n"
        
        # Trades by portfolio
        if 'PortfolioName' in trades_df.columns:
            trades_by_portfolio = trades_df.groupby('PortfolioName').size().to_dict()
            summary += "Trades count by portfolio:\n"
            for portfolio, count in sorted(trades_by_portfolio.items()):
                summary += f"  - {portfolio}: {count} trades\n"
            summary += "\n"
        
        # Unique portfolios
        if 'PortfolioName' in trades_df.columns:
            unique_portfolios = trades_df['PortfolioName'].unique().tolist()
            summary += f"Unique portfolios in trades: {', '.join(sorted(unique_portfolios))}\n\n"
        
        # Sample trades (first 5)
        summary += "Sample trades (first 5 rows):\n"
        for idx, row in trades_df.head(5).iterrows():
            summary += f"\nTrade {idx + 1}:\n"
            for col in ['PortfolioName', 'TradeTypeName', 'SecurityType', 'Name', 'Quantity', 'Price']:
                if col in trades_df.columns:
                    summary += f"  {col}: {row[col]}\n"
        summary += "\n"
    
    # HOLDINGS DATA
    if holdings_df is not None and not holdings_df.empty:
        summary += "--- HOLDINGS DATA ---\n"
        summary += f"Total number of holdings: {len(holdings_df)}\n"
        summary += f"Columns: {', '.join(holdings_df.columns.tolist())}\n\n"
        
        # Holdings count by portfolio/fund
        if 'PortfolioName' in holdings_df.columns:
            holdings_by_portfolio = holdings_df.groupby('PortfolioName').size().to_dict()
            summary += "Holdings count by portfolio:\n"
            for portfolio, count in sorted(holdings_by_portfolio.items()):
                summary += f"  - {portfolio}: {count} holdings\n"
            summary += "\n"
        
        # Holdings count by ShortName (fund)
        if 'ShortName' in holdings_df.columns:
            holdings_by_fund = holdings_df.groupby('ShortName').size().to_dict()
            summary += "Holdings count by fund (ShortName):\n"
            for fund, count in sorted(holdings_by_fund.items()):
                summary += f"  - {fund}: {count} holdings\n"
            summary += "\n"
        
        # CRITICAL: YTD P&L by fund (aggregated)
        if 'ShortName' in holdings_df.columns and 'PL_YTD' in holdings_df.columns:
            # Convert PL_YTD to numeric, handling any non-numeric values
            holdings_df['PL_YTD_numeric'] = pd.to_numeric(holdings_df['PL_YTD'], errors='coerce')
            
            pl_ytd_by_fund = holdings_df.groupby('ShortName')['PL_YTD_numeric'].sum().sort_values(ascending=False).to_dict()
            summary += "Year-to-Date Profit & Loss (PL_YTD) by fund:\n"
            for fund, pl_ytd in pl_ytd_by_fund.items():
                summary += f"  - {fund}: {pl_ytd:,.2f}\n"
            summary += "\n"
            
            # Best and worst performing funds
            best_fund = max(pl_ytd_by_fund.items(), key=lambda x: x[1])
            worst_fund = min(pl_ytd_by_fund.items(), key=lambda x: x[1])
            summary += f"Best performing fund: {best_fund[0]} with PL_YTD of {best_fund[1]:,.2f}\n"
            summary += f"Worst performing fund: {worst_fund[0]} with PL_YTD of {worst_fund[1]:,.2f}\n\n"
        
        # PL_YTD by PortfolioName (if different from ShortName)
        if 'PortfolioName' in holdings_df.columns and 'PL_YTD' in holdings_df.columns:
            pl_ytd_by_portfolio = holdings_df.groupby('PortfolioName')['PL_YTD_numeric'].sum().sort_values(ascending=False).to_dict()
            summary += "Year-to-Date Profit & Loss (PL_YTD) by portfolio:\n"
            for portfolio, pl_ytd in pl_ytd_by_portfolio.items():
                summary += f"  - {portfolio}: {pl_ytd:,.2f}\n"
            summary += "\n"
        
        # Unique funds/portfolios
        if 'ShortName' in holdings_df.columns:
            unique_funds = holdings_df['ShortName'].unique().tolist()
            summary += f"Unique funds (ShortName): {', '.join(sorted(unique_funds))}\n"
        
        if 'PortfolioName' in holdings_df.columns:
            unique_portfolios = holdings_df['PortfolioName'].unique().tolist()
            summary += f"Unique portfolios: {', '.join(sorted(unique_portfolios))}\n\n"
        
        # Sample holdings (first 5)
        summary += "Sample holdings (first 5 rows):\n"
        for idx, row in holdings_df.head(5).iterrows():
            summary += f"\nHolding {idx + 1}:\n"
            for col in ['ShortName', 'PortfolioName', 'SecurityTypeName', 'SecName', 'Qty', 'PL_YTD']:
                if col in holdings_df.columns:
                    summary += f"  {col}: {row[col]}\n"
        summary += "\n"
    
    return summary

def get_ai_response(user_message):
    """Get response from OpenAI API"""
    
    if st.session_state.trades_data is None and st.session_state.holdings_data is None:
        return "Please upload at least one CSV file (trades.csv or holdings.csv) to get started."
    
    # Create system prompt with data context
    system_prompt = f"""You are a helpful financial data analyst assistant. You have access to trading and holdings data uploaded by the user.

IMPORTANT INSTRUCTIONS:
1. Answer questions ONLY based on the data provided below
2. If you cannot find the answer in the data, respond with: "Sorry, I cannot find the answer in the provided data."
3. Do NOT use external knowledge or make assumptions beyond the data
4. Be specific and provide numbers when available
5. The data summary below contains COMPLETE AGGREGATIONS - use these for accurate answers
6. For fund performance, the PL_YTD (Year-to-Date Profit & Loss) totals are already calculated below

DATA SUMMARY:

{st.session_state.data_context}

KEY NOTES:
- The "Year-to-Date Profit & Loss (PL_YTD) by fund" section shows the TOTAL PL_YTD for each fund (already summed)
- The "Holdings count by fund" shows how many holdings each fund has
- The "Best performing fund" is already identified in the data summary
- Use the aggregated statistics above to answer questions about totals, counts, and comparisons
"""

    # Build messages for API
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    # Add conversation history (limit to last 10 exchanges to save tokens)
    recent_history = st.session_state.conversation_history[-20:] if len(st.session_state.conversation_history) > 20 else st.session_state.conversation_history
    for msg in recent_history:
        messages.append(msg)
    
    # Add current user message
    messages.append({"role": "user", "content": user_message})
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1500,
            temperature=0.3
        )
        
        assistant_message = response.choices[0].message.content
        
        # Update conversation history
        st.session_state.conversation_history.append(
            {"role": "user", "content": user_message}
        )
        st.session_state.conversation_history.append(
            {"role": "assistant", "content": assistant_message}
        )
        
        return assistant_message
        
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

def main():
    # Header
    st.title("📊 Trading Data Assistant")
    st.markdown("### AI-powered analysis of your trades and holdings")
    
    # Sidebar for file uploads
    with st.sidebar:
        st.header("📁 Upload Data Files")
        
        trades_file = st.file_uploader("Upload trades.csv", type="csv")
        holdings_file = st.file_uploader("Upload holdings.csv", type="csv")
        
        st.markdown("---")
        
        # Load trades data
        if trades_file is not None:
            try:
                st.session_state.trades_data = pd.read_csv(trades_file)
                st.success(f"✅ Trades loaded: {len(st.session_state.trades_data)} records")
                # Regenerate data context when files change
                st.session_state.data_context = create_enhanced_data_summary(
                    st.session_state.trades_data,
                    st.session_state.holdings_data
                )
            except Exception as e:
                st.error(f"❌ Error loading trades.csv: {e}")
        
        # Load holdings data
        if holdings_file is not None:
            try:
                st.session_state.holdings_data = pd.read_csv(holdings_file)
                st.success(f"✅ Holdings loaded: {len(st.session_state.holdings_data)} records")
                # Regenerate data context when files change
                st.session_state.data_context = create_enhanced_data_summary(
                    st.session_state.trades_data,
                    st.session_state.holdings_data
                )
            except Exception as e:
                st.error(f"❌ Error loading holdings.csv: {e}")
        
        # Show data stats
        if st.session_state.trades_data is not None or st.session_state.holdings_data is not None:
            st.markdown("---")
            st.markdown("### 📈 Quick Stats")
            
            if st.session_state.holdings_data is not None and 'ShortName' in st.session_state.holdings_data.columns:
                unique_funds = st.session_state.holdings_data['ShortName'].nunique()
                st.metric("Unique Funds", unique_funds)
            
            if st.session_state.holdings_data is not None and 'PL_YTD' in st.session_state.holdings_data.columns:
                st.session_state.holdings_data['PL_YTD_numeric'] = pd.to_numeric(
                    st.session_state.holdings_data['PL_YTD'], errors='coerce'
                )
                total_pl = st.session_state.holdings_data['PL_YTD_numeric'].sum()
                st.metric("Total PL_YTD", f"${total_pl:,.2f}")
        
        # Clear conversation button
        if st.button("🗑️ Clear Conversation"):
            st.session_state.conversation_history = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 💡 Example Questions")
        st.markdown("""
        - How many holdings does Garfield have?
        - Which fund has the best YTD P&L?
        - List all unique portfolio names
        - What is the total number of trades?
        - Compare fund performances
        - Show me the top 3 performing funds
        """)
    
    # Main chat area
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Trades Loaded", 
            len(st.session_state.trades_data) if st.session_state.trades_data is not None else 0
        )
    
    with col2:
        st.metric(
            "Holdings Loaded", 
            len(st.session_state.holdings_data) if st.session_state.holdings_data is not None else 0
        )
    
    with col3:
        st.metric(
            "Conversation Length", 
            len(st.session_state.conversation_history) // 2
        )
    
    with col4:
        status = "Ready" if (st.session_state.trades_data is not None or 
                             st.session_state.holdings_data is not None) else "Waiting for data"
        st.metric("Status", status)
    
    st.markdown("---")
    
    # Chat interface
    st.subheader("💬 Chat")
    
    # Display conversation history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.conversation_history:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])
    
    # Input area
    user_input = st.chat_input("Ask a question about your trading data...")
    
    if user_input:
        # Display user message
        st.chat_message("user").write(user_input)
        
        # Get AI response
        with st.spinner("Analyzing data..."):
            response = get_ai_response(user_input)
        
        # Display assistant response
        st.chat_message("assistant").write(response)
        
        # Rerun to update the chat display
        st.rerun()
    
    # Quick action buttons
    if st.session_state.trades_data is not None or st.session_state.holdings_data is not None:
        st.markdown("### 🚀 Quick Questions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Count holdings by fund"):
                user_input = "How many holdings does each fund have?"
                with st.spinner("Analyzing..."):
                    response = get_ai_response(user_input)
                st.rerun()
        
        with col2:
            if st.button("💰 Best performing fund"):
                user_input = "Which fund has the best YTD profit and loss?"
                with st.spinner("Analyzing..."):
                    response = get_ai_response(user_input)
                st.rerun()
        
        with col3:
            if st.button("📝 List all portfolios"):
                user_input = "List all unique portfolio names"
                with st.spinner("Analyzing..."):
                    response = get_ai_response(user_input)
                st.rerun()

if __name__ == "__main__":
    main()
