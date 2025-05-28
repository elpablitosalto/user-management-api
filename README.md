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

## Domain Configuration

### Using Nginx as Reverse Proxy

1. Install Nginx:
   - Windows: Download from [Nginx website](http://nginx.org/en/download.html)
   - Linux: `sudo apt-get install nginx`
   - macOS: `brew install nginx`

2. Create Nginx configuration file:
   ```bash
   sudo nano /etc/nginx/sites-available/user-management-api
   ```

3. Add the following configuration:
   ```nginx
   server {
       listen 80;
       server_name api.yourdomain.com;  # Replace with your domain

       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

4. Enable the site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/user-management-api /etc/nginx/sites-enabled/
   sudo nginx -t  # Test configuration
   sudo systemctl restart nginx
   ```

### Using Gunicorn as WSGI Server

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Create a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/user-management-api.service
   ```

3. Add the following configuration:
   ```ini
   [Unit]
   Description=User Management API
   After=network.target

   [Service]
   User=youruser
   WorkingDirectory=/path/to/user-management-api
   Environment="PATH=/path/to/user-management-api/venv/bin"
   ExecStart=/path/to/user-management-api/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 wsgi:app

   [Install]
   WantedBy=multi-user.target
   ```

4. Start and enable the service:
   ```bash
   sudo systemctl start user-management-api
   sudo systemctl enable user-management-api
   ```

### SSL Configuration with Let's Encrypt

1. Install Certbot:
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   ```

2. Obtain SSL certificate:
   ```bash
   sudo certbot --nginx -d api.yourdomain.com
   ```

3. Update Nginx configuration to use HTTPS:
   ```nginx
   server {
       listen 443 ssl;
       server_name api.yourdomain.com;

       ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;

       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }

   server {
       listen 80;
       server_name api.yourdomain.com;
       return 301 https://$server_name$request_uri;
   }
   ```

4. Restart Nginx:
   ```bash
   sudo systemctl restart nginx
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

### Database Initialization Errors

If you encounter "no password supplied" error when running `python -m app.init_db`:

1. Check your `.env` file format:
   ```
   # Correct format:
   DATABASE_URL=postgresql://username:password@localhost:5432/user_management
   
   # Make sure there are no spaces around the = sign
   # Make sure the password is properly URL-encoded if it contains special characters
   ```

2. Verify the database exists:
   ```bash
   sudo -u postgres psql
   ```
   ```sql
   \l  -- List all databases
   CREATE DATABASE user_management;  -- Create if doesn't exist
   ```

3. Verify user permissions:
   ```sql
   -- Connect as postgres user
   sudo -u postgres psql
   
   -- Create user if doesn't exist
   CREATE USER myuser WITH PASSWORD 'mypassword';
   
   -- Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE user_management TO myuser;
   
   -- Connect to the database
   \c user_management
   
   -- Grant schema privileges
   GRANT ALL ON SCHEMA public TO myuser;
   ```

4. Test connection with psql:
   ```bash
   # Try connecting with the same credentials as in DATABASE_URL
   psql "postgresql://myuser:mypassword@localhost:5432/user_management"
   ```

5. If using environment variables, make sure they are loaded:
   ```bash
   # Install python-dotenv if not already installed
   pip install python-dotenv
   
   # Verify .env file is being read
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('DATABASE_URL'))"
   ```

### PostgreSQL Authentication Issues

If you encounter "Peer authentication failed" error when trying to connect as postgres user:

1. Find pg_hba.conf location:
   ```bash
   sudo find / -name "pg_hba.conf"
   ```

2. Edit pg_hba.conf:
   ```bash
   sudo nano /etc/postgresql/[version]/main/pg_hba.conf
   ```

3. Change authentication method from 'peer' to 'md5':
   ```
   # Find this line:
   local   all             postgres                                peer
   
   # Change it to:
   local   all             postgres                                md5
   ```

4. Restart PostgreSQL:
   ```bash
   sudo systemctl restart postgresql
   ```

5. Set password for postgres user:
   ```bash
   sudo -u postgres psql
   ```
   ```sql
   ALTER USER postgres WITH PASSWORD 'your_password';
   ```

6. Now you can connect using password:
   ```bash
   psql -U postgres -h localhost
   # or
   PGPASSWORD=your_password psql -U postgres
   ```

Remember to update your `.env` file with the new password:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/user_management
```

### Domain Configuration Issues

1. Check Nginx status:
   ```bash
   sudo systemctl status nginx
   ```

2. Check Nginx error logs:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```

3. Verify SSL certificate:
   ```bash
   sudo certbot certificates
   ```

4. Common issues:
   - DNS records not properly configured
   - Firewall blocking ports 80/443
   - SSL certificate expired
   - Nginx configuration syntax errors

## Documentation

For detailed API documentation, please refer to the Postman collection included in the project. 