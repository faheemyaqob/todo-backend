# Todo Backend API with JWT Authentication

A production-ready Todo Backend API built with **FastAPI**, **Apache Kafka (Redpanda)**, **Dapr**, and **JWT-based authentication**.

## Technology Stack

- **Language**: Python 3.10+
- **Web Framework**: FastAPI
- **Message Broker**: Apache Kafka (Redpanda)
- **Distributed Runtime**: Dapr
- **API Server**: Uvicorn
- **Data Validation**: Pydantic
- **Authentication**: JWT (JSON Web Tokens) with Bcrypt password hashing
- **Password Hashing**: Passlib with Bcrypt

## Project Structure

```
todo-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py                    # All API endpoints (auth + todos)
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py                    # Application configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── todo.py                      # Pydantic models for Todo
│   ├── services/
│   │   ├── __init__.py
│   │   └── kafka_service.py             # Kafka producer/consumer service
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt.py                       # JWT token creation/verification
│   │   └── dependencies.py              # FastAPI auth dependencies
│   └── dapr/
│       ├── __init__.py
│       └── pubsub.yaml                  # Dapr Pub/Sub configuration
├── requirements.txt                     # Python dependencies
├── docker-compose.yml                   # Docker Compose setup
├── Dockerfile                           # Docker image definition
├── .env                                 # Environment variables
├── .gitignore                           # Git configuration
└── README.md                            # This file
```

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Docker and Docker Compose (for containerized setup)
- Virtual environment (recommended)

## Setup Instructions

### 1. Install Dependencies

```bash
cd todo-backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Environment Variables

The `.env` file is pre-configured with default values:
```
DEBUG=True
KAFKA_BROKER=localhost:9092
KAFKA_TOPIC=todos
DAPR_HOST=localhost
DAPR_PORT=3500
SECRET_KEY=your-super-secret-key-change-this-in-production-environment
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**⚠️ IMPORTANT**: For production, change `SECRET_KEY` to a secure random value.

### 3. Install and Run Kafka (Redpanda)

**Option A: Using Docker Compose (Recommended)**

```bash
docker-compose up -d
```

This will start:
- Redpanda (Kafka-compatible broker) on `localhost:9092`
- FastAPI application on `http://localhost:8000`

**Option B: Manual Kafka Setup**

If you have Kafka installed locally, ensure it's running on `localhost:9092`.

## Running the Application

### Development Mode (with Hot Reload)

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run with Uvicorn
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Authentication Flow

### Overview

This API uses **JWT (JSON Web Tokens)** for authentication:

1. **User Login**: Send credentials to `/auth/login` endpoint
2. **Token Received**: Server returns JWT access token
3. **Protected Requests**: Include token in `Authorization` header
4. **Token Validation**: Server verifies token on each request

### Demo Users

For testing, the following credentials are available:

| Username | Password |
|----------|----------|
| `admin` | `admin123` |
| `user` | `user123` |
| `demo` | `demo123` |

⚠️ **Note**: These are demo users only. In production, use a real database and proper user management.

## API Endpoints

### Health & Status

#### Health Check
- **GET** `/health`
  ```json
  {
    "status": "healthy",
    "version": "2.0.0",
    "app": "Todo Backend API with Auth"
  }
  ```

#### Root Status
- **GET** `/`
  ```json
  { "status": "Todo backend running" }
  ```

---

### Authentication Endpoints

#### Login
- **POST** `/auth/login`
  
  **Query Parameters**:
  - `username` (string, required): Username
  - `password` (string, required): Password

  **Response** (200 OK):
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```

  **Error** (401 Unauthorized):
  ```json
  { "detail": "Invalid username or password" }
  ```

---

### Todo CRUD Endpoints (Authentication Required)

All todo endpoints require a valid JWT token in the `Authorization` header:
```
Authorization: Bearer {access_token}
```

#### Create Todo
- **POST** `/todos`
  
  **Headers**: 
  ```
  Authorization: Bearer {access_token}
  Content-Type: application/json
  ```
  
  **Body**:
  ```json
  {
    "title": "Learn FastAPI",
    "description": "Master FastAPI and async programming",
    "completed": false
  }
  ```
  
  **Response** (201 Created):
  ```json
  {
    "id": 1,
    "title": "Learn FastAPI",
    "description": "Master FastAPI and async programming",
    "completed": false,
    "created_at": "2025-01-15T10:30:00",
    "updated_at": "2025-01-15T10:30:00"
  }
  ```

#### Get All Todos
- **GET** `/todos`
  
  **Headers**:
  ```
  Authorization: Bearer {access_token}
  ```
  
  **Response** (200 OK):
  ```json
  [
    {
      "id": 1,
      "title": "Learn FastAPI",
      "description": "Master FastAPI and async programming",
      "completed": false,
      "created_at": "2025-01-15T10:30:00",
      "updated_at": "2025-01-15T10:30:00"
    },
    {
      "id": 2,
      "title": "Build API",
      "description": "Build a production-ready API",
      "completed": true,
      "created_at": "2025-01-15T10:35:00",
      "updated_at": "2025-01-15T10:40:00"
    }
  ]
  ```

#### Get Single Todo
- **GET** `/todos/{id}`
  
  **Parameters**:
  - `id` (integer): Todo ID
  
  **Headers**:
  ```
  Authorization: Bearer {access_token}
  ```

#### Update Todo
- **PUT** `/todos/{id}`
  
  **Parameters**:
  - `id` (integer): Todo ID
  
  **Headers**:
  ```
  Authorization: Bearer {access_token}
  Content-Type: application/json
  ```
  
  **Body**:
  ```json
  {
    "title": "Updated Title",
    "description": "Updated description",
    "completed": true
  }
  ```

#### Delete Todo
- **DELETE** `/todos/{id}`
  
  **Parameters**:
  - `id` (integer): Todo ID
  
  **Headers**:
  ```
  Authorization: Bearer {access_token}
  ```
  
  **Response** (204 No Content)

---

## Testing the API

### Using FastAPI Interactive Docs (Swagger UI)

1. Navigate to: `http://localhost:8000/docs`
2. Click "Try it out" on `/auth/login`
3. Enter credentials:
   - username: `admin`
   - password: `admin123`
4. Execute and copy the `access_token` from response
5. Click the lock icon in the top right or on any protected endpoint
6. Paste token in the format: `Bearer {copied_token}`
7. Now you can use protected endpoints

### Using cURL

#### 1. Login and Get Token
```bash
curl -X POST "http://localhost:8000/auth/login?username=admin&password=admin123" \
  -H "Content-Type: application/json"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 2. Create a Todo
```bash
curl -X POST "http://localhost:8000/todos" \
  -H "Authorization: Bearer {your_access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Test Todo",
    "description":"Testing the API",
    "completed":false
  }'
```

#### 3. Get All Todos
```bash
curl -X GET "http://localhost:8000/todos" \
  -H "Authorization: Bearer {your_access_token}"
```

#### 4. Update a Todo
```bash
curl -X PUT "http://localhost:8000/todos/1" \
  -H "Authorization: Bearer {your_access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Updated Title",
    "description":"Updated description",
    "completed":true
  }'
```

#### 5. Delete a Todo
```bash
curl -X DELETE "http://localhost:8000/todos/1" \
  -H "Authorization: Bearer {your_access_token}"
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Login
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    params={
        "username": "admin",
        "password": "admin123"
    }
)
token = login_response.json()["access_token"]

# 2. Create a todo
headers = {"Authorization": f"Bearer {token}"}
todo_response = requests.post(
    f"{BASE_URL}/todos",
    headers=headers,
    json={
        "title": "Test",
        "description": "Test",
        "completed": False
    }
)
print(todo_response.json())

# 3. Get all todos
todos = requests.get(f"{BASE_URL}/todos", headers=headers)
print(todos.json())
```

---

## JWT Authentication Details

### Token Structure

JWT tokens consist of three parts separated by dots:
```
header.payload.signature
```

**Example decoded token payload**:
```json
{
  "sub": "admin",
  "exp": 1234567890,
  "iat": 1234567800
}
```

- `sub`: Subject (username)
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp

### Token Expiration

- **Default**: 30 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **After expiration**: Request returns 401 Unauthorized
- **Solution**: User must login again to get a new token

### Password Security

- Passwords are hashed using **Bcrypt**
- Plain passwords are never stored
- Hashing is one-way (cannot be reversed)
- Comparison uses constant-time algorithms to prevent timing attacks

---

## Kafka Integration

### Publishing Messages

When a todo is created, updated, or deleted, a message is automatically published to Kafka:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Master FastAPI",
  "completed": false,
  "created_at": "2025-01-15T10:30:00",
  "created_by": "admin",
  "event": "todo_created"
}
```

### Message Events

- `todo_created` - Published when a new todo is created
- `todo_updated` - Published when a todo is updated
- `todo_deleted` - Published when a todo is deleted

### Consuming Messages

The `KafkaService` class handles both publishing and consuming. Messages are logged with the logging module for real-time monitoring.

---

## Dapr Integration

Dapr configuration is defined in `app/dapr/pubsub.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "localhost:9092"
```

### Running with Dapr

```bash
dapr run --app-id todo-backend --app-port 8000 uvicorn app.main:app --reload
```

---

## Logging

All operations are logged to the console at INFO level by default.

**Log Example**:
```
2025-01-15 10:30:00,123 - app.api.routes - INFO - User logged in successfully: admin
2025-01-15 10:30:01,456 - app.api.routes - INFO - Todo created with ID: 1 by user: admin
2025-01-15 10:30:02,789 - app.services.kafka_service - INFO - Message published to todos: {...}
```

