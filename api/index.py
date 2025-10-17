"""
API entry point for Vercel
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import the Flask app
try:
    from app import crear_aplicacion
    app = crear_aplicacion()
except Exception as e:
    # Fallback minimal app
    from flask import Flask, jsonify
    app = Flask(__name__)

    @app.route('/')
    def index():
        return jsonify({
            'status': 'error',
            'message': 'Failed to initialize application',
            'error': str(e),
            'tip': 'Check Vercel build logs for details'
        }), 500

    @app.route('/health')
    def health():
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503

# Vercel expects a handler
def handler(request):
    """Vercel serverless handler"""
    return app(request.environ, lambda *args: None)
