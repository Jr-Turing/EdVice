# Quiz questions data and analysis logic

QUIZ_QUESTIONS = [
    {
        'id': 1,
        'question': 'What type of activities do you enjoy most?',
        'type': 'mcq',
        'options': [
            {'value': 'problem_solving', 'text': 'Solving complex problems and puzzles'},
            {'value': 'helping_others', 'text': 'Helping and caring for others'},
            {'value': 'creative_work', 'text': 'Creating art, writing, or designing'},
            {'value': 'leadership', 'text': 'Leading teams and organizing projects'}
        ]
    },
    {
        'id': 2,
        'question': 'Which subjects did you enjoy most in school?',
        'type': 'mcq',
        'options': [
            {'value': 'stem', 'text': 'Mathematics, Physics, Chemistry'},
            {'value': 'bio_medical', 'text': 'Biology, Chemistry, Health Sciences'},
            {'value': 'humanities', 'text': 'History, Literature, Languages'},
            {'value': 'commerce', 'text': 'Economics, Accounts, Business Studies'}
        ]
    },
    {
        'id': 3,
        'question': 'How do you prefer to work?',
        'type': 'mcq',
        'options': [
            {'value': 'individual', 'text': 'Independently on focused tasks'},
            {'value': 'team', 'text': 'Collaboratively in teams'},
            {'value': 'public', 'text': 'Interacting with the public'},
            {'value': 'research', 'text': 'In research and analysis'}
        ]
    },
    {
        'id': 4,
        'question': 'What motivates you most in your future career?',
        'type': 'mcq',
        'options': [
            {'value': 'innovation', 'text': 'Creating innovative solutions'},
            {'value': 'service', 'text': 'Serving society and making a difference'},
            {'value': 'financial', 'text': 'Financial stability and growth'},
            {'value': 'recognition', 'text': 'Recognition and prestige'}
        ]
    },
    {
        'id': 5,
        'question': 'Which work environment appeals to you?',
        'type': 'mcq',
        'options': [
            {'value': 'tech_office', 'text': 'Modern tech office with latest tools'},
            {'value': 'hospital', 'text': 'Hospital or healthcare facility'},
            {'value': 'government', 'text': 'Government office serving citizens'},
            {'value': 'school', 'text': 'Educational institution'}
        ]
    },
    {
        'id': 6,
        'question': 'How comfortable are you with technology?',
        'type': 'likert',
        'scale': 5,
        'labels': ['Not comfortable', 'Slightly comfortable', 'Moderately comfortable', 'Very comfortable', 'Extremely comfortable']
    },
    {
        'id': 7,
        'question': 'Do you enjoy learning new things regularly?',
        'type': 'yes_no'
    },
    {
        'id': 8,
        'question': 'Are you interested in entrepreneurship or starting your own business?',
        'type': 'yes_no'
    },
    {
        'id': 9,
        'question': 'How important is work-life balance to you?',
        'type': 'likert',
        'scale': 5,
        'labels': ['Not important', 'Slightly important', 'Moderately important', 'Very important', 'Extremely important']
    },
    {
        'id': 10,
        'question': 'Which type of challenges excite you most?',
        'type': 'mcq',
        'options': [
            {'value': 'technical', 'text': 'Technical and analytical challenges'},
            {'value': 'human', 'text': 'Understanding and helping people'},
            {'value': 'creative', 'text': 'Creative and artistic challenges'},
            {'value': 'strategic', 'text': 'Strategic and business challenges'}
        ]
    },
    {
        'id': 11,
        'question': 'What size organization would you prefer to work in?',
        'type': 'mcq',
        'options': [
            {'value': 'startup', 'text': 'Small startup (10-50 people)'},
            {'value': 'medium', 'text': 'Medium company (100-1000 people)'},
            {'value': 'large', 'text': 'Large corporation (1000+ people)'},
            {'value': 'government', 'text': 'Government organization'}
        ]
    },
    {
        'id': 12,
        'question': 'How do you handle stress and pressure?',
        'type': 'mcq',
        'options': [
            {'value': 'analytical', 'text': 'Break down problems systematically'},
            {'value': 'collaborative', 'text': 'Seek help and collaborate with others'},
            {'value': 'calm', 'text': 'Stay calm and focused under pressure'},
            {'value': 'creative', 'text': 'Find creative solutions to problems'}
        ]
    },
    {
        'id': 13,
        'question': 'Are you willing to relocate for better career opportunities?',
        'type': 'yes_no'
    },
    {
        'id': 14,
        'question': 'What type of impact do you want to make?',
        'type': 'mcq',
        'options': [
            {'value': 'technological', 'text': 'Technological advancement'},
            {'value': 'health', 'text': 'Improving health and saving lives'},
            {'value': 'social', 'text': 'Social change and justice'},
            {'value': 'economic', 'text': 'Economic growth and development'}
        ]
    },
    {
        'id': 15,
        'question': 'How important is job security to you?',
        'type': 'likert',
        'scale': 5,
        'labels': ['Not important', 'Slightly important', 'Moderately important', 'Very important', 'Extremely important']
    },
    {
        'id': 16,
        'question': 'Do you prefer structured or flexible work schedules?',
        'type': 'mcq',
        'options': [
            {'value': 'structured', 'text': 'Structured 9-5 schedule'},
            {'value': 'flexible', 'text': 'Flexible timing'},
            {'value': 'project_based', 'text': 'Project-based deadlines'},
            {'value': 'shift_based', 'text': 'Shift-based work'}
        ]
    },
    {
        'id': 17,
        'question': 'What level of education are you willing to pursue?',
        'type': 'mcq',
        'options': [
            {'value': 'undergraduate', 'text': 'Bachelor\'s degree'},
            {'value': 'postgraduate', 'text': 'Master\'s degree'},
            {'value': 'doctoral', 'text': 'PhD or equivalent'},
            {'value': 'professional', 'text': 'Professional certification courses'}
        ]
    },
    {
        'id': 18,
        'question': 'Are you interested in research and development work?',
        'type': 'yes_no'
    },
    {
        'id': 19,
        'question': 'How important is having a prestigious job title?',
        'type': 'likert',
        'scale': 5,
        'labels': ['Not important', 'Slightly important', 'Moderately important', 'Very important', 'Extremely important']
    },
    {
        'id': 20,
        'question': 'What type of learning style suits you best?',
        'type': 'mcq',
        'options': [
            {'value': 'theoretical', 'text': 'Theoretical and conceptual learning'},
            {'value': 'practical', 'text': 'Hands-on practical experience'},
            {'value': 'visual', 'text': 'Visual and graphical learning'},
            {'value': 'discussion', 'text': 'Discussion and debate-based learning'}
        ]
    }
]

