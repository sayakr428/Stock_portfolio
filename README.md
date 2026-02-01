<img width="1914" height="890" alt="image" src="https://github.com/user-attachments/assets/bdd5c735-bf9c-497b-babc-c27e5df169ed" />
# Trading Data Assistant 📊

An AI-powered Streamlit chatbot that analyzes trading and holdings data using OpenAI's GPT-4. The bot provides insights into portfolio performance, fund analysis, and trading statistics based on uploaded CSV files.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-red.svg)
![OpenAI](https://img.shields.io/badge/openai-gpt--4o-green.svg)

## 🌟 Features

- **Data-Constrained Responses**: Answers questions ONLY based on uploaded data
- **Portfolio Analysis**: Compare fund performance using YTD P&L metrics
- **Holdings Insights**: Count and analyze holdings by fund
- **Trade Analytics**: Track trade counts and patterns by portfolio
- **Interactive Chat**: Natural language interface for data queries
- **Quick Actions**: Pre-built buttons for common queries
- **Real-time Statistics**: Live dashboard with key metrics

## 📋 Requirements

- Python 3.8 or higher
- OpenAI API key

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sayakr428/Stock_portfolio.git
   cd Stock_portfolio
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key**
   
   **Option A: Environment Variable (Recommended)**
   ```bash
   # Windows (Command Prompt)
   set OPENAI_API_KEY=your-api-key-here
   
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your-api-key-here"
   
   # Mac/Linux
   export OPENAI_API_KEY=your-api-key-here
   ```
   
   **Option B: Streamlit Secrets**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

4. **Run the application**
   ```bash
   streamlit run trading_assistant_improved.py
   ```

## 📁 Data Format

### trades.csv
Expected columns:
- `PortfolioName`: Name of the portfolio/fund
- `TradeTypeName`: Buy/Sell
- `SecurityType`: Type of security (Equity, Bond, etc.)
- `Name`: Security name
- `Quantity`: Trade quantity
- `Price`: Trade price
- `TradeFXRate`: Foreign exchange rate
- `AllocationCash`: Cash allocated

### holdings.csv
Expected columns:
- `ShortName`: Short name of the fund
- `PortfolioName`: Full portfolio name
- `SecurityTypeName`: Type of security
- `SecName`: Security name
- `Qty`: Quantity held
- `PL_YTD`: Year-to-date profit/loss
- `MV_Base`: Market value

## 💡 Example Questions

- "How many holdings does Garfield have?"
- "Which fund has the best YTD profit and loss?"
- "List all unique portfolio names"
- "What is the total number of trades?"
- "Compare the performance of all funds"
- "Show me the top 3 performing funds"
- "How many trades were executed for HoldCo 1?"

## 🎯 Key Features Explained

### Data-Constrained Analysis
The chatbot is specifically designed to:
- Answer questions ONLY from the uploaded data
- Return "Sorry, I cannot find the answer in the provided data" when information is not available
- Prevent hallucination by not using external knowledge

### Performance Metrics
- Automatically calculates total PL_YTD for each fund
- Identifies best and worst performing funds
- Provides aggregated statistics for quick insights

### Interactive Dashboard
- Real-time metrics display
- Conversation history tracking
- Quick action buttons for common queries

## 🔒 Security Notes

⚠️ **Important**: Never commit your OpenAI API key to the repository!

- Use environment variables or Streamlit secrets
- Add `.streamlit/secrets.toml` to `.gitignore`
- Regenerate your API key if accidentally exposed

## 📊 Project Structure

```
Stock_portfolio/
├── trading_assistant_improved.py   # Main application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
├── trades.csv                      # Sample trades data (optional)
└── holdings.csv                    # Sample holdings data (optional)
```

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **OpenAI GPT-4o**: Natural language processing
- **Python 3.8+**: Core programming language

## 📝 Problem Statement

This project was created to solve the following requirements:
- Create a chatbot trained on trading and holdings CSV files
- Answer questions related to data from the provided files
- Return error message when answer is not found in files
- Calculate total holdings/trades for given funds
- Compare fund performance based on yearly Profit & Loss

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Sayak Roy**
- GitHub: [@sayakr428](https://github.com/sayakr428)

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI](https://openai.com/)
- Inspired by the need for efficient portfolio analysis tools

---

**Note**: This is a demo application for portfolio analysis. Always verify results with your financial advisor before making investment decisions.
