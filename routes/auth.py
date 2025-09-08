from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from services.blockchain_service import blockchain_service

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Hardcoded user credentials for demonstration
USERS = {
    'farmer1@example.com': ('pass123', 'farmer'),
    'dist1@example.com': ('pass123', 'distributor'),
    'retail1@example.com': ('pass123', 'retailer'),
}

# Decorator to ensure a user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        user = USERS.get(uname)

        if user and user[0] == pwd:
            session['username'] = uname
            session['role'] = user[1]
            
            return redirect(url_for(f"{user[1]}.dashboard"))
        else:
            flash("Invalid credentials. Please try again.", 'danger')
            return render_template('login.html', error="Invalid credentials"), 401

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/blockchain_explorer')
@login_required
def blockchain_explorer():
    """
    Renders the blockchain explorer page for logged-in users.
    """
    full_chain = blockchain_service.get_full_chain()
    display_chain = full_chain[1:] # Exclude the genesis block
    
    return render_template('blockchain/view_chain.html', blockchain_chain=display_chain)