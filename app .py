import os
import socket
import logging
import pymysql
from flask import Flask

app = Flask(__name__)

# Setup logging architecture so you can debug inside your log files
logging.basicConfig(level=logging.INFO)

# Dynamically source configuration details directly from the OS environment strings
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'admin')
DB_PASS = os.environ.get('DB_PASS', 'Akshat@2026')
DB_NAME = os.environ.get('DB_NAME', 'webappdb')

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5  # Prevent the app from hanging forever if RDS drops
    )

@app.route('/health')
def health_check():
    """Explicitly dedicated health check route to satisfy the ALB Target Group."""
    return "OK", 200

@app.route('/')
def home():
    hostname = socket.gethostname()
    try:
        conn = get_conn()
        with conn.cursor() as c:
            c.execute("CREATE TABLE IF NOT EXISTS visits (id INT AUTO_INCREMENT PRIMARY KEY, visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            c.execute("INSERT INTO visits (visited_at) VALUES (NOW())")
            c.execute("SELECT COUNT(*) as total FROM visits")
            count = c.fetchone()['total']
        conn.commit()
        conn.close()
        db = "Connected Successfully to AWS RDS"
    except Exception as e:
        count = "N/A"
        db = f"Database Error: {str(e)}"

    return f"""<html><body style='font-family:Arial;text-align:center;margin-top:100px'>
    <h1>AWS Auto-Scaling Web App Portfolio Lab</h1>
    <hr style='width:50%'>
    <p>Target EC2 Server Hostname: <span style='color:blue;font-weight:bold'>{hostname}</span></p>
    <p>Database Connectivity: <span style='color:green;font-weight:bold'>{db}</span></p>
    <p>Total Visits: <b>{count}</b></p>
    <p><small>Refresh to see the ALB shift traffic between servers!</small></p>
    </body></html>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
