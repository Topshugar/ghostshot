# GHOSTSHOT
### Wireless Security Defense Suite

**Developed by Temitope Abraham Olorunmola**
Abuja, Nigeria

> GhostShot is a professional wireless security assessment suite for detection of Evil Twin, Deauthentication, Fake Captive Portal, and Unauthorized Device intrusions.

---

## 🌐 Live Deployment

**GhostShot Defense (Web Tool) - Open in Browser:**

**https://topshugar.github.io/ghostshot/**

No installation required. Works on mobile and desktop.

---

## 📦 What's Inside This Repo

| File | Tool | For Whom |
| :--- | :--- | :--- |
| `index.html` | **GhostShot Defense** | Everyday users, shop owners, home users |
| `ghostshot.py` | **GhostShot Mapper** | Security professionals, authorized testing |
| `README.md` | This documentation | Everyone |

Do not rename `index.html`. GitHub Pages only serves `index.html` as the website.

---

## 1. GhostShot Defense - Web Tool (`index.html`)

**No code. No installation. Open link and use.**

### Features

1.  **Airgeddon Attack Overview** - Understand how Evil Twin attacks work
2.  **Evil Twin Detection** - Detect duplicate SSID broadcasts
3.  **Deauthentication Assessment** - Detect forced disconnection attacks
4.  **Password Strength Assessment** - Assess WiFi password resilience
5.  **Captive Portal Detector** - Detect fake login pages designed to steal WiFi passwords
6.  **Device Check** - Detect unauthorized devices connected to your router
7.  **Wireless Security Audit** - Full checklist for home / shop WiFi hardening
8.  **Assessment Report** - Generate and copy a professional report for sharing

### How To Use

1.  Open the Live Deployment link above: https://topshugar.github.io/ghostshot/
2.  Enter your WiFi name (SSID), encryption type, and number of networks with same name
3.  Answer the Captive Portal questions if a login page appears
4.  Check your router for connected devices and compare with devices you own
5.  Generate and share the Assessment Report

### Example - Evil Twin Test

- SSID: `MyWiFi`
- Encryption: `WPA2`
- Count: `2`
- **Result:** `HIGH RISK: EVIL TWIN INDICATED - Do not connect.`

### Example - Captive Portal Test

- Login page appeared: `Yes`
- Page asks for: `WiFi Password`
- HTTPS Lock: `No`
- **Result:** `HIGH RISK: FAKE PORTAL LIKELY - Do NOT enter your password.`

---

## 2. GhostShot Mapper - Python Tool (`ghostshot.py`)

**For authorized network assessment only.**

Discovers active HTTP/HTTPS services on a local network range, captures screenshots, and generates a professional HTML triage report.

### Requirements

- Python 3.8+
- Chromium or Google Chrome (for screenshots)
- Network access to target range you own / are authorized to test

### Installation

```bash
git clone https://github.com/topshugar/ghostshot.git
cd ghostshot
No external Python libraries required. Uses standard library only.

### Usage
# Scan a range
python3 ghostshot.py 192.168.1.1-20

# Scan a single host
python3 ghostshot.py 192.168.1.5
### Output
./shots/        - Screenshots of each discovered web service
./report.html   - Professional HTML triage report
### Example Output
[+] Browser found: /usr/bin/chromium
[*] Scanning 192.168.1.1 - 192.168.1.20 (20 hosts)...
[+] Found: http://192.168.1.1
[+] Found: http://192.168.1.5:8080
[✓] Done! Found 2 web service(s).
[✓] Report: ./report.html
---

## 🛡️ Security Guidance

*If you detect an attack:*

1.  *Evil Twin:* Disconnect immediately. Forget the network. Use mobile data.
2.  *Deauth Attack:* Disconnect WiFi. Move location. Use mobile data.
3.  *Fake Portal:* NEVER enter your WiFi password into a browser pop-up page. A real router does not ask for it that way.
4.  *Unknown Device:* Change WiFi password immediately. Restart router. Re-check device list.
5.  *General Hardening:* Use WPA2/WPA3 only. Disable WPS. Change default admin password. Update router firmware.

---

## ⚖️ Legal Notice & Authorized Use

*GhostShot Defense* is for defensive education and self-assessment.

*GhostShot Mapper* is for *Educational and Authorized Testing Use Only.*

Only scan networks you own or have explicit written permission to test. Unauthorized scanning, interception, or access may be unlawful in your jurisdiction. The author assumes no liability for misuse.

---

## 👤 Author

*Temitope Abraham Olorunmola*
GhostShot - Wireless Security Defense
Abuja, Nigeria

---

## 📄 License

Community Edition - Free for defensive and educational use with attribution.
Commercial redistribution without permission is not permitted.