def analyze_quiz_results(answers):
    """
    Analyze quiz answers and return career recommendations
    """
    # Initialize scoring for different career categories
    scores = {
        'Technology': 0,
        'Healthcare': 0,
        'Government': 0,
        'Education': 0,
        'Business': 0
    }
    
    # Analyze each answer and add scores
    for question_id, answer in answers.items():
        qid = int(question_id)
        
        if qid == 1:  # Activity preferences
            if answer == 'problem_solving':
                scores['Technology'] += 3
                scores['Business'] += 1
            elif answer == 'helping_others':
                scores['Healthcare'] += 3
                scores['Education'] += 2
            elif answer == 'creative_work':
                scores['Education'] += 2
                scores['Business'] += 1
            elif answer == 'leadership':
                scores['Government'] += 3
                scores['Business'] += 3
        
        elif qid == 2:  # Subject preferences
            if answer == 'stem':
                scores['Technology'] += 4
            elif answer == 'bio_medical':
                scores['Healthcare'] += 4
            elif answer == 'humanities':
                scores['Education'] += 3
                scores['Government'] += 2
            elif answer == 'commerce':
                scores['Business'] += 4
        
        elif qid == 3:  # Work preferences
            if answer == 'individual':
                scores['Technology'] += 2
            elif answer == 'team':
                scores['Business'] += 2
                scores['Technology'] += 1
            elif answer == 'public':
                scores['Government'] += 3
                scores['Healthcare'] += 2
            elif answer == 'research':
                scores['Technology'] += 2
                scores['Healthcare'] += 1
        
        elif qid == 4:  # Motivation
            if answer == 'innovation':
                scores['Technology'] += 3
            elif answer == 'service':
                scores['Healthcare'] += 3
                scores['Government'] += 3
                scores['Education'] += 3
            elif answer == 'financial':
                scores['Business'] += 3
                scores['Technology'] += 2
            elif answer == 'recognition':
                scores['Government'] += 2
                scores['Business'] += 2
        
        elif qid == 5:  # Work environment
            if answer == 'tech_office':
                scores['Technology'] += 4
            elif answer == 'hospital':
                scores['Healthcare'] += 4
            elif answer == 'government':
                scores['Government'] += 4
            elif answer == 'school':
                scores['Education'] += 4
        
        elif qid == 6:  # Technology comfort
            tech_score = int(answer) if answer.isdigit() else 3
            scores['Technology'] += tech_score
            scores['Business'] += max(0, tech_score - 2)
        
        elif qid == 7:  # Learning new things
            if answer == 'yes':
                scores['Technology'] += 2
                scores['Education'] += 2
                scores['Healthcare'] += 1
        
        elif qid == 8:  # Entrepreneurship
            if answer == 'yes':
                scores['Business'] += 3
                scores['Technology'] += 1
        
        elif qid == 10:  # Type of challenges
            if answer == 'technical':
                scores['Technology'] += 3
            elif answer == 'human':
                scores['Healthcare'] += 3
                scores['Education'] += 2
            elif answer == 'creative':
                scores['Education'] += 2
                scores['Business'] += 1
            elif answer == 'strategic':
                scores['Business'] += 3
                scores['Government'] += 2
        
        elif qid == 11:  # Organization size
            if answer == 'startup':
                scores['Technology'] += 2
                scores['Business'] += 2
            elif answer == 'government':
                scores['Government'] += 3
            elif answer == 'large':
                scores['Business'] += 2
        
        elif qid == 14:  # Type of impact
            if answer == 'technological':
                scores['Technology'] += 3
            elif answer == 'health':
                scores['Healthcare'] += 4
            elif answer == 'social':
                scores['Government'] += 3
                scores['Education'] += 3
            elif answer == 'economic':
                scores['Business'] += 3
        
        elif qid == 18:  # Research interest
            if answer == 'yes':
                scores['Technology'] += 2
                scores['Healthcare'] += 2
                scores['Education'] += 1
    
    # Calculate percentages and sort
    total_possible = 50  # Rough estimate of maximum possible score
    recommendations = []
    
    for category, score in scores.items():
        percentage = min(100, (score / total_possible) * 100)
        if percentage > 20:  # Only include categories with significant match
            recommendations.append({
                'category': category,
                'match_percentage': round(percentage)
            })
    
    # Sort by match percentage
    recommendations.sort(key=lambda x: x['match_percentage'], reverse=True)
    
    # Return top 5 recommendations
    return recommendations[:5]
