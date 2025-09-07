from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json
import uuid

# User Management Models
class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # student, parent, teacher, admin
    phone = db.Column(db.String(15))
    category = db.Column(db.String(10))  # General, SC, ST, OBC
    class_level = db.Column(db.String(10))  # 10th, 12th
    state = db.Column(db.String(100))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True)
    saved_colleges = db.relationship('SavedCollege', backref='user', lazy=True)
    mentorship_sessions = db.relationship('MentorshipSession', foreign_keys='MentorshipSession.user_id', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class ParentChildRelation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    child_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    relationship_type = db.Column(db.String(20), default='parent')  # parent, guardian
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    parent = db.relationship('User', foreign_keys=[parent_id], backref='children')
    child = db.relationship('User', foreign_keys=[child_id], backref='parents')

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=True)
    session_id = db.Column(db.String(100), nullable=False)
    answers = db.Column(db.Text, nullable=False)  # JSON string of answers
    career_recommendations = db.Column(db.Text)  # JSON string of recommendations
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Engineering, Medical, Arts, etc.
    courses = db.Column(db.Text)  # JSON string of available courses
    fees_range = db.Column(db.String(50))
    facilities = db.Column(db.Text)  # JSON string of facilities
    cutoff_info = db.Column(db.Text)
    seats = db.Column(db.Integer)
    scholarships = db.Column(db.Text)
    website = db.Column(db.String(200))

class Career(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    required_education = db.Column(db.Text)
    job_roles = db.Column(db.Text)  # JSON string
    salary_range = db.Column(db.String(50))
    growth_opportunities = db.Column(db.Text)
    skills_required = db.Column(db.Text)  # JSON string
    path_after_10th = db.Column(db.Text)  # JSON string
    path_after_12th = db.Column(db.Text)  # JSON string
    government_exams = db.Column(db.Text)  # JSON string
    reservation_benefits = db.Column(db.Text)  # JSON string

# Scholarship and Exam Models
class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    provider = db.Column(db.String(200))  # Government body/organization
    category_eligible = db.Column(db.Text)  # JSON: ["SC", "ST", "OBC", "General"]
    class_eligible = db.Column(db.Text)  # JSON: ["10th", "12th", "graduation"]
    min_marks = db.Column(db.Float)
    max_family_income = db.Column(db.Integer)
    amount = db.Column(db.String(100))
    description = db.Column(db.Text)
    eligibility_criteria = db.Column(db.Text)
    application_deadline = db.Column(db.DateTime)
    application_link = db.Column(db.String(500))
    documents_required = db.Column(db.Text)  # JSON string
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    exam_type = db.Column(db.String(50))  # entrance, competitive, board
    conducting_body = db.Column(db.String(200))
    description = db.Column(db.Text)
    eligibility_class = db.Column(db.Text)  # JSON: ["10th", "12th"]
    subjects_covered = db.Column(db.Text)  # JSON string
    exam_pattern = db.Column(db.Text)
    syllabus_link = db.Column(db.String(500))
    registration_start = db.Column(db.DateTime)
    registration_end = db.Column(db.DateTime)
    exam_date = db.Column(db.DateTime)
    result_date = db.Column(db.DateTime)
    application_fee = db.Column(db.String(100))
    official_website = db.Column(db.String(500))
    category_benefits = db.Column(db.Text)  # JSON string
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# User Interaction Models
class SavedCollege(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    college = db.relationship('College', backref='saved_by_users')

class SavedScholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarship.id'), nullable=False)
    application_status = db.Column(db.String(50), default='saved')  # saved, applied, approved, rejected
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='saved_scholarships')
    scholarship = db.relationship('Scholarship', backref='saved_by_users')

class MentorshipSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    mentor_type = db.Column(db.String(20), default='ai')  # ai, human
    mentor_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=True)  # for human mentors
    session_type = db.Column(db.String(50))  # chat, career_guidance, exam_prep
    messages = db.Column(db.Text)  # JSON string of conversation
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    mentor = db.relationship('User', foreign_keys=[mentor_id], backref='mentoring_sessions_as_mentor')

