# GhostShot

### Local Network Web Service Mapper

> Discover active HTTP/HTTPS services on a local network range, capture screenshots of each service, and generate an HTML triage report.

---

## Author

*Topshugar*
Built for Educational & Authorized Testing Use Only.

---

## Features

- Scans a local IP range for active web servers
- Detects ports: 80, 443, 8080, 8000
- Captures automated screenshots using Headless Chromium
- Generates a clean, interactive HTML report
- Lightweight - No external Python dependencies required

---

## Installation

    git clone https://github.com/Topshugar/ghostshot.git
    cd ghostshot
    sudo apt update && sudo apt install chromium -y

---

## Usage

    python3 http://ghostshot.py 192.168.1.1-20

    python3 http://ghostshot.py 192.168.1.1-1

### Output

- shots/ - Screenshots of discovered services
- http://report.html - Interactive HTML triage report

Open http://report.html in your browser to view results.

---

## Example Output

    [*] GhostShot scanning 192.168.1.1 - 192.168.1.20...
    [+] Found: http://192.168.1.1
    [+] Found: http://192.168.1.5:8080
    [✓] Done! Open http://report.html - Found 2 web servers

---

## Disclaimer

This tool is intended for educational purposes and authorized testing only.

Do NOT use GhostShot to scan networks you do not own or do not have explicit written permission to test. Unauthorized scanning may be illegal in your jurisdiction. The author is not responsible for misuse.

---

## License

MIT License - Free to use, modify and share with attribution.