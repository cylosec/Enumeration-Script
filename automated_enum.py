import os
import subprocess
import json

# Target information
TARGET_IP = "xxx.xxx.xxx.xxx" # Replace with actual IP  
DOMAIN = "example.com"  # Replace with actual domain  
OUTPUT_DIR = "recon_results"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to execute and save command output
def run_command(command, output_file):
    print(f"\n[+] Running: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        with open(f"{OUTPUT_DIR}/{output_file}", "w") as f:
            f.write(result.stdout)
        print(f"[+] Saved results to {OUTPUT_DIR}/{output_file}")
    except Exception as e:
        print(f"[-] Error running {command}: {e}")

# 1️⃣ Full Port Scan (Detect all services)
run_command(f"nmap -p- -sV -sC -T4 -oN {OUTPUT_DIR}/nmap_full.txt {TARGET_IP}", "nmap_full.txt")

# 2️⃣ Web Technology Fingerprinting
run_command(f"whatweb -v {TARGET_IP} > {OUTPUT_DIR}/whatweb.txt", "whatweb.txt")

# 3️⃣ Directory & File Enumeration
run_command(f"gobuster dir -u https://{TARGET_IP} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50 -o {OUTPUT_DIR}/gobuster.txt", "gobuster.txt")

# 4️⃣ Subdomain Enumeration (Cloudflare Bypass Attempt)
run_command(f"subfinder -d {DOMAIN} -o {OUTPUT_DIR}/subdomains.txt", "subdomains.txt")

# 5️⃣ Cloudflare Bypass Test
run_command(f"curl -s https://{TARGET_IP} --header 'Host: {DOMAIN}' -o {OUTPUT_DIR}/cloudflare_bypass.txt", "cloudflare_bypass.txt")

# 6️⃣ Shodan API Query (Find Exposed Services)
SHODAN_API_KEY = "your_shodan_api_key_here"  # Replace with your Shodan API key
if SHODAN_API_KEY:
    run_command(f"shodan host {TARGET_IP} > {OUTPUT_DIR}/shodan_results.txt", "shodan_results.txt")

# 7️⃣ TLS Security Check
run_command(f"nmap --script ssl-enum-ciphers -p 443,8443 {TARGET_IP} -oN {OUTPUT_DIR}/ssl_scan.txt", "ssl_scan.txt")

# 8️⃣ DNS & WHOIS Reconnaissance
run_command(f"whois {TARGET_IP} > {OUTPUT_DIR}/whois.txt", "whois.txt")
run_command(f"dig axfr @{TARGET_IP} {DOMAIN} > {OUTPUT_DIR}/dns_zone_transfer.txt", "dns_zone_transfer.txt")

print("\n🎯 Enumeration completed. Check the recon_results/ directory for output.")
