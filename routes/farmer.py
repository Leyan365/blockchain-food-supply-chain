from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from services.blockchain_service import blockchain_service
from routes.auth import role_required
from datetime import datetime
from uuid import uuid4 

farmer_bp = Blueprint('farmer', __name__, url_prefix='/farmer')


@farmer_bp.route('/dashboard')
@role_required('farmer')
def dashboard():
    farmer = session['username']
   
    all_transactions = blockchain_service.get_all_transactions()

    farmer_related_transactions = [
        tx for tx in all_transactions
        if tx.get("sender") == farmer or tx.get("recipient") == farmer
    ]

    # --- Logic to get the LATEST state of each unique product for the table ---
    products_current_state = {}
    for tx in farmer_related_transactions:
        product_id = tx.get("product_id")
        if product_id:
            # Only store the transaction if it's new, or newer than the one already stored for this product_id
            if product_id not in products_current_state or \
               tx.get("timestamp", 0) > products_current_state[product_id].get("timestamp", 0):
                products_current_state[product_id] = tx

    products_for_table = []
    unique_product_ids = set() # To count total unique products
    for product_id, latest_tx_data in products_current_state.items():
        unique_product_ids.add(product_id)
        products_for_table.append({
            "name": latest_tx_data.get("product_name", "N/A"),
            "id": latest_tx_data.get("product_id", "N/A"), 
            "location": latest_tx_data.get("location", "Unknown"),
            "status": latest_tx_data.get("status", "In Transit"),
            "last_updated": datetime.fromtimestamp(latest_tx_data.get("timestamp")).strftime("%Y-%m-%d %H:%M") if latest_tx_data.get("timestamp") else "--" # Renamed key to 'last_updated'
        })

    #Summary Statistics for Overview Cards
    total_products_registered_by_farmer = len(unique_product_ids) #Count unique products for the "Total Products" card
    
    # Pending transactions where the current farmer is the sender
    pending_tx_count = sum(1 for tx in farmer_related_transactions if tx.get("sender") == farmer and tx.get("status") == "Pending")
    
    # Last transaction date initiated by this farmer 
    # Using 'sender' to denote an action initiated by the farmer
    last_sent_tx_timestamp = max(
        (tx.get("timestamp") for tx in farmer_related_transactions if tx.get("sender") == farmer),
        default=None
    )
    last_harvest_formatted = datetime.fromtimestamp(last_sent_tx_timestamp).strftime("%Y-%m-%d %H:%M") if last_sent_tx_timestamp else "--"

    stats = {
        "total_products": total_products_registered_by_farmer,
        "pending_transactions": pending_tx_count,
        "last_harvest": last_harvest_formatted,
        "status": "Operational" # Hardcoded as this is for demonstration
    }

    # --- Recent Activities Feed ---
    # Sort all farmer-related transactions by timestamp in descending order
    recent_activity_list = sorted(farmer_related_transactions, key=lambda x: x.get("timestamp", 0), reverse=True)
    activity_feed_strings = []
    for tx in recent_activity_list[:5]: 
        activity_type = "Registered" if tx.get("status") == "Registered" else "Transferred" if tx.get("recipient") else "Updated"
        actor = "You" if tx.get("sender") == farmer else tx.get("sender", "Someone")
        
   
        activity_str = f"[{datetime.fromtimestamp(tx.get('timestamp')).strftime('%Y-%m-%d %H:%M')}] Product '{tx.get('product_name', 'N/A')}' (ID: {tx.get('product_id', 'N/A')[:8]}...) {activity_type} by {actor} at {tx.get('location', 'Unknown')}. Status: {tx.get('status', 'N/A')}."
        activity_feed_strings.append(activity_str)


    return render_template(
        "dashboard/farmer.html",
        stats=stats,                 
        products=products_for_table, 
        recent_activities=activity_feed_strings 
    )


@farmer_bp.route('/add_transaction', methods=['POST'])
@role_required('farmer')
def add_transaction():
    sender = session['username']
    product_name = request.form.get("product_name")
    recipient = request.form.get("recipient")
    location = request.form.get("location")
    temperature = request.form.get("temperature")
    humidity = request.form.get("humidity")
    transport_info = request.form.get("transport_info")

    # Generate a unique UUID for the product_id for new registrations
    product_id = str(uuid4())

    tx_data = {
        "product_name": product_name,
        "product_id": product_id, 
        "sender": sender,
        "recipient": recipient,
        "location": location,
        "temperature": float(temperature) if temperature else None,
        "humidity": float(humidity) if humidity else None,
        "transport_info": transport_info,
        "status": "Registered" 
    }

    try:
        blockchain_service.add_transaction(tx_data)
        flash(f"Product '{product_name}' (ID: {product_id[:8]}...) registered successfully!", "success")
    except Exception as e:
        flash(f"Error registering product: {str(e)}", "danger")

    return redirect(url_for("farmer.dashboard"))
