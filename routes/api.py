from flask import Blueprint, jsonify

from services.blockchain_service import blockchain_service


api_bp = Blueprint('api', __name__)


@api_bp.route('/blockchain/status')
def blockchain_status():
    chain = blockchain_service.get_full_chain()
    pending_transactions = blockchain_service.get_pending_transactions()
    supply_chain_transactions = blockchain_service.get_supply_chain_transactions()

    return jsonify({
        'chain_valid': blockchain_service.get_blockchain().is_chain_valid(),
        'network_status': 'Active',
        'total_blocks': len(chain),
        'total_transactions': len(supply_chain_transactions),
        'pending_transactions': len(pending_transactions),
        'latest_block_hash': chain[-1].hash if chain else None,
        'latest_block_index': chain[-1].index if chain else None,
        'latest_block_timestamp': chain[-1].timestamp if chain else None,
    })


@api_bp.route('/products')
def products():
    product_summaries = [
        _serialize_product_summary(product)
        for product in blockchain_service.get_product_summaries()
    ]
    return jsonify({
        'count': len(product_summaries),
        'products': product_summaries,
    })


@api_bp.route('/products/<product_id>')
def product_detail(product_id):
    history = blockchain_service.get_transaction_history(product_id)
    if not history:
        return jsonify({
            'error': 'Product not found',
            'product_id': product_id,
        }), 404

    latest = history[-1]
    return jsonify({
        'product': _serialize_product_summary(latest),
        'history_count': len(history),
        'history_url': f'/api/products/{product_id}/history',
    })


@api_bp.route('/products/<product_id>/history')
def product_history(product_id):
    history = blockchain_service.get_transaction_history(product_id)
    if not history:
        return jsonify({
            'error': 'Product not found',
            'product_id': product_id,
        }), 404

    return jsonify({
        'product_id': product_id,
        'count': len(history),
        'history': history,
    })


def _serialize_product_summary(tx):
    return {
        'product_id': tx.get('product_id'),
        'product_name': tx.get('product_name'),
        'latest_status': tx.get('status'),
        'latest_location': tx.get('location'),
        'sender': tx.get('sender'),
        'recipient': tx.get('recipient'),
        'temperature': tx.get('temperature'),
        'humidity': tx.get('humidity'),
        'expiry_date': tx.get('expiry_date'),
        'last_updated': tx.get('timestamp'),
        'tracking_url': f"/consumer/track/{tx.get('product_id')}",
        'qr_url': f"/consumer/qr/{tx.get('product_id')}",
    }
