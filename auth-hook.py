#!/path/to/venv/certbot-dns/bin/python
import os
import requests
import time
import logging

logging.info("Auth-hook script started.")

# Environment variables set by Certbot and your script
base_domain = os.environ.get("CERTBOT_DOMAIN")
dns_key = os.environ.get("CERTBOT_VALIDATION")
log_filename = os.environ.get("LOGFILENAME", "default-auth-hook.log")
log_level = os.environ.get("LOGLEVEL", "INFO")
log_file_path = os.environ.get("LOGFILEPATH", os.path.join(os.getcwd(), log_filename))

# GoDaddy API credentials from environment variables
api_key = os.environ["GODADDY_API_KEY"]
api_secret = os.environ["GODADDY_API_SECRET"]

# Break down the base domain into subdomain and domain
domain_parts = base_domain.split('.')
if len(domain_parts) >= 3:
    godaddy_domain = '.'.join(domain_parts[-2:])
else:
    godaddy_domain = base_domain

# Determine the record name for the DNS TXT record
subdomain = base_domain.split('.')[0]
record_name = "_acme-challenge." + subdomain if subdomain != base_domain else "_acme-challenge"

# Configure logging level
numeric_level = getattr(logging, log_level.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError(f"Invalid log level: {log_level}")

# Configure logging
logging.basicConfig(filename=log_file_path, level=numeric_level, format='%(asctime)s %(levelname)s: %(message)s')

def create_dns_record(domain, record_name, record_value):
    url = f"https://api.godaddy.com/v1/domains/{domain}/records/TXT/{record_name}"
    headers = {
        "Authorization": f"sso-key {api_key}:{api_secret}",
        "Content-Type": "application/json"
    }
    data = [{
        "data": record_value,
        "ttl": 600
    }]
    response = requests.put(url, headers=headers, json=data)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error("Failed to create DNS record:", response.text)
        raise

logging.info(f"Creating DNS TXT record for {record_name}.{godaddy_domain} with value {dns_key}...")
create_dns_record(godaddy_domain, record_name, dns_key)

logging.info(f"Waiting for DNS propagation. This may take some time...")
time.sleep(120)  # Wait 120 seconds for propagation

logging.info("Auth-hook script finished.")
