# Shadow Goose Entertainment - API Documentation

## Overview
The Shadow Goose Entertainment API provides authentication, user management, and project management capabilities for the NavImpact platform.

**Base URL:** `https://shadow-goose-api-staging.onrender.com` (Staging)
**Version:** 4.0.0
**Authentication:** JWT Bearer Token

## Authentication

### Login
**POST** `/auth/login`

Authenticate a user and receive a JWT token.

**Request Body:**
```json
{
  "username": "test",
  "password": "test"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "test",
    "email": "test@shadow-goose.com",
    "role": "admin"
  }
}
```

### Get User Info
**GET** `/auth/user`

Get current user information.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "username": "test",
  "email": "test@shadow-goose.com",
  "role": "admin"
}
```

## Projects

### List Projects
**GET** `/api/projects`

Get all projects for the authenticated user.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "projects": [
    {
      "id": 1,
      "name": "Test Project",
      "description": "This is a test project",
      "status": "draft",
      "created_by": 1,
      "created_at": "2025-08-08T11:12:28.384937",
      "updated_at": "2025-08-08T11:12:28.384956"
    }
  ]
}
```

### Create Project
**POST** `/api/projects`

Create a new project.

**Headers:**
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "name": "New Project",
  "description": "Project description",
  "status": "draft"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "New Project",
  "description": "Project description",
  "status": "draft",
  "created_by": 1,
  "created_at": "2025-08-08T11:15:30.123456",
  "updated_at": "2025-08-08T11:15:30.123456"
}
```

## System Endpoints

### Health Check
**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "ok",
  "version": "4.0.0"
}
```

### Root
**GET** `/`

Get API information.

**Response:**
```json
{
  "message": "Shadow Goose API v4.0.0",
  "status": "running",
  "features": ["auth", "projects"]
}
```

### Debug
**GET** `/debug`

Get debug information.

**Response:**
```json
{
  "version": "4.0.0",
  "database_url": "not_set",
  "secret_key": "not_set",
  "features": ["in_memory_storage", "project_management", "user_management"]
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Invalid credentials"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to create project: <error_message>"
}
```

## Status Codes

| Status | Description |
|--------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Internal Server Error |

## Project Status Values

| Status | Description |
|--------|-------------|
| draft | Project in planning |
| active | Project in progress |
| completed | Project finished |
| archived | Project archived |

## Testing

### cURL Examples

**Login:**
```bash
curl -X POST https://shadow-goose-api-staging.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
```

**Create Project:**
```bash
curl -X POST https://shadow-goose-api-staging.onrender.com/api/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"Test Project","description":"Description","status":"draft"}'
```

**Get Projects:**
```bash
curl -H "Authorization: Bearer <token>" \
  https://shadow-goose-api-staging.onrender.com/api/projects
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| SECRET_KEY | JWT secret key | shadow-goose-secret-key-2025-staging |
| DATABASE_URL | PostgreSQL connection string | not_set |
| CORS_ORIGINS | Allowed origins | * |

## Rate Limiting
Currently no rate limiting implemented.

## Security
- JWT tokens expire after 30 minutes
- CORS enabled for all origins
- Input validation using Pydantic models
