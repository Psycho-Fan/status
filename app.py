from flask import Flask, render_template
import requests
import time
from datetime import datetime

app = Flask(__name__)

# CONFIGURATION
SERVICES = [
    {"name": "Website", "url": "https://pssyho.site/", "desc": "Main web server"},
]

def get_service_status(url):
    try:
        start = time.time()
        res = requests.get(url, timeout=3) 
        latency = round((time.time() - start) * 1000)
        
        if res.status_code == 200:
            return "operational", latency
        else:
            return "degraded", latency
    except:
        return "outage", 0

@app.route('/')
def index():
    overall_status = "All Systems Operational"
    status_class = "operational"
    results = []
    
    # Check all services
    for service in SERVICES:
        status, latency = get_service_status(service["url"])
        results.append({
            "name": service["name"],
            "desc": service["desc"],
            "status": status,
            "latency": latency
        })
        
        if status == "degraded":
            overall_status = "Partial Outage"
            status_class = "degraded"
        elif status == "outage":
            overall_status = "Major Outage"
            status_class = "outage"

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    return render_template(
        'index.html', 
        results=results, 
        overall_status=overall_status, 
        status_class=status_class,
        last_updated=now
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')