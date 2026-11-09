"""
GhostShot Mapper - Local Network Web Service Mapper


DESCRIPTION:
    Discovers active HTTP/HTTPS services on a local network range,
    captures screenshots of each service, and generates an HTML
    triage report for authorized assessment.

AUTHOR:     Temitope Abraham Olorunmola
PRODUCT:    GhostShot Mapper - Part of GhostShot Security Suite
            GhostShot Defense (index.html) - For Users
            GhostShot Mapper (ghostshot.py) - For Authorized Assessment

USAGE:      python3 ghostshot.py 192.168.1.1-20
OUTPUT:     ./shots/ + ./report.html

LEGAL NOTICE:
    For Educational and Authorized Testing Use Only.
    Only scan networks you own or have explicit written permission to test.
    Unauthorized scanning may be unlawful in your jurisdiction.
"""

import socket
import subprocess
import os
import sys
import shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# ============================================================================
# CONFIGURATION
# ============================================================================
COMMON_PORTS = [80, 443, 8080, 8000, 8443, 8888]
SCAN_TIMEOUT = 1.0
SCREENSHOT_TIMEOUT = 20
MAX_WORKERS = 20

BROWSER_CANDIDATES = [
    "chromium",
    "chromium-browser",
    "google-chrome",
    "google-chrome-stable",
]

# ============================================================================
# SECTION 1: BROWSER DETECTION
# Purpose: Locate an available headless Chromium browser on the system.
# ============================================================================
def find_browser():
    """Return first available browser binary, or None if not found."""
    for candidate in BROWSER_CANDIDATES:
        path = shutil.which(candidate)
        if path:
            return path
    return None

# ============================================================================
# SECTION 2: NETWORK SCANNING
# Purpose: Verify if a specific TCP port is open on a target host.
# ============================================================================
def scan_port(ip, port):
    """Return True if port is open, False otherwise."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(SCAN_TIMEOUT)
        result = s.connect_ex((ip, port))
        s.close()
        return result == 0
    except Exception:
        return False

def scan_host(ip):
    """Scan a single host for common web ports. Returns list of open ports."""
    open_ports = []
    for port in COMMON_PORTS:
        if scan_port(ip, port):
            open_ports.append(port)
    return ip, open_ports

# ============================================================================
# SECTION 3: SCREENSHOT CAPTURE
# Purpose: Capture a visual snapshot of a web service using headless Chromium.
# ============================================================================
def take_screenshot(browser, url, output):
    """Capture screenshot. Returns True on success, False otherwise."""
    if not browser:
        return False
    try:
        subprocess.run(
            [
                browser,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                f"--screenshot={output}",
                "--window-size=1200,800",
                "--hide-scrollbars",
                "--timeout=10000",
                url,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=SCREENSHOT_TIMEOUT,
        )
        return os.path.exists(output) and os.path.getsize(output) > 0
    except Exception:
        return False

# ============================================================================
# SECTION 4: TARGET PARSING
# Purpose: Parse input range e.g. 192.168.1.1-20 into list of IPs.
# ============================================================================
def parse_range(range_input):
    """Parse 192.168.1.1-20 or 192.168.1.5 into list of IPs."""
    try:
        parts = range_input.split(".")
        if len(parts) != 4:
            raise ValueError("Expected format: 192.168.1.1-20")
        base = ".".join(parts[:3])
        last = parts[3]
        if "-" in last:
            start_s, end_s = last.split("-", 1)
            start = int(start_s)
            end = int(end_s)
        else:
            start = end = int(last)
        if not (0 <= start <= 255 and 0 <= end <= 255 and start <= end):
            raise ValueError("IP range out of bounds")
        if (end - start) > 254:
            raise ValueError("Range too large. Maximum 254 hosts per scan.")
        return [f"{base}.{i}" for i in range(start, end + 1)]
    except ValueError as e:
        print(f"[!] Invalid range: {e}")
        print(f"    Usage: python3 ghostshot.py 192.168.1.1-20")
        sys.exit(1)

# ============================================================================
# SECTION 5: REPORT GENERATION
# Purpose: Compile all findings into a single professional HTML report.
# ============================================================================
def generate_report(results, target_range, scan_time):
    """Generate report.html with GhostShot professional styling."""
    html_header = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GhostShot Mapper - Assessment Report</title>
<style>
body{{background:#0a0e1a;color:#e8eaf0;font-family:Arial,sans-serif;margin:0;padding:16px}}
.card{{background:#11182b;border:1px solid #26314f;border-radius:10px;padding:16px;margin-bottom:14px}}
h1{{color:#ffffff;font-size:26px;letter-spacing:2px;margin:4px 0}}
h3{{margin:0 0 8px 0;font-size:15px}}
.badge{{display:inline-block;background:#1e6bff;color:#fff;padding:5px 12px;border-radius:4px;font-size:11px;font-weight:bold;letter-spacing:1px}}
.small{{font-size:12px;color:#9aa3b8;line-height:1.6}}
img{{width:100%;border-radius:8px;border:1px solid #26314f}}
.warn{{background:#3a2a10;border:1px solid #ffaa00;padding:10px;border-radius:8px;font-size:13px}}
.good{{color:#2ecc71}}
.meta{{color:#9aa3b8;font-size:13px}}
</style>
</head>
<body>
<div class="card">
<h1>GHOSTSHOT MAPPER</h1>
<div><span class="badge">WIRELESS SECURITY DEFENSE &nbsp;|&nbsp; AUTHORIZED ASSESSMENT</span></div>
<p class="small">Developed by Temitope Abraham Olorunmola<br>Local Network Web Service Assessment Report</p>
<p class="meta">Target Range: {target_range}<br>Generated: {scan_time}<br>Services Found: {len(results)}</p>
<p class="warn"><b>Authorized Use Only:</b> This report was generated for a network the operator owns or has explicit permission to assess.</p>
</div>
"""

    html_body = ""
    if not results:
        html_body = """<div class="card"><h3>No Web Services Found</h3>
<p class="small">No HTTP/HTTPS services responded on ports 80, 443, 8000, 8080, 8443, 8888 in the scanned range.</p></div>
"""
    else:
        for ip, port, url, shot in results:
            html_body += f"<div class='card'><h3>{url} &nbsp;|&nbsp; IP: {ip} &nbsp;|&nbsp; Port: {port}</h3>"
            if shot and os.path.exists(shot):
                html_body += f"<img src='{shot}' alt='Screenshot of {url}'></div>\n"
            else:
                html_body += "<p class='small'>Screenshot unavailable - Service is reachable but screenshot capture failed or browser not installed.</p></div>\n"

    html_footer = """<div class="card"><p class="small">GhostShot Mapper - Wireless Security Defense<br>Abuja, Nigeria<br>For Educational &amp; Authorized Testing Use Only</p></div>
</body></html>
"""
    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html_header + html_body + html_footer)

# ============================================================================
# SECTION 6: MAIN EXECUTION
# Purpose: Parse range, scan hosts, capture evidence, compile HTML report.
# ============================================================================
def main():
    if len(sys.argv) < 2:
        print("GhostShot Mapper - Local Network Web Service Mapper")
        print("Usage: python3 ghostshot.py 192.168.1.1-20")
        print("       python3 ghostshot.py 192.168.1.5")
        return

    range_input = sys.argv[1]
    ips = parse_range(range_input)
    browser = find_browser()

    print("=" * 60)
    print("GHOSTSHOT MAPPER - Wireless Security Defense")
    print("Developed by Temitope Abraham Olorunmola")
    print("Authorized Testing Use Only - Scan only networks you own")
    print("=" * 60)
    if browser:
        print(f"[+] Browser found: {browser}")
    else:
        print("[!] No Chromium/Chrome found. Screenshots will be skipped.")
        print("    Install chromium or google-chrome to enable screenshots.")
    print(f"[*] Scanning {ips[0]} - {ips[-1]} ({len(ips)} hosts)...")
    print(f"[*] Ports: {', '.join(map(str, COMMON_PORTS))}")
    print("-" * 60)

    os.makedirs("shots", exist_ok=True)
    results = []

    # Parallel scan for speed
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        scan_results = list(executor.map(scan_host, ips))

    for ip, open_ports in scan_results:
        for port in open_ports:
            protocol = "https" if port in [443, 8443] else "http"
            if port in [80, 443]:
                url = f"{protocol}://{ip}"
            else:
                url = f"{protocol}://{ip}:{port}"
            print(f"[+] Found: {url}")
            shot_file = f"shots/{ip}_{port}.png"
            shot_ok = take_screenshot(browser, url, shot_file) if browser else False
            if shot_ok:
                results.append((ip, port, url, shot_file))
            else:
                # Remove empty file if created
                if os.path.exists(shot_file) and os.path.getsize(shot_file) == 0:
                    try:
                        os.remove(shot_file)
                    except OSError:
                        pass
                results.append((ip, port, url, None))

    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    generate_report(results, range_input, scan_time)

    print("-" * 60)
    print(f"[✓] Done! Found {len(results)} web service(s).")
    print(f"[✓] Report: ./report.html")
    print(f"[✓] Screenshots: ./shots/")

if __name__ == "__main__":
    main()