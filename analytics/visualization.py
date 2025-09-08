import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json

# --- Mapping for the Pie Chart ---
# Maps user emails to their roles for easier aggregation.
ROLE_MAP = {
    'farmer1@example.com': 'Farmer',
    'dist1@example.com': 'Distributor',
    'retail1@example.com': 'Retailer'
}

def create_avg_temp_humidity_chart(df: pd.DataFrame):
    """Generates a grouped bar chart for average temperature and humidity per product."""
    if df.empty: return None
    
    # Group by product and calculate the mean for temp/humidity
    stats = df.groupby('product_name')[['temperature', 'humidity']].mean().reset_index()

    fig = go.Figure(data=[
        go.Bar(name='Avg Temperature (°C)', x=stats['product_name'], y=stats['temperature']),
        go.Bar(name='Avg Humidity (%)', x=stats['product_name'], y=stats['humidity'])
    ])
    fig.update_layout(
        title_text='Average Temperature & Humidity per Product',
        barmode='group',
        xaxis_title="Product",
        yaxis_title="Value"
    )
    return json.loads(fig.to_json())

def create_delivery_time_boxplot(journey_details_df: pd.DataFrame):
    """Generates a box plot of delivery times per product."""
    if journey_details_df.empty: return None

    fig = px.box(
        journey_details_df,
        x='duration_hours',
        y='product_name',
        orientation='h',
        title='Time from Harvest to Delivery (Hours)',
        labels={'duration_hours': 'Journey Duration (Hours)', 'product_name': 'Product'}
    )
    fig.update_traces(marker_color='blue')
    return json.loads(fig.to_json())

def create_temp_anomaly_scatter(df: pd.DataFrame, upper_threshold=25.0):
    """Generates a scatter plot of temperature readings over time."""
    if df.empty: return None

    fig = px.scatter(
        df,
        x='timestamp',
        y='temperature',
        color='product_name',
        title='Temperature Readings Over Time',
        labels={'timestamp': 'Date', 'temperature': 'Temperature (°C)'}
    )
    # Add a red line to show the anomaly threshold
    fig.add_hline(y=upper_threshold, line_dash="dot", line_color="red",
                  annotation_text="Anomaly Threshold", annotation_position="bottom right")
    return json.loads(fig.to_json())

def create_stakeholder_pie_chart(df: pd.DataFrame):
    """Generates a pie chart of transactions per stakeholder role."""
    if df.empty: return None
    
    # Map sender emails to roles using the ROLE_MAP
    df['role'] = df['sender'].map(ROLE_MAP)
    
    # Count transactions per role
    role_counts = df['role'].value_counts()
    
    fig = px.pie(
        names=role_counts.index,
        values=role_counts.values,
        title='Transactions per Stakeholder'
    )
    return json.loads(fig.to_json())