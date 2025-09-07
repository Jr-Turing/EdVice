from app import db
from datetime import datetime
import json

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

def initialize_data():
    """Initialize the database with sample data if empty"""
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
                'skills_required': json.dumps(['Leadership', 'Strategic Thinking', 'Communication', 'Problem Solving'])
            }
        ]
        
        for career_data in careers_data:
            career = Career(**career_data)
            db.session.add(career)
    
    db.session.commit()
