"""
WSGI entry point para Vercel
"""
from app import crear_aplicacion

# Crear la aplicación Flask
app = crear_aplicacion()

# Para Vercel
application = app

if __name__ == "__main__":
    app.run()
