from main import app, run_bot
import threading

# Start the bot logic in background
threading.Thread(target=run_bot, daemon=True).start()

# Flask app is served by Gunicorn via this file
