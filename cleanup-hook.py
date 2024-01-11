#!/path/to/venv/certbot-dns/bin/python
import os
import requests
import logging

print("Cleanup-hook script started.")

# Use environment variables set by Certbot
fqdn = os.environ.get("CERTBOT_DOMAIN")
log_filename = os.environ.get("LOGFILENAME", "default-cleanup-hook.log")
log_level = os.environ.get("LOGLEVEL", "INFO")
log_file_path = os.environ.get("LOGFILEPATH", os.path.join(os.getcwd(), log_filename))

# GoDaddy API credentials from environment variables
api_key = os.environ["GODADDY_API_KEY"]
api_secret = os.environ["GODADDY_API_SECRET"]

# Break down the base domain into subdomain and domain
domain_parts = fqdn.split('.')
if len(domain_parts) >= 3:
    godaddy_domain = '.'.join(domain_parts[-2:])
else:
    godaddy_domain = fqdn

# Configure logging level
numeric_level = getattr(logging, log_level.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError(f"Invalid log level: {log_level}")

# Configure logging
logging.basicConfig(filename=log_file_path, level=numeric_level, format='%(asctime)s %(levelname)s: %(message)s')

# Determine the record name for the DNS TXT record
subdomain = fqdn.split('.')[0]
record_name = "_acme-challenge." + subdomain if subdomain != fqdn else "_acme-challenge"

def delete_dns_record(domain, record_name):
    url = f"https://api.godaddy.com/v1/domains/{domain}/records/TXT/{record_name}"
    headers = {
        "Authorization": f"sso-key {api_key}:{api_secret}",
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Failed to delete DNS record:", response.text)
        raise
    
logging.info(f"Deleting DNS TXT record for {record_name}.{godaddy_domain}...")
delete_dns_record(godaddy_domain, record_name)

logging.info("Cleanup-hook script finished.")