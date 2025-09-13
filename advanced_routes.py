from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import (User, Scholarship, Exam, SavedScholarship, CareerSimulation, 
                   Notification, MentorshipSession, College, Career)
import json
from datetime import datetime, timedelta
from sqlalchemy import and_, or_

advanced_bp = Blueprint('advanced', __name__, url_prefix='/advanced')

@advanced_bp.route('/scholarships')
def scholarships():
    # Get filter parameters
    category_filter = request.args.get('category', '')
    class_filter = request.args.get('class', '')
    amount_filter = request.args.get('amount', '')
    
    # Build query
    query = Scholarship.query.filter_by(is_active=True)
    
    if category_filter:
        query = query.filter(Scholarship.category_eligible.contains(f'"{category_filter}"'))
    
    if class_filter:
        query = query.filter(Scholarship.class_eligible.contains(f'"{class_filter}"'))
    
    scholarships = query.all()
    
    # Get unique categories and classes for filters
    all_categories = ['General', 'SC', 'ST', 'OBC']
    all_classes = ['10th', '12th', 'graduation', 'post_graduation']
    
    return render_template('advanced/scholarships.html', 
                         scholarships=scholarships,
                         categories=all_categories,
                         classes=all_classes,
                         current_category=category_filter,
                         current_class=class_filter)

@advanced_bp.route('/scholarship-matcher')
@login_required
def scholarship_matcher():
    user_category = current_user.category
    user_class = current_user.class_level
    
    # Find matching scholarships
    matching_scholarships = []
    
    scholarships = Scholarship.query.filter_by(is_active=True).all()
    for scholarship in scholarships:
        categories = json.loads(scholarship.category_eligible) if scholarship.category_eligible else []
        classes = json.loads(scholarship.class_eligible) if scholarship.class_eligible else []
        
        if (user_category in categories or 'General' in categories) and user_class in classes:
            matching_scholarships.append(scholarship)
    
    return render_template('advanced/scholarship_matcher.html', 
                         scholarships=matching_scholarships,
                         user=current_user)

@advanced_bp.route('/exams')
def exams():
    class_filter = request.args.get('class', '')
    exam_type_filter = request.args.get('type', '')
    
    query = Exam.query.filter_by(is_active=True)
    
    if class_filter:
        query = query.filter(Exam.eligibility_class.contains(f'"{class_filter}"'))
    
    if exam_type_filter:
        query = query.filter_by(exam_type=exam_type_filter)
    
    exams = query.order_by(Exam.exam_date.asc()).all()
    
    # Get upcoming exams (next 6 months)
    upcoming_date = datetime.now() + timedelta(days=180)
    upcoming_exams = [exam for exam in exams if exam.exam_date and exam.exam_date <= upcoming_date]
    
    return render_template('advanced/exams.html', 
                         exams=exams,
                         upcoming_exams=upcoming_exams)

@advanced_bp.route('/college-eligibility-checker', methods=['GET', 'POST'])
def college_eligibility_checker():
    if request.method == 'POST':
        marks_10th = float(request.form.get('marks_10th', 0))
        marks_12th = float(request.form.get('marks_12th', 0))
        category = request.form.get('category', 'General')
        stream = request.form.get('stream', '')
        state_preference = request.form.get('state_preference', '')
        
        # Simple eligibility logic (can be enhanced)
        eligible_colleges = []
        colleges = College.query.all()
        
        for college in colleges:
            # Basic eligibility check
            min_percentage = 60  # Base requirement
            if category == 'SC':
                min_percentage = 50
            elif category == 'ST':
                min_percentage = 45
            elif category == 'OBC':
                min_percentage = 55
            
            if marks_12th >= min_percentage:
                if not stream or college.type.lower().find(stream.lower()) != -1:
                    if not state_preference or college.state.lower() == state_preference.lower():
                        eligible_colleges.append(college)
        
        return render_template('advanced/eligibility_results.html',
                             colleges=eligible_colleges,
                             marks_12th=marks_12th,
                             category=category,
                             stream=stream)
    
    return render_template('advanced/college_eligibility_checker.html')

@advanced_bp.route('/career-simulator', methods=['GET', 'POST'])
@login_required
def career_simulator():
    if request.method == 'POST':
        stream_choice = request.form.get('stream_choice')
        subjects = request.form.getlist('subjects')
        interests = request.form.getlist('interests')
        
        # Generate simulation based on choices
        simulation_data = generate_career_simulation(stream_choice, subjects, interests)
        
        # Save simulation
        simulation = CareerSimulation(
            user_id=current_user.id,
            scenario_name=f"What if I choose {stream_choice}?",
            chosen_stream=stream_choice,
            chosen_subjects=json.dumps(subjects),
            simulation_results=json.dumps(simulation_data)
        )
        db.session.add(simulation)
        db.session.commit()
        
        return render_template('advanced/simulation_results.html',
                             simulation=simulation_data,
                             stream=stream_choice)
    
    return render_template('advanced/career_simulator.html')

