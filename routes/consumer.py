from flask import Blueprint, render_template, request
from services.blockchain_service import blockchain_service

consumer_bp = Blueprint('consumer', __name__)

@consumer_bp.route('/dashboard')
def dashboard():
    product_id = request.args.get('product_id', '').strip()
    products = blockchain_service.get_product_summaries()[:12]
    history = blockchain_service.get_transaction_history(product_id) if product_id else []
    latest = history[-1] if history else None

    return render_template(
        'dashboard/consumer.html',
        product_id=product_id,
        products=products,
        history=history,
        latest=latest,
        chain_valid=blockchain_service.get_blockchain().is_chain_valid()
    )

@consumer_bp.route('/track', methods=['GET'])
def track_product():
    product_id = request.args.get('product_id', '').strip()
    return dashboard() if product_id else dashboard()

@consumer_bp.route('/track/<product_id>')
def track_product_by_id(product_id):
    history = blockchain_service.get_transaction_history(product_id)
    latest = history[-1] if history else None

    return render_template(
        'dashboard/consumer.html',
        product_id=product_id,
        products=blockchain_service.get_product_summaries()[:12],
        history=history,
        latest=latest,
        chain_valid=blockchain_service.get_blockchain().is_chain_valid()
    )
