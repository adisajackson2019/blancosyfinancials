"""
Official Blancosy Financial Data Processor
=========================================
Uses the official financial statements as the authoritative source
Matches the official P&L Account figures exactly
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)

class OfficialBlancosyDataProcessor:
    """Uses official financial statements as authoritative source"""
    
    def __init__(self):
        self.consolidated_data: Optional[pd.DataFrame] = None
        
    def load_and_clean_data(self) -> bool:
        """Load data using official financial statements as primary source"""
        logger.info("📥 Loading financial data using OFFICIAL P&L figures...")
        
        all_data = []
        success = False
        
        # Create 2024 data based on official P&L figures
        try:
            logger.info("Creating 2024 data from official P&L...")
            
            # Revenue - Sales: KES 22,619,122
            sales_data = {
                'Date': pd.to_datetime('2024-12-31'),  # Year-end summary
                'Amount': 22619122,
                'Year': 2024,
                'Category': 'Sales',
                'Type': 'Income',
                'Details': 'Total Sales Revenue (Official P&L)'
            }
            all_data.append(pd.DataFrame([sales_data]))
            
            # Cost of Sales - Stock Purchase: KES 17,244,564
            cogs_data = {
                'Date': pd.to_datetime('2024-12-31'),
                'Amount': 17244564,
                'Year': 2024,
                'Category': 'Stock Purchase',
                'Type': 'Expense',
                'Details': 'Cost of Goods Sold - Purchases (Official P&L)'
            }
            all_data.append(pd.DataFrame([cogs_data]))
            
            # Operating Expenses from Official P&L
            expenses_2024 = [
                {'Category': 'Labour', 'Amount': 601155, 'Details': 'Labour Expenses (Official P&L)'},
                {'Category': 'Rent', 'Amount': 192000, 'Details': 'Rent Expenses (Official P&L)'},
                {'Category': 'Transport', 'Amount': 1028770, 'Details': 'Transport Expenses (Official P&L)'},
                {'Category': 'Transaction Costs', 'Amount': 163557.65, 'Details': 'Transaction Costs & Charges (Official P&L)'}
            ]
            
            for expense in expenses_2024:
                expense_data = {
                    'Date': pd.to_datetime('2024-12-31'),
                    'Amount': expense['Amount'],
                    'Year': 2024,
                    'Category': expense['Category'],
                    'Type': 'Expense',
                    'Details': expense['Details']
                }
                all_data.append(pd.DataFrame([expense_data]))
            
            logger.info("  ✅ 2024 Official P&L data created")
            success = True
            
        except Exception as e:
            logger.error(f"❌ Error creating 2024 official data: {e}")
        
        # Load detailed 2025 transaction data (keep existing logic)
        try:
            logger.info("Loading detailed 2025 transaction data...")
            
            # Sales 2025
            try:
                df = pd.read_excel("blancosy book of accounts 2025.xlsx", sheet_name='Sales')
                df.columns = ['Date', 'Value_Date', 'Withdrawals', 'Amount', 'Details']
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
                df = df.dropna(subset=['Date', 'Amount'])
                df['Year'] = 2025
                df['Category'] = 'Sales'
                df['Type'] = 'Income'
                df = df[['Date', 'Amount', 'Year', 'Category', 'Type', 'Details']]
                all_data.append(df)
                logger.info(f"  ✅ Sales 2025: {len(df)} transactions")
                success = True
            except Exception as e:
                logger.error(f"  ❌ Error loading Sales 2025: {e}")
            
            # Labour 2025
            try:
                df = pd.read_excel("blancosy book of accounts 2025.xlsx", sheet_name='Labour')
                df['Tran Date'] = pd.to_datetime(df['Tran Date'], errors='coerce')
                df = df.dropna(subset=['Tran Date', 'Withdrawals'])
                df = df.rename(columns={'Tran Date': 'Date', 'Withdrawals': 'Amount', 'Transaction Narrative': 'Details'})
                df['Year'] = 2025
                df['Category'] = 'Labour'
                df['Type'] = 'Expense'
                df = df[['Date', 'Amount', 'Year', 'Category', 'Type', 'Details']]
                all_data.append(df)
                logger.info(f"  ✅ Labour 2025: {len(df)} transactions")
                success = True
            except Exception as e:
                logger.error(f"  ❌ Error loading Labour 2025: {e}")
            
            # Rent 2025
            try:
                df = pd.read_excel("blancosy book of accounts 2025.xlsx", sheet_name='rent')
                df = df.iloc[1:].copy()
                df.columns = ['Date1', 'Date', 'Amount', 'Col3', 'Details']
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
                df = df.dropna(subset=['Date', 'Amount'])
                df['Year'] = 2025
                df['Category'] = 'Rent'
                df['Type'] = 'Expense'
                df = df[['Date', 'Amount', 'Year', 'Category', 'Type', 'Details']]
                all_data.append(df)
                logger.info(f"  ✅ Rent 2025: {len(df)} transactions")
                success = True
            except Exception as e:
                logger.error(f"  ❌ Error loading Rent 2025: {e}")
            
            # Purchase of stock 2025
            try:
                df = pd.read_excel("blancosy book of accounts 2025.xlsx", sheet_name='Purchase of stock')
                df['Tran Date'] = pd.to_datetime(df['Tran Date'], errors='coerce')
                df = df.dropna(subset=['Tran Date', 'Deposits'])
                df = df.rename(columns={'Tran Date': 'Date', 'Deposits': 'Amount', 'Transaction Narrative': 'Details'})
                df['Year'] = 2025
                df['Category'] = 'Stock Purchase'
                df['Type'] = 'Expense'
                df = df[['Date', 'Amount', 'Year', 'Category', 'Type', 'Details']]
                all_data.append(df)
                logger.info(f"  ✅ Stock Purchase 2025: {len(df)} transactions")
                success = True
            except Exception as e:
                logger.error(f"  ❌ Error loading Stock Purchase 2025: {e}")
            
            # Utilities 2025
            try:
                df = pd.read_excel("blancosy book of accounts 2025.xlsx", sheet_name='Utilities')
                df['Tran Date'] = pd.to_datetime(df['Tran Date'], errors='coerce')
                df['Amount'] = df['Withdrawals'].fillna(0) + df['Deposits'].fillna(0)
                df = df.dropna(subset=['Tran Date'])
                df = df[df['Amount'] > 0]
                df = df.rename(columns={'Tran Date': 'Date', 'Transaction Narrative': 'Details'})
                df['Year'] = 2025
                df['Category'] = 'Utilities'
                df['Type'] = 'Expense'
                df = df[['Date', 'Amount', 'Year', 'Category', 'Type', 'Details']]
                all_data.append(df)
                logger.info(f"  ✅ Utilities 2025: {len(df)} transactions")
                success = True
            except Exception as e:
                logger.error(f"  ❌ Error loading Utilities 2025: {e}")
            
            # Savings 2025
            try:
                df = pd.read_excel("blancosy book of accounts 2025.xlsx", sheet_name='Saving')
                df['Tran Date'] = pd.to_datetime(df['Tran Date'], errors='coerce')
                
                # Income from deposits
                income_df = df[df['Deposits'].notna() & (df['Deposits'] > 0)].copy()
                if len(income_df) > 0:
                    income_df = income_df.rename(columns={'Tran Date': 'Date', 'Deposits': 'Amount', 'Transaction Narrative': 'Details'})
                    income_df['Year'] = 2025
                    income_df['Category'] = 'Savings'
                    income_df['Type'] = 'Income'
                    income_df = income_df[['Date', 'Amount', 'Year', 'Category', 'Type', 'Details']]
                    all_data.append(income_df)
                    logger.info(f"  ✅ Savings Income 2025: {len(income_df)} transactions")
                
                # Expenses from withdrawals
                expense_df = df[df['Withdrawals'].notna() & (df['Withdrawals'] > 0)].copy()
                if len(expense_df) > 0:
                    expense_df = expense_df.rename(columns={'Tran Date': 'Date', 'Withdrawals': 'Amount', 'Transaction Narrative': 'Details'})
                    expense_df['Year'] = 2025
                    expense_df['Category'] = 'Savings Withdrawal'
                    expense_df['Type'] = 'Expense'
                    expense_df = expense_df[['Date', 'Amount', 'Year', 'Category', 'Type', 'Details']]
                    all_data.append(expense_df)
                    logger.info(f"  ✅ Savings Withdrawals 2025: {len(expense_df)} transactions")
                
                success = True
            except Exception as e:
                logger.error(f"  ❌ Error loading Savings 2025: {e}")
            
            # Other Expenses 2025
            try:
                df = pd.read_excel("blancosy book of accounts 2025.xlsx", sheet_name='Expense')
                df['Tran Date'] = pd.to_datetime(df['Tran Date'], errors='coerce')
                df = df.dropna(subset=['Tran Date', 'Withdrawals'])
                df = df.rename(columns={'Tran Date': 'Date', 'Withdrawals': 'Amount', 'Transaction Narrative': 'Details'})
                df['Year'] = 2025
                df['Category'] = 'Other Expenses'
                df['Type'] = 'Expense'
                df = df[['Date', 'Amount', 'Year', 'Category', 'Type', 'Details']]
                all_data.append(df)
                logger.info(f"  ✅ Other Expenses 2025: {len(df)} transactions")
                success = True
            except Exception as e:
                logger.error(f"  ❌ Error loading Other Expenses 2025: {e}")
                
        except Exception as e:
            logger.error(f"❌ Error loading 2025 file: {e}")
        
        # Consolidate all data
        if all_data and success:
            self.consolidated_data = pd.concat(all_data, ignore_index=True)
            self.consolidated_data['Date'] = pd.to_datetime(self.consolidated_data['Date'])
            self.consolidated_data['Month'] = self.consolidated_data['Date'].dt.to_period('M').astype(str)
            self.consolidated_data['Quarter'] = self.consolidated_data['Date'].dt.to_period('Q').astype(str)
            
            logger.info(f"🎉 Successfully consolidated {len(self.consolidated_data)} transactions")
            logger.info(f"📅 Date range: {self.consolidated_data['Date'].min()} to {self.consolidated_data['Date'].max()}")
            logger.info(f"🏷️ Categories: {', '.join(sorted(self.consolidated_data['Category'].unique()))}")
            logger.info(f"📊 Years: {sorted(self.consolidated_data['Year'].unique())}")
            
            # Show summary by category and type
            summary = self.consolidated_data.groupby(['Category', 'Type']).agg({
                'Amount': ['count', 'sum']
            }).round(2)
            logger.info(f"📋 OFFICIAL Data Summary:\\n{summary}")
            
        else:
            logger.warning("⚠️ No data could be loaded and cleaned")
        
        return success
    
    def get_consolidated_data(self) -> Optional[pd.DataFrame]:
        """Get the consolidated dataset"""
        return self.consolidated_data
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary statistics of the loaded data"""
        if self.consolidated_data is None:
            return {}
        
        summary = {
            'total_transactions': len(self.consolidated_data),
            'date_range': {
                'start': self.consolidated_data['Date'].min(),
                'end': self.consolidated_data['Date'].max()
            },
            'categories': sorted(self.consolidated_data['Category'].unique().tolist()),
            'years': sorted(self.consolidated_data['Year'].unique().tolist()),
            'transaction_types': sorted(self.consolidated_data['Type'].unique().tolist())
        }
        
        # Add year-wise breakdown
        summary['year_breakdown'] = {}
        for year in summary['years']:
            year_data = self.consolidated_data[self.consolidated_data['Year'] == year]
            summary['year_breakdown'][year] = {
                'transactions': len(year_data),
                'total_income': year_data[year_data['Type'] == 'Income']['Amount'].sum(),
                'total_expenses': year_data[year_data['Type'] == 'Expense']['Amount'].sum()
            }
        
        return summary
    
    def filter_data(self, year: Optional[int] = None, 
                   categories: Optional[List[str]] = None,
                   transaction_type: Optional[str] = None) -> pd.DataFrame:
        """Filter consolidated data based on criteria"""
        if self.consolidated_data is None:
            return pd.DataFrame()
        
        filtered_data = self.consolidated_data.copy()
        
        if year and year != 'both':
            filtered_data = filtered_data[filtered_data['Year'] == year]
        
        if categories:
            filtered_data = filtered_data[filtered_data['Category'].isin(categories)]
        
        if transaction_type and transaction_type != 'both':
            filtered_data = filtered_data[filtered_data['Type'] == transaction_type]
        
        return filtered_data
    
    def calculate_kpis(self, filtered_data: pd.DataFrame) -> Dict[str, float]:
        """Calculate key performance indicators"""
        if filtered_data.empty:
            return {
                'total_income': 0,
                'total_expenses': 0,
                'net_profit': 0,
                'profit_margin': 0
            }
        
        total_income = filtered_data[filtered_data['Type'] == 'Income']['Amount'].sum()
        total_expenses = filtered_data[filtered_data['Type'] == 'Expense']['Amount'].sum()
        net_profit = total_income - total_expenses
        profit_margin = (net_profit / total_income * 100) if total_income > 0 else 0
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_profit': net_profit,
            'profit_margin': profit_margin
        }
    
    def get_official_2024_summary(self) -> Dict[str, float]:
        """Get the official 2024 P&L summary"""
        return {
            'sales': 22619122,
            'cogs': 17244564,
            'gross_profit': 5374558,
            'labour': 601155,
            'rent': 192000,
            'transport': 1028770,
            'transaction_costs': 163557.65,
            'total_operating_expenses': 1985482.65,
            'net_profit': 3389075.35,
            'gross_profit_margin': 23.8,
            'net_profit_margin': 15.0
        }

