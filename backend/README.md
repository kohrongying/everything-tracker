# Everything Tracker Backend

FastAPI backend for the Everything Tracker application, providing REST API endpoints for expense tracking, food logging, exercise tracking, focus sessions, and authentication.

## 🚀 Quick Start

### Prerequisites

- Python 3.14 or higher
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

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

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Run the application**:
   ```bash
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at: http://localhost:8000

## Adding Dependency

```bash
// Dev
uv add --dev <package>

// Dev and Prod
uv add <package>
```

## 📋 Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback

# AWS Configuration
DYNAMODB_TABLE=EverythingTracker
AWS_REGION=ap-southeast-1

# Optional: OpenAI API Key (for AI features)
OPENAI_API_KEY=your-openai-api-key
```

## 🛠️ Development

### Running with Auto-reload

```bash
uvicorn app.main:app --reload
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

## 🚀 Deployment

### Local Development
```bash
# Run with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run with gunicorn (production-like)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

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
