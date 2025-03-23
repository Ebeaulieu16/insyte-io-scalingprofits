import uvicorn
import sys
import os

# Add the parent directory to the path so imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    print("Starting backend server on http://localhost:8001")
    try:
        uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True, log_level="debug")
    except Exception as e:
        print(f"Error starting server: {e}") 