class CareerSimulation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    scenario_name = db.Column(db.String(200))  # "What if I choose Science?"
    chosen_stream = db.Column(db.String(50))
    chosen_subjects = db.Column(db.Text)  # JSON string
    expected_careers = db.Column(db.Text)  # JSON string
    salary_projections = db.Column(db.Text)  # JSON string
    simulation_results = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50))  # scholarship, exam, career, system
    reference_id = db.Column(db.Integer)  # ID of related scholarship/exam
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='notifications')

def initialize_data():
    """Initialize the database with sample data if empty"""
    # Initialize scholarships
    if Scholarship.query.count() == 0:
        scholarships_data = [
            {
                'name': 'Post Matric Scholarship for SC Students',
                'provider': 'Ministry of Social Justice and Empowerment',
                'category_eligible': json.dumps(['SC']),
                'class_eligible': json.dumps(['12th', 'graduation', 'post_graduation']),
                'min_marks': 50.0,
                'max_family_income': 250000,
                'amount': 'Up to ₹1,20,000 per year',
                'description': 'Financial assistance for Scheduled Caste students pursuing higher education',
                'eligibility_criteria': 'Must belong to SC category, family income below 2.5 LPA, minimum 50% marks',
                'application_deadline': datetime(2024, 12, 31),
                'application_link': 'https://scholarships.gov.in',
                'documents_required': json.dumps(['Caste Certificate', 'Income Certificate', 'Mark Sheets', 'Bank Details']),
                'is_active': True
            },
            {
                'name': 'Post Matric Scholarship for ST Students',
                'provider': 'Ministry of Tribal Affairs',
                'category_eligible': json.dumps(['ST']),
                'class_eligible': json.dumps(['12th', 'graduation', 'post_graduation']),
                'min_marks': 50.0,
                'max_family_income': 250000,
                'amount': 'Up to ₹1,20,000 per year',
                'description': 'Financial assistance for Scheduled Tribe students pursuing higher education',
                'eligibility_criteria': 'Must belong to ST category, family income below 2.5 LPA, minimum 50% marks',
                'application_deadline': datetime(2024, 12, 31),
                'application_link': 'https://scholarships.gov.in',
                'documents_required': json.dumps(['Tribal Certificate', 'Income Certificate', 'Mark Sheets', 'Bank Details']),
                'is_active': True
            },
            {
                'name': 'Central Sector Scholarship for Top Class Education',
                'provider': 'Ministry of Education',
                'category_eligible': json.dumps(['General', 'SC', 'ST', 'OBC']),
                'class_eligible': json.dumps(['12th']),
                'min_marks': 80.0,
                'max_family_income': 800000,
                'amount': 'Up to ₹20,000 per year',
                'description': 'Merit-based scholarship for students with top performance in 12th board exams',
                'eligibility_criteria': 'Top 1% students in 12th board exam, family income below 8 LPA',
                'application_deadline': datetime(2024, 10, 31),
                'application_link': 'https://scholarships.gov.in',
                'documents_required': json.dumps(['12th Mark Sheet', 'Income Certificate', 'Bank Details', 'Domicile Certificate']),
                'is_active': True
            },
            {
                'name': 'Inspire Scholarship for Higher Education',
                'provider': 'Department of Science and Technology',
                'category_eligible': json.dumps(['General', 'SC', 'ST', 'OBC']),
                'class_eligible': json.dumps(['12th']),
                'min_marks': 85.0,
                'max_family_income': 600000,
                'amount': '₹80,000 per year',
                'description': 'Scholarship for students pursuing Science stream in higher education',
                'eligibility_criteria': 'Top 1% in Science subjects, pursuing BSc/BTech, family income below 6 LPA',
                'application_deadline': datetime(2024, 11, 30),
                'application_link': 'https://online-inspire.gov.in',
                'documents_required': json.dumps(['Science Stream Certificate', 'Income Certificate', 'Merit Certificate']),
                'is_active': True
            }
        ]
        
        for scholarship_data in scholarships_data:
            scholarship = Scholarship(**scholarship_data)
            db.session.add(scholarship)
    
    # Initialize exams
    if Exam.query.count() == 0:
        exams_data = [
            {
                'name': 'Joint Entrance Examination (JEE Main)',
                'exam_type': 'entrance',
                'conducting_body': 'National Testing Agency (NTA)',
                'description': 'National level entrance exam for admission to engineering colleges',
                'eligibility_class': json.dumps(['12th']),
                'subjects_covered': json.dumps(['Physics', 'Chemistry', 'Mathematics']),
                'exam_pattern': 'Multiple Choice Questions, 3 hours duration, 300 marks',
                'syllabus_link': 'https://nta.ac.in/jee-main',
                'registration_start': datetime(2024, 12, 1),
                'registration_end': datetime(2025, 1, 15),
                'exam_date': datetime(2025, 4, 15),
                'result_date': datetime(2025, 5, 15),
                'application_fee': 'General: ₹1000, SC/ST: ₹500',
                'official_website': 'https://nta.ac.in',
                'category_benefits': json.dumps({'SC': 'Fee concession, lower cutoff', 'ST': 'Fee concession, lower cutoff', 'OBC': 'Lower cutoff'}),
                'is_active': True
            },
            {
                'name': 'National Eligibility cum Entrance Test (NEET)',
                'exam_type': 'entrance',
                'conducting_body': 'National Testing Agency (NTA)',
                'description': 'National level entrance exam for medical colleges',
                'eligibility_class': json.dumps(['12th']),
                'subjects_covered': json.dumps(['Physics', 'Chemistry', 'Biology']),
                'exam_pattern': 'Multiple Choice Questions, 3 hours duration, 720 marks',
                'syllabus_link': 'https://nta.ac.in/neet',
                'registration_start': datetime(2024, 12, 15),
                'registration_end': datetime(2025, 1, 31),
                'exam_date': datetime(2025, 5, 5),
                'result_date': datetime(2025, 6, 5),
                'application_fee': 'General: ₹1600, SC/ST: ₹900',
                'official_website': 'https://nta.ac.in',
                'category_benefits': json.dumps({'SC': 'Fee concession, reserved seats', 'ST': 'Fee concession, reserved seats', 'OBC': 'Reserved seats'}),
                'is_active': True
            },
            {
                'name': 'Common University Entrance Test (CUET)',
                'exam_type': 'entrance',
                'conducting_body': 'National Testing Agency (NTA)',
                'description': 'Common entrance test for admission to central universities',
                'eligibility_class': json.dumps(['12th']),
                'subjects_covered': json.dumps(['Languages', 'Domain Subjects', 'General Test']),
                'exam_pattern': 'Computer Based Test, subject-wise timing varies',
                'syllabus_link': 'https://nta.ac.in/cuet',
                'registration_start': datetime(2024, 11, 1),
                'registration_end': datetime(2025, 1, 10),
                'exam_date': datetime(2025, 5, 20),
                'result_date': datetime(2025, 6, 20),
                'application_fee': 'Varies by number of subjects chosen',
                'official_website': 'https://nta.ac.in',
                'category_benefits': json.dumps({'SC': 'Fee concession, reserved seats', 'ST': 'Fee concession, reserved seats', 'OBC': 'Reserved seats'}),
                'is_active': True
            }
        ]
        
        for exam_data in exams_data:
            exam = Exam(**exam_data)
            db.session.add(exam)
    
    if College.query.count() == 0:
        # Add sample colleges
        colleges_data = [
            {
                'name': 'Indian Institute of Technology Delhi',
                'state': 'Delhi',
                'city': 'New Delhi',
                'type': 'Engineering',
                'courses': json.dumps(['B.Tech Computer Science', 'B.Tech Mechanical', 'B.Tech Electrical', 'B.Tech Civil']),
                'fees_range': '₹2-3 Lakhs/year',
                'facilities': json.dumps(['Hostel', 'Library', 'Labs', 'Sports Complex', 'Wi-Fi']),
                'cutoff_info': 'JEE Advanced Rank: 1-1000',
                'seats': 1000,
                'scholarships': 'Merit-cum-means scholarship available',
                'website': 'https://home.iitd.ac.in'
            },
            {
                'name': 'Jawaharlal Nehru University',
                'state': 'Delhi',
                'city': 'New Delhi',
                'type': 'Arts & Humanities',
                'courses': json.dumps(['BA History', 'BA Political Science', 'BA Economics', 'MA International Relations']),
                'fees_range': '₹50,000-1 Lakh/year',
                'facilities': json.dumps(['Hostel', 'Library', 'Research Centers', 'Cultural Centers']),
                'cutoff_info': 'CUET Score: 600+',
                'seats': 500,
                'scholarships': 'Need-based scholarships available',
                'website': 'https://www.jnu.ac.in'
            },
            {
                'name': 'All India Institute of Medical Sciences Delhi',
                'state': 'Delhi',
                'city': 'New Delhi',
                'type': 'Medical',
                'courses': json.dumps(['MBBS', 'BDS', 'B.Sc Nursing', 'B.Pharma']),
                'fees_range': '₹1-2 Lakhs/year',
                'facilities': json.dumps(['Hospital', 'Hostel', 'Library', 'Research Labs', 'Cafeteria']),
                'cutoff_info': 'NEET Score: 650+',
                'seats': 100,
                'scholarships': 'Central sector scholarship scheme',
                'website': 'https://www.aiims.edu'
            },
            {
                'name': 'University of Delhi',
                'state': 'Delhi',
                'city': 'New Delhi',
                'type': 'Arts & Science',
                'courses': json.dumps(['B.A Honours', 'B.Sc Honours', 'B.Com Honours', 'BBA']),
                'fees_range': '₹30,000-80,000/year',
                'facilities': json.dumps(['Multiple Colleges', 'Libraries', 'Sports Facilities', 'Cultural Activities']),
                'cutoff_info': 'CUET Score: 500-700',
                'seats': 5000,
                'scholarships': 'Various merit and need-based scholarships',
                'website': 'https://www.du.ac.in'
            },
            {
                'name': 'National Institute of Technology Trichy',
                'state': 'Tamil Nadu',
                'city': 'Tiruchirappalli',
                'type': 'Engineering',
                'courses': json.dumps(['B.Tech CSE', 'B.Tech ECE', 'B.Tech Mechanical', 'B.Arch']),
                'fees_range': '₹1.5-2.5 Lakhs/year',
                'facilities': json.dumps(['Hostel', 'Labs', 'Library', 'Sports', 'Internet']),
                'cutoff_info': 'JEE Main Rank: 1000-10000',
                'seats': 800,
                'scholarships': 'Fee waiver for economically weaker sections',
                'website': 'https://www.nitt.edu'
            }
        ]
        
        for college_data in colleges_data:
            college = College(**college_data)
            db.session.add(college)
    
    if Career.query.count() == 0:
        # Add sample careers
        careers_data = [
            {
                'name': 'Software Engineering',
                'category': 'Technology',
                'description': 'Design, develop, and maintain software applications and systems',
                'required_education': 'B.Tech/B.E in Computer Science, Information Technology',
                'job_roles': json.dumps(['Software Developer', 'Full Stack Developer', 'DevOps Engineer', 'Technical Lead']),
                'salary_range': '₹5-25 Lakhs/year',
                'growth_opportunities': 'Senior Developer → Tech Lead → Engineering Manager → CTO',
                'skills_required': json.dumps(['Programming', 'Problem Solving', 'Algorithms', 'System Design'])
            },
            {
                'name': 'Medicine',
                'category': 'Healthcare',
                'description': 'Diagnose and treat patients, promote health and prevent disease',
                'required_education': 'MBBS, MD/MS specialization',
                'job_roles': json.dumps(['General Physician', 'Specialist Doctor', 'Surgeon', 'Medical Researcher']),
                'salary_range': '₹8-50 Lakhs/year',
                'growth_opportunities': 'Junior Doctor → Senior Specialist → Department Head → Medical Director',
                'skills_required': json.dumps(['Medical Knowledge', 'Communication', 'Empathy', 'Decision Making'])
            },
            {
                'name': 'Civil Services',
                'category': 'Government',
                'description': 'Serve the public through administrative roles in government',
                'required_education': 'Any Bachelor\'s degree + UPSC examination',
                'job_roles': json.dumps(['IAS Officer', 'IPS Officer', 'IFS Officer', 'District Collector']),
                'salary_range': '₹7-30 Lakhs/year',
                'growth_opportunities': 'Assistant Secretary → Joint Secretary → Additional Secretary → Secretary',
                'skills_required': json.dumps(['Leadership', 'Public Administration', 'Communication', 'Analytical Thinking'])
            },
            {
                'name': 'Teaching',
                'category': 'Education',
                'description': 'Educate and inspire students across various subjects and levels',
                'required_education': 'B.Ed, M.Ed, Subject specialization',
                'job_roles': json.dumps(['School Teacher', 'Professor', 'Education Administrator', 'Curriculum Designer']),
                'salary_range': '₹3-15 Lakhs/year',
                'growth_opportunities': 'Teacher → Senior Teacher → Principal → Education Director',
                'skills_required': json.dumps(['Subject Knowledge', 'Communication', 'Patience', 'Creativity'])
            },
            {
                'name': 'Business Management',
                'category': 'Business',
                'description': 'Manage business operations, strategy, and organizational growth',
                'required_education': 'BBA, MBA, Bachelor\'s in any field + management skills',
                'job_roles': json.dumps(['Business Analyst', 'Project Manager', 'Operations Manager', 'CEO']),
                'salary_range': '₹4-40 Lakhs/year',
                'growth_opportunities': 'Analyst → Manager → Senior Manager → Director → VP',
                'skills_required': json.dumps(['Leadership', 'Strategic Thinking', 'Communication', 'Problem Solving']),
                'path_after_10th': json.dumps(['Commerce Stream', 'Business Studies', 'Economics', 'Accountancy']),
                'path_after_12th': json.dumps(['BBA', 'B.Com', 'BA Economics', 'Integrated MBA']),
                'government_exams': json.dumps(['UPSC CSE', 'SSC CGL', 'Bank PO', 'RBI Grade B']),
                'reservation_benefits': json.dumps({'SC': '15% reservation', 'ST': '7.5% reservation', 'OBC': '27% reservation'})
            }
        ]
        
        # Update existing careers with new fields
        for i, career_data in enumerate(careers_data):
            if i == 0:  # Software Engineering
                career_data.update({
                    'path_after_10th': json.dumps(['Science Stream with PCM', 'Computer Science Optional']),
                    'path_after_12th': json.dumps(['B.Tech Computer Science', 'B.Sc Computer Science', 'BCA']),
                    'government_exams': json.dumps(['GATE', 'ISRO', 'DRDO', 'Railway Technical']),
                    'reservation_benefits': json.dumps({'SC': '15% reservation in PSUs', 'ST': '7.5% reservation in PSUs', 'OBC': '27% reservation in PSUs'})
                })
            elif i == 1:  # Medicine
                career_data.update({
                    'path_after_10th': json.dumps(['Science Stream with PCB', 'Biology and Chemistry focus']),
                    'path_after_12th': json.dumps(['MBBS', 'BDS', 'BAMS', 'BHMS', 'B.Pharma']),
                    'government_exams': json.dumps(['NEET', 'AIIMS', 'JIPMER', 'State Medical Entrance']),
                    'reservation_benefits': json.dumps({'SC': '15% reservation in medical colleges', 'ST': '7.5% reservation', 'OBC': '27% reservation'})
                })
            elif i == 2:  # Civil Services
                career_data.update({
                    'path_after_10th': json.dumps(['Any Stream', 'Focus on Social Sciences recommended']),
                    'path_after_12th': json.dumps(['BA', 'B.Sc', 'B.Com', 'B.Tech', 'Any Graduate Degree']),
                    'government_exams': json.dumps(['UPSC CSE', 'State PSC', 'SSC', 'Railway Group A']),
                    'reservation_benefits': json.dumps({'SC': '15% reservation', 'ST': '7.5% reservation', 'OBC': '27% reservation'})
                })
            elif i == 3:  # Teaching
                career_data.update({
                    'path_after_10th': json.dumps(['Any Stream based on subject interest']),
                    'path_after_12th': json.dumps(['B.Ed', 'BA B.Ed', 'B.Sc B.Ed', 'Subject Graduation + B.Ed']),
                    'government_exams': json.dumps(['CTET', 'State TET', 'DSSSB', 'KVS', 'NVS']),
                    'reservation_benefits': json.dumps({'SC': '15% reservation in govt schools', 'ST': '7.5% reservation', 'OBC': '27% reservation'})
                })
            
            career = Career(**career_data)
            db.session.add(career)
    
    db.session.commit()