# Test the official processor
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    processor = OfficialBlancosyDataProcessor()
    success = processor.load_and_clean_data()
    
    if success:
        data = processor.get_consolidated_data()
        summary = processor.get_data_summary()
        official_2024 = processor.get_official_2024_summary()
        
        print("\\n" + "="*60)
        print("OFFICIAL BLANCOSY FINANCIAL DATA")
        print("="*60)
        print(f"Total transactions: {summary['total_transactions']}")
        print(f"Date range: {summary['date_range']['start']} to {summary['date_range']['end']}")
        print(f"Categories: {', '.join(summary['categories'])}")
        print(f"Years: {summary['years']}")
        
        print("\\n" + "="*60)
        print("OFFICIAL 2024 P&L SUMMARY (KES)")
        print("="*60)
        print(f"Sales Revenue:           {official_2024['sales']:>12,.0f}")
        print(f"Cost of Goods Sold:      {official_2024['cogs']:>12,.0f}")
        print(f"Gross Profit:            {official_2024['gross_profit']:>12,.0f}")
        print(f"")
        print(f"Operating Expenses:")
        print(f"  Labour:                {official_2024['labour']:>12,.0f}")
        print(f"  Rent:                  {official_2024['rent']:>12,.0f}")
        print(f"  Transport:             {official_2024['transport']:>12,.0f}")
        print(f"  Transaction Costs:     {official_2024['transaction_costs']:>12,.2f}")
        print(f"Total Operating Exp:     {official_2024['total_operating_expenses']:>12,.2f}")
        print(f"")
        print(f"NET PROFIT:              {official_2024['net_profit']:>12,.2f}")
        print(f"")
        print(f"Gross Profit Margin:     {official_2024['gross_profit_margin']:>11.1f}%")
        print(f"Net Profit Margin:       {official_2024['net_profit_margin']:>11.1f}%")
        
        for year, breakdown in summary['year_breakdown'].items():
            print(f"\\n{year} Summary:")
            print(f"  Transactions: {breakdown['transactions']}")
            print(f"  Income: KES {breakdown['total_income']:,.0f}")
            print(f"  Expenses: KES {breakdown['total_expenses']:,.0f}")
            print(f"  Net Profit: KES {breakdown['total_income'] - breakdown['total_expenses']:,.0f}")
    else:
        print("Failed to load data correctly")
