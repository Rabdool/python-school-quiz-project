#!/usr/bin/env python3

import requests
import socket
import threading
import time
import sys
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import json

class SubdomainFinder:
    def __init__(self, domain, threads=50):
        self.domain = self.sanitize_domain(domain)
        self.threads = threads
        self.found_subdomains = set()
        self.lock = threading.Lock()
        self.wordlist = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk', 'ns2',
            'cpanel', 'whm', 'autodiscover', 'autoconfig', 'mx', 'imap', 'pop3', 'mobile', 'api',
            'dev', 'staging', 'test', 'admin', 'blog', 'shop', 'forum', 'support', 'cdn', 'assets',
            'images', 'img', 'static', 'media', 'secure', 'ssl', 'vpn', 'portal', 'app', 'apps',
            'beta', 'alpha', 'demo', 'git', 'svn', 'cvs', 'wiki', 'docs', 'news', 'store',
            'crm', 'erp', 'helpdesk', 'kb', 'internal', 'intranet', 'extranet', 'remote',
            'old', 'new', 'backup', 'archive', 'mirror', 'download', 'downloads', 'files',
            'service', 'services', 'chat', 'conference', 'video', 'voice', 'call', 'sip',
            'search', 'status', 'monitor', 'stats', 'analytics', 'track', 'tracking',
            'client', 'customer', 'partner', 'vendor', 'supplier', 'public', 'private',
            'ftp2', 'ns3', 'ns4', 'mx1', 'mx2', 'mx3', 'email', 'server', 'host', 'hosting',
            'cloud', 'saas', 'paas', 'iaas', 'dns', 'ntp', 'time', 'ldap', 'ad', 'dc',
            'sql', 'db', 'database', 'oracle', 'mysql', 'postgres', 'redis', 'mongo',
            'staging2', 'staging3', 'test2', 'test3', 'dev2', 'dev3', 'qa', 'uat',
            'preprod', 'production', 'prod', 'live', 'preview', 'stage', 'sandbox',
            'us', 'eu', 'asia', 'uk', 'ca', 'au', 'de', 'fr', 'jp', 'cn', 'in',
            'east', 'west', 'north', 'south', 'central', 'global', 'local',
            '1', '2', '3', '4', '5', 'v1', 'v2', 'v3', 'v4', 'v5',
            'ios', 'android', 'mobile', 'app', 'apps', 'play', 'download',
            'social', 'facebook', 'twitter', 'linkedin', 'instagram', 'youtube',
            'login', 'signin', 'signup', 'register', 'auth', 'oauth', 'sso',
            'dashboard', 'panel', 'console', 'manage', 'account', 'profile',
            'help', 'faq', 'contact', 'about', 'legal', 'privacy', 'terms',
            'careers', 'jobs', 'press', 'media', 'investor', 'ir'
        ]
    
    def sanitize_domain(self, domain):
        domain = re.sub(r'^https?://', '', domain)
        domain = re.sub(r'^www\.', '', domain)
        domain = domain.split('/')[0]
        domain = domain.split(':')[0]
        return domain.lower().strip()
    
    def is_valid_domain(self, domain):
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9](?:\.[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9])*$'
        return re.match(pattern, domain) is not None
    
    def dns_lookup(self, subdomain):
        full_domain = f"{subdomain}.{self.domain}"
        try:
            ip = socket.gethostbyname(full_domain)
            return {'subdomain': full_domain, 'ip': ip, 'method': 'DNS'}
        except socket.gaierror:
            return None
    
    def http_check(self, subdomain):
        full_domain = f"{subdomain}.{self.domain}"
        for protocol in ['https', 'http']:
            try:
                url = f"{protocol}://{full_domain}"
                response = requests.head(url, timeout=5, allow_redirects=True)
                if response.status_code < 400:
                    return {
                        'subdomain': full_domain, 
                        'status': response.status_code,
                        'method': 'HTTP',
                        'protocol': protocol,
                        'server': response.headers.get('Server', 'Unknown')
                    }
            except requests.RequestException:
                continue
        return None
    
    def certificate_transparency_check(self):
        print(f"Checking Certificate Transparency logs for {self.domain}...")
        try:
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                certificates = response.json()
                ct_subdomains = set()
                for cert in certificates:
                    name_value = cert.get('name_value', '')
                    for domain in name_value.split('\n'):
                        domain = domain.strip()
                        if domain.endswith(f".{self.domain}") and domain.count('.') >= 1:
                            subdomain_part = domain.replace(f".{self.domain}", "")
                            if subdomain_part and not subdomain_part.startswith('*'):
                                ct_subdomains.add(domain)
                print(f"Found {len(ct_subdomains)} subdomains in CT logs")
                return ct_subdomains
        except Exception as e:
            print(f"CT logs check failed: {e}")
        return set()
    
    def check_subdomain(self, subdomain):
        dns_result = self.dns_lookup(subdomain)
        if dns_result:
            http_result = self.http_check(subdomain)
            if http_result:
                dns_result.update({
                    'status': http_result['status'],
                    'protocol': http_result['protocol'],
                    'server': http_result['server']
                })
            with self.lock:
                self.found_subdomains.add(dns_result['subdomain'])
            return dns_result
        return None
    
    def run_wordlist_scan(self):
        print(f"Starting wordlist scan with {len(self.wordlist)} subdomains using {self.threads} threads...")
        results = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_subdomain = {
                executor.submit(self.check_subdomain, subdomain): subdomain 
                for subdomain in self.wordlist
            }
            completed = 0
            for future in as_completed(future_to_subdomain):
                completed += 1
                subdomain = future_to_subdomain[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                        print(f"Found: {result['subdomain']} ({result['ip']})")
                    if completed % 20 == 0:
                        print(f"Progress: {completed}/{len(self.wordlist)} ({completed/len(self.wordlist)*100:.1f}%)")
                except Exception as e:
                    print(f"Error checking {subdomain}: {e}")
        return results
    
    def save_results(self, results, filename=None):
        if not filename:
            filename = f"subdomains_{self.domain}_{int(time.time())}.json"
        output_data = {
            'domain': self.domain,
            'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_found': len(results),
            'subdomains': results
        }
        try:
            with open(filename, 'w') as f:
                json.dump(output_data, f, indent=2)
            print(f"Results saved to {filename}")
        except Exception as e:
            print(f"Failed to save results: {e}")
    
    def display_results(self, results):
        if not results:
            print("No subdomains found!")
            return
        print(f"\n Found {len(results)} subdomains for {self.domain}:")
        print("=" * 80)
        results.sort(key=lambda x: x['subdomain'])
        for i, result in enumerate(results, 1):
            subdomain = result['subdomain']
            ip = result['ip']
            status = result.get('status', 'N/A')
            protocol = result.get('protocol', 'N/A')
            server = result.get('server', 'N/A')
            print(f"{i:2d}. {subdomain}")
            print(f"    IP: {ip}")
            if status != 'N/A':
                print(f"    HTTP: {protocol.upper()} - Status {status}")
            if server != 'N/A':
                print(f"    Server: {server}")
            print()
    
    def run_full_scan(self):
        if not self.is_valid_domain(self.domain):
            print(f"Invalid domain: {self.domain}")
            return []
        print(f"Starting subdomain discovery for: {self.domain}")
        print(f"Using {self.threads} threads")
        print("=" * 60)
        start_time = time.time()
        ct_subdomains = self.certificate_transparency_check()
        wordlist_results = self.run_wordlist_scan()
        additional_ct_results = []
        if ct_subdomains:
            new_subdomains = []
            for subdomain in ct_subdomains:
                if subdomain not in self.found_subdomains:
                    subdomain_part = subdomain.replace(f".{self.domain}", "")
                    if subdomain_part:
                        new_subdomains.append(subdomain_part)
            if new_subdomains:
                print(f"Checking {len(new_subdomains)} additional subdomains from CT logs...")
                with ThreadPoolExecutor(max_workers=self.threads) as executor:
                    futures = [executor.submit(self.check_subdomain, sub) for sub in new_subdomains]
                    for future in as_completed(futures):
                        try:
                            result = future.result()
                            if result:
                                additional_ct_results.append(result)
                                print(f"CT Found: {result['subdomain']} ({result['ip']})")
                        except Exception as e:
                            pass
        all_results = wordlist_results + additional_ct_results
        end_time = time.time()
        scan_duration = end_time - start_time
        print(f"\n Scan completed in {scan_duration:.2f} seconds")
        print(f"Total subdomains found: {len(all_results)}")
        return all_results

def main():
    print("Advanced Subdomain Discovery Tool")
    print("=" * 50)
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = input("Enter domain to scan (e.g., example.com): ").strip()
    if not domain:
        print("No domain provided!")
        return
    threads = 50
    try:
        if len(sys.argv) > 2:
            threads = int(sys.argv[2])
        else:
            thread_input = input(f"Number of threads (default {threads}): ").strip()
            if thread_input:
                threads = int(thread_input)
    except ValueError:
        print(f"Invalid thread count, using default: {threads}")
    scanner = SubdomainFinder(domain, threads)
    results = scanner.run_full_scan()
    scanner.display_results(results)
    save = input("\nSave results to file? (y/N): ").strip().lower()
    if save in ['y', 'yes']:
        scanner.save_results(results)
    print("\n Scan complete!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n Error: {e}")
        sys.exit(1)
