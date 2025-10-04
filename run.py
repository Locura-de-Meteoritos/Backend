import os
from app import create_app

# Crear aplicación
app = create_app(os.getenv('FLASK_ENV') or 'default')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)