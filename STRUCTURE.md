# Project Structure Documentation

## Directory Layout

```
todo-backend/
│
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application entry point
│   │
│   ├── api/                     # API routes module
│   │   ├── __init__.py
│   │   └── routes.py            # All API endpoints (auth + todos)
│   │
│   ├── auth/                    # Authentication module (NEW)
│   │   ├── __init__.py
│   │   ├── jwt.py              # JWT token creation, verification, password hashing
│   │   └── dependencies.py      # FastAPI auth dependency injection
│   │
│   ├── core/                    # Core configuration
│   │   ├── __init__.py
│   │   └── config.py            # Environment-based settings
│   │
│   ├── models/                  # Pydantic data models
│   │   ├── __init__.py
│   │   └── todo.py             # Todo model definitions
│   │
│   ├── services/                # Business logic services
│   │   ├── __init__.py
│   │   └── kafka_service.py    # Kafka producer/consumer
│   │
│   └── dapr/                    # Dapr integration
│       ├── __init__.py
│       └── pubsub.yaml         # Dapr Pub/Sub component config
│
├── static/                      # Frontend assets (NEW)
│   ├── index.html              # Login page
│   ├── todos.html              # Todo management dashboard
│   ├── css/
│   │   └── style.css           # Professional styling
│   └── js/
│       ├── auth.js             # Authentication logic
│       └── todos.js            # Todo management logic
│
├── venv/                        # Python virtual environment
│
├── requirements.txt             # Python dependencies
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image definition
├── .env                        # Environment variables (git-ignored)
├── .env.example               # Environment template
├── .editorconfig              # Code editor standards
├── .gitignore                 # Git ignore rules
├── README.md                  # Main documentation
├── CHANGELOG.md               # Version history
└── STRUCTURE.md               # This file
```

## Module Descriptions

### `app/main.py`
**Purpose**: FastAPI application entry point
- Initializes FastAPI app
- Configures middleware (CORS)
- Mounts static file directory
- Defines startup/shutdown events
- Serves index.html on root path

### `app/api/routes.py`
**Purpose**: All API endpoint definitions
- Authentication endpoints
  - `POST /auth/login` - User login with JWT
- Todo endpoints (all protected by JWT)
  - `POST /todos` - Create new todo
  - `GET /todos` - List all todos
  - `GET /todos/{id}` - Get single todo
  - `PUT /todos/{id}` - Update todo
  - `DELETE /todos/{id}` - Delete todo

### `app/auth/jwt.py`
**Purpose**: JWT token utilities
- Token creation/encoding
- Token verification/decoding
- Password hashing (Bcrypt)
- Password verification
- Token payload models

### `app/auth/dependencies.py`
**Purpose**: FastAPI dependency injection for auth
- HTTP Bearer security scheme
- Current user extraction from token
- Request-level authentication validation

### `app/core/config.py`
**Purpose**: Application configuration
- Settings loaded from environment variables
- Database, Kafka, Dapr configuration
- JWT settings (secret key, algorithm, expiry)

### `app/models/todo.py`
**Purpose**: Pydantic data models
- TodoBase - Shared fields
- TodoCreate - Request body for creating todos
- Todo - Complete todo response model

### `app/services/kafka_service.py`
**Purpose**: Kafka integration
- Message publishing to Kafka
- Message consumption from Kafka
- Connection management
- Event logging

### `app/dapr/pubsub.yaml`
**Purpose**: Dapr configuration
- Defines Kafka as pub/sub component
- Broker configuration
- Consumer group settings

### `static/index.html`
**Purpose**: Login page interface
- Professional login form
- Demo credentials display
- Error handling UI
- Form validation

### `static/todos.html`
**Purpose**: Todo management dashboard
- Sidebar navigation
- User profile section
- Todo creation form
- Todo list display
- Edit/delete actions
- Statistics view

### `static/css/style.css`
**Purpose**: Styling and layout
- Professional design system
- Responsive mobile-first design
- Light/dark color scheme
- Animations and transitions
- Component styling

### `static/js/auth.js`
**Purpose**: Client-side authentication
- Login form handling
- Token management (localStorage)
- Session persistence
- Redirect logic

### `static/js/todos.js`
**Purpose**: Client-side todo management
- CRUD operations communication
- UI updates and rendering
- State management
- Error handling
- Real-time status messages

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python 3.10+) |
| Authentication | JWT + Bcrypt |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Message Bus | Kafka (Redpanda) |
| Runtime | Dapr |
| Server | Uvicorn |
| Containerization | Docker & Docker Compose |
| Validation | Pydantic |

## File Purposes by Category

### Configuration Files
- `.env` - Runtime environment variables
- `.env.example` - Template for environment setup
- `.gitignore` - Git ignore patterns
- `.editorconfig` - Code formatting standards
- `requirements.txt` - Python dependencies
- `docker-compose.yml` - Docker container orchestration
- `Dockerfile` - Container image definition

### Documentation Files
- `README.md` - Main project documentation
- `CHANGELOG.md` - Version history and changes
- `STRUCTURE.md` - This file

### Python Modules
- All files in `app/` directory
- Organized by feature/responsibility

### Web Assets
- All files in `static/` directory
- HTML templates, CSS, JavaScript

### Environment
- `venv/` - Python virtual environment (auto-created)

## Development Workflow

### Setup
1. Navigate to project root: `cd todo-backend`
2. Create venv: `python3 -m venv venv`
3. Activate venv: `source venv/bin/activate`
4. Install packages: `pip install -r requirements.txt`
5. Configure .env if needed: `cp .env.example .env`

### Running
```bash
uvicorn app.main:app --reload
```

### Building Docker
```bash
docker build -t todo-backend:latest .
docker-compose up
```

## Security Considerations

- ✅ JWT tokens for stateless auth
- ✅ Bcrypt password hashing
- ✅ Environment-based secret key
- ✅ CORS configured
- ✅ Protected API endpoints
- ✅ Token expiration (30 min default)
- ✅ HTTPBearer authentication

## Scalability Notes

### Current Limitations
- In-memory todo storage (no persistence)
- Single-instance deployment
- No rate limiting
- No request validation for large payloads

### Future Improvements
- PostgreSQL/MongoDB integration
- Redis caching layer
- Load balancing setup
- Rate limiting middleware
- Database migrations
- User management system
- Role-based access control (RBAC)

## Standards & Conventions

- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Docstrings**: Triple-quoted docstrings for all functions
- **Imports**: Organized by standard library, third-party, local
- **Error Handling**: Proper HTTP status codes and error messages
- **Logging**: INFO level for key operations, ERROR for failures
- **Comments**: Used sparingly for complex logic
- **Code Style**: Follows PEP 8

## Asset Locations

### Static Files
- HTML files: `static/*.html`
- CSS files: `static/css/`
- JavaScript: `static/js/`

### Configuration
- App config: `app/core/config.py`
- Dapr config: `app/dapr/pubsub.yaml`
- Environment: `.env` (root)
