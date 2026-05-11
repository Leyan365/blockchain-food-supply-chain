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


    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
    

    anomalies = df[df['temperature'] > upper_threshold].copy()
    

    return anomalies.sort_values(by='temperature', ascending=False)