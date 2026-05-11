from flask import Blueprint, render_template, request, session
from routes.auth import login_required
from services.analytics_service import analytics_service

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/overview')
@login_required
def analytics_overview():
    """
    Displays the main analytics dashboard.
    """
    filters = {
        'product_name': request.args.get('product_name', '').strip(),
        'status': request.args.get('status', '').strip(),
        'stakeholder': request.args.get('stakeholder', '').strip(),
        'start_date': request.args.get('start_date', '').strip(),
        'end_date': request.args.get('end_date', '').strip(),
        'data_scope': request.args.get('data_scope', '').strip(),
        'anomalies_only': request.args.get('anomalies_only') == '1',
    }
    filters = {key: value for key, value in filters.items() if value not in ('', None, False)}
    analytics_data = analytics_service.get_dashboard_analytics(
        filters=filters,
        username=session.get('username'),
        role=session.get('role'),
    )

   
    return render_template('analytics/overview.html', **analytics_data)
