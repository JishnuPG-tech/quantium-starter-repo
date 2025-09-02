
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('processed_transaction_data.csv')
df['date'] = pd.to_datetime(df['date'])

app = dash.Dash(__name__)

# Modern dark theme styling
app.layout = html.Div([
    # Hero Header
    html.Div([
        html.Div([
            html.H1("🥨 Soul Foods", 
                   style={'fontSize': '3.5rem', 'fontWeight': '700', 'marginBottom': '0.5rem', 'color': '#FF6B6B'}),
            html.H2("Pink Morsel Sales Analytics", 
                   style={'fontSize': '1.8rem', 'fontWeight': '300', 'color': '#4ECDC4', 'marginBottom': '1rem'}),
            html.P("Interactive dashboard to analyze sales performance across regions",
                  style={'fontSize': '1.1rem', 'color': '#95A5A6', 'maxWidth': '600px', 'margin': '0 auto'})
        ], style={'textAlign': 'center'})
    ], style={
        'background': 'linear-gradient(135deg, #2C3E50 0%, #34495E 100%)',
        'padding': '4rem 2rem',
        'color': 'white'
    }),
    
    # Main Content
    html.Div([
        # Controls Card
        html.Div([
            html.H3("🎛️ Regional Filter", style={'color': '#2C3E50', 'marginBottom': '1.5rem'}),
            dcc.RadioItems(
                id='region-filter',
                options=[
                    {'label': html.Span(['🌐 ', 'All Regions'], style={'fontSize': '1.1rem'}), 'value': 'all'},
                    {'label': html.Span(['🧭 ', 'North'], style={'fontSize': '1.1rem'}), 'value': 'north'},
                    {'label': html.Span(['🧭 ', 'South'], style={'fontSize': '1.1rem'}), 'value': 'south'},
                    {'label': html.Span(['🧭 ', 'East'], style={'fontSize': '1.1rem'}), 'value': 'east'},
                    {'label': html.Span(['🧭 ', 'West'], style={'fontSize': '1.1rem'}), 'value': 'west'}
                ],
                value='all',
                labelStyle={'display': 'block', 'marginBottom': '1rem', 'cursor': 'pointer'},
                inputStyle={'marginRight': '0.8rem', 'transform': 'scale(1.2)'}
            )
        ], className='control-card'),
        
        # Chart Card
        html.Div([
            dcc.Graph(id='sales-chart')
        ], className='chart-card'),
        
        # Insights Card
        html.Div([
            html.H3("💡 Business Insights", style={'color': '#2C3E50', 'marginBottom': '1.5rem'}),
            html.Div(id='insights-content')
        ], className='insights-card')
        
    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '2rem'})
    
], style={'backgroundColor': '#F8F9FA', 'minHeight': '100vh', 'fontFamily': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif'})

# Enhanced callback with animations
@app.callback(
    [Output('sales-chart', 'figure'),
     Output('insights-content', 'children')],
    [Input('region-filter', 'value')]
)
def update_dashboard(selected_region):
    # Data filtering logic (same as before)
    if selected_region == 'all':
        filtered_df = df.groupby('date')['sales'].sum().reset_index()
        title = "📊 Pink Morsel Sales - All Regions"
    else:
        region_data = df[df['region'] == selected_region]
        filtered_df = region_data.groupby('date')['sales'].sum().reset_index()
        title = f"📊 Pink Morsel Sales - {selected_region.title()} Region"
    
    # Create modern chart
    fig = px.line(filtered_df, x='date', y='sales', title=title)
    
    # Modern styling
    fig.update_traces(
        line=dict(color='#FF6B6B', width=3),
        fill='tonexty',
        fillcolor='rgba(255, 107, 107, 0.1)'
    )
    
    # Add price increase marker
    price_date = pd.to_datetime('2021-01-15')
    fig.add_vline(
        x=price_date.timestamp() * 1000,
        line_dash="dash",
        line_color="#4ECDC4",
        line_width=3,
        annotation_text="💰 Price Increase<br>Jan 15, 2021",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title_font_size=18,
        title_font_color='#2C3E50',
        height=450,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family='"Segoe UI", sans-serif',
        showlegend=False,
        hovermode='x unified'
    )
    
    # Calculate insights
    before = filtered_df[filtered_df['date'] < price_date]['sales'].mean()
    after = filtered_df[filtered_df['date'] >= price_date]['sales'].mean()
    
    if pd.notna(before) and pd.notna(after):
        change = after - before
        change_pct = (change / before) * 100
        
        if change > 0:
            icon, color, direction = "📈", "#27AE60", "increased"
        else:
            icon, color, direction = "📉", "#E74C3C", "decreased"
        
        insights = html.Div([
            html.Div([
                html.H4(f"Before: ${before:,.0f}", style={'color': '#7F8C8D'}),
                html.H4(f"After: ${after:,.0f}", style={'color': color}),
                html.H3([icon, f" {direction.title()} {abs(change_pct):.1f}%"], 
                       style={'color': color, 'fontWeight': 'bold'})
            ], style={'display': 'flex', 'justifyContent': 'space-around', 'textAlign': 'center'})
        ])
    else:
        insights = html.P("Select a region to view analysis", style={'textAlign': 'center', 'fontStyle': 'italic'})
    
    return fig, insights

# CSS styling
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .control-card, .chart-card, .insights-card {
                background: white;
                border-radius: 15px;
                padding: 2rem;
                margin-bottom: 2rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }
            .control-card:hover, .chart-card:hover, .insights-card:hover {
                transform: translateY(-5px);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
