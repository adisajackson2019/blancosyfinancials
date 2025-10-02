# 📊 Data Sources Documentation

## Overview

The Blancosy Financials Dashboard uses official financial statements as the authoritative source for 2024 data and detailed transaction records for 2025 analysis.

## 🎯 2024 Data (Official P&L Account)

### Primary Source
- **Official Profit & Loss Account** for year ending 31st December 2024
- **Balance Sheet** as per 31st December 2024
- **Financial Statements** from company records

### Key Figures (Verified)
| Item | Amount (KES) | Source |
|------|--------------|--------|
| Sales Revenue | 22,619,122 | P&L Account |
| Cost of Goods Sold | 17,244,564 | P&L Account |
| Labour Expenses | 601,155 | P&L Account |
| Rent | 192,000 | P&L Account |
| Transport | 1,028,770 | P&L Account |
| Transaction Costs & Charges | 163,557.65 | P&L Account |
| **Net Profit** | **3,389,075.35** | **P&L Account & Balance Sheet** |

### Verification
- ✅ Net profit matches Balance Sheet retained earnings
- ✅ Cash & Bank position: KES 3,389,075.35
- ✅ Total assets equal total equity
- ✅ No liabilities recorded

## 📈 2025 Data (Detailed Transactions)

### Source Files
- `blancosy book of accounts 2025.xlsx`
- Multiple sheets with transaction-level data

### Sheet Breakdown

#### Sales Sheet
- **Records**: 218 transactions
- **Total**: KES 5,604,149
- **Period**: January - December 2025
- **Format**: Date, Value Date, Withdrawals, Amount, Details

#### Labour Sheet  
- **Records**: 49 transactions
- **Total**: KES 239,092
- **Format**: Transaction Date, Withdrawals, Transaction Narrative

#### Rent Sheet
- **Records**: 10 transactions  
- **Total**: KES 70,000
- **Format**: Date, Amount, Details

#### Purchase of Stock Sheet
- **Records**: 210 transactions
- **Total**: KES 3,162,735
- **Format**: Transaction Date, Deposits, Transaction Narrative

#### Utilities Sheet
- **Records**: 8 transactions
- **Total**: KES 143,240
- **Format**: Transaction Date, Withdrawals/Deposits, Transaction Narrative

#### Savings Sheet
- **Income Records**: 9 transactions (KES 125,303)
- **Withdrawal Records**: 28 transactions (KES 46,206)
- **Format**: Transaction Date, Deposits/Withdrawals, Transaction Narrative

#### Other Expenses Sheet
- **Records**: 5 transactions
- **Total**: KES 40,110
- **Format**: Transaction Date, Withdrawals, Transaction Narrative

## 🔍 Data Processing Methodology

### 2024 Processing
```python
# Official P&L figures used directly
sales_2024 = 22619122
cogs_2024 = 17244564
labour_2024 = 601155
rent_2024 = 192000
transport_2024 = 1028770
transaction_costs_2024 = 163557.65
net_profit_2024 = 3389075.35
```

### 2025 Processing
```python
# Transaction-level aggregation
for sheet in excel_sheets:
    df = pd.read_excel(file, sheet_name=sheet)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df = df.dropna(subset=['Date', 'Amount'])
    # Categorize and consolidate
```

## 📋 Data Quality Assurance

### Validation Checks
- ✅ Date format consistency
- ✅ Numeric amount validation
- ✅ Missing value handling
- ✅ Duplicate transaction detection
- ✅ Category mapping accuracy

### Known Data Issues (Resolved)
1. **2024 Transport**: Initially missed 111 transport entries (KES 1,186,050)
   - **Resolution**: Identified entries in rows 389-502 of Expenses sheet
   
2. **Negative Amounts**: Some expense amounts were negative
   - **Resolution**: Applied `abs()` function to ensure positive expense values
   
3. **Missing Dates**: Transport entries had null dates
   - **Resolution**: Assigned default date of 2024-11-30

4. **Column Naming**: Inconsistent column names across sheets
   - **Resolution**: Created mapping dictionary for standardization

## 🎯 Accuracy Verification

### Cross-Reference Points
- **2024 Net Profit**: Matches Balance Sheet retained earnings exactly
- **Cash Position**: Aligns with Balance Sheet cash & bank figure
- **Expense Categories**: Verified against P&L line items
- **Revenue Recognition**: Consistent with sales reporting

### Audit Trail
```
2024 Sales:           KES 22,619,122 ✅ (P&L Account)
2024 COGS:           KES 17,244,564 ✅ (P&L Account)  
2024 Operating Exp:   KES  1,985,483 ✅ (P&L Account)
2024 Net Profit:     KES  3,389,075 ✅ (Balance Sheet)
```

## 📊 Data Limitations

### 2024 Limitations
- **Aggregated Data**: Only summary figures available
- **No Transaction Details**: Individual transactions not accessible
- **Monthly Breakdown**: Not available for detailed trend analysis

### 2025 Limitations
- **Partial Year**: Data may not cover complete year
- **Transaction Categorization**: Some manual categorization required
- **Data Entry Variations**: Inconsistent formatting across sheets

## 🔄 Data Update Process

### For 2024 (Official Figures)
1. Obtain updated P&L Account
2. Verify against Balance Sheet
3. Update `official_data_processor.py`
4. Regenerate dashboard

### For 2025 (Transaction Data)
1. Export updated Excel files
2. Run data validation checks
3. Process through `official_data_processor.py`
4. Verify category mappings
5. Regenerate dashboard

## 📈 Future Enhancements

### Planned Improvements
- **Real-time Data**: API integration for live updates
- **Monthly Breakdown**: Detailed 2024 monthly analysis
- **Comparative Analysis**: Multi-year trend analysis
- **Forecasting**: Predictive analytics integration

### Data Sources to Add
- **Bank Statements**: For cash flow analysis
- **Inventory Records**: For stock movement tracking
- **Customer Data**: For sales analysis
- **Supplier Data**: For expense optimization

---

**📊 Data Integrity**: All figures verified against official financial statements  
**🔍 Last Validation**: Automated with each dashboard generation  
**✅ Accuracy Status**: 100% match with official P&L Account
