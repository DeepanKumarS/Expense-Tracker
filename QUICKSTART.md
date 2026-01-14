# Quick Start Guide - Expense Tracker

## 🚀 Getting Started in 5 Minutes

### 1. Setup

```bash
# Clone/Navigate to project
cd "c:\Users\dselva708\OneDrive - Comcast\Desktop\Project\expense_tracker"

# Activate virtual environment (Windows)
..\env\Scripts\activate

# Or on Mac/Linux
source ../env/bin/activate
```

### 2. Start Server

```bash
python manage.py runserver
```

Visit: **http://localhost:8000**

### 3. Create Admin User (First time only)

```bash
python manage.py createsuperuser
```

## 📱 Web UI

| Page | URL | Description |
|------|-----|-------------|
| **Home** | http://localhost:8000/ | Dashboard with expense list |
| **Summary** | http://localhost:8000/summary/ | Charts and statistics |
| **Add Expense** | http://localhost:8000/add/ | Create new expense |
| **Profile** | http://localhost:8000/profile/ | User settings |
| **Admin** | http://localhost:8000/admin | Django admin panel |

## 🔌 API Testing

### Using curl

```bash
# List expenses
curl http://localhost:8000/api/expenses/

# Create expense
curl -X POST http://localhost:8000/api/expenses/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Lunch","amount":15.50,"category":"Food","date":"2026-01-02"}'

# Get summary
curl http://localhost:8000/api/expenses/summary/
```

### Using Postman

1. Create new collection
2. Set base URL: `http://localhost:8000/api`
3. Add endpoints:
   - `GET /expenses/`
   - `POST /expenses/`
   - `GET /expenses/summary/`

## 🧪 Running Tests

```bash
# All tests
pytest

# Specific test
pytest expenses/test_api.py::TestExpenseAPI::test_create_expense -v

# With coverage
pytest --cov=expenses --cov-report=html

# Then open: htmlcov/index.html
```

## 📁 Important Files

- `expenses/models.py` - Database models
- `expenses/serializers.py` - API serializers  
- `expenses/api_views.py` - REST API endpoints
- `expenses/api_urls.py` - API routing
- `expenses/test_api.py` - Tests (18 comprehensive tests)
- `expenses/templates/` - HTML templates
- `README.md` - Full documentation
- `requirements.txt` - Dependencies

## 🔧 Common Commands

```bash
# Create database
python manage.py migrate

# Make migrations after model changes
python manage.py makemigrations

# Shell (Python REPL with Django)
python manage.py shell

# Create sample data
python manage.py shell
# In shell:
# from django.contrib.auth.models import User
# from expenses.models import Expense
# user = User.objects.first()
# Expense.objects.create(user=user, title="Test", amount=50, category="Food")

# Clear database
python manage.py flush

# Collect static files (production)
python manage.py collectstatic --noinput
```

## 🚨 Troubleshooting

### Port 8000 already in use
```bash
python manage.py runserver 8001
```

### Import errors
```bash
# Ensure venv is activated and dependencies installed
pip install -r requirements.txt
```

### Database errors
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
```

### Tests failing
```bash
# Ensure pytest-django is installed
pip install pytest-django

# Run with verbose output
pytest -vv
```

## 📊 API Response Examples

### Create Expense
```bash
POST /api/expenses/

Request:
{
  "title": "Grocery Shopping",
  "amount": 45.50,
  "category": "Food",
  "date": "2026-01-02"
}

Response (201 Created):
{
  "id": 1,
  "title": "Grocery Shopping",
  "amount": "45.50",
  "category": "Food",
  "category_display": "Food",
  "date": "2026-01-02",
  "description": null,
  "user": 1
}
```

### Get Expenses
```bash
GET /api/expenses/?category=Food

Response (200 OK):
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Grocery Shopping",
      "amount": "45.50",
      "category": "Food",
      "category_display": "Food",
      "date": "2026-01-02"
    },
    ...
  ]
}
```

### Get Summary
```bash
GET /api/expenses/summary/

Response (200 OK):
{
  "start_date": "2026-01-02",
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

## 🎯 Key Features

✅ **Web Dashboard** - View all expenses with filtering  
✅ **Charts** - Real-time visualization with Chart.js  
✅ **REST API** - Full CRUD with custom actions  
✅ **Permissions** - Users only see their own data  
✅ **Filtering** - By category, date, search term  
✅ **Statistics** - Monthly breakdown and summaries  
✅ **Profile** - User bio and avatar  
✅ **Testing** - 18 comprehensive tests with 63%+ coverage  

## 📚 More Info

- **Full Docs**: See `README.md`
- **Production Setup**: See `PRODUCTION_READY.md`
- **API Details**: See `expenses/api_views.py` docstrings
- **Test Coverage**: See `htmlcov/` after running pytest --cov

## 💡 Pro Tips

1. **Use Python shell for quick testing**
   ```bash
   python manage.py shell
   from expenses.models import Expense
   Expense.objects.filter(category="Food").sum('amount')
   ```

2. **Check migrations**
   ```bash
   python manage.py showmigrations
   python manage.py sqlmigrate expenses 0001
   ```

3. **Test API with curl in GitBash or PowerShell**
   ```bash
   $body = @{title="Test"; amount=50; category="Food"; date="2026-01-02"} | ConvertTo-Json
   Invoke-WebRequest -Uri "http://localhost:8000/api/expenses/" -Method POST -Body $body -ContentType "application/json"
   ```

---

**Status**: ✅ Production Ready  
**Latest Update**: January 2026  
**Test Coverage**: 63%+  
**API Endpoints**: 8+  

