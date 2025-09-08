# Career & Education Advisor

## Overview

A modern web application designed to guide Class 10 and 12 students in making informed career decisions with a focus on government college options. The application provides personalized career recommendations through psychometric assessments, college discovery tools, and comprehensive career path exploration. Built to address the confusion students face when choosing streams, careers, and educational institutions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive UI components
- **CSS Framework**: Bootstrap 5 with custom CSS for enhanced styling and animations
- **JavaScript**: Vanilla JavaScript with class-based architecture for interactive components
- **Typography**: Google Fonts (Inter and Poppins) for modern, readable text
- **Icons**: Feather Icons for consistent iconography
- **Responsive Design**: Mobile-first approach with progressive enhancement

### Backend Architecture
- **Web Framework**: Flask with application factory pattern
- **Database ORM**: SQLAlchemy with declarative base model
- **Session Management**: Flask sessions for quiz state persistence
- **Database Schema**: Three core models - QuizResult, College, and Career with JSON field storage for flexible data
- **Application Structure**: Modular design with separate files for models, routes, and quiz logic
- **Configuration**: Environment-based configuration for database URLs and session secrets

### Data Storage Solutions
- **Primary Database**: SQLite for development with PostgreSQL support through environment configuration
- **Connection Pooling**: SQLAlchemy engine options with pool recycling and pre-ping for reliability
- **JSON Fields**: Flexible storage for arrays and complex data structures (courses, facilities, skills)
- **Session Storage**: Flask session management for quiz progress and user state

### Quiz System Architecture
- **Question Engine**: Modular quiz data structure supporting multiple question types (MCQ, Yes/No, Likert scale)
- **Progress Tracking**: Client-side and server-side progress management with visual indicators
- **Result Analysis**: Algorithm-based career matching using quiz responses
- **Data Persistence**: Session-based answer storage with database backup for completed quizzes

### Application Features
- **Landing Page**: Hero section with statistics and call-to-action elements
- **Aptitude Quiz**: Multi-step psychometric assessment with 15-20 questions
- **Career Explorer**: Visual career path mapping with flowcharts and salary information
- **College Finder**: Searchable directory with advanced filtering capabilities
- **Results System**: Personalized recommendations with match percentages and detailed insights

## External Dependencies

### Frontend Dependencies
- **Bootstrap 5.3.0**: CSS framework for responsive design and UI components
- **Feather Icons**: Icon library for consistent visual elements
- **Google Fonts API**: Typography (Inter and Poppins font families)

### Backend Dependencies
- **Flask**: Core web framework for routing and request handling
- **SQLAlchemy**: ORM for database operations and model definitions
- **Werkzeug**: WSGI utilities including ProxyFix middleware for deployment
- **Python Standard Library**: UUID generation, JSON handling, datetime management, logging, and OS environment access

### Database
- **SQLite**: Default database for development and testing environments
- **PostgreSQL**: Production database support through environment configuration
- **Database URL**: Configurable through DATABASE_URL environment variable

### Deployment Configuration
- **Environment Variables**: SESSION_SECRET for session encryption, DATABASE_URL for database connection
- **WSGI Middleware**: ProxyFix for handling proxy headers in production deployments
- **Host Configuration**: Configurable host and port settings for different deployment environments