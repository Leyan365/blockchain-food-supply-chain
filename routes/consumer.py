from flask import Blueprint

consumer_bp = Blueprint('consumer', __name__)

@consumer_bp.route('/dashboard')
def consumer_dashboard():
    return "Consumer Dashboard"