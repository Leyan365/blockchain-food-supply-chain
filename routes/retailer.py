from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from services.blockchain_service import blockchain_service
from services.validation_service import (
    parse_humidity,
    parse_temperature,
    validate_email_like,
    validate_optional_date,
    validate_required_fields,
)
from routes.auth import role_required
from datetime import datetime

retailer_bp = Blueprint('retailer', __name__, url_prefix='/retailer')

@retailer_bp.route('/dashboard')
@role_required('retailer')
def dashboard():
    user = session['username']
    all_tx = blockchain_service.get_all_transactions()

    # Incoming deliveries: recipient == user and status == "In Transit"
    incoming = [
        tx for tx in all_tx
        if tx.get('recipient') == user and tx.get('status') == 'In Transit'
    ]

    # Build latest states for items where user is recipient or sender
    latest = {}
    for tx in all_tx:
        pid = tx.get('product_id')
        if pid and (tx.get('sender') == user or tx.get('recipient') == user):
            if pid not in latest or tx['timestamp'] > latest[pid]['timestamp']:
                latest[pid] = tx

    inventory = []
    pending_sales = 0
    for tx in latest.values():
        # Check if the current user is the recipient of the latest transaction
        if tx.get('recipient') == user:
            # If so, the item is considered "In Stock" at the retailer's location
            status = "In Stock"
            pending_sales += 1  # Count as a possible sale
        else:
            # Otherwise, use the existing status from the transaction
            status = tx.get('status')
        
        # Pull other info from the latest transaction
        expiry = tx.get('expiry_date', None)
        storage_temp = tx.get('storage_temp') or tx.get('temperature') 
        
        inventory.append({
            "id": tx['product_id'],
            "name": tx.get('product_name'),
            "supplier": tx.get('sender'),
            "storage_temp": storage_temp,
            "expiry_date": expiry,
            "status": status,
            "last_updated": datetime.fromtimestamp(tx['timestamp']).strftime("%Y-%m-%d %H:%M")
        })

    stats = {
        "incoming": len(incoming),
        "in_stock": len([item for item in inventory if item['status'] == "In Stock"]),
        "pending_sales": pending_sales
    }

    return render_template(
        "dashboard/retailer.html",
        stats=stats,
        incoming_list=incoming,
        inventory=inventory
    )

@retailer_bp.route('/update_inventory', methods=['POST'])
@role_required('retailer')
def update_inventory():
    user = session['username']
    required, errors = validate_required_fields(request.form, {
        'product_id': 'Product ID',
    })
    next_rcpt = (request.form.get('next_recipient') or '').strip()
    recipient_error = validate_email_like(next_rcpt, 'Consumer email')
    if recipient_error:
        errors.append(recipient_error)

    temp, temp_error = parse_temperature(request.form.get('storage_temp'), 'Storage temperature')
    hum, humidity_error = parse_humidity(request.form.get('storage_humidity'), 'Storage humidity')
    expiry = (request.form.get('expiry_date') or '').strip()
    expiry_error = validate_optional_date(expiry, 'Expiry date')
    errors.extend(error for error in (temp_error, humidity_error, expiry_error) if error)

    if errors:
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('retailer.dashboard'))

    pid = required['product_id']

    # Get the last transaction to retrieve product name and location
    last = blockchain_service.get_latest_tx_for_product(pid)
    
    # Check if a last transaction was found. If not, the product ID is invalid.
    if not last:
        flash(f"Error: Product ID {pid} not found in the blockchain.", "danger")
        return redirect(url_for('retailer.dashboard'))

    # Build the inventory update transaction
    tx = {
        "product_id": pid,
        "sender": user,
        "recipient": next_rcpt or user,
        "location": last.get("location"), 
        "temperature": temp,
        "humidity": hum,
        "transport_info": None, 
        "status": "In Stock" if not next_rcpt else "Sold",
        "expiry_date": expiry,
        "product_name": last.get("product_name") 
    }

    blockchain_service.add_transaction(tx)
    flash(f"Inventory for {pid} updated.", "success")
    return redirect(url_for('retailer.dashboard'))
