from flask import Blueprint, render_template
from routes.auth import login_required
from services.analytics_service import analytics_service

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/overview')
@login_required
def analytics_overview():
    """
    Displays the main analytics dashboard.
    """
   
    analytics_data = analytics_service.get_dashboard_analytics()

   
    return render_template('analytics/overview.html', **analytics_data)