# Everything Tracker Backend

FastAPI backend for the Everything Tracker application, providing REST API endpoints for expense tracking, food logging, exercise tracking, focus sessions, and authentication.

## 🚀 Quick Start

### Prerequisites

- Python 3.14 or higher
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Docker (for local DynamoDB)

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd everything-tracker/backend
   ```

2. **Create environment and Install deps**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

4. **Start local DynamoDB** (optional, for local development):
   ```bash
   make db-init
   ```

5. **Set up local database tables** (if using local DynamoDB):
   ```bash
   uv run python setup_local_db.py
   ```

6. **Run the application**:
   ```bash
   # Port on 8080
   uv run fastapi dev
   ```

The API will be available at: http://localhost:8000

## 🧪 Testing

### Local DynamoDB Testing

For testing with local DynamoDB:
```bash
make db-init
```

### Test Coverage

```bash
uv run pytest --cov=app --cov-report=html
```

## 📋 Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
MAGIC_LINK_EXPIRY_MINUTES=15
FRONTEND_URL=http://localhost:3000

# AWS SES Configuration
SES_FROM_EMAIL=noreply@yourdomain.com
AWS_REGION=ap-southeast-1

# DynamoDB Configuration
USERS_TABLE_NAME=everything-tracker-users
EXPENSES_TABLE_NAME=everything-tracker-expenses

# Local DynamoDB (set to true for local development)
USE_LOCAL_DYNAMODB=true
LOCAL_DYNAMODB_ENDPOINT=http://localhost:8000

# Legacy Database (deprecated)
DYNAMODB_TABLE=EverythingTracker
```

## 🛠️ Development

### Running with Auto-reload

```bash
uv run fastapi dev
```

### API Documentation

When the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── core/                # Core functionality (config, database)
│   ├── models/              # Pydantic models
│   ├── routers/             # API route handlers
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── expense.py       # Expense tracking
│   │   ├── food.py          # Food logging
│   │   ├── exercise.py      # Exercise tracking
│   │   └── focus.py         # Focus sessions
│   └── services/            # Business logic services
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🔌 API Endpoints

### Authentication
- `GET /auth/login` - Initiate Google OAuth login
- `GET /auth/callback` - OAuth callback handler

### Expenses
- `POST /expense/` - Add new expense
- `GET /expense/` - Get expenses (with optional filters)
- `GET /expense/{id}` - Get specific expense
- `PUT /expense/{id}` - Update expense
- `DELETE /expense/{id}` - Delete expense

### Food Tracking
- `POST /food/` - Log food intake
- `GET /food/` - Get food logs
- `GET /food/{id}` - Get specific food log
- `PUT /food/{id}` - Update food log
- `DELETE /food/{id}` - Delete food log

### Exercise Tracking
- `POST /exercise/` - Log exercise session
- `GET /exercise/` - Get exercise logs
- `GET /exercise/{id}` - Get specific exercise log
- `PUT /exercise/{id}` - Update exercise log
- `DELETE /exercise/{id}` - Delete exercise log

### Focus Sessions
- `POST /focus/start` - Start focus session
- `POST /focus/{session_id}/end` - End focus session
- `GET /focus/` - Get focus sessions
- `GET /focus/{id}` - Get specific focus session

## 🧪 Testing

### Manual Testing with curl

```bash
# Test the root endpoint
curl http://localhost:8000/

# Test expense creation
curl -X POST "http://localhost:8000/expense/" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 25.50,
    "description": "Lunch at cafe",
    "category": "Food & Dining"
  }'
```

### Using the Interactive API Docs

1. Start the server
2. Visit http://localhost:8000/docs
3. Use the interactive Swagger UI to test endpoints

### AWS Lambda Deployment

The application is configured for AWS Lambda deployment using the CDK infrastructure:

1. The `mangum` adapter is included for Lambda integration
2. Lambda handler is defined in `app.main.handler`
3. Use the CDK commands from the root directory:
   ```bash
   npm run cdk:deploy
   ```

## 🔧 Troubleshooting

### Common Issues

1. **Pydantic Field Name Conflicts**:
   If you encounter errors like `pydantic.errors.PydanticUserError: Error when building FieldInfo from annotated attribute`, this is due to field names conflicting with type annotations in Pydantic v2. The models have been fixed to use `date as Date` imports to avoid this issue.

2. **Module not found errors**:
   ```bash
   uv sync
   ```

3. **Environment variables not loaded**:
   - Ensure `.env` file exists
   - Check that `python-dotenv` is installed
   - Verify variable names match exactly

4. **Port already in use**:
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill the process
   kill -9 <PID>
   ```

5. **CORS issues**:
   - The API is configured with CORS middleware
   - For local development, ensure frontend runs on a different port

### Logs and Debugging

- Enable debug logging by setting `LOG_LEVEL=DEBUG` in your `.env`
- Check uvicorn logs in the terminal
- Use the `/docs` endpoint for interactive testing

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
