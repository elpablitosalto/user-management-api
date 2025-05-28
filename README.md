# User Management API

A RESTful API for user management built with Flask, PostgreSQL, and JWT authentication.

## Features

- User registration and authentication
- Role-based access control
- JWT token-based authentication
- PostgreSQL database integration
- API documentation (Postman)

## Project Structure

```
user-management-api/
├── app/
│   ├── __init__.py      # Application factory and extensions
│   ├── models.py        # Database models
│   ├── routes.py        # API endpoints
│   ├── schemas.py       # Request/response schemas
│   └── init_db.py       # Database initialization
├── config.py            # Configuration settings
├── requirements.txt     # Project dependencies
├── wsgi.py             # Application entry point
├── .env                # Environment variables
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:

   a. Install PostgreSQL if you haven't already:
   - Windows: Download and install from [PostgreSQL website](https://www.postgresql.org/download/windows/)
   - Linux: `sudo apt-get install postgresql postgresql-contrib`
   - macOS: `brew install postgresql`

   b. Start PostgreSQL service:
   - Windows: PostgreSQL service should start automatically
   - Linux: `sudo service postgresql start`
   - macOS: `brew services start postgresql`

   c. Create database and user:
   ```sql
   -- Connect to PostgreSQL
   psql -U postgres

   -- Create database
   CREATE DATABASE user_management;

   -- Create user (replace username and password with your values)
   CREATE USER myuser WITH PASSWORD 'mypassword';

   -- Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE user_management TO myuser;

   -- Connect to the database
   \c user_management

   -- Grant schema privileges
   GRANT ALL ON SCHEMA public TO myuser;
   ```

4. Create a `.env` file with the following variables:
```
DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/user_management
JWT_SECRET_KEY=your-secret-key
```

5. Initialize the database:
```bash
python -m app.init_db
```

6. Run the application:
```bash
python wsgi.py
```

## API Endpoints

### Authentication
- POST /api/auth/register - Register a new user
- POST /api/auth/login - Login and get JWT token
- POST /api/auth/logout - Logout (invalidate token)

### User Management
- GET /api/users - Get all users (admin only)
- GET /api/users/<id> - Get user by ID
- PUT /api/users/<id> - Update user
- DELETE /api/users/<id> - Delete user

## Role-Based Access Control

The API implements the following roles:
- Admin: Full access to all endpoints
- User: Limited access to their own data

## Development

The project uses a modular structure with Flask Blueprints:

- `app/__init__.py`: Application factory pattern for creating Flask app instances
- `app/models.py`: SQLAlchemy models for database tables
- `app/routes.py`: API endpoints organized in blueprints
- `app/schemas.py`: Marshmallow schemas for request/response validation
- `app/init_db.py`: Database initialization script

## Troubleshooting

### Database Connection Issues

1. Verify PostgreSQL is running:
   - Windows: Check Services app for "PostgreSQL" service
   - Linux: `sudo service postgresql status`
   - macOS: `brew services list`

2. Check database connection:
   ```bash
   psql -U myuser -d user_management -h localhost
   ```

3. Common issues:
   - Wrong password in DATABASE_URL
   - PostgreSQL not running
   - Wrong port number (default is 5432)
   - Database or user doesn't exist

## Documentation

For detailed API documentation, please refer to the Postman collection included in the project. 