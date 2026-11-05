# GhostShot - Mini EyeWitness Clone
# For EDUCATIONAL use on YOUR OWN network only
# Usage: python3 ghostshot.py 192.168.1.1-20

import socket
import subprocess
import os
import sys
from datetime import datetime

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        s.close()
        return result == 0
    except:
        return False

def take_screenshot(url, output):
    try:
        # Uses chromium headless - already in Kali
        subprocess.run(
            ["chromium", "--headless", "--disable-gpu", "--no-sandbox",
             f"--screenshot={output}", "--window-size=1200,800", "--timeout=10000", url],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15
        )
        return os.path.exists(output)
    except:
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ghostshot.py 192.168.1.1-20")
        return

    range_input = sys.argv[1]
    base = ".".join(range_input.split(".")[:3])
    start_end = range_input.split(".")[3].split("-")
    start = int(start_end[0])
    end = int(start_end[1]) if len(start_end) > 1 else start

    os.makedirs("shots", exist_ok=True)
    results = []

    print(f"[*] GhostShot scanning {base}.{start} - {base}.{end}...")

    for i in range(start, end+1):
        ip = f"{base}.{i}"
        for port in [80, 443, 8080, 8000]:
            if scan_port(ip, port):
                protocol = "https" if port in [443] else "http"
                url = f"{protocol}://{ip}:{port}" if port not in [80,443] else f"{protocol}://{ip}"
                print(f"[+] Found: {url}")
                shot_file = f"shots/{ip}_{port}.png"
                if take_screenshot(url, shot_file):
                    results.append((ip, port, url, shot_file))
                else:
                    results.append((ip, port, url, None))

    # Build HTML Report like EyeWitness
    html = f"""
    <html><head><title>GhostShot Report</title>
    <style>body{{background:#0f172a;color:white;font-family:Arial;padding:20px}}
    .card{{background:#1e293b;padding:15px;margin:15px;border-radius:12px}}
    img{{width:100%;border-radius:8px}}</style></head>
    <body><h1>👁️ GhostShot Report</h1>
    <p>Generated: {datetime.now()} | Targets: {len(results)}</p>
    """
    for ip, port, url, shot in results:
        html += f"<div class='card'><h3>{url} | IP: {ip} | Port: {port}</h3>"
        if shot:
            html += f"<img src='{shot}'></div>"
        else:
            html += "<p>Screenshot failed - server up but blocked screenshot</p></div>"

    html += "</body></html>"
    with open("report.html", "w") as f:
        f.write(html)

    print(f"\n[✓] Done! Open report.html - Found {len(results)} web servers")

if __name__ == "__main__":
    main()