from flask import render_template, request, session, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import app, db
from models import QuizResult, College, Career, User, ParentChildRelation
from quiz_data import QUIZ_QUESTIONS, analyze_quiz_results
from auth_routes import auth_bp
from advanced_routes import advanced_bp
import json
import uuid
import os
from dotenv import load_dotenv

# Optional: lazy import inside handler to avoid cold-start overhead if needed

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(advanced_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'parent':
        return redirect(url_for('parent_dashboard'))
    elif current_user.role == 'teacher':
        return redirect(url_for('teacher_dashboard'))
    else:
        return render_template('dashboard/student_dashboard.html', user=current_user)

@app.route('/parent-dashboard')
@login_required
def parent_dashboard():
    if current_user.role != 'parent':
        return redirect(url_for('dashboard'))
    
    # Get linked children
    children_relations = ParentChildRelation.query.filter_by(parent_id=current_user.id).all()
    children = [relation.child for relation in children_relations]
    
    return render_template('dashboard/parent_dashboard.html', user=current_user, children=children)

@app.route('/teacher-dashboard')
@login_required
def teacher_dashboard():
    if current_user.role != 'teacher':
        return redirect(url_for('dashboard'))
    
    return render_template('dashboard/teacher_dashboard.html', user=current_user)

@app.route('/quiz')
def quiz():
    # Generate a session ID if not exists
    if 'quiz_session_id' not in session:
        session['quiz_session_id'] = str(uuid.uuid4())

    # Reset quiz answers for new attempt
    session['quiz_answers'] = {}

    return render_template('quiz.html', questions=QUIZ_QUESTIONS, total_questions=len(QUIZ_QUESTIONS))

@app.route('/quiz/question/<int:question_id>')
def quiz_question(question_id):
    if question_id < 1 or question_id > len(QUIZ_QUESTIONS):
        return redirect(url_for('quiz'))
    
    question = QUIZ_QUESTIONS[question_id - 1]
    return render_template('quiz.html', 
                         current_question=question,
                         question_number=question_id,
                         total_questions=len(QUIZ_QUESTIONS),
                         progress_percent=(question_id / len(QUIZ_QUESTIONS)) * 100)

@app.route('/quiz/submit', methods=['POST'])
def submit_quiz_answer():
    question_id = request.form.get('question_id')
    answer = request.form.get('answer')
    
    if 'quiz_answers' not in session:
        session['quiz_answers'] = {}
    
    session['quiz_answers'][question_id] = answer
    session.permanent = True
    
    next_question = int(question_id) + 1
    if next_question <= len(QUIZ_QUESTIONS):
        return redirect(url_for('quiz_question', question_id=next_question))
    else:
        return redirect(url_for('quiz_results'))

@app.route('/results')
def quiz_results():
    if 'quiz_answers' not in session or not session['quiz_answers']:
        return redirect(url_for('quiz'))
    
    # Analyze quiz results
    recommendations = analyze_quiz_results(session['quiz_answers'])
    
    # Save results to database
    quiz_result = QuizResult(
        user_id=current_user.id if current_user.is_authenticated else None,
        session_id=session.get('quiz_session_id'),
        answers=json.dumps(session['quiz_answers']),
        career_recommendations=json.dumps(recommendations)
    )
    db.session.add(quiz_result)
    db.session.commit()
    
    # end quiz_results
    # Get detailed career information
    career_details = []
    for rec in recommendations:
        career = Career.query.filter_by(category=rec['category']).first()
        if career:
            career_info = {
                'name': career.name,
                'category': career.category,
                'description': career.description,
                'job_roles': json.loads(career.job_roles) if career.job_roles else [],
                'salary_range': career.salary_range,
                'match_percentage': rec['match_percentage']
            }
            career_details.append(career_info)
    
    return render_template('results.html', 
                         recommendations=career_details,
                         quiz_session_id=session.get('quiz_session_id'))

@app.route('/career-explorer')
def career_explorer():
    careers = Career.query.all()
    career_data = []
    
    for career in careers:
        career_info = {
            'id': career.id,
            'name': career.name,
            'category': career.category,
            'description': career.description,
            'required_education': career.required_education,
            'job_roles': json.loads(career.job_roles) if career.job_roles else [],
            'salary_range': career.salary_range,
            'growth_opportunities': career.growth_opportunities,
            'skills_required': json.loads(career.skills_required) if career.skills_required else []
        }
        career_data.append(career_info)
    
    return render_template('career_explorer.html', careers=career_data)

@app.route('/college-finder')
def college_finder():
    # Get filter parameters
    state_filter = request.args.get('state', '')
    type_filter = request.args.get('type', '')
    search_query = request.args.get('search', '')
    
    # Build query
    query = College.query
    
    if state_filter:
        query = query.filter(College.state.ilike(f'%{state_filter}%'))
    
    if type_filter:
        query = query.filter(College.type.ilike(f'%{type_filter}%'))
    
    if search_query:
        query = query.filter(College.name.ilike(f'%{search_query}%'))
    
    colleges = query.all()
    
    # Get unique states and types for filters
    all_states = db.session.query(College.state).distinct().all()
    all_types = db.session.query(College.type).distinct().all()
    
    states = [state[0] for state in all_states]
    types = [type_[0] for type_ in all_types]
    
    # Format college data
    college_data = []
    for college in colleges:
        college_info = {
            'id': college.id,
            'name': college.name,
            'state': college.state,
            'city': college.city,
            'type': college.type,
            'courses': json.loads(college.courses) if college.courses else [],
            'fees_range': college.fees_range,
            'facilities': json.loads(college.facilities) if college.facilities else [],
            'cutoff_info': college.cutoff_info,
            'seats': college.seats,
            'scholarships': college.scholarships,
            'website': college.website
        }
        college_data.append(college_info)
    
    return render_template('college_finder.html', 
                         colleges=college_data,
                         states=states,
                         types=types,
                         current_state=state_filter,
                         current_type=type_filter,
                         current_search=search_query)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

"""
Chatbot API (Gemini)
"""
@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json(silent=True) or {}
    user_message = (data.get('message') or '').strip()
    if not user_message:
        return jsonify({"error": "message is required"}), 400
    
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return jsonify({"error": "Server not configured: GEMINI_API_KEY missing"}), 500

    # Minimal payload (matches your working curl)
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_message}
                ]
            }
        ]
    }

    import requests
    model = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    try:
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': api_key,
        }
        r = requests.post(url, json=payload, headers=headers, timeout=25)
        if r.status_code >= 400:
            return jsonify({"error": f"Upstream {r.status_code}", "details": r.text[:500]}), 502
        resp = r.json()
        parts = (resp.get('candidates') or [{}])[0].get('content', {}).get('parts', [])
        reply = "".join(p.get('text', '') for p in parts).strip()
        if not reply:
            return jsonify({"error": "Empty response from model", "raw": resp}), 502
        return jsonify({"reply": reply})
    except requests.Timeout:
        return jsonify({"error": "Upstream timeout"}), 504
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
