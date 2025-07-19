# server.py
from flask import Flask, redirect
import subprocess
import threading

# Path to your Streamlit app
STREAMLIT_SCRIPT = "app.py"

app = Flask(__name__)

def run_streamlit():
    # Launch Streamlit app on port 8501
    subprocess.run(
        ["streamlit", "run", STREAMLIT_SCRIPT, "--server.port=8501", "--server.address=0.0.0.0"]
    )

@app.route('/')
def index():
    # Redirect all requests to the Streamlit app
    return redirect("http://0.0.0.0:8501", code=302)

if __name__ == "__main__":
    # Run Streamlit in a separate thread so Flask can proxy
    threading.Thread(target=run_streamlit, daemon=True).start()
    # Start Flask on port 5000
    app.run(host="0.0.0.0", port=5000)
