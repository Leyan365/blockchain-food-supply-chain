import pandas as pd

def calculate_journey_stats(df: pd.DataFrame):
    """
    Calculates the total journey time for each product from registration to in-stock.

    Args:
        df (pd.DataFrame): The DataFrame containing all transactions.

    Returns:
        dict: A dictionary containing average, min, and max journey times in hours.
    """
    if df.empty or 'status' not in df.columns or 'timestamp' not in df.columns:
        return {'avg_hours': 0, 'min_hours': 0, 'max_hours': 0, 'details': []}

    # Ensure timestamp is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # Find the start time (Registered) and end time (In Stock) for each product
    journey_times = df.groupby('product_id')['timestamp'].agg(['min', 'max']).reset_index()
    
    # Calculate the duration in hours
    journey_times['duration_hours'] = (journey_times['max'] - journey_times['min']).dt.total_seconds() / 3600
    
    # Get product names to make the results more readable
    product_names = df[['product_id', 'product_name']].drop_duplicates()
    journey_times = pd.merge(journey_times, product_names, on='product_id')
    
    # Calculate overall statistics
    avg_duration = round(journey_times['duration_hours'].mean(), 2)
    min_duration = round(journey_times['duration_hours'].min(), 2)
    max_duration = round(journey_times['duration_hours'].max(), 2)
    
    return {
        'avg_hours': avg_duration,
        'min_hours': min_duration,
        'max_hours': max_duration,
        'details': journey_times.sort_values(by='duration_hours', ascending=False).to_dict('records')
    }