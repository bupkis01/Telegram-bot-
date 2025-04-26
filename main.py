from flask import Flask
from scheduler import start
from datetime import datetime
import threading, time, os, sys

app = Flask(__name__)

def log(msg):
    print(f"[{datetime.now()}] {msg}")

@app.route('/')
@app.route('/health')
def health():
    return 'OK', 200

def run_bot():
    log("🚀 Starting AI-powered bot...")
    try:
        start()
        log("⏱️ Scheduler started; entering main loop")
        while True:
            time.sleep(1)
    except Exception as e:
        log(f"💥 CRASHED: {e}")
        time.sleep(5)
        os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == "__main__":
    run_bot()