@advanced_bp.route('/notifications')
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    
    # Mark as read
    if request.args.get('mark_read'):
        for notification in notifications:
            notification.is_read = True
        db.session.commit()
    
    return render_template('advanced/notifications.html', notifications=notifications)

@advanced_bp.route('/mentorship')
@login_required
def mentorship():
    # Get user's mentorship sessions
    sessions = MentorshipSession.query.filter_by(user_id=current_user.id).order_by(MentorshipSession.created_at.desc()).all()
    
    # Get available human mentors
    mentors = User.query.filter_by(role='teacher').all()
    
    return render_template('advanced/mentorship.html', sessions=sessions, mentors=mentors)

@advanced_bp.route('/ai-chat', methods=['POST'])
@login_required
def ai_chat():
    message = request.json.get('message')
    
    # Simple AI response logic (can be enhanced with actual AI integration)
    ai_response = generate_ai_response(message, current_user)
    
    # Save conversation
    session_obj = MentorshipSession.query.filter_by(
        user_id=current_user.id, 
        mentor_type='ai', 
        status='active'
    ).first()
    
    if not session_obj:
        session_obj = MentorshipSession(
            user_id=current_user.id,
            mentor_type='ai',
            session_type='chat',
            messages=json.dumps([])
        )
        db.session.add(session_obj)
    
    # Update messages
    messages = json.loads(session_obj.messages) if session_obj.messages else []
    messages.append({
        'user': message,
        'ai': ai_response,
        'timestamp': datetime.utcnow().isoformat()
    })
    session_obj.messages = json.dumps(messages)
    session_obj.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'response': ai_response})

def generate_career_simulation(stream, subjects, interests):
    """Generate career simulation based on user choices"""
    
    # Career mapping based on stream
    career_mapping = {
        'Science': {
            'careers': ['Engineering', 'Medicine', 'Research', 'IT & Software'],
            'avg_salary': '₹6-15 LPA',
            'growth_rate': 'High',
            'job_security': 'High'
        },
        'Commerce': {
            'careers': ['Banking', 'Finance', 'Business Management', 'CA/CS'],
            'avg_salary': '₹4-12 LPA',
            'growth_rate': 'Medium-High',
            'job_security': 'Medium-High'
        },
        'Arts': {
            'careers': ['Civil Services', 'Teaching', 'Media', 'Social Work'],
            'avg_salary': '₹3-10 LPA',
            'growth_rate': 'Medium',
            'job_security': 'Medium'
        }
    }
    
    stream_data = career_mapping.get(stream, career_mapping['Science'])
    
    return {
        'chosen_stream': stream,
        'possible_careers': stream_data['careers'],
        'salary_range': stream_data['avg_salary'],
        'growth_prospects': stream_data['growth_rate'],
        'job_security': stream_data['job_security'],
        'subjects_relevance': subjects,
        'recommended_colleges': ['IIT', 'NIT', 'State Universities'],
        'entrance_exams': ['JEE Main', 'State CET', 'University Entrance'],
        'timeline': {
            '12th_completion': '2025',
            'graduation': '2028-2029',
            'career_start': '2029-2030'
        }
    }

def generate_ai_response(message, user):
    """Generate AI response based on user message and profile"""
    message_lower = message.lower()
    
    # Career guidance responses
    if any(word in message_lower for word in ['career', 'job', 'profession']):
        return f"Hi {user.first_name}! Based on your profile as a {user.class_level} {user.category} student, I can help you explore various career options. What specific field interests you - Science, Commerce, or Arts?"
    
    # Scholarship responses
    elif any(word in message_lower for word in ['scholarship', 'financial aid', 'money']):
        return f"Great question! As a {user.category} category student, you're eligible for several scholarships. I recommend checking the Scholarship Matcher for personalized recommendations based on your profile."
    
    # College responses
    elif any(word in message_lower for word in ['college', 'university', 'admission']):
        return f"For college admissions, I suggest using our College Eligibility Checker. Based on your {user.class_level} performance and {user.category} category, I can help you find suitable government colleges."
    
    # Exam responses
    elif any(word in message_lower for word in ['exam', 'test', 'entrance']):
        return "I can guide you about upcoming entrance exams! Check our Exams section for detailed information about JEE, NEET, CUET, and other important exams with dates and eligibility criteria."
    
    # General response
    else:
        return f"Hello {user.first_name}! I'm here to help with your career and education questions. You can ask me about careers, scholarships, colleges, or exams. How can I assist you today?"