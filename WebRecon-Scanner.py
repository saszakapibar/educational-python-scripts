import requests
from bs4 import BeautifulSoup
import ssl
import socket
from datetime import datetime

def total_scan(url):
    print("-" * 50)
    print("Tool created by: saszakapibar")
    print("Check out more at: https://saszakapibar.github.io/")
    print("-" * 50)
    
    print(f"\n[***] Starting Total Recon for: {url} [***]\n")
    
    try:
        hostname = url.split("://")[-1].split("/")[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expiry = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                print(f"[+] SSL Valid until: {expiry}")
    except Exception as e:
        print(f"[-] SSL Check failed: {e}")

    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        print(f"[+] Server: {headers.get('Server', 'Unknown')}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        generator = soup.find("meta", {"name": "generator"})
        if generator:
            print(f"[+] CMS/Generator detected: {generator.get('content')}")
        
        security_headers = ['X-Frame-Options', 'Content-Security-Policy', 'Strict-Transport-Security']
        print("[*] Security Headers Check:")
        for h in security_headers:
            status = "PRESENT" if h in headers else "MISSING"
            print(f"    - {h}: {status}")

    except Exception as e:
        print(f"[-] Request failed: {e}")
        return

    scripts = soup.find_all('script')
    js_files = [s.get('src') for s in scripts if s.get('src')]
    print(f"\n[*] Found {len(js_files)} JS resources:")
    for js in js_files[:10]: # Print first 10 for brevity
        print(f"    - {js}")

    try:
        robots_url = url.rstrip('/') + '/robots.txt'
        robots_resp = requests.get(robots_url, timeout=3)
        if robots_resp.status_code == 200:
            print(f"\n[+] robots.txt found at: {robots_url}")
    except:
        print("\n[-] No robots.txt found.")

if __name__ == "__main__":
    target = input("Enter target URL (with https://): ")
    if not target.startswith("http"):
        print("Please include http:// or https://")
    else:
        total_scan(target)
