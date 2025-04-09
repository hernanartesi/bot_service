# Expense Tracking and Analysis API

A REST API built with FastAPI that connects to OpenAI using LangChain to analyze expense messages and track expenses in a PostgreSQL database.

## Project Structure

```
bot-service/
├── app/                    # Main application package
│   ├── api/                # API layer
│   │   ├── routes/         # Route definitions
│   │   │   ├── health.py   # Health check endpoints
│   │   │   └── message.py  # Message analysis endpoints
│   │   └── api.py          # API router 
│   ├── core/               # Core modules
│   │   ├── config.py       # Configuration settings
│   │   └── database.py     # Database connection
│   ├── models/             # Database models
│   │   └── expense.py      # Expense model
│   ├── schemas/            # Pydantic models for requests/responses
│   │   ├── message.py      # Message request/response schemas
│   │   ├── expense.py      # Expense schemas
│   │   └── expense_filter.py # Expense filter schemas
│   ├── services/           # Business logic services
│   │   ├── ai_service.py   # OpenAI integration service
│   │   ├── expense_service.py # Expense management service
│   │   └── expense_category_service.py # Category management
│   └── main.py             # FastAPI application initialization
├── tests/                  # Test suite
│   ├── conftest.py         # Test configuration and fixtures
│   ├── test_health.py      # Health endpoint tests
│   └── test_message_api.py # Message API tests
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
├── requirements.txt        # Project dependencies
└── run.py                  # Entry point script
```

## Features

- **Expense Analysis**: Analyze natural language messages to extract expense details
- **Expense Tracking**: Store and manage expenses in a PostgreSQL database
- **Concurrent Access**: Safe handling of concurrent requests with proper transaction isolation

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example` and add your configuration:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=postgresql://user:password@localhost:5432/expenses
   ```

## Running the API

Start the API server with:

```
python run.py
```

Alternatively, use uvicorn directly:

```
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

- **GET /api/v1/** - Health check endpoint
- **POST /api/v1/messages/analyze** - Submit a message for expense analysis

### Example Requests

1. **Expense Recording**:
```bash
curl -X POST "http://localhost:8000/api/v1/messages/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bought coffee for 4.5 dollars",
    "user_id": 1
  }'
```


### Response Format

1. **Expense Response**:
```json
{
   "amount": 4.5,
   "category": "Food",
   "description": "Bought coffee"
}
```
```

3. **Error Response**:
```json
{
    "type": "error",
    "data": null,
    "error": "Error message here"
}
```

## Running Tests

Run the test suite with:

```
pytest
```

## Interactive API Documentation

When the server is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 