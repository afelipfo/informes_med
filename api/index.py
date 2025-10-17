"""
API entry point for Vercel - WSGI compatible
"""
import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import and create the Flask app
try:
    from app import crear_aplicacion
    app = crear_aplicacion()
except Exception as e:
    # Fallback minimal app if initialization fails
    from flask import Flask, jsonify

    app = Flask(__name__)
    app.config['PROPAGATE_EXCEPTIONS'] = True

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

# Export app for Vercel
# Vercel's Python runtime expects the WSGI app to be named 'app'
# No need for a custom handler function
