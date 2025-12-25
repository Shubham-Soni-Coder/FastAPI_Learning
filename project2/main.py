"""
Entry Point
===========

This script serves as the entry point for the application.
It uses Uvicorn to run the FastAPI app defined in `app.app`.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)
