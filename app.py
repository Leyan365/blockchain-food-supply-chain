from flask import Flask, render_template
from config import config_by_name
from flask_session import Session
from datetime import datetime
import time
import pandas as pd # <-- 1. IMPORT PANDAS

# Blueprint imports
from routes.auth import auth_bp
from routes.farmer import farmer_bp
from routes.distributor import distributor_bp
from routes.retailer import retailer_bp
from routes.consumer import consumer_bp
from routes.analytics import analytics_bp

# Import the blockchain service
from services.blockchain_service import blockchain_service

def create_app(config_name='dev'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    Session(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(farmer_bp, url_prefix='/farmer')
    app.register_blueprint(distributor_bp, url_prefix='/distributor')
    app.register_blueprint(retailer_bp, url_prefix='/retailer')
    app.register_blueprint(consumer_bp, url_prefix='/consumer')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')

    # Register a custom Jinja filter to format timestamps
    @app.template_filter('timestamp_to_datetime')
    def timestamp_to_datetime_filter(s):
        """
        Converts a Unix timestamp OR a pandas Timestamp object 
        to a readable datetime string.
        """
        if not s:
            return "N/A"
        
        # --- 2. ADD THIS LOGIC ---
        # Check if the object is a pandas Timestamp
        if isinstance(s, pd.Timestamp):
            return s.strftime('%Y-%m-%d %H:%M:%S')
        
        # Otherwise, handle it as a numeric unix timestamp
        try:
            return datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')
        except (TypeError, ValueError):
            return "Invalid Date"
        # --- END OF NEW LOGIC ---

    @app.template_filter('time_ago')
    def time_ago_filter(s):
        """Converts a Unix timestamp to a human-readable 'X minutes ago' string."""
        if not s:
            return "N/A"
        
        # This filter also needs to handle the new Timestamp object
        if isinstance(s, pd.Timestamp):
            s = s.timestamp() # Convert pandas Timestamp to a numeric unix timestamp

        now = time.time()
        diff = now - s
        if diff < 60:
            return f"{int(diff)} seconds ago"
        elif diff < 3600:
            return f"{int(diff / 60)} minutes ago"
        elif diff < 86400:
            return f"{int(diff / 3600)} hours ago"
        else:
            return f"{int(diff / 86400)} days ago"

    @app.route('/')
    def index():
        return render_template('index.html', current_year=datetime.now().year)

    @app.route('/blockchain-data')
    def view_blockchain_data():
        full_chain = blockchain_service.get_full_chain()
        pending_transactions = blockchain_service.get_pending_transactions()
        
        total_blocks = len(full_chain)
        total_transactions = sum(len(block.transactions) for block in full_chain) + len(pending_transactions)
        last_block_time = full_chain[-1].timestamp if full_chain else None

        return render_template('blockchain/product_history.html',
                               current_year=datetime.now().year,
                               total_blocks=total_blocks,
                               total_transactions=total_transactions,
                               network_status='Active',
                               last_block_time=last_block_time,
                               full_chain=full_chain,
                               pending_transactions=pending_transactions)

    return app