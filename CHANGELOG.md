# Changelog

All notable changes to the Todo Backend project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-09

### Added
- JWT-based authentication system
- Login endpoint with `/auth/login`
- Professional web UI for sign-in and todo management
- Static file serving (HTML, CSS, JavaScript)
- User authentication dependency injection
- Token expiration (30 minutes configurable)
- Password hashing with Bcrypt
- Frontend dashboard with todo management interface
- Demo credentials for testing
- Professional CSS styling with responsive design
- Client-side token management in localStorage

### Changed
- Updated all Todo endpoints to require authentication
- Enhanced main.py to serve static files
- Improved security with HTTP Bearer authentication
- Updated README with authentication flow documentation
- Enhanced configuration with JWT settings

### Security
- Added password hashing support
- Implemented JWT token validation
- Protected all API endpoints with authentication
- Token expiration mechanism

## [1.0.0] - 2026-02-08

### Added
- Initial project setup with FastAPI framework
- Kafka integration with Redpanda
- Dapr pub/sub configuration
- Todo CRUD API endpoints
- In-memory todo storage
- Kafka message publishing on todo events
- Docker and Docker Compose support
- Comprehensive documentation
- Logging throughout the application
- Health check endpoint
- CORS support

### Features
- POST /todos - Create todo
- GET /todos - Get all todos
- GET /todos/{id} - Get single todo
- PUT /todos/{id} - Update todo
- DELETE /todos/{id} - Delete todo
- Automatic Kafka event publishing
