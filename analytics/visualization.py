import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ROLE_MAP = {
    'farmer1@example.com': 'Farmer',
    'dist1@example.com': 'Distributor',
    'retail1@example.com': 'Retailer',
    'consumer1@example.com': 'Consumer',
    'consumer': 'Consumer',
}

def _to_plotly_json(fig):
    fig.update_layout(
        margin=dict(l=40, r=30, t=60, b=40),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(size=12),
    )
    return json.loads(fig.to_json())

def create_avg_temp_humidity_chart(df: pd.DataFrame):
    if df.empty:
        return None

    stats = df.groupby('product_name')[['temperature', 'humidity']].mean().reset_index()
    fig = go.Figure(data=[
        go.Bar(name='Avg Temperature (deg C)', x=stats['product_name'], y=stats['temperature']),
        go.Bar(name='Avg Humidity (%)', x=stats['product_name'], y=stats['humidity'])
    ])
    fig.update_layout(
        title_text='Average Temperature and Humidity by Product',
        barmode='group',
        xaxis_title='Product',
        yaxis_title='Value'
    )
    return _to_plotly_json(fig)

def create_delivery_time_boxplot(journey_details_df: pd.DataFrame):
    if journey_details_df.empty:
        return None

    fig = px.box(
        journey_details_df,
        x='duration_hours',
        y='product_name',
        orientation='h',
        title='Journey Duration Distribution',
        labels={'duration_hours': 'Journey Duration (Hours)', 'product_name': 'Product'}
    )
    fig.update_traces(marker_color='#3498DB')
    return _to_plotly_json(fig)

def create_temp_anomaly_scatter(df: pd.DataFrame, upper_threshold=25.0):
    if df.empty:
        return None

    fig = px.scatter(
        df,
        x='timestamp',
        y='temperature',
        color='product_name',
        hover_data=['status', 'location'],
        title='Temperature Readings Over Time',
        labels={'timestamp': 'Date', 'temperature': 'Temperature (deg C)'}
    )
    fig.add_hline(
        y=upper_threshold,
        line_dash='dot',
        line_color='red',
        annotation_text='Anomaly Threshold',
        annotation_position='bottom right'
    )
    return _to_plotly_json(fig)

def create_stakeholder_pie_chart(df: pd.DataFrame):
    if df.empty:
        return None

    role_series = pd.concat([df['sender'], df['recipient']], ignore_index=True)
    role_counts = role_series.map(ROLE_MAP).fillna('Other').value_counts()
    fig = px.pie(
        names=role_counts.index,
        values=role_counts.values,
        title='Activity by Stakeholder Role',
        hole=0.35
    )
    return _to_plotly_json(fig)

def create_status_distribution_chart(df: pd.DataFrame):
    if df.empty or 'status' not in df.columns:
        return None

    status_counts = df['status'].fillna('Unknown').value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    fig = px.bar(
        status_counts,
        x='status',
        y='count',
        title='Transactions by Status',
        labels={'status': 'Status', 'count': 'Transactions'},
        color='status'
    )
    return _to_plotly_json(fig)

def create_anomalies_by_product_chart(anomalies_df: pd.DataFrame):
    if anomalies_df.empty:
        return None

    counts = anomalies_df['product_name'].fillna('Unknown').value_counts().reset_index()
    counts.columns = ['product_name', 'count']
    fig = px.bar(
        counts,
        x='product_name',
        y='count',
        title='Temperature Anomalies by Product',
        labels={'product_name': 'Product', 'count': 'Anomalies'},
        color='count',
        color_continuous_scale='Reds'
    )
    return _to_plotly_json(fig)