---

## Docker Deployment

### Build Docker Image
```bash
docker build -t todo-backend:latest .
```

### Run with Docker Compose
```bash
docker-compose up
```

### Run Individual Container
```bash
docker run -p 8000:8000 \
  -e KAFKA_BROKER=redpanda:9092 \
  -e SECRET_KEY=your-secret-key \
  -e DEBUG=True \
  todo-backend:latest
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KAFKA_BROKER` | `localhost:9092` | Kafka broker address |
| `KAFKA_TOPIC` | `todos` | Kafka topic for todos |
| `DAPR_HOST` | `localhost` | Dapr runtime host |
| `DAPR_PORT` | `3500` | Dapr runtime port |
| `DAPR_PUBSUB_NAME` | `kafka-pubsub` | Dapr pub/sub component name |
| `DEBUG` | `True` | Enable debug mode |
| `SECRET_KEY` | `your-super-secret-key-...` | JWT signing key (change in production!) |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration time in minutes |

---

## Security Best Practices

✅ **JWT-based Authentication**: Stateless, scalable authentication
✅ **Password Hashing**: Bcrypt with salt for secure storage
✅ **Token Expiration**: Automatic token invalidation after 30 minutes
✅ **HTTP Headers**: Authorization header for token transmission
✅ **CORS Support**: Configured for frontend integration
✅ **Protected Endpoints**: All todo endpoints require authentication
✅ **Logging**: Track all authentication and authorization events

---

## Development Tips

### Hot Reload
The development server (`uvicorn app.main:app --reload`) automatically reloads when you make code changes.

### Interactive API Documentation
Visit `http://localhost:8000/docs` to interact with the API and see all available endpoints.

### Testing Authentication in Swagger UI
1. Open the Swagger UI at `/docs`
2. Login using `/auth/login` endpoint
3. Copy the `access_token`
4. Click the lock icon (🔐) on any protected endpoint
5. Select "Bearer Token" and paste your token
6. Test the protected endpoint

### Database Integration (Future Enhancement)
To add a real database:
- Install `sqlalchemy` and `psycopg2` (PostgreSQL)
- Create models in `app/models/`
- Replace in-memory todos dict with database queries
- Implement user management with proper database storage

### Monitoring & Observability
- Use `prometheus` for metrics
- Use `jaeger` for distributed tracing
- Integrate with `sentry` for error tracking

---

## Troubleshooting

### Issue: "Invalid or expired token" error
**Solution**: Your token has likely expired or is invalid. Login again using `/auth/login` to get a fresh token.

### Issue: Connection refused to Kafka
**Solution**: Ensure Kafka is running. Check with:
```bash
docker-compose ps
```

### Issue: Port 8000 already in use
**Solution**: Kill the process using port 8000 or use a different port:
```bash
uvicorn app.main:app --port 8001 --reload
```

### Issue: ModuleNotFoundError
**Solution**: Ensure virtual environment is activated and all dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Cannot connect to Kafka from Docker"
**Solution**: Ensure the Kafka broker address in `.env` matches your setup (use service name for Docker Compose).

---

## Best Practices Implemented

✅ **Modular Architecture** - Separation of concerns with api, services, models, and auth
✅ **Async/Await** - Async endpoints for better concurrency
✅ **JWT Authentication** - Industry-standard token-based authentication
✅ **Password Security** - Bcrypt hashing with salt
✅ **Error Handling** - Proper HTTP exception handling and logging
✅ **Dependency Injection** - FastAPI dependencies for clean code
✅ **Configuration Management** - Centralized settings with environment variables
✅ **Data Validation** - Pydantic models for type-safe requests/responses
✅ **Event Publishing** - Kafka integration for event streaming
✅ **Dapr Support** - Pub/Sub configuration for distributed patterns
✅ **Docker Support** - Complete containerization setup
✅ **CORS Support** - Configured for frontend integration
✅ **Comprehensive Documentation** - Detailed README with examples

---

## Next Steps

1. **Database Integration**: Replace in-memory storage with PostgreSQL/MongoDB
2. **User Management**: Implement proper user creation and management endpoints
3. **Role-Based Access**: Add role-based authorization (admin, user, etc.)
4. **Rate Limiting**: Implement rate limiting middleware
5. **Caching**: Add Redis for caching frequently accessed data
6. **Testing**: Add unit and integration tests with pytest
7. **CI/CD**: Set up GitHub Actions for automated testing and deployment
8. **Monitoring**: Integrate with Prometheus and Grafana
9. **API Versioning**: Implement API versioning strategy
10. **Documentation**: Generate API documentation with redoc

---

## License

This project is open-source and available for educational and commercial use.

## Support

For issues, questions, or suggestions, refer to the documentation or create an issue in the repository.

---

**Happy coding! 🚀**
