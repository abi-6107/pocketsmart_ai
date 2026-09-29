# PocketSmart AI

## AI-Powered Budget Planning Website

PocketSmart AI is a web-based AI-powered budget planning system designed to help users plan their spending for everyday needs. The system provides personalized budget recommendations for Home Interior, Party Planning, and Jewelry based on the user's requirements and available budget.

The application combines a simple web interface with AI-powered recommendations to help users make informed budget-planning decisions.

---

## 1. Problem Statement

Managing a budget for different personal requirements can be difficult. Users often need to compare their available budget with their expected expenses and decide how much to spend on different items.

Traditional budgeting methods may require manual calculations and do not provide personalized recommendations.

PocketSmart AI addresses this problem by providing an easy-to-use website where users can enter their requirements and budget and receive AI-powered recommendations.

---

## 2. Project Objectives

The main objectives of PocketSmart AI are:

- To provide a simple online budget-planning system.
- To help users plan their expenses according to their available budget.
- To provide personalized AI-based recommendations.
- To support different budgeting categories.
- To maintain users' budget history.
- To provide a user-friendly dashboard.
- To reduce the effort required for manual budget planning.

---

## 3. Key Features

### Home Interior Budget Planner

Users can plan their budget for home interior requirements and receive recommendations based on their available budget.

### Party Budget Planner

Users can enter their party requirements and budget and receive suggestions for managing party-related expenses.

### Jewelry Budget Planner

Users can plan their jewelry purchases according to their available budget and requirements.

### AI-Powered Recommendations

The system uses AI to generate personalized suggestions based on the information provided by the user.

### User Authentication

The application provides registration and login functionality for users.

### Dashboard

The dashboard provides access to the different budget-planning features.

### Budget History

Users can view previously created budget plans.

---

## 4. Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

### Backend

- Python
- FastAPI
- Uvicorn

### Database

- SQLite

### AI

- Google Gemini AI

### Development Tools

- Visual Studio Code
- Git
- GitHub

---

## 5. System Architecture

The general working flow of the application is:

```text
User
  |
  v
Web Browser
  |
  v
FastAPI Web Application
  |
  +----------------------+
  |                      |
  v                      v
Database              AI Service
  |                      |
  |                      v
  |                AI Recommendation
  |                      |
  +----------+-----------+
             |
             v
        User Dashboard
```

The user interacts with the website through a browser. FastAPI handles the application requests, the database stores application information, and the AI service generates personalized recommendations.

---

## 6. Main Modules

### Authentication Module

Handles:

- User registration
- User login
- User sessions
- Logout

### Dashboard Module

Provides access to the application's main features.

### Home Budget Module

Handles home interior budget planning.

### Party Budget Module

Handles party budget planning.

### Jewelry Budget Module

Handles jewelry budget planning.

### Recommendation Module

Processes the user's requirements and generates AI-based recommendations.

### Database Module

Handles database initialization and storage of application information.

### History Module

Allows users to view their previous budget-planning activities.

---

## 7. Project Structure

```text
pocket_smart_ai-main/
│
├── app/
│   ├── __init__.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── pages.py
│   │   ├── planners.py
│   │   └── session.py
│   │
│   └── services/
│       ├── auth.py
│       ├── database.py
│       ├── gemini_utils.py
│       └── recommendations.py
│
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── app.js
│   ├── images/
│   └── uploads/
│
├── templates/
│   ├── app_nav.html
│   ├── base.html
│   ├── dashboard.html
│   ├── history.html
│   ├── home_planner.html
│   ├── index.html
│   └── register.html
│
├── tests/
│   └── test_app.py
│
├── .env
├── .env.example
├── .gitignore
├── main.py
├── Procfile
├── README.md
├── requirements.txt
├── run.sh
└── setup.sh
```

---

## 8. How the System Works

### Step 1: User Opens the Website

The user opens PocketSmart AI through a web browser.

### Step 2: User Registers or Logs In

A new user can register, while an existing user can log in.

### Step 3: User Opens the Dashboard

After authentication, the user can access the available budget planners.

### Step 4: User Selects a Planner

The user can select:

- Home Interior
- Party
- Jewelry

### Step 5: User Enters Requirements

The user provides the required information and available budget.

### Step 6: AI Processes the Information

The application sends the relevant information to the AI recommendation service.

### Step 7: Recommendation is Generated

The system provides personalized recommendations based on the user's requirements and budget.

### Step 8: User Views the Result

The user can review the recommendation and use it for planning.

---

## 9. Installation and Setup

### Prerequisites

Make sure the following are installed:

- Python 3
- pip
- Git
- Visual Studio Code

### Clone the Repository

```bash
git clone https://github.com/abi-6107/pocketsmart_ai.git
```

Move into the project directory:

```bash
cd pocketsmart_ai
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment - Windows

```cmd
.venv\Scripts\activate
```

### Activate Virtual Environment - Linux

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 10. Environment Configuration

Create or update the `.env` file with the required environment variables.

Example:

```text
GEMINI_API_KEY=your_api_key_here
```

Do not upload private API keys to GitHub.

Use `.env.example` to show the required environment variable format without exposing the actual key.

---

## 11. Running the Application

From the project directory:

```bash
python main.py
```

The application can then be accessed through:

```text
http://127.0.0.1:8000
```

---

## 12. Testing

The project contains automated tests in the `tests` directory.

Run the tests using:

```bash
pytest
```

---

## 13. Expected Benefits

PocketSmart AI provides:

- Easy budget planning
- Personalized recommendations
- Multiple planning categories
- Simple user interface
- Centralized budget history
- AI-assisted decision support
- Browser-based access

---

## 14. Future Enhancements

Possible future improvements include:

- Additional budget categories
- Improved AI recommendations
- Expense tracking
- Graphical spending analysis
- Monthly budget reports
- Exporting budget reports
- Mobile-responsive improvements
- Advanced user preferences
- More detailed financial insights

---

## 15. Conclusion

PocketSmart AI provides a web-based approach to personal budget planning by combining a simple interface with AI-powered recommendations. The system allows users to plan budgets for home interiors, parties, and jewelry while keeping their previous planning information organized.

The project demonstrates the integration of Python, FastAPI, database management, web technologies, and generative AI into a practical budget-planning application.

---

## 16. License

This project is developed for educational purposes.
