import uvicorn
import os
import sys

if __name__ == "__main__":
    # Ensure current directory is on PYTHONPATH
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print("=" * 60)
    print("Starting SIH26168 Intelligent Dead Reckoning Backend Server")
    print(f"Open Dashboard at: http://localhost:{port}")
    print("=" * 60)
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=False)
