import pandas as pd
from services.blockchain_service import blockchain_service
from analytics.fraud_detection import find_temperature_anomalies
from analytics.supply_chain_analytics import calculate_journey_stats
# --- Import the new visualization functions ---
from analytics.visualization import (
    create_avg_temp_humidity_chart,
    create_delivery_time_boxplot,
    create_temp_anomaly_scatter,
    create_stakeholder_pie_chart
)

class AnalyticsService:
    def get_dashboard_analytics(self):
        """
        Gathers all analytical data for the main dashboard, including chart JSON.
        """
        all_txs = blockchain_service.get_all_transactions()
        
        if not all_txs:
            # Return a default empty structure if no data
            return {
                "kpis": {"total_products": 0, "total_anomalies": 0, "avg_journey_hours": 0},
                "anomalies": [],
                "journey_stats": {"details": []},
                "charts": {} # Add empty charts dict
            }

        df = pd.DataFrame(all_txs)
        
        # --- Clean data before analysis and visualization ---
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
        df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
        # Drop rows where essential data for charts is missing
        df.dropna(subset=['temperature', 'humidity'], inplace=True)

        # --- Perform tabular analyses ---
        temp_anomalies_df = find_temperature_anomalies(df.copy())
        journey_stats = calculate_journey_stats(df.copy())
        
        # --- Generate Chart JSON data by calling the visualization functions ---
        charts_json = {
            "bar_chart": create_avg_temp_humidity_chart(df.copy()),
            "box_plot": create_delivery_time_boxplot(pd.DataFrame(journey_stats['details'])),
            "scatter_plot": create_temp_anomaly_scatter(df.copy()),
            "pie_chart": create_stakeholder_pie_chart(df.copy())
        }
        
        # --- Calculate high-level Key Performance Indicators (KPIs) ---
        kpis = {
            "total_products": df['product_id'].nunique(),
            "total_anomalies": len(temp_anomalies_df),
            "avg_journey_hours": journey_stats.get('avg_hours', 0)
        }
        
        # --- Assemble all results into a single package, including the charts ---
        return {
            "kpis": kpis,
            "anomalies": temp_anomalies_df.to_dict('records'),
            "journey_stats": journey_stats,
            "charts": charts_json # Add the charts to the payload
        }

# Instantiate the service so we can import it easily elsewhere
analytics_service = AnalyticsService()