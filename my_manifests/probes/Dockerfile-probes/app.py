import time
import datetime
import socket
import os
from flask import Flask,jsonify

app_version = os.getenv('APP_VERSION', "latest")
app_name = os.getenv('APP_NAME', "Flask")
app_port = os.getenv('APP_PORT', 5000)
app_startup_delay= os.getenv('APP_STARTUP_DELAY', 0)

if int(app_startup_delay) > 0:
    print(f"[Warning]: Application will wait for {app_startup_delay} seconds before starting")

# Delay the application startup
time.sleep(int(app_startup_delay))

# Get Hostname
hostname = socket.gethostname()

print(f"[Info]: App {app_name} with version {app_version} started on port {app_port}")

app = Flask(__name__)

@app.route("/readiness")
def ready():
    return jsonify(
        status="ready",
        version=app_version,
        hostname=hostname
    )

@app.route("/liveness")
def alive():
    ts = time.time()
    return jsonify(
        status="alive",
        timestamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),
        version=app_version,
        hostname=hostname
    )

@app.route("/")
@app.route("/health")
def home():
    return jsonify(
        msg="Hello there!, You have just hit the homepage!",
        version=app_version,
        hostname=hostname
    )
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(app_port), debug=True)
	