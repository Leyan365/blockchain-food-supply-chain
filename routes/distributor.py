from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from services.blockchain_service import blockchain_service
from services.validation_service import (
    clean_text,
    parse_humidity,
    parse_temperature,
    validate_email_like,
    validate_required_fields,
)
from routes.auth import role_required
from datetime import datetime

distributor_bp = Blueprint('distributor', __name__, url_prefix='/distributor')

@distributor_bp.route('/dashboard')
@role_required('distributor')
def dashboard():
    user = session['username']
    all_tx = blockchain_service.get_all_transactions()

    # Incoming shipments: where recipient == this user and status == "Registered"
    incoming = [
        tx for tx in all_tx
        if tx.get('recipient') == user and tx.get('status') == 'Registered'
    ]

    # In-transit: where sender == this user and status != "Completed"
    in_transit = [
        tx for tx in all_tx
        if tx.get('sender') == user and tx.get('status') not in ('Completed',)
    ]

    # Pending transfers: where sender == this user and status == "Pending"
    pending = [
        tx for tx in all_tx
        if tx.get('sender') == user and tx.get('status') == 'Pending'
    ]

    # Build shipments list: latest state per product where either sender or recipient is this user
    latest = {}
    for tx in all_tx:
        pid = tx.get('product_id')
        if pid and (tx.get('sender') == user or tx.get('recipient') == user):
            # pick newest
            if pid not in latest or tx['timestamp'] > latest[pid]['timestamp']:
                latest[pid] = tx

    shipments = []
    for tx in latest.values():
        shipments.append({
            "id": tx['product_id'],
            "name": tx.get('product_name'),
            "sender": tx.get('sender'),
            "location": tx.get('location'),
            "status": tx.get('status'),
            "last_updated": datetime.fromtimestamp(tx['timestamp']).strftime("%Y-%m-%d %H:%M")
        })

    stats = {
        "incoming": len(incoming),
        "in_transit": len(in_transit),
        "pending": len(pending)
    }

    return render_template(
        "dashboard/distributor.html",
        stats=stats,
        incoming_list=incoming,
        shipments=shipments
    )

@distributor_bp.route('/update_shipment', methods=['POST'])
@role_required('distributor')
def update_shipment():
    user = session['username']
    required, errors = validate_required_fields(request.form, {
        'product_id': 'Product ID',
        'next_recipient': 'Next recipient',
    })
    recipient_error = validate_email_like(required.get('next_recipient'), 'Next recipient')
    if recipient_error:
        errors.append(recipient_error)

    temp, temp_error = parse_temperature(request.form.get('temperature'))
    hum, humidity_error = parse_humidity(request.form.get('humidity'))
    errors.extend(error for error in (temp_error, humidity_error) if error)

    if errors:
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('distributor.dashboard'))

    pid = required['product_id']
    info = clean_text(request.form.get('transport_info'))
    next_rcpt = required['next_recipient']

    # Get the last transaction for the product to retrieve existing data
    last = blockchain_service.get_latest_tx_for_product(pid)
    
    # Add a check to ensure the product ID is valid
    if not last:
        flash(f"Error: Product ID {pid} not found in the blockchain.", "danger")
        return redirect(url_for('distributor.dashboard'))

    # Build the update transaction using the existing product's info
    tx = {
        "product_id": pid, 
        "product_name": last.get('product_name'), 
        "sender": user,
        "recipient": next_rcpt,
        "location": last.get('location'),
        "temperature": temp,
        "humidity": hum,
        "transport_info": info,
        "status": "In Transit"
    }

    blockchain_service.add_transaction(tx)
    flash(f"Shipment {pid} updated and forwarded to {next_rcpt}.", "success")
    return redirect(url_for('distributor.dashboard'))
