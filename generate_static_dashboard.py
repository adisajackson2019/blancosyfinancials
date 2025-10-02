"""
Generate Static Dashboard for GitHub Pages
==========================================
Creates a static HTML dashboard with embedded charts and data
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
import json
from official_data_processor import OfficialBlancosyDataProcessor

class StaticDashboardGenerator:
    """Generate static dashboard for GitHub Pages deployment"""
    
    def __init__(self):
        self.data_processor = OfficialBlancosyDataProcessor()
        self.consolidated_data = None
        self.official_2024 = None
        
    def load_data(self):
        """Load official data"""
        print("📊 Loading official data for static dashboard...")
        success = self.data_processor.load_and_clean_data()
        
        if success:
            self.consolidated_data = self.data_processor.get_consolidated_data()
            self.official_2024 = self.data_processor.get_official_2024_summary()
            print(f"✅ Loaded {len(self.consolidated_data)} transactions")
            return True
        else:
            print("❌ Failed to load data")
            return False
    
    def create_waterfall_chart(self):
        """Create 2024 P&L waterfall chart"""
        fig = go.Figure(go.Waterfall(
            name="2024 P&L",
            orientation="v",
            measure=["absolute", "relative", "relative", "relative", "relative", "relative", "total"],
            x=["Sales", "COGS", "Labour", "Rent", "Transport", "Transaction Costs", "Net Profit"],
            textposition="outside",
            text=[f"KES {self.official_2024['sales']:,.0f}", 
                  f"-KES {self.official_2024['cogs']:,.0f}",
                  f"-KES {self.official_2024['labour']:,.0f}",
                  f"-KES {self.official_2024['rent']:,.0f}",
                  f"-KES {self.official_2024['transport']:,.0f}",
                  f"-KES {self.official_2024['transaction_costs']:,.0f}",
                  f"KES {self.official_2024['net_profit']:,.0f}"],
            y=[self.official_2024['sales'], 
               -self.official_2024['cogs'],
               -self.official_2024['labour'],
               -self.official_2024['rent'],
               -self.official_2024['transport'],
               -self.official_2024['transaction_costs'],
               self.official_2024['net_profit']],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        
        fig.update_layout(
            title="2024 Official P&L Waterfall Analysis",
            showlegend=False,
            template='plotly_white',
            height=500,
            font=dict(size=12)
        )
        
        return fig
    
    def create_expense_pie_chart(self):
        """Create 2024 expense breakdown pie chart"""
        expenses = {
            'Stock Purchase (COGS)': self.official_2024['cogs'],
            'Transport': self.official_2024['transport'],
            'Labour': self.official_2024['labour'],
            'Rent': self.official_2024['rent'],
            'Transaction Costs': self.official_2024['transaction_costs']
        }
        
        fig = px.pie(
            values=list(expenses.values()),
            names=list(expenses.keys()),
            title="2024 Official Expense Breakdown",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(template='plotly_white', height=500, font=dict(size=12))
        
        return fig
    
    def create_yoy_comparison(self):
        """Create year-over-year comparison chart"""
        summary = self.data_processor.get_data_summary()
        
        years = []
        income = []
        expenses = []
        
        for year, breakdown in summary['year_breakdown'].items():
            years.append(year)
            income.append(breakdown['total_income'])
            expenses.append(breakdown['total_expenses'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Income',
            x=years,
            y=income,
            marker_color='#28a745',
            text=[f'KES {val:,.0f}' for val in income],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            name='Expenses',
            x=years,
            y=expenses,
            marker_color='#dc3545',
            text=[f'KES {val:,.0f}' for val in expenses],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Year-over-Year Financial Performance",
            xaxis_title="Year",
            yaxis_title="Amount (KES)",
            barmode='group',
            template='plotly_white',
            height=500,
            font=dict(size=12)
        )
        
        return fig
    
    def create_monthly_trends(self):
        """Create monthly trends chart for 2025"""
        data_2025 = self.consolidated_data[self.consolidated_data['Year'] == 2025].copy()
        
        if data_2025.empty:
            return go.Figure()
        
        # Group by month and type
        data_2025['Month'] = data_2025['Date'].dt.to_period('M').astype(str)
        monthly_data = data_2025.groupby(['Month', 'Type'])['Amount'].sum().reset_index()
        
        fig = go.Figure()
        
        for transaction_type in ['Income', 'Expense']:
            type_data = monthly_data[monthly_data['Type'] == transaction_type]
            color = '#28a745' if transaction_type == 'Income' else '#dc3545'
            
            fig.add_trace(go.Scatter(
                x=type_data['Month'],
                y=type_data['Amount'],
                mode='lines+markers',
                name=transaction_type,
                line=dict(color=color, width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title="2025 Monthly Financial Trends",
            xaxis_title="Month",
            yaxis_title="Amount (KES)",
            template='plotly_white',
            height=500,
            font=dict(size=12),
            hovermode='x unified'
        )
        
        return fig
    
    def generate_data_json(self):
        """Generate JSON data for the dashboard"""
        summary = self.data_processor.get_data_summary()
        
        # Create summary data
        dashboard_data = {
            'official_2024': self.official_2024,
            'summary': {
                'total_transactions': summary['total_transactions'],
                'years': summary['years'],
                'categories': summary['categories'],
                'year_breakdown': summary['year_breakdown']
            },
            'key_metrics': {
                '2024_net_profit': self.official_2024['net_profit'],
                '2024_profit_margin': self.official_2024['net_profit_margin'],
                '2024_gross_margin': self.official_2024['gross_profit_margin'],
                'total_revenue_2024': self.official_2024['sales'],
                'total_expenses_2024': self.official_2024['total_operating_expenses'] + self.official_2024['cogs']
            }
        }
        
        return dashboard_data
    
    def generate_static_dashboard(self):
        """Generate complete static dashboard HTML"""
        if not self.load_data():
            return False
        
        print("🎨 Creating charts...")
        
        # Generate all charts
        waterfall_chart = self.create_waterfall_chart()
        expense_pie = self.create_expense_pie_chart()
        yoy_chart = self.create_yoy_comparison()
        monthly_trends = self.create_monthly_trends()
        
        # Convert charts to HTML
        waterfall_html = pyo.plot(waterfall_chart, output_type='div', include_plotlyjs=False)
        expense_html = pyo.plot(expense_pie, output_type='div', include_plotlyjs=False)
        yoy_html = pyo.plot(yoy_chart, output_type='div', include_plotlyjs=False)
        monthly_html = pyo.plot(monthly_trends, output_type='div', include_plotlyjs=False)
        
        # Generate data
        dashboard_data = self.generate_data_json()
        
        # Create HTML template
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blancosy Financials - Official Analysis Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            background-color: #f8f9fa;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .hero-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 0;
            margin-bottom: 40px;
        }}
        .metric-card {{
            transition: transform 0.2s;
            border: none;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
        }}
        .chart-container {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .footer {{
            background-color: #343a40;
            color: white;
            padding: 40px 0;
            margin-top: 60px;
        }}
        .badge-custom {{
            font-size: 0.9em;
            padding: 8px 12px;
        }}
    </style>
</head>
<body>
    <!-- Hero Section -->
    <div class="hero-section">
        <div class="container">
            <div class="row">
                <div class="col-lg-8 mx-auto text-center">
                    <h1 class="display-4 fw-bold mb-4">
                        <i class="fas fa-chart-line me-3"></i>Blancosy Financials
                    </h1>
                    <p class="lead mb-4">Official Financial Analysis Dashboard</p>
                    <span class="badge bg-light text-dark badge-custom">
                        <i class="fas fa-calendar me-2"></i>Based on Official P&L Account & Balance Sheet
                    </span>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <!-- Key Metrics -->
        <div class="row mb-5">
            <div class="col-md-3 mb-4">
                <div class="card metric-card h-100 border-success">
                    <div class="card-body text-center">
                        <i class="fas fa-dollar-sign fa-2x text-success mb-3"></i>
                        <h4 class="text-success">KES {dashboard_data['official_2024']['sales']:,.0f}</h4>
                        <p class="card-text">2024 Sales Revenue</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-4">
                <div class="card metric-card h-100 border-info">
                    <div class="card-body text-center">
                        <i class="fas fa-chart-pie fa-2x text-info mb-3"></i>
                        <h4 class="text-info">KES {dashboard_data['official_2024']['gross_profit']:,.0f}</h4>
                        <p class="card-text">Gross Profit</p>
                        <small class="text-muted">{dashboard_data['official_2024']['gross_profit_margin']:.1f}% Margin</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-4">
                <div class="card metric-card h-100 border-primary">
                    <div class="card-body text-center">
                        <i class="fas fa-trophy fa-2x text-primary mb-3"></i>
                        <h4 class="text-primary">KES {dashboard_data['official_2024']['net_profit']:,.0f}</h4>
                        <p class="card-text">Net Profit (Official)</p>
                        <small class="text-muted">{dashboard_data['official_2024']['net_profit_margin']:.1f}% Margin</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-4">
                <div class="card metric-card h-100 border-warning">
                    <div class="card-body text-center">
                        <i class="fas fa-database fa-2x text-warning mb-3"></i>
                        <h4 class="text-warning">{dashboard_data['summary']['total_transactions']}</h4>
                        <p class="card-text">Total Transactions</p>
                        <small class="text-muted">2024-2025</small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Charts Row 1 -->
        <div class="row mb-4">
            <div class="col-lg-8">
                <div class="chart-container">
                    <h5 class="mb-3"><i class="fas fa-chart-bar me-2"></i>2024 Official P&L Waterfall Analysis</h5>
                    {waterfall_html}
                </div>
            </div>
            <div class="col-lg-4">
                <div class="chart-container">
                    <h5 class="mb-3"><i class="fas fa-chart-pie me-2"></i>2024 Expense Breakdown</h5>
                    {expense_html}
                </div>
            </div>
        </div>

        <!-- Charts Row 2 -->
        <div class="row mb-4">
            <div class="col-lg-6">
                <div class="chart-container">
                    <h5 class="mb-3"><i class="fas fa-chart-line me-2"></i>Year-over-Year Comparison</h5>
                    {yoy_html}
                </div>
            </div>
            <div class="col-lg-6">
                <div class="chart-container">
                    <h5 class="mb-3"><i class="fas fa-chart-area me-2"></i>2025 Monthly Trends</h5>
                    {monthly_html}
                </div>
            </div>
        </div>

        <!-- Summary Table -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="chart-container">
                    <h5 class="mb-3"><i class="fas fa-table me-2"></i>Financial Summary</h5>
                    <div class="table-responsive">
                        <table class="table table-striped table-hover">
                            <thead class="table-dark">
                                <tr>
                                    <th>Metric</th>
                                    <th>2024 (Official)</th>
                                    <th>2025 (Detailed)</th>
                                    <th>Change</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Sales Revenue</strong></td>
                                    <td>KES {dashboard_data['summary']['year_breakdown'][2024]['total_income']:,.0f}</td>
                                    <td>KES {dashboard_data['summary']['year_breakdown'][2025]['total_income']:,.0f}</td>
                                    <td class="text-danger">
                                        {((dashboard_data['summary']['year_breakdown'][2025]['total_income'] - dashboard_data['summary']['year_breakdown'][2024]['total_income']) / dashboard_data['summary']['year_breakdown'][2024]['total_income'] * 100):+.1f}%
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>Total Expenses</strong></td>
                                    <td>KES {dashboard_data['summary']['year_breakdown'][2024]['total_expenses']:,.0f}</td>
                                    <td>KES {dashboard_data['summary']['year_breakdown'][2025]['total_expenses']:,.0f}</td>
                                    <td class="text-success">
                                        {((dashboard_data['summary']['year_breakdown'][2025]['total_expenses'] - dashboard_data['summary']['year_breakdown'][2024]['total_expenses']) / dashboard_data['summary']['year_breakdown'][2024]['total_expenses'] * 100):+.1f}%
                                    </td>
                                </tr>
                                <tr class="table-info">
                                    <td><strong>Net Profit</strong></td>
                                    <td>KES {dashboard_data['summary']['year_breakdown'][2024]['total_income'] - dashboard_data['summary']['year_breakdown'][2024]['total_expenses']:,.0f}</td>
                                    <td>KES {dashboard_data['summary']['year_breakdown'][2025]['total_income'] - dashboard_data['summary']['year_breakdown'][2025]['total_expenses']:,.0f}</td>
                                    <td class="text-warning">
                                        {(((dashboard_data['summary']['year_breakdown'][2025]['total_income'] - dashboard_data['summary']['year_breakdown'][2025]['total_expenses']) - (dashboard_data['summary']['year_breakdown'][2024]['total_income'] - dashboard_data['summary']['year_breakdown'][2024]['total_expenses'])) / (dashboard_data['summary']['year_breakdown'][2024]['total_income'] - dashboard_data['summary']['year_breakdown'][2024]['total_expenses']) * 100):+.1f}%
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Key Insights -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="chart-container">
                    <h5 class="mb-3"><i class="fas fa-lightbulb me-2"></i>Key Insights</h5>
                    <div class="row">
                        <div class="col-md-4">
                            <div class="alert alert-success">
                                <h6><i class="fas fa-check-circle me-2"></i>Strong Profitability</h6>
                                <p class="mb-0">2024 net profit margin of {dashboard_data['official_2024']['net_profit_margin']:.1f}% indicates healthy business performance.</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="alert alert-info">
                                <h6><i class="fas fa-info-circle me-2"></i>Official Verification</h6>
                                <p class="mb-0">2024 figures match official P&L Account and Balance Sheet exactly.</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="alert alert-warning">
                                <h6><i class="fas fa-exclamation-triangle me-2"></i>Revenue Decline</h6>
                                <p class="mb-0">2025 shows declining revenue trend requiring strategic attention.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <div class="footer">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>Blancosy Financials Dashboard</h5>
                    <p>Official financial analysis based on P&L Account and Balance Sheet data.</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p><i class="fas fa-calendar me-2"></i>Generated: {pd.Timestamp.now().strftime('%B %d, %Y')}</p>
                    <p><i class="fas fa-check-circle me-2"></i>2024 Net Profit: KES {dashboard_data['official_2024']['net_profit']:,.0f}</p>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
        """
        
        return html_template

if __name__ == "__main__":
    generator = StaticDashboardGenerator()
    html_content = generator.generate_static_dashboard()
    
    if html_content:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ Static dashboard generated successfully!")
        print("📁 File created: index.html")
        print("🌐 Ready for GitHub Pages deployment!")
    else:
        print("❌ Failed to generate static dashboard")
