# 🏢 Blancosy Financials - Official Analysis Dashboard

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://yourusername.github.io/blancosy-financials/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Official Financial Analysis Dashboard** based on P&L Account and Balance Sheet data

## 📊 Live Dashboard

**🌐 [View Live Dashboard](https://yourusername.github.io/blancosy-financials/)**

## 🎯 Key Features

### ✅ Official Data Verification
- **2024 Net Profit: KES 3,389,075.35** (matches Balance Sheet)
- Based on official P&L Account figures
- Verified against Balance Sheet data

### 📈 Interactive Visualizations
- **P&L Waterfall Analysis** - Visual breakdown of 2024 profit flow
- **Expense Breakdown** - Pie chart of major expense categories
- **Year-over-Year Comparison** - 2024 vs 2025 performance
- **Monthly Trends** - 2025 detailed transaction patterns

### 💼 Financial Metrics
- **Gross Profit Margin**: 23.8%
- **Net Profit Margin**: 15.0%
- **Total Revenue 2024**: KES 22,619,122
- **Operating Efficiency**: Strong profitability indicators

## 📋 2024 Official P&L Summary

| Metric | Amount (KES) | Percentage |
|--------|--------------|------------|
| **Sales Revenue** | 22,619,122 | 100.0% |
| **Cost of Goods Sold** | 17,244,564 | 76.2% |
| **Gross Profit** | 5,374,558 | 23.8% |
| | | |
| **Operating Expenses:** | | |
| Labour | 601,155 | 2.7% |
| Rent | 192,000 | 0.8% |
| Transport | 1,028,770 | 4.5% |
| Transaction Costs | 163,558 | 0.7% |
| **Total Operating Expenses** | 1,985,483 | 8.8% |
| | | |
| **Net Profit** | **3,389,075** | **15.0%** |

## 🚀 Deployment Instructions

### Option 1: Fork and Deploy
1. Fork this repository
2. Go to repository Settings → Pages
3. Select "Deploy from a branch"
4. Choose "main" branch and "/ (root)" folder
5. Your dashboard will be live at `https://yourusername.github.io/blancosy-financials/`

### Option 2: Manual Setup
1. Create a new repository named `blancosy-financials`
2. Upload the `index.html` file
3. Enable GitHub Pages in repository settings
4. Access your dashboard at the GitHub Pages URL

## 📁 File Structure

```
blancosy-financials/
├── index.html                          # Main dashboard (GitHub Pages)
├── README.md                           # This file
├── generate_static_dashboard.py        # Dashboard generator
├── official_data_processor.py          # Data processing engine
├── requirements.txt                    # Python dependencies
└── docs/                              # Additional documentation
    ├── deployment-guide.md
    └── data-sources.md
```

## 🛠️ Local Development

### Prerequisites
- Python 3.8+
- Required packages (see `requirements.txt`)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/blancosy-financials.git
cd blancosy-financials

# Install dependencies
pip install -r requirements.txt

# Generate updated dashboard
python generate_static_dashboard.py

# Open index.html in your browser
```

### Regenerating the Dashboard
```bash
# Update data and regenerate
python generate_static_dashboard.py

# Commit and push changes
git add index.html
git commit -m "Update dashboard with latest data"
git push origin main
```

## 📊 Data Sources

- **2024 Data**: Official P&L Account and Balance Sheet
- **2025 Data**: Detailed transaction records from Excel sheets
- **Verification**: All figures cross-referenced with official financial statements

## 🔍 Key Insights

### ✅ Strengths
- **Strong Profitability**: 15.0% net profit margin
- **Efficient Operations**: Low operating expense ratio (8.8%)
- **Verified Accuracy**: Matches official financial statements

### ⚠️ Areas for Attention
- **Revenue Decline**: 2025 showing reduced sales activity
- **Market Analysis**: Need to understand revenue drop causes
- **Strategic Planning**: Focus on revenue growth initiatives

## 📈 Performance Highlights

- **2024 Net Profit**: KES 3,389,075.35
- **Gross Margin**: 23.8% (healthy for retail/trading business)
- **Operating Efficiency**: 91.2% (expenses are only 8.8% of sales)
- **Cash Position**: Strong (KES 3.4M in cash & bank)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For questions about the financial data or dashboard:
- **Business**: Blancosy Financials
- **Technical**: Dashboard Developer

---

**🎯 Dashboard Status**: ✅ Live and Updated  
**📅 Last Updated**: Generated automatically  
**🔍 Data Accuracy**: Verified against official P&L Account