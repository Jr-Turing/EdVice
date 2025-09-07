from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from models import User, ParentChildRelation
import uuid
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('dashboard')
            
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(next_page)
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        role = request.form.get('role', 'student')
        phone = request.form.get('phone')
        category = request.form.get('category')
        class_level = request.form.get('class_level')
        state = request.form.get('state')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('auth/register.html')
        
        # Create new user
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            phone=phone,
            category=category,
            class_level=class_level,
            state=state
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Registration successful! Welcome to Career & Education Advisor!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/role-selector')
def role_selector():
    return render_template('auth/role_selector.html')

@auth_bp.route('/parent-child-link', methods=['GET', 'POST'])
@login_required
def parent_child_link():
    if current_user.role != 'parent':
        flash('Only parents can access this feature', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        child_email = request.form.get('child_email')
        relationship_type = request.form.get('relationship_type', 'parent')
        
        child = User.query.filter_by(email=child_email, role='student').first()
        if not child:
            flash('Student not found with this email', 'error')
            return render_template('auth/parent_child_link.html')
        
        # Check if relation already exists
        existing_relation = ParentChildRelation.query.filter_by(
            parent_id=current_user.id, 
            child_id=child.id
        ).first()
        
        if existing_relation:
            flash('Child is already linked to your account', 'warning')
        else:
            relation = ParentChildRelation(
                parent_id=current_user.id,
                child_id=child.id,
                relationship_type=relationship_type
            )
            db.session.add(relation)
            db.session.commit()
            flash(f'Successfully linked {child.get_full_name()} to your account', 'success')
        
        return redirect(url_for('parent_dashboard'))
    
    return render_template('auth/parent_child_link.html')