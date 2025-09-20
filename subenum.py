import requests

def enumerate_subdomains(domain, subdomains_list):
    found_subdomains = []
    for subdomain in subdomains_list:
        url = f"http://{subdomain}.{domain}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                found_subdomains.append(url)
                print(f"[+] Found: {url}")
        except requests.exceptions.RequestException:
            pass
    return found_subdomains

domain = "facebook.com"
subdomains = ["www", "mail", "ftp", "admin", "test", "blog", "dev", "shop"]

found = enumerate_subdomains(domain, subdomains)
print("\nFound subdomains:")
for subdomain in found:
    print(subdomain)
