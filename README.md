# Prosparity Collection Dashboard Backend

A FastAPI-based backend for the Prosparity Collection Dashboard application.

## Features

- FastAPI REST API with automatic OpenAPI documentation
- MySQL database integration with SQLAlchemy ORM
- User management and authentication
- Application data management
- Payment tracking and status management
- Comprehensive filtering and search capabilities
- CORS enabled for frontend integration

## Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package installer)

## Database Setup

1. **Create MySQL Database:**
   ```sql
   CREATE DATABASE prosparity_collection_database;
   ```

2. **Configure Database Connection:**
   Update the database URL in `app/core/config.py`:
   ```python
   DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/prosparity_collection_database"
   ```

## Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Database Initialization

1. **Create database tables:**
   ```bash
   python3 -m app.db.init_db
   ```

2. **Populate initial data:**
   ```bash
   python3 -m app.db.populate_repayment_status
   ```

## Running the Application

### Development Mode (with auto-reload)
```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode
```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Alternative: Direct Python execution
```bash
python3 -m app.main
```

## API Documentation

Once the server is running, you can access:

- **Interactive API Docs (Swagger UI):** http://localhost:8000/docs
- **Alternative API Docs (ReDoc):** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

## API Endpoints

### Users
- `GET /api/v1/users/` - Get all users
- `POST /api/v1/users/` - Create new user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Applications
- `GET /api/v1/applications/` - Get filtered applications
- `GET /api/v1/applications/{application_id}` - Get application details

### Filters
- `GET /api/v1/filters/options` - Get filter options (branches, dealers, lenders, etc.)

### Summary Status
- `GET /api/v1/summary_status/{emi_month}` - Get summary status for a month

## Project Structure

```
backend/
├── app/
│   ├── api/                    # API routes and endpoints
│   │   └── v1/
│   │       └── routes/         # Route handlers
│   ├── core/                   # Core configuration
│   ├── crud/                   # Database CRUD operations
│   ├── db/                     # Database configuration and models
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic services
│   └── utils/                  # Utility functions
├── alembic/                    # Database migrations (if using)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Troubleshooting

### Common Issues

1. **Module not found errors:**
   - Make sure you're in the `backend` directory
   - Ensure virtual environment is activated
   - Check that all dependencies are installed

2. **Database connection errors:**
   - Verify MySQL is running
   - Check database credentials in `config.py`
   - Ensure database exists

3. **Port already in use:**
   - Change the port in the uvicorn command
   - Kill existing processes using the port

### Database Schema Issues

If you encounter database schema mismatches:

1. **Recreate tables:**
   ```bash
   python3 -m app.db.init_db
   ```

2. **Check model definitions:**
   - Ensure column names match database schema
   - Verify foreign key relationships
   - Check data types compatibility

## Development

### Adding New Models

1. Create model in `app/models/`
2. Add to `app/db/init_db.py`
3. Create corresponding CRUD operations
4. Add API routes

### Database Migrations

Currently using manual table creation. Consider implementing Alembic for proper migrations:

```bash
# Install alembic
pip install alembic

# Initialize
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

## Testing

Run tests with pytest:
```bash
pytest
```

## Deployment

For production deployment:

1. Use a production ASGI server like Gunicorn
2. Set up reverse proxy (Nginx/Apache)
3. Configure environment variables
4. Set up SSL certificates
5. Implement proper logging and monitoring

## Support

For issues and questions, check the project documentation or contact the development team.
