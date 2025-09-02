
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load and prepare data
df = pd.read_csv('processed_transaction_data.csv')
df['date'] = pd.to_datetime(df['date'])

# Create the Dash app
app = dash.Dash(__name__)

# Custom CSS styling
app.layout = html.Div([
    # Header Section
    html.Div([
        html.H1("Soul Foods Pink Morsel Sales Dashboard", 
                style={
                    'textAlign': 'center',
                    'marginBottom': '10px',
                    'color': '#FFFFFF',
                    'fontFamily': 'Georgia, serif',
                    'fontSize': '48px',
                    'fontWeight': 'bold',
                    'textShadow': '2px 2px 4px rgba(0,0,0,0.5)'
                }),
        html.H3("Interactive Analysis: Sales Before vs After Price Increase", 
                style={
                    'textAlign': 'center',
                    'color': '#F8F9FA',
                    'fontFamily': 'Georgia, serif',
                    'fontSize': '24px',
                    'fontStyle': 'italic',
                    'marginBottom': '30px'
                })
    ], style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'padding': '40px 20px',
        'borderRadius': '15px',
        'marginBottom': '30px',
        'boxShadow': '0 8px 32px rgba(0,0,0,0.1)'
    }),
    
    # Controls Section
    html.Div([
        html.Div([
            html.H4("📍 Select Region to Analyze:", 
                   style={'color': '#2c3e50', 'marginBottom': '15px', 'fontFamily': 'Arial, sans-serif'}),
            dcc.RadioItems(
                id='region-filter',
                options=[
                    {'label': '🌍 All Regions', 'value': 'all'},
                    {'label': '⬆️ North', 'value': 'north'},
                    {'label': '⬇️ South', 'value': 'south'},
                    {'label': '➡️ East', 'value': 'east'},
                    {'label': '⬅️ West', 'value': 'west'}
                ],
                value='all',
                style={'fontSize': '16px', 'fontFamily': 'Arial, sans-serif'},
                labelStyle={'display': 'block', 'marginBottom': '8px', 'cursor': 'pointer'}
            )
        ], style={
            'backgroundColor': '#f8f9fa',
            'padding': '25px',
            'borderRadius': '10px',
            'border': '2px solid #e9ecef',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
        })
    ], style={'marginBottom': '30px'}),
    
    # Chart Section
    html.Div([
        dcc.Graph(id='sales-chart')
    ], style={
        'backgroundColor': '#ffffff',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
        'border': '1px solid #e9ecef'
    }),
    
    # Insights Section
    html.Div([
        html.H4("🔍 Key Insights", 
               style={'color': '#2c3e50', 'marginBottom': '15px', 'fontFamily': 'Arial, sans-serif'}),
        html.Div(id='insights-content')
    ], style={
        'backgroundColor': '#f8f9fa',
        'padding': '25px',
        'borderRadius': '10px',
        'marginTop': '30px',
        'border': '2px solid #e9ecef',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
    }),
    
    # Footer
    html.Div([
        html.P("📊 Created for Soul Foods | Quantium Data Science Virtual Experience",
               style={'textAlign': 'center', 'color': '#6c757d', 'marginTop': '20px', 'fontStyle': 'italic'})
    ])
    
], style={
    'maxWidth': '1200px',
    'margin': '0 auto',
    'padding': '20px',
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f5f5f5',
    'minHeight': '100vh'
})

# Callback for interactive chart
@app.callback(
    [Output('sales-chart', 'figure'),
     Output('insights-content', 'children')],
    [Input('region-filter', 'value')]
)
def update_chart(selected_region):
    # Filter data based on selection
    if selected_region == 'all':
        filtered_df = df.groupby('date')['sales'].sum().reset_index()
        title_suffix = "All Regions"
        region_text = "all regions combined"
    else:
        region_data = df[df['region'] == selected_region]
        filtered_df = region_data.groupby('date')['sales'].sum().reset_index()
        title_suffix = f"{selected_region.title()} Region"
        region_text = f"the {selected_region} region"
    
    # Create the chart
    fig = px.line(filtered_df, 
                  x='date', 
                  y='sales',
                  title=f'Pink Morsel Sales Over Time - {title_suffix}',
                  labels={'date': 'Date', 'sales': 'Total Daily Sales ($)'})
    
    # Add price increase line
    price_increase_date = pd.to_datetime('2021-01-15')
    fig.add_vline(x=price_increase_date.timestamp() * 1000,
                  line_dash="dash", 
                  line_color="red",
                  line_width=3,
                  annotation_text="Price Increase<br>Jan 15, 2021",
                  annotation_position="top right")
    
    # Style the chart
    fig.update_layout(
        title_font_size=20,
        title_font_color='#2c3e50',
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family="Arial",
        showlegend=False
    )
    
    fig.update_traces(line_color='#667eea', line_width=3)
    
    # Calculate insights
    before_increase = filtered_df[filtered_df['date'] < price_increase_date]['sales'].mean()
    after_increase = filtered_df[filtered_df['date'] >= price_increase_date]['sales'].mean()
    
    if pd.notna(before_increase) and pd.notna(after_increase):
        change = after_increase - before_increase
        change_percent = (change / before_increase) * 100
        
        if change > 0:
            trend_icon = "📈"
            trend_text = "increased"
            trend_color = "#28a745"
        else:
            trend_icon = "📉"
            trend_text = "decreased"
            trend_color = "#dc3545"
        
        insights = html.Div([
            html.P([
                f"🎯 Analysis for {region_text}:",
                html.Br(),
                f"• Average daily sales before price increase: ${before_increase:,.2f}",
                html.Br(),
                f"• Average daily sales after price increase: ${after_increase:,.2f}",
                html.Br(),
                html.Span([
                    f"{trend_icon} Sales {trend_text} by ${abs(change):,.2f} ({abs(change_percent):.1f}%)"
                ], style={'color': trend_color, 'fontWeight': 'bold'})
            ], style={'fontSize': '16px', 'lineHeight': '1.6'})
        ])
    else:
        insights = html.P("Select a region to see detailed analysis.", 
                         style={'fontSize': '16px', 'fontStyle': 'italic'})
    
    return fig, insights

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
