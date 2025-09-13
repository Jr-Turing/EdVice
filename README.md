# EdVice - Career & Education Advisor

A comprehensive web platform designed to help students make informed career and education decisions. Built with Flask and modern web technologies, EdVice provides personalized career guidance, college recommendations, and educational resources.

## 🚀 Features

### Core Functionality
- **Aptitude Assessment**: Comprehensive 20-question psychometric quiz to determine career interests
- **Career Explorer**: Detailed career paths with salary ranges, job roles, and growth opportunities
- **College Finder**: Search and filter through 2000+ government colleges across India
- **AI Chatbot**: Intelligent career guidance powered by Gemini AI
- **Scholarship Matcher**: Find relevant scholarships based on student profile
- **Exam Calendar**: Track important entrance exam dates and deadlines

### User Experience
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Dark/Light Theme**: User preference-based theme switching
- **Accessibility**: WCAG compliant with keyboard navigation support
- **Performance**: Fast loading with optimized assets and lazy loading
- **SEO Optimized**: Meta tags, structured data, and sitemap

### Technical Features
- **Modern UI/UX**: Clean, intuitive interface with smooth animations
- **Error Handling**: Comprehensive error pages and user feedback
- **Loading States**: Visual feedback during data processing
- **Form Validation**: Client and server-side validation
- **Security**: CSRF protection and secure authentication

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **Flask-Login**: User authentication
- **PostgreSQL/SQLite**: Database
- **Gunicorn**: WSGI server

### Frontend
- **Bootstrap 5**: CSS framework
- **JavaScript (ES6+)**: Modern JavaScript
- **Feather Icons**: Icon library
- **CSS3**: Custom styling with CSS variables

### AI & External Services
- **Google Gemini AI**: Chatbot and career guidance
- **Google Fonts**: Typography

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/edvise-website.git
   cd edvise-website
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your configuration:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///career_advisor.db
   GEMINI_API_KEY=your-gemini-api-key
   ```

5. **Initialize the database**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

## 🚀 Deployment

### Using Vercel (Recommended)

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   vercel
   ```

3. **Set environment variables in Vercel dashboard**

### Using Heroku

1. **Install Heroku CLI**

2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set GEMINI_API_KEY=your-api-key
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

## 📁 Project Structure

```
Edvise-Website/
├── app.py                 # Main Flask application
├── routes.py             # Route definitions
├── models.py             # Database models
├── extensions.py         # Flask extensions
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
├── static/              # Static assets
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── images/         # Images and icons
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Homepage
│   ├── quiz.html       # Aptitude quiz
│   └── ...             # Other pages
└── instance/           # Database files
```

## 🎯 Key Improvements Made

### Performance Optimizations
- Added preconnect links for external resources
- Implemented lazy loading for images
- Optimized CSS and JavaScript loading
- Added debounced scroll handlers

### Accessibility Enhancements
- WCAG compliant focus management
- Skip links for keyboard navigation
- Proper ARIA labels and semantic HTML
- High contrast mode support

### SEO Improvements
- Comprehensive meta tags
- Open Graph and Twitter Card support
- Structured data markup
- XML sitemap and robots.txt

### User Experience
- Loading states and skeleton screens
- Smooth animations and transitions
- Error handling with helpful messages
- Mobile-first responsive design

### Code Quality
- Fixed duplicate route registration
- Added proper error handlers
- Improved code organization
- Enhanced security measures

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Tech Questers Team** for the original concept and development
- **Google Gemini AI** for intelligent career guidance
- **Bootstrap** for the responsive framework
- **Feather Icons** for the beautiful icon set

## 📞 Support

For support, email support@edvise.com or join our [Discord community](https://discord.gg/edvise).

---

**Made with ❤️ for Indian Students**
