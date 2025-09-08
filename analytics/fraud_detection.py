import pandas as pd

def find_temperature_anomalies(df: pd.DataFrame, upper_threshold: float = 25.0):
    """
    Finds transactions where the temperature exceeds a given threshold.

    Args:
        df (pd.DataFrame): The DataFrame containing all transactions.
        upper_threshold (float): The temperature in Celsius above which is considered an anomaly.

    Returns:
        pd.DataFrame: A DataFrame containing only the anomalous transactions.
    """
    if 'temperature' not in df.columns:
        return pd.DataFrame()

    # Ensure temperature is a numeric type, converting errors to 'Not a Number'
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
    
    # Filter for rows where temperature is above the threshold
    anomalies = df[df['temperature'] > upper_threshold].copy()
    
    # Sort by temperature to see the worst offenders first
    return anomalies.sort_values(by='temperature', ascending=False)