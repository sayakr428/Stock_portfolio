<img width="1914" height="890" alt="image" src="https://github.com/user-attachments/assets/bdd5c735-bf9c-497b-babc-c27e5df169ed" />

# Trading Data Assistant 📊

An AI-powered Streamlit chatbot that analyzes trading and holdings data using OpenAI's GPT-4. The bot provides insights into portfolio performance, fund analysis, and trading statistics based on CSV files uploaded through the web interface.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-red.svg)
![OpenAI](https://img.shields.io/badge/openai-gpt--4o-green.svg)

## 🌟 Features

- **File Upload Interface**: Upload your trades.csv and holdings.csv files directly in the browser
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
- Your trading data in CSV format (trades.csv and/or holdings.csv)

## 🚀 Quick Start

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
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your-api-key-here"
   
   # Windows (Command Prompt)
   set OPENAI_API_KEY=your-api-key-here
   
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
   streamlit run streamlit_app.py
   ```

5. **Upload your data**
   - Once the app opens in your browser, use the sidebar to upload your CSV files
   - Upload `trades.csv` and/or `holdings.csv`
   - Start asking questions about your data!

## 📁 Data Format

The application expects CSV files with the following structure:

### trades.csv
Required/Expected columns:
- `PortfolioName`: Name of the portfolio/fund
- `TradeTypeName`: Buy/Sell
- `SecurityType`: Type of security (Equity, Bond, etc.)
- `Name`: Security name
- `Quantity`: Trade quantity
- `Price`: Trade price
- `TradeFXRate`: Foreign exchange rate (optional)
- `AllocationCash`: Cash allocated (optional)

### holdings.csv
Required/Expected columns:
- `ShortName`: Short name of the fund
- `PortfolioName`: Full portfolio name
- `SecurityTypeName`: Type of security
- `SecName`: Security name
- `Qty`: Quantity held
- `PL_YTD`: Year-to-date profit/loss ⭐ (critical for performance analysis)
- `MV_Base`: Market value (optional)

**Note**: You can upload one or both files. The chatbot will analyze whatever data you provide.

## 💡 Example Questions

Once you've uploaded your data files, try asking:

- "How many holdings does Garfield have?"
- "Which fund has the best YTD profit and loss?"
- "List all unique portfolio names"
- "What is the total number of trades?"
- "Compare the performance of all funds"
- "Show me the top 3 performing funds"
- "How many trades were executed for HoldCo 1?"

## 🎯 How It Works

### Data Upload
1. Launch the application with `streamlit run streamlit_app.py`
2. Use the file upload widgets in the left sidebar
3. Upload your `trades.csv` and/or `holdings.csv` files
4. The app automatically processes and summarizes your data

### Data-Constrained Analysis
The chatbot is specifically designed to:
- Answer questions ONLY from the uploaded data
- Return "Sorry, I cannot find the answer in the provided data" when information is not available
- Prevent hallucination by not using external knowledge
- Work entirely in-memory (no data is stored or persisted)

### Performance Metrics
- Automatically calculates total PL_YTD for each fund
- Identifies best and worst performing funds
- Provides aggregated statistics for quick insights
- Groups data by portfolio and fund for comprehensive analysis

### Interactive Dashboard
- Real-time metrics display showing:
  - Number of trades loaded
  - Number of holdings loaded
  - Conversation history length
  - System status
- Conversation history tracking
- Quick action buttons for common queries

## 🔒 Security Notes

⚠️ **Important Security Considerations**:

- **Never commit your OpenAI API key** to the repository
- Use environment variables or Streamlit secrets for API key storage
- Add `.streamlit/secrets.toml` to `.gitignore`
- Regenerate your API key if accidentally exposed
- **Your CSV data is processed in-memory only** and is not stored or persisted
- Data is cleared when you close the browser or refresh the page

## 📊 Project Structure

```
Stock_portfolio/
├── streamlit_app.py            # Main application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

**Note**: CSV data files are NOT included in the repository. Users upload their own data through the web interface.

## 🛠️ Technologies Used

- **Streamlit**: Web application framework with file upload capabilities
- **Pandas**: Data manipulation and analysis
- **OpenAI GPT-4o**: Natural language processing
- **Python 3.8+**: Core programming language

## 📝 Problem Statement

This project was created to solve the following requirements:
- Create a chatbot trained on trading and holdings CSV files
- Answer questions related to data from user-uploaded files
- Return error message when answer is not found in files
- Calculate total holdings/trades for given funds
- Compare fund performance based on yearly Profit & Loss
- Ensure data privacy by processing files in-memory only

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

## ❓ Troubleshooting

### "OpenAI API key not found" error
- Make sure you've set the `OPENAI_API_KEY` environment variable
- Check that the key is valid and has sufficient credits
- Try restarting your terminal after setting the environment variable

### Files not uploading
- Ensure your CSV files are properly formatted
- Check that column names match the expected format
- File size should be reasonable (< 200MB recommended)

### No responses from the chatbot
- Verify that at least one CSV file has been uploaded successfully
- Check that your OpenAI API key is working
- Look for error messages in the Streamlit interface

---

**Note**: This is a demo application for portfolio analysis. Always verify results with your financial advisor before making investment decisions.
