import pandas as pd

from analytics.fraud_detection import find_temperature_anomalies
from analytics.supply_chain_analytics import calculate_journey_stats
from analytics.visualization import (
    create_anomalies_by_product_chart,
    create_avg_temp_humidity_chart,
    create_delivery_time_boxplot,
    create_status_distribution_chart,
    create_stakeholder_pie_chart,
    create_temp_anomaly_scatter,
)
from services.blockchain_service import blockchain_service


class AnalyticsService:
    TEMPERATURE_THRESHOLD = 25.0

    def get_dashboard_analytics(self, filters=None, username=None, role=None):
        filters = filters or {}
        all_txs = blockchain_service.get_supply_chain_transactions()
        base_df = self._prepare_dataframe(all_txs)
        options = self._build_filter_options(base_df)
        scoped_df = self._scope_for_user(base_df, filters=filters, username=username, role=role)
        filtered_df = self._apply_filters(scoped_df, filters)
        anomalies_df = find_temperature_anomalies(filtered_df.copy(), self.TEMPERATURE_THRESHOLD)

        if filters.get('anomalies_only'):
            filtered_df = anomalies_df.copy()

        journey_stats = calculate_journey_stats(filtered_df.copy())
        charts_json = {
            'bar_chart': create_avg_temp_humidity_chart(filtered_df.copy()),
            'box_plot': create_delivery_time_boxplot(pd.DataFrame(journey_stats['details'])),
            'scatter_plot': create_temp_anomaly_scatter(filtered_df.copy(), self.TEMPERATURE_THRESHOLD),
            'pie_chart': create_stakeholder_pie_chart(filtered_df.copy()),
            'status_chart': create_status_distribution_chart(filtered_df.copy()),
            'anomaly_chart': create_anomalies_by_product_chart(anomalies_df.copy()),
        }

        kpis = self._calculate_kpis(filtered_df, anomalies_df, journey_stats)

        return {
            'active_filters': filters,
            'available_filters': options,
            'scope': self._scope_label(filters=filters, role=role),
            'can_filter_my_activity': role in {'farmer', 'distributor', 'retailer'} and bool(username),
            'kpis': kpis,
            'insights': self._build_insights(filtered_df, anomalies_df, journey_stats),
            'anomalies': anomalies_df.sort_values(by='temperature', ascending=False).to_dict('records'),
            'journey_stats': journey_stats,
            'charts': charts_json,
        }

    def _prepare_dataframe(self, transactions):
        if not transactions:
            return pd.DataFrame(columns=[
                'id', 'sender', 'recipient', 'product_id', 'product_name', 'location',
                'temperature', 'humidity', 'transport_info', 'status', 'timestamp',
                'expiry_date',
            ])

        df = pd.DataFrame(transactions)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
        df['temperature'] = pd.to_numeric(df.get('temperature'), errors='coerce')
        df['humidity'] = pd.to_numeric(df.get('humidity'), errors='coerce')
        df['status'] = df.get('status').fillna('Unknown')
        df['product_name'] = df.get('product_name').fillna('Unknown')
        return df.dropna(subset=['timestamp'])

    def _scope_for_user(self, df, filters=None, username=None, role=None):
        filters = filters or {}
        if (
            df.empty
            or filters.get('data_scope') != 'mine'
            or role not in {'farmer', 'distributor', 'retailer'}
            or not username
        ):
            return df
        return df[(df['sender'] == username) | (df['recipient'] == username)].copy()

    def _apply_filters(self, df, filters):
        filtered = df.copy()
        product = filters.get('product_name')
        status = filters.get('status')
        stakeholder = filters.get('stakeholder')
        start_date = filters.get('start_date')
        end_date = filters.get('end_date')

        if product:
            filtered = filtered[filtered['product_name'] == product]
        if status:
            filtered = filtered[filtered['status'] == status]
        if stakeholder:
            filtered = filtered[
                (filtered['sender'] == stakeholder) | (filtered['recipient'] == stakeholder)
            ]
        if start_date:
            filtered = filtered[filtered['timestamp'] >= pd.to_datetime(start_date)]
        if end_date:
            filtered = filtered[filtered['timestamp'] <= pd.to_datetime(end_date) + pd.Timedelta(days=1)]

        return filtered

    def _build_filter_options(self, df):
        if df.empty:
            return {'products': [], 'statuses': [], 'stakeholders': []}

        stakeholders = pd.concat([df['sender'], df['recipient']], ignore_index=True).dropna()
        return {
            'products': sorted(df['product_name'].dropna().unique().tolist()),
            'statuses': sorted(df['status'].dropna().unique().tolist()),
            'stakeholders': sorted(stakeholders.unique().tolist()),
        }

    def _calculate_kpis(self, df, anomalies_df, journey_stats):
        total_transactions = len(df)
        total_products = int(df['product_id'].nunique()) if not df.empty else 0
        avg_temperature = round(df['temperature'].dropna().mean(), 1) if not df.empty and df['temperature'].notna().any() else 0
        anomaly_rate = round((len(anomalies_df) / total_transactions) * 100, 1) if total_transactions else 0

        return {
            'total_products': total_products,
            'total_transactions': total_transactions,
            'in_transit': int((df['status'] == 'In Transit').sum()) if not df.empty else 0,
            'completed_or_sold': int(df['status'].isin(['Sold', 'In Stock', 'Completed']).sum()) if not df.empty else 0,
            'total_anomalies': len(anomalies_df),
            'anomaly_rate': anomaly_rate,
            'avg_temperature': avg_temperature,
            'avg_journey_hours': journey_stats.get('avg_hours', 0),
            'chain_valid': blockchain_service.get_blockchain().is_chain_valid(),
        }

    def _build_insights(self, df, anomalies_df, journey_stats):
        if df.empty:
            return ['No transactions match the current filters.']

        insights = []
        if not anomalies_df.empty:
            hottest = anomalies_df.sort_values(by='temperature', ascending=False).iloc[0]
            insights.append(
                f"{hottest['product_name']} reached the highest recorded temperature at {round(hottest['temperature'], 1)} deg C."
            )
        else:
            insights.append('No temperature anomalies were found for the current view.')

        status_counts = df['status'].value_counts()
        if not status_counts.empty:
            insights.append(f"Most filtered transactions are currently marked as {status_counts.idxmax()}.")

        if journey_stats.get('avg_hours', 0):
            insights.append(f"Average product journey time is {journey_stats['avg_hours']} hours.")

        return insights[:3]

    def _scope_label(self, filters=None, role=None):
        filters = filters or {}
        if filters.get('data_scope') == 'mine' and role in {'farmer', 'distributor', 'retailer'}:
            return f"My {role.title()} activity"
        return 'All supply-chain activity'


analytics_service = AnalyticsService()
