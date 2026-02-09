# Quick Start Guide

Get Todo Backend up and running in 5 minutes!

## Prerequisites

- Python 3.10 or later
- pip (comes with Python)
- Terminal/Command prompt

## Installation Steps

### 1️⃣ Setup Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment

```bash
# Copy example to .env (already provided)
# .env is ready to use with default values
```

### 4️⃣ Start the Server

```bash
uvicorn app.main:app --reload
```

You'll see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 5️⃣ Open in Browser

Navigate to:
```
http://localhost:8000
```

## Login

Use demo credentials:

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin123` |

Alternative:
- Username: `user`, Password: `user123`
- Username: `demo`, Password: `demo123`

## What's Running?

✅ **FastAPI Server** on port 8000
✅ **Frontend Login UI** - http://localhost:8000
✅ **API Documentation** - http://localhost:8000/docs
✅ **Todo Dashboard** - After login

## Key Features

- 🔐 JWT Authentication with login page
- 📝 Create, read, update, delete todos
- 📡 Real-time Kafka event publishing
- 📱 Responsive mobile-friendly UI
- 📚 Interactive API documentation

## Testing the API

### In Browser

1. Visit http://localhost:8000
2. Enter credentials (admin/admin123)
3. Create and manage todos
4. Check the console for Kafka events

### Using Swagger Docs

1. Visit http://localhost:8000/docs
2. Test `/auth/login` endpoint
3. Use the token for protected endpoints

## Project Structure

```
todo-backend/
├── app/                 # Backend code
│   ├── auth/           # Authentication
│   ├── api/            # API endpoints
│   ├── models/         # Data models
│   ├── services/       # Business logic
│   └── core/           # Configuration
├── static/             # Frontend
│   ├── index.html      # Login page
│   ├── todos.html      # Dashboard
│   ├── css/            # Styling
│   └── js/             # Logic
└── venv/               # Virtual environment
```

## Common Commands

```bash
# Start server with auto-reload
uvicorn app.main:app --reload

# Start with custom port
uvicorn app.main:app --port 8001 --reload

# Run in production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Stop server
CTRL + C

# Deactivate virtual environment
deactivate
```

## API Endpoint Examples

### Login

```bash
curl -X POST "http://localhost:8000/auth/login?username=admin&password=admin123"
```

### Get Todos (replace TOKEN with your token)

```bash
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/todos
```

### Create Todo

```bash
curl -X POST http://localhost:8000/todos \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Master async Python web development",
    "completed": false
  }'
```

## Troubleshooting

### Port 8000 already in use

```bash
# Use a different port
uvicorn app.main:app --port 8001 --reload
```

### Module not found error

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Authentication failed

- Check username and password are correct
- Use demo credentials: admin/admin123
- Clear browser localStorage: F12 → Application → localStorage → clear

### Can't connect to Kafka

- Kafka is optional (demo works without it)
- Messages are logged to console regardless

## Next Steps

1. ✅ Log in with admin/admin123
2. ✅ Create your first todo
3. ✅ Update and delete todos
4. ✅ Check the API docs at /docs
5. ✅ Read [README.md](README.md) for detailed docs

## Need Help?

- 📖 Read [README.md](README.md) for comprehensive docs
- 📋 Check [STRUCTURE.md](STRUCTURE.md) for project organization
- 🔧 See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- 🐛 Check /docs for API schema

## Ready to Develop?

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code standards
- Git workflow
- How to add features
- Testing guidelines

---

**Enjoy coding! 🚀**
