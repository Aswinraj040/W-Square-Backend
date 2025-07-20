# run.py
from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(
        debug=os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1'],
        host='0.0.0.0',
        port=int(os.getenv('FLASK_RUN_PORT', 5000)),
    )
