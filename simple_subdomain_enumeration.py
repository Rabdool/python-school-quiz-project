#!/usr/bin/env python3

import requests
import socket
import sys
import time

class SimpleSubdomainFinder:
    def __init__(self, domain):
        self.domain = self.clean_domain(domain)
        self.found_subdomains = []
        self.wordlist = [
            'www', 'mail', 'ftp', 'admin', 'test', 'blog', 'dev', 'shop',
            'api', 'cdn', 'static', 'media', 'secure', 'mobile', 'app',
            'support', 'help', 'news', 'forum', 'store', 'beta', 'demo',
            'portal', 'login', 'dashboard', 'cpanel', 'webmail', 'mx',
            'ns1', 'ns2', 'pop', 'smtp', 'imap', 'staging', 'prod'
        ]
    
    def clean_domain(self, domain):
        domain = domain.replace('http://', '').replace('https://', '')
        domain = domain.replace('www.', '')
        domain = domain.split('/')[0]
        return domain.strip().lower()
    
    def check_subdomain(self, subdomain):
        full_domain = f"{subdomain}.{self.domain}"
        try:
            ip_address = socket.gethostbyname(full_domain)
            status_code = None
            try:
                response = requests.get(f"http://{full_domain}", timeout=5)
                status_code = response.status_code
            except:
                try:
                    response = requests.get(f"https://{full_domain}", timeout=5)
                    status_code = response.status_code
                except:
                    status_code = "No HTTP"
            return {
                'subdomain': full_domain,
                'ip': ip_address,
                'status': status_code
            }
        except socket.gaierror:
            return None
    
    def scan(self):
        print(f"Scanning subdomains for: {self.domain}")
        print("=" * 50)
        total = len(self.wordlist)
        found_count = 0
        for i, subdomain in enumerate(self.wordlist, 1):
            print(f"Checking {i}/{total}: {subdomain}.{self.domain}", end=" ... ")
            result = self.check_subdomain(subdomain)
            if result:
                self.found_subdomains.append(result)
                found_count += 1
                print(f"FOUND! ({result['ip']})")
            else:
                print("Not found")
            time.sleep(0.1)
        return self.found_subdomains
    
    def display_results(self):
        if not self.found_subdomains:
            print("\nNo subdomains found!")
            return
        print(f"\nFound {len(self.found_subdomains)} subdomains:")
        print("=" * 60)
        for i, result in enumerate(self.found_subdomains, 1):
            print(f"{i}. {result['subdomain']}")
            print(f"   IP Address: {result['ip']}")
            print(f"   HTTP Status: {result['status']}")
            print()
    
    def save_results(self, filename=None):
        if not self.found_subdomains:
            print("No results to save!")
            return
        if not filename:
            filename = f"subdomains_{self.domain}.txt"
        try:
            with open(filename, 'w') as f:
                f.write(f"Subdomain scan results for: {self.domain}\n")
                f.write(f"Scan date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total found: {len(self.found_subdomains)}\n")
                f.write("=" * 50 + "\n\n")
                for result in self.found_subdomains:
                    f.write(f"Subdomain: {result['subdomain']}\n")
                    f.write(f"IP: {result['ip']}\n")
                    f.write(f"Status: {result['status']}\n")
                    f.write("-" * 30 + "\n")
            print(f"Results saved to: {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")

def main():
    print("Simple Subdomain Finder")
    print("=" * 30)
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = input("Enter domain to scan (e.g., example.com): ").strip()
    if not domain:
        print("Please provide a domain!")
        return
    scanner = SimpleSubdomainFinder(domain)
    results = scanner.scan()
    scanner.display_results()
    if results:
        save = input("Save results to file? (y/n): ").strip().lower()
        if save in ['y', 'yes']:
            scanner.save_results()
    print("Scan completed!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScan stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
