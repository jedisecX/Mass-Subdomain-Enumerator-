#!/usr/bin/env python3
# JediSecX Mass Subdomain Enumerator
# jedisec.com | jedisec.us | jedisec.cloud | jedisec.online | jedisec.me

import requests
import sys
import threading

# Config
wordlist = [
    "www", "mail", "ftp", "webmail", "smtp", "remote", "blog", "ns1", "ns2",
    "admin", "intranet", "portal", "vpn", "dev", "test", "staging", "beta", "m"
]
threads = 10  # Adjust based on your network speed

found = []

def check_subdomain(domain, subdomain):
    url = f"http://{subdomain}.{domain}"
    try:
        requests.get(url, timeout=3)
        print(f"[+] Found: {subdomain}.{domain}")
        found.append(f"{subdomain}.{domain}")
    except requests.ConnectionError:
        pass

def main(domain):
    print(f"[*] Scanning {domain} for subdomains...")
    jobs = []
    for sub in wordlist:
        t = threading.Thread(target=check_subdomain, args=(domain, sub))
        jobs.append(t)
        t.start()

        if len(jobs) >= threads:
            for j in jobs:
                j.join()
            jobs = []

    # Wait for any remaining threads
    for j in jobs:
        j.join()

    if found:
        print("\n[+] Discovered Subdomains:")
        for sub in found:
            print(sub)
    else:
        print("[-] No subdomains found with the current wordlist.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} domain.com")
        sys.exit(1)
    main(sys.argv[1])
