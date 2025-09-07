from flask import render_template, request, session, redirect, url_for, jsonify
from app import app, db
from models import QuizResult, College, Career
from quiz_data import QUIZ_QUESTIONS, analyze_quiz_results
import json
import uuid

@app.route('/')
def index():
    return render_template('index.html')

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
        session_id=session.get('quiz_session_id'),
        answers=json.dumps(session['quiz_answers']),
        career_recommendations=json.dumps(recommendations)
    )
    db.session.add(quiz_result)
    db.session.commit()
    
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
