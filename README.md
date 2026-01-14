# Expense Tracker - Production Ready Django App

A comprehensive expense tracking application built with Django and Django REST Framework. Features user authentication, expense management with categories, real-time visualization, and a RESTful API.

## Features

✅ **User Authentication** - Secure login/signup with Django auth  
✅ **Expense Management** - Create, read, update, delete expenses with categories  
✅ **Real-time Dashboard** - Track expenses with interactive charts (Chart.js)  
✅ **Category Filtering** - Filter expenses by category and date ranges  
✅ **REST API** - Full CRUD API with Django REST Framework  
✅ **Custom Permissions** - Users can only see their own expenses  
✅ **Profile Management** - User profiles with bio and avatar  
✅ **Monthly Statistics** - Breakdown of spending by month and category  
✅ **Responsive UI** - Mobile-friendly design with Tailwind CSS  
✅ **Comprehensive Tests** - 18+ pytest tests with 63%+ code coverage  

## Tech Stack

- **Backend**: Django 5.2.6, Django REST Framework 3.16.1
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Tailwind CSS, Chart.js
- **Authentication**: Session-based + Token-based (DRF)
- **Testing**: pytest, pytest-django, pytest-cov
- **Python**: 3.13.7

## Project Structure

```
expense_tracker/
├── expense_tracker/          # Main Django project config
│   ├── settings.py          # Django settings with DRF config
│   ├── urls.py              # Main URL routing (includes API)
│   ├── asgi.py              # ASGI config
│   └── wsgi.py              # WSGI config
├── expenses/                # Core app
│   ├── models.py            # Expense, Profile, User models
│   ├── serializers.py       # DRF serializers for API
│   ├── api_views.py         # REST API ViewSets
│   ├── api_urls.py          # API URL routing
│   ├── views.py             # Web views for templates
│   ├── forms.py             # Django forms
│   ├── signals.py           # Auto-create Profile on User creation
│   ├── test_api.py          # 18+ comprehensive API tests
│   ├── urls.py              # Web URL routing
│   ├── migrations/          # Database migrations
│   └── templates/           # HTML templates
├── manage.py                # Django management script
├── pytest.ini               # pytest configuration
├── requirements.txt         # Python dependencies
├── db.sqlite3              # SQLite database
└── .env                    # Environment variables
```

## Installation & Setup

### Prerequisites
- Python 3.10+
- pip or conda
- Virtual environment (recommended)

### 1. Clone & Setup Environment

```bash
# Clone repository
git clone <repo-url>
cd expense_tracker

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create `.env` file:
```
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## API Documentation

The REST API is fully documented and accessible at `/api/`.

### Base URL
```
http://localhost:8000/api/
```

### Authentication
APIs use **Session Authentication** (for web) or **Token Authentication** (for mobile/CLI).

### Endpoints

#### Expenses
```
GET    /api/expenses/                 # List user's expenses (paginated)
POST   /api/expenses/                 # Create new expense
GET    /api/expenses/{id}/            # Retrieve specific expense
PUT    /api/expenses/{id}/            # Update expense
DELETE /api/expenses/{id}/            # Delete expense
GET    /api/expenses/summary/         # Get summary stats
GET    /api/expenses/monthly_stats/   # Get 12-month breakdown
```

#### Profiles
```
GET    /api/profiles/me/              # Get current user profile
PATCH  /api/profiles/{id}/            # Update profile
```

### Query Filters

```bash
# Filter by category
GET /api/expenses/?category=Food

# Filter by date
GET /api/expenses/?date__gte=2026-01-01

# Combine filters
GET /api/expenses/?category=Food&date__gte=2026-01-01

# Order by
GET /api/expenses/?ordering=-date

# Search by title
GET /api/expenses/?search=groceries
```

### Example API Calls

#### Create an Expense
```bash
curl -X POST http://localhost:8000/api/expenses/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Grocery Shopping",
    "amount": 45.50,
    "category": "Food",
    "date": "2026-01-02",
    "description": "Weekly groceries"
  }'
```

#### Get Expense Summary
```bash
curl http://localhost:8000/api/expenses/summary/
```

