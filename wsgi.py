"""
WSGI entry point para Vercel
"""
import os
import sys

# Asegurar que el directorio raíz está en el path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import crear_aplicacion

    # Crear la aplicación Flask
    app = crear_aplicacion()

    # Para Vercel
    application = app

except Exception as e:
    # Crear una aplicación Flask mínima en caso de error
    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.route('/')
    def index():
        return jsonify({
            'error': 'Error al inicializar la aplicación',
            'details': str(e),
            'message': 'La aplicación no pudo iniciarse correctamente'
        }), 500

    application = app

if __name__ == "__main__":
    app.run()
