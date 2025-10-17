"""
Vercel-specific entry point
This file is specifically designed to work with Vercel's Python runtime
"""
from api.index import app

# Vercel looks for this
application = app

if __name__ == "__main__":
    app.run()
