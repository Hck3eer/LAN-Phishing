# LAN Phishing
 
Here's a professional `README.md` file for your GitHub repository:

```markdown
# UMT Portal Phishing Simulator

⚠️ **Disclaimer**: This project is for **educational purposes only**. It demonstrates how phishing attacks work to raise cybersecurity awareness. Unauthorized use against real systems is illegal.

## 📌 Overview

A Python-based educational tool that simulates a UMT student portal phishing attack, including:
- Realistic UMT login page
- 2FA verification page
- Credential logging (local storage only)
- IP address tracking

## 🛠️ Technical Stack

- **Python 3** (Flask framework)
- HTML/CSS for frontend
- Socket programming for log viewing

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Flask (`pip install flask`)

### Installation
```
bash
```
git clone https://github.com/yourusername/umt-phishing-simulator.git
cd umt-phishing-simulator
```

### Usage
1. Run the simulator:
```bash
python3 umt_phishing_simulator.py
```

2. Access from any device on your local network:
```
http://[YOUR_LOCAL_IP]:5000
```

3. View captured logs:
```bash
cat umt_credentials_log.txt
```
Or via socket:
```bash
nc [YOUR_LOCAL_IP] 12345
```

 🔐 Security Features (For Educational Use)
- Local logging only (no external data transmission)
- Automatic redirect to real UMT site after simulation
- Clear educational disclaimer on all pages

 📂 File Structure
```
.
├── umt_phishing_simulator.py  # Main application
├── umt_credentials_log.txt    # Generated log file
├── README.md
└── requirements.txt
```

 ⚠️ Important Notes
1. Legal Use Only**: Only test on your own devices with permission
2. Never deploy** this against real systems
3. Disable after testing**: Kill the server when not in use

## 📚 Learning Resources
- [OWASP Phishing Guide](https://owasp.org/www-community/attacks/Phishing)
- [UMT Security Policies](https://www.umt.edu.pk/security)
- [Ethical Hacking Best Practices](https://www.eccouncil.org/ethical-hacking/)

## 🤝 Contributing
This project is for educational demonstration only and not accepting contributions.

## 📜 License
This project is licensed under the **Educational Use License** - see [LICENSE](LICENSE) file for details.
