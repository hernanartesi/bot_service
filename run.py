import uvicorn

if __name__ == "__main__":
    """
    Run the API server.
    
    Use this script as an entry point to run the API server directly:
    python run.py
    """
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0", 
        port=8000, 
        reload=True
    ) 