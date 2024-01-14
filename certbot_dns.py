#!/path/to/venv/certbot-dns/bin/python
""" Certbot DNS automation script for GoDaddy DNS """
import subprocess
import os
import argparse
import logging
from dotenv import load_dotenv

# Load environment variables for GoDaddy API credentials
load_dotenv('/Users/rahnev/github/certbot-dns-stage/config.env')

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--domain",
                    help="Domain for the certificate",
                    default="")
parser.add_argument("--hostname",
                    help="Hostname for the certificate",
                    default="")
parser.add_argument("--email",
                    help="Email address for the certificate",
                    default="")
parser.add_argument("--certonly",
                    help="Issue a new certificate instead of renewing",
                    action="store_true")
parser.add_argument("--dryrun",
                    help="Perform a test run of the client, obtaining \
                    test (invalid) certificates but not saving them to disk",
                    action="store_true")
parser.add_argument("--sans",
                    nargs='*',
                    help="Additional Subject Alternative Names (SANs)",
                    default=[])
parser.add_argument("--noroot",
                    help="Run Certbot without root privileges",
                    action="store_true")
parser.add_argument("--logfilename",
                    help="Log file name",
                    default="certbot-dns.log")
parser.add_argument("--loglevel",
                    help="Logging level (INFO, WARNING, ERROR, DEBUG)",
                    default="INFO")
cli_args = parser.parse_args()

# Determine log file path
log_file_path = os.path.join(os.getcwd(), cli_args.logfilename)

# Set certbot directories
config_dir = os.path.expanduser(os.environ.get("CERTBOT_CONFIG_DIR"))
work_dir = os.path.expanduser(os.environ.get("CERTBOT_WORK_DIR"))
logs_dir = os.path.expanduser(os.environ.get("CERTBOT_LOGS_DIR"))

# Load environment variables for GoDaddy API credentials
api_key = os.environ.get("GODADDY_API_KEY")
api_secret = os.environ.get("GODADDY_API_SECRET")

# Set environment variables for the hook scripts
os.environ["DOMAIN"] = cli_args.domain
os.environ["HOSTNAME"] = cli_args.hostname
os.environ["LOGFILENAME"] = cli_args.logfilename
os.environ["LOGLEVEL"] = cli_args.loglevel
os.environ["LOGFILEPATH"] = log_file_path

# Configure logging level
numeric_level = getattr(logging, cli_args.loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError(f"Invalid log level: {cli_args.loglevel}")

# Configure logging
logging.basicConfig(filename=log_file_path,
                    level=numeric_level,
                    format='%(asctime)s %(levelname)s: %(message)s')

def certbot_exec(renew):
    """ Execute Certbot """
    command =   [
        "certbot", 
        "renew" if renew else "certonly", 
        "--manual", 
        "--preferred-challenges", "dns",
        "--manual-auth-hook", "python auth_hook.py",
        "--manual-cleanup-hook", "python cleanup_hook.py",
        "--email", cli_args.email,
        "--agree-tos",
    ]
    if not renew:
        command += ["-d", f"{cli_args.hostname}.{cli_args.domain}"]
        for san in cli_args.sans:
            command += ["-d", f"{san}.{cli_args.domain}"]
    if cli_args.dryrun:
        command += ["--dry-run"]
    if cli_args.noroot:
        command += ["--work-dir", work_dir, "--config-dir", config_dir, "--logs-dir", logs_dir]
    with open(log_file_path, 'a', encoding="utf-8") as log_file:
        try:
            subprocess.run(command, check=True, stdout=log_file, stderr=log_file)
            logging.info("Certbot command executed successfully.")
        except subprocess.CalledProcessError as command_error:
            logging.error("An error occurred while running Certbot: %s", command_error)
logging.info("Starting Certbot DNS automation script...")

if cli_args.certonly:
    logging.info("Issuing a new certificate for: %s.%s", cli_args.hostname, cli_args.domain)
    try:
        logging.info("Certbot process for issuing a new certificate completed.")
        certbot_exec(renew=False)
    except subprocess.CalledProcessError as e:
        logging.error("An error occurred while running Certbot: %s", e)
else:
    logging.info("Renewing certificate...")
    try:
        logging.info("Certbot process for renewing certificates completed.")
        certbot_exec(renew=True)
    except subprocess.CalledProcessError as e:
        logging.error("An error occurred while renewing certificates: %s", e)

logging.info("Certbot DNS automation script finished.")
