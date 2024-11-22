import re
import subprocess
from urllib.parse import urlparse


def extract_domain(url):
    parsed_uri = urlparse(url)
    domain = parsed_uri.netloc.split(':')[0]
    return domain


def get_ip_from_nslookup(domain):
    try:
        nslookup_result = subprocess.check_output(['nslookup', domain], stderr=subprocess.STDOUT, text=True)

        ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ipv4_addresses = []
        addresses_started = False

        for line in nslookup_result.splitlines():
            if 'Address:' in line:
                addresses_started = True
                match = re.search(ipv4_pattern, line)
                if match:
                    ipv4_addresses.append(match.group(0))

        if len(ipv4_addresses) >= 2:
            return ipv4_addresses[1]

        return None
    except subprocess.CalledProcessError as e:
        print(f"Failed to resolve domain {domain}: {e.output}")
        return None


def process_urls(input_file, output_file):
    unique_ips = set()

    with open(input_file, 'r') as file:
        for line in file:
            url = line.strip()
            if url:
                domain = extract_domain(url)
                ip_address = get_ip_from_nslookup(domain)
                if ip_address:
                    unique_ips.add(ip_address)
    with open(output_file, 'w') as file:
        for ip in unique_ips:
            file.write(ip + '\n')


input_file = './result/urls.txt'
output_file = './result/resolved_ip.txt'

process_urls(input_file, output_file)