Response:
```json
{
  "start_date": "2026-01-01",
  "end_date": "2026-01-02",
  "total_amount": 180.0,
  "expense_count": 3,
  "average_expense": 60.0,
  "by_category": [
    {
      "category": "Food",
      "total": 80.0,
      "count": 2,
      "average": 40.0
    },
    ...
  ]
}
```

## Web UI Features

### Dashboard
- View all expenses in a table
- Real-time line chart showing spending trends
- Category-wise breakdown

### Expense Management
- Add new expense with title, amount, category, and date
- Edit existing expenses
- Delete expenses
- Filter by category

### Profile
- View profile information
- Edit bio and upload profile picture
- Change password

### Navigation
- Top header with profile dropdown
- Left sidebar with expandable navigation
- Mobile-responsive design

## Testing

Run comprehensive test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=expenses --cov-report=html

# Run specific test
pytest expenses/test_api.py::TestExpenseAPI::test_create_expense -v

# Run with verbose output
pytest -vv
```

### Test Coverage
- **Model Tests**: Creation, validation, relationships
- **API Tests**: CRUD operations, permissions, filtering
- **Serializer Tests**: Data validation, transformations
- **Integration Tests**: End-to-end workflows

Current coverage: **63%+** across core modules

## Database Models

### Expense
```python
- user: ForeignKey(User)
- title: CharField
- amount: DecimalField
- category: CharField (choices: Food, Travel, Entertainment, Utilities, Sharing, Other)
- date: DateField
- description: TextField (optional)
```

### Profile
```python
- user: OneToOneField(User)
- bio: TextField (optional)
- profile_pic: ImageField (optional)
```

Auto-created on user registration via Django signals.

## Deployment

### 1. Production Settings

Create production `.env`:
```
SECRET_KEY=<generate-secure-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### 2. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Use Production WSGI Server

```bash
# Using Gunicorn
gunicorn expense_tracker.wsgi:application --bind 0.0.0.0:8000

# Using uWSGI
uwsgi --http :8000 --wsgi-file expense_tracker/wsgi.py --master --processes 4
```

### Deployment Options
- **Render.com** - Free tier available
- **Heroku** - Easy deployment with buildpacks
- **PythonAnywhere** - Beginner-friendly hosting
- **AWS/DigitalOcean** - Full control and scalability
- **Docker** - Containerized deployment

## Code Quality

### Running Linters
```bash
# Format code with Black
black expenses/ expense_tracker/

# Check with flake8
flake8 expenses/ expense_tracker/ --max-line-length=100

# Sort imports
isort expenses/ expense_tracker/
```

### Docstrings
All functions and classes include docstrings following PEP 257.

## Security Features

✅ CSRF Protection  
✅ SQL Injection Prevention (ORM)  
✅ XSS Protection  
✅ Password Hashing (Django default)  
✅ User Permission Checks (IsOwner custom permission)  
✅ Session Security  
✅ HTTPS Ready (requires reverse proxy in production)  

## Performance Optimization

- **Query Optimization**: Using select_related, prefetch_related
- **Pagination**: 20 items per page for API list views
- **Caching**: Ready for Django cache framework
- **Database Indexing**: On user_id, date, category fields

## Troubleshooting

### ImportError: No module named 'decouple'
```bash
pip install python-decouple
```

### Database Lock Error
```bash
# Remove database and start fresh
rm db.sqlite3
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Tests Failing
```bash
# Ensure test database exists
pytest --create-db

# Run with verbose output
pytest -vv
```

## Future Enhancements

- [ ] Advanced analytics (trends, projections)
- [ ] Budget management and alerts
- [ ] Export to CSV/PDF
- [ ] Multi-currency support
- [ ] Recurring expenses
- [ ] Receipt image uploads
- [ ] Expense sharing with other users
- [ ] Mobile app (React Native)
- [ ] Invoice generation
- [ ] Integration with payment gateways

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: support@example.com
- Documentation: [Full Docs](./DOCS.md)

---

Built with ❤️ using Django, Django REST Framework, and Tailwind CSS
