
import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load the processed data
df = pd.read_csv('processed_transaction_data.csv')
df['date'] = pd.to_datetime(df['date'])

# Create daily sales summary
daily_sales = df.groupby('date')['sales'].sum().reset_index()
daily_sales = daily_sales.sort_values('date')

# Create the Dash app
app = dash.Dash(__name__)

# Create the line chart
fig = px.line(daily_sales, 
              x='date', 
              y='sales',
              title='Pink Morsel Sales Over Time',
              labels={
                  'date': 'Date',
                  'sales': 'Total Daily Sales ($)'
              })

# Add vertical line for price increase date
price_increase_date = pd.to_datetime('2021-01-15')
fig.add_vline(x=price_increase_date.timestamp() * 1000,
              line_dash="dash", 
              line_color="red",
              annotation_text="Price Increase<br>Jan 15, 2021",
              annotation_position="top right")

# Customize appearance
fig.update_layout(
    title_font_size=20,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
    height=600,
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Define the app layout
app.layout = html.Div([
    # Header
    html.H1("Soul Foods Pink Morsel Sales Dashboard", 
            style={
                'textAlign': 'center', 
                'marginBottom': 30, 
                'color': '#2c3e50',
                'fontFamily': 'Arial, sans-serif'
            }),
    
    html.Hr(),
    
    # Subtitle
    html.H3("Analysis: Sales Before vs After Price Increase (January 15, 2021)", 
            style={
                'textAlign': 'center', 
                'marginBottom': 30, 
                'color': '#34495e',
                'fontFamily': 'Arial, sans-serif'
            }),
    
    # The main chart
    dcc.Graph(
        id='sales-line-chart',
        figure=fig
    ),
    
    # Analysis section
    html.Div([
        html.H4("Key Insights:", 
                style={'color': '#2c3e50', 'marginBottom': 15}),
        html.Ul([
            html.Li("Red dashed line marks the Pink Morsel price increase on January 15, 2021"),
            html.Li("This visualization answers: Were sales higher before or after the price increase?"),
            html.Li("Data spans from 2018 to 2022, showing comprehensive sales trends"),
            html.Li("Each point represents total daily sales across all regions (North, South, East, West)")
        ])
    ], style={
        'margin': '20px', 
        'padding': '20px', 
        'backgroundColor': '#f8f9fa', 
        'borderRadius': '5px',
        'fontFamily': 'Arial, sans-serif'
    })
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
