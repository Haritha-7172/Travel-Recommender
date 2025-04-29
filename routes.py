from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, get_db_connection
from models import User, Destination, Accommodation
import logging

@app.route('/')
def index():
    # Get accommodation types for the form dropdown
    accommodation_types = Accommodation.get_types()
    
    # If no accommodation types found, add some defaults
    if not accommodation_types:
        accommodation_types = ["Hotel", "Hostel", "Resort", "Apartment", "Cabin"]
    
    return render_template('index.html', accommodation_types=accommodation_types)

@app.route('/search', methods=['POST'])
def search():
    # Get search parameters from form
    dest_type = request.form.get('destination_type')
    budget = request.form.get('budget')
    if budget:
        try:
            budget = float(budget)
        except ValueError:
            budget = None
    
    climate = request.form.get('climate')
    days = request.form.get('days')
    if days:
        try:
            days = int(days)
        except ValueError:
            days = None
    
    accommodation_type = request.form.get('accommodation_type')
    
    # Search for destinations matching criteria
    destinations = Destination.search(
        dest_type=dest_type,
        budget=budget,
        climate=climate,
        accommodation_type=accommodation_type,
        days=days
    )
    
    # Prepare detailed information for each destination
    destination_details = []
    for dest in destinations:
        details = Destination.get_destination_details(dest.dest_id)
        if details:
            destination_details.append(details)
    
    return render_template('results.html', 
                          destinations=destination_details,
                          search_params={
                              'destination_type': dest_type,
                              'budget': budget,
                              'climate': climate,
                              'days': days,
                              'accommodation_type': accommodation_type
                          })

@app.route('/destination/<int:dest_id>')
def destination_details(dest_id):
    details = Destination.get_destination_details(dest_id)
    if not details:
        flash('Destination not found', 'danger')
        return redirect(url_for('index'))
    
    return render_template('destination.html', details=details)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Basic validation
        if not name or not email or not password:
            flash('All fields are required', 'danger')
            return render_template('register.html')
        
        # Check if user already exists
        existing_user = User.get_by_email(email)
        if existing_user:
            flash('Email already registered', 'danger')
            return render_template('register.html')
        
        # Create new user
        user = User(name=name, email=email, password=password)
        if user.create():
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.login(email, password)
        if user:
            session['user_id'] = user.user_id
            session['user_name'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to view your profile', 'warning')
        return redirect(url_for('login'))
    
    user = User.get_by_id(session['user_id'])
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('index'))
    
    return render_template('profile.html', user=user)

@app.route('/api/destination_types')
def get_destination_types():
    conn = get_db_connection()
    if not conn:
        return jsonify([])
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT Type FROM Destination")
        types = [row[0] for row in cursor.fetchall()]
        return jsonify(types)
    except Exception as e:
        logging.error(f"Error fetching destination types: {e}")
        return jsonify([])
    finally:
        cursor.close()
        conn.close()

@app.route('/api/climates')
def get_climates():
    conn = get_db_connection()
    if not conn:
        return jsonify([])
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT climate FROM Chooses")
        climates = [row[0] for row in cursor.fetchall()]
        return jsonify(climates)
    except Exception as e:
        logging.error(f"Error fetching climates: {e}")
        return jsonify([])
    finally:
        cursor.close()
        conn.close()
