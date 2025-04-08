# OpenAI Analysis API

A REST API built with FastAPI that connects to OpenAI using LangChain to analyze messages.

## Project Structure

```
openai-api/
├── app/                    # Main application package
│   ├── api/                # API layer
│   │   ├── routes/         # Route definitions
│   │   │   ├── health.py   # Health check endpoints
│   │   │   └── message.py  # Message analysis endpoints
│   │   └── api.py          # API router 
│   ├── core/               # Core modules
│   │   └── config.py       # Configuration settings
│   ├── models/             # Database models (for future use)
│   ├── schemas/            # Pydantic models for requests/responses
│   │   └── message.py      # Message request/response schemas
│   ├── services/           # Business logic services
│   │   └── ai_service.py   # OpenAI integration service
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
4. Create a `.env` file based on `.env.example` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
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
- **POST /api/v1/messages/analyze** - Submit a message for analysis

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/messages/analyze" \
  -H "Content-Type: application/json" \
  -d '{"message":"What can you tell me about artificial intelligence?"}'
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