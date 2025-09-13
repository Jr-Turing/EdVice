from flask import render_template, request, session, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from extensions import db
from models import QuizResult, College, Career, User, ParentChildRelation
from quiz_data import QUIZ_QUESTIONS, analyze_quiz_results
import json
import uuid
import os
from dotenv import load_dotenv

def register_routes(app):
    # Import blueprints
    from auth_routes import auth_bp
    from advanced_routes import advanced_bp
    
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
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)
        
        # Build query
        query = College.query
        
        if state_filter:
            query = query.filter(College.state.ilike(f'%{state_filter}%'))
        
        if type_filter:
            query = query.filter(College.type.ilike(f'%{type_filter}%'))
        
        if search_query:
            query = query.filter(College.name.ilike(f'%{search_query}%'))
        
        # Order by name for consistent pagination
        query = query.order_by(College.name.asc())

        # Paginate results (compatible with Flask-SQLAlchemy 3)
        try:
            pagination = db.paginate(query, page=page, per_page=per_page, error_out=False)
            colleges_page = pagination.items
            total = pagination.total
            pages = pagination.pages
            has_next = pagination.has_next
            has_prev = pagination.has_prev
            next_num = pagination.next_num
            prev_num = pagination.prev_num
        except Exception:
            # Fallback manual pagination for environments without db.paginate
            total = query.count()
            pages = (total + per_page - 1) // per_page
            offset = (page - 1) * per_page
            colleges_page = query.limit(per_page).offset(offset).all()
            has_prev = page > 1
            has_next = page < pages
            next_num = page + 1 if has_next else None
            prev_num = page - 1 if has_prev else None
        
        # Get unique states and types for filters
        all_states = db.session.query(College.state).distinct().all()
        all_types = db.session.query(College.type).distinct().all()
        
        states = [state[0] for state in all_states]
        types = [type_[0] for type_ in all_types]
        
        # Format college data
        college_data = []
        for college in colleges_page:
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
                             current_search=search_query,
                             page=page,
                             per_page=per_page,
                             total=total,
                             pages=pages,
                             has_next=has_next,
                             has_prev=has_prev,
                             next_num=next_num,
                             prev_num=prev_num)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/newsletter')
    def newsletter():
        return render_template('newsletter.html')

    @app.route('/sitemap.xml')
    def sitemap():
        from datetime import datetime
        return render_template('sitemap.xml', moment=lambda: datetime.utcnow()), 200, {'Content-Type': 'application/xml'}

    @app.route('/robots.txt')
    def robots():
        return app.send_static_file('robots.txt')

    # Helper functions for chatbot
    def is_career_related_query(message):
        """Check if the user query is related to career guidance or education"""
        # Handle greetings and general queries
        greeting_patterns = [
            'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
            'greetings', 'what can you help', 'what can you do', 'how can you help',
            'what is this', 'who are you', 'introduce yourself'
        ]
        
        message_lower = message.lower().strip()
        
        # Check if it's a greeting or general query about the bot
        if any(pattern in message_lower for pattern in greeting_patterns):
            return True  # We'll handle greetings as a special case
        
        career_keywords = [
            # Education & Career
            'career', 'job', 'profession', 'education', 'study', 'course', 'degree', 'diploma',
            'college', 'university', 'school', 'admission', 'entrance', 'exam', 'test',
            'scholarship', 'fee', 'eligibility', 'qualification', 'certificate',
            
            # Specific Exams
            'neet', 'jee', 'cuet', 'jkcet', 'upsc', 'ssc', 'gate', 'cat', 'mat', 'gmat',
            'ielts', 'toefl', 'sat', 'gre', 'clat', 'nift', 'cmat', 'xat',
            
            # Fields & Subjects
            'engineering', 'medical', 'doctor', 'nurse', 'teacher', 'lawyer', 'management',
            'business', 'commerce', 'science', 'arts', 'humanities', 'technology', 'computer',
            'pharmacy', 'dentistry', 'veterinary', 'agriculture', 'architecture',
            
            # J&K Specific
            'jammu', 'kashmir', 'srinagar', 'jammu university', 'kashmir university',
            'nit srinagar', 'iit jammu', 'pmsss', 'j&k', 'jk',
            
            # Career Guidance
            'guidance', 'advice', 'help', 'suggest', 'recommend', 'choose', 'select',
            'future', 'opportunity', 'scope', 'salary', 'placement', 'internship'
        ]
        
        return any(keyword in message_lower for keyword in career_keywords)

    def is_greeting_query(message):
        """Check if the message is a greeting or general bot inquiry"""
        greeting_patterns = [
            'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
            'greetings', 'what can you help', 'what can you do', 'how can you help',
            'what is this', 'who are you', 'introduce yourself', 'tell me about yourself'
        ]
        
        message_lower = message.lower().strip()
        return any(pattern in message_lower for pattern in greeting_patterns)

    def generate_greeting_response():
        """Generate a structured greeting response"""
        import random
        
        greetings = [
            {
                "summary": "Hello! 👋 I'm your EdVise Career Assistant, ready to guide your educational journey in J&K!",
                "points": [
                    "Get personalized career guidance based on your interests and academic strengths.",
                    "Discover entrance exams like NEET, JEE, CUET, JKCET with preparation strategies.",
                    "Explore top government and private colleges in Jammu & Kashmir with admission details.",
                    "Learn about scholarships including PMSSS, state merit awards, and financial assistance.",
                    "Receive expert advice on admission timelines, eligibility criteria, and career pathways."
                ]
            },
            {
                "summary": "Welcome to EdVise! 🎓 Your trusted companion for education and career decisions in J&K.",
                "points": [
                    "Ask me about any career field - from engineering to medicine, arts to commerce.",
                    "Get updated information on competitive exams, dates, syllabus, and cut-offs.",
                    "Find the perfect college match based on your preferences and qualifications.",
                    "Discover government schemes, scholarships, and funding opportunities for students.",
                    "Plan your academic journey with step-by-step guidance and expert recommendations."
                ]
            },
            {
                "summary": "Hi there! 🌟 I'm here to help you make informed decisions about your future in J&K.",
                "points": [
                    "Share your interests and I'll suggest suitable career paths and opportunities.",
                    "Get comprehensive exam guidance including NEET, JEE, and state-level tests.",
                    "Explore colleges in Srinagar, Jammu, and across J&K with detailed information.",
                    "Learn about PMSSS and other scholarship programs available for J&K students.",
                    "Receive personalized advice on courses, admissions, and career planning."
                ]
            }
        ]
        
        selected_greeting = random.choice(greetings)
        
        return {
            "status": "success",
            "queryType": "greeting",
            "response": {
                "summary": selected_greeting["summary"],
                "points": selected_greeting["points"],
                "wordCount": len(' '.join(selected_greeting["points"] + [selected_greeting["summary"]]).split())
            }
        }

    def determine_query_type(message):
        """Determine the type of career query"""
        message_lower = message.lower()
        
        if any(exam in message_lower for exam in ['neet', 'jee', 'cuet', 'jkcet', 'upsc']):
            return 'exam_guidance'
        elif any(word in message_lower for word in ['college', 'university', 'admission']):
            return 'college_guidance'
        elif any(word in message_lower for word in ['scholarship', 'fee', 'financial']):
            return 'scholarship_guidance'
        elif any(word in message_lower for word in ['career', 'job', 'profession']):
            return 'career_guidance'
        else:
            return 'general_education'

    def format_career_response(ai_response, query_type, word_count):
        """Format AI response into structured JSON format"""
        # Split the response into points
        lines = [line.strip() for line in ai_response.split('\n') if line.strip()]
        points = []
        summary = ""
        
        # Extract summary (first non-empty line or paragraph)
        if lines:
            summary = lines[0]
            
        # Extract points from the response
        for line in lines[1:]:
            if line and (line.startswith(('-', '•', '*')) or 'point' in line.lower() or len(line) > 20):
                # Clean up the point text
                point = line.lstrip('-•* ').strip()
                if len(point) > 10:  # Only add substantial points
                    points.append(point)
        
        # If no clear points found, create them from sentences
        if len(points) < 3:
            sentences = ai_response.replace('\n', ' ').split('. ')
            points = [sent.strip() + '.' for sent in sentences if len(sent.strip()) > 20][:5]
        
        # Ensure we have 3-5 points
        if len(points) > 5:
            points = points[:5]
        elif len(points) < 3:
            # Add generic helpful points if needed
            points.extend([
                "Consider consulting with career counselors for personalized guidance.",
                "Research thoroughly about admission requirements and deadlines.",
                "Explore government schemes and scholarships available in J&K."
            ])
            points = points[:5]
        
        return {
            "status": "success",
            "queryType": query_type,
            "response": {
                "summary": summary or "Here is the career guidance you requested.",
                "points": points,
                "wordCount": word_count
            }
        }

    def count_words(text):
        """Count words in text"""
        return len(text.split())

    @app.route('/api/chat', methods=['POST'])
    def chat_api():
        data = request.get_json(silent=True) or {}
        user_message = (data.get('message') or '').strip()
        if not user_message:
            return jsonify({"error": "message is required"}), 400
        
        # Check if it's a greeting first
        if is_greeting_query(user_message):
            return jsonify(generate_greeting_response())
        
        # Check if query is career-related
        if not is_career_related_query(user_message):
            return jsonify({
                "status": "error",
                "queryType": "unsupported",
                "response": {
                    "message": "Sorry, I can only provide answers related to career guidance and education in Jammu & Kashmir. Feel free to ask about careers, exams, colleges, or scholarships!"
                }
            })
        
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return jsonify({"error": "Server not configured: GEMINI_API_KEY missing"}), 500

        # Determine query type
        query_type = determine_query_type(user_message)
        
        # Enhanced prompt for structured career guidance
        system_prompt = f"""You are a career guidance counselor specializing in education and career opportunities in Jammu & Kashmir, India. 
        
        User Query: {user_message}
        
        Please provide a comprehensive response in exactly 150-250 words that includes:
        
        1. A brief summary sentence
        2. 4-5 specific actionable points related to:
           - Relevant exams (NEET, JKCET, CUET, JEE, etc.)
           - Government and private colleges in J&K
           - Available scholarships (PMSSS, state merit, etc.)
           - Career pathways and opportunities
           - Admission timelines and preparation tips
        
        Format your response as:
        
        [Summary sentence]
        
        • Point 1: [Specific guidance]
        • Point 2: [Specific guidance]  
        • Point 3: [Specific guidance]
        • Point 4: [Specific guidance]
        • Point 5: [Specific guidance]
        
        Focus specifically on J&K education system, local colleges, and opportunities available to students in the region.
        Keep the response practical, actionable, and within 150-250 words."""

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": system_prompt}
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
            
            # Count words and format response
            word_count = count_words(reply)
            formatted_response = format_career_response(reply, query_type, word_count)
            
            return jsonify(formatted_response)
            
        except requests.Timeout:
            return jsonify({"error": "Upstream timeout"}), 504
        except Exception as e:
            return jsonify({"error": "Server error", "details": str(e)}), 500



