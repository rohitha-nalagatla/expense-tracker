# Personal Expense Tracking System

## 📋 Project Overview

A comprehensive web-based application for managing personal finances, built with Flask and Bootstrap.
## ✨ Features

- **User Authentication**: Secure registration and login system
- **Expense Management**: Add, edit, delete, and categorize expenses
- **Income Tracking**: Record income from multiple sources  
- **Budget Management**: Set monthly budgets and monitor spending
- **Financial Reports**: Generate detailed reports with visualizations
- **Data Export**: Export data in CSV format for external analysis
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask 2.3+
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Authentication**: Flask-Login, Werkzeug Security
- **Forms**: Flask-WTF, WTForms
- **Frontend**: Bootstrap 5, Chart.js, Jinja2 Templates
- **Migrations**: Flask-Migrate

## 📁 Project Structure

```
personal-expense-tracker/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── auth/                # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── routes.py        # Auth routes
│   │   └── forms.py         # Auth forms
│   ├── main/                # Main blueprint
│   │   ├── __init__.py
│   │   └── routes.py        # Dashboard routes
│   ├── expenses/            # Expenses blueprint
│   │   ├── __init__.py
│   │   └── routes.py        # Expense management routes
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   └── auth/
│   └── static/              # CSS, JS, images
├── migrations/              # Database migrations
├── config.py               # Configuration settings
├── run.py                  # Application entry point
├── init_db.py             # Database initialization
├── setup.ps1              # Windows setup script
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git (optional)

### Installation & Setup

1. **Clone or Download the Project**
   ```bash
   # If using git
   git clone <repository-url>
   cd personal-expense-tracker
   ```

2. **Run Automated Setup (Windows)**
   ```powershell
   # Execute the setup script
   .\setup.ps1
   ```

3. **Manual Setup (Alternative)**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Initialize database
   python init_db.py
   ```

4. **Run the Application**
   ```bash
   python run.py
   ```

5. **Access the Application**
   Open your web browser and navigate to: `http://127.0.0.1:5000`

## 📊 Database Schema

The application uses the following main entities:

- **Users**: Store user accounts with authentication
- **Categories**: Predefined expense and income categories
- **Expenses**: Individual expense records
- **Income**: Income tracking records  
- **Budgets**: Monthly budget settings by category

## 🏗️ Architecture

### Application Factory Pattern
The application uses Flask's application factory pattern for better modularity and testing.

### Blueprint Organization
- **main**: Dashboard and home pages
- **auth**: Authentication (login, register, logout)
- **expenses**: Expense management, budgets, reports

### Database Design
Based on the ER diagram in the project synopsis, implementing:
- User-centric data isolation
- Category-based expense organization
- Budget monitoring and alerts
- Comprehensive audit trails

## 🎯 Current Development Status

### ✅ Completed Features
- [x] Project structure and configuration
- [x] Database models and relationships
- [x] User authentication system
- [x] Basic application structure with blueprints
- [x] Bootstrap-based responsive templates
- [x] Dashboard with financial overview
- [x] Database initialization with default categories

### 🚧 In Progress
- [ ] Expense CRUD operations
- [ ] Income management
- [ ] Budget management
- [ ] Reporting and charts
- [ ] Data export functionality

### 📋 Next Steps

1. **Expense Management Module** (Week 3-4)
   - Add expense form and validation
   - Expense listing and search
   - Edit/delete expense functionality
   - Category-based filtering

2. **Budget and Reporting Features** (Week 5-6)
   - Budget setting and monitoring
   - Report generation
   - Chart visualizations
   - CSV export functionality

## 🔧 Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use descriptive variable and function names
- Add docstrings for classes and functions
- Keep templates organized and reusable

### Database Operations
- Always use SQLAlchemy ORM, avoid raw SQL
- Implement proper error handling with rollback
- Use database migrations for schema changes
- Test database operations thoroughly

### Security Best Practices
- Never store plain text passwords
- Use CSRF protection for all forms
- Implement proper user data isolation
- Validate all user inputs
- Use environment variables for sensitive config

## 📖 Academic Compliance

This project fulfills the requirements for:
- **Course**: BCA-V Project
- **Institution**: Uttaranchal University
- **Guidelines**: Follows university synopsis requirements
- **Documentation**: Comprehensive technical documentation
- **Timeline**: 8-week development schedule

## 🤝 Contributing

This is an academic project, but contributions and suggestions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make changes with proper documentation
4. Submit a pull request

## 📄 License

This project is created for educational purposes as part of the BCA curriculum at Uttaranchal University.

## 📞 Support

For questions or issues:
- Check the documentation
- Review error logs in the console
- Ensure all dependencies are installed correctly
- Verify database initialization completed successfully

---

**Happy Coding! 🚀**