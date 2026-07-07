import requests
from bs4 import BeautifulSoup
import ssl
import socket
from datetime import datetime

def get_ssl_expiry(hostname):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expiry = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                return expiry
    except Exception:
        return "N/A (SSL Error)"

def total_scan(url):
    print("\n" + "="*60)
    print(f"TOTAL RECON SCANNER - ANALYSIS: {url}")
    print("="*60)
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    
    try:
        hostname = url.split("://")[-1].split("/")[0]
        print(f"[*] SSL certificate valid until: {get_ssl_expiry(hostname)}")
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("[*] Checking security headers:")
        sec_headers = ['X-Frame-Options', 'Content-Security-Policy', 'Strict-Transport-Security']
        for h in sec_headers:
            status = "OK" if h in response.headers else "MISSING"
            print(f"    - {h}: {status}")
            
        scripts = soup.find_all('script')
        js_files = [s.get('src') for s in scripts if s.get('src')]
        
        print(f"\n[+] Found {len(js_files)} JavaScript files:")
        if js_files:
            for i, js in enumerate(js_files, 1):
                full_js_url = js if js.startswith('http') else url.rstrip('/') + '/' + js.lstrip('/')
                print(f"    {i}. {full_js_url}")
        else:
            print("    - No external JS files found.")
            
    except Exception as e:
        print(f"[-] Scan error: {e}")

if __name__ == "__main__":
    print("Welcome to Total Recon Scanner!")
    while True:
        target = input("\nEnter target URL (or 'exit' to quit): ")
        if target.lower() == 'exit':
            print("Closing scanner. Goodbye!")
            break
            
        if not target.startswith("http"):
            target = "https://" + target
            
        total_scan(target)
