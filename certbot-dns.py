import subprocess
import os
import argparse
import logging
from dotenv import load_dotenv

# Load environment variables for GoDaddy API credentials
load_dotenv('/Users/rahnev/github/certbot-dns-stage/config.env')

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--domain", help="Domain for the certificate", default="")
parser.add_argument("--hostname", help="Hostname for the certificate", default="")
parser.add_argument("--email", help="Email address for the certificate", default="")
parser.add_argument("--certonly", help="Issue a new certificate instead of renewing", action="store_true")
parser.add_argument("--dryrun", help="Perform a test run of the client, obtaining test (invalid) certificates but not saving them to disk", action="store_true")
parser.add_argument("--sans", nargs='*', help="Additional Subject Alternative Names (SANs)", default=[])
parser.add_argument("--noroot", help="Run Certbot without root privileges", action="store_true")
parser.add_argument("--logfilename", help="Log file name", default="certbot-dns.log")
parser.add_argument("--loglevel", help="Logging level (INFO, WARNING, ERROR, DEBUG)", default="INFO")
args = parser.parse_args()

# Determine log file path
log_file_path = os.path.join(os.getcwd(), args.logfilename)

# Set certbot directories
config_dir = os.path.expanduser(os.environ.get("CERTBOT_CONFIG_DIR"))
work_dir = os.path.expanduser(os.environ.get("CERTBOT_WORK_DIR"))
logs_dir = os.path.expanduser(os.environ.get("CERTBOT_LOGS_DIR"))

# Load environment variables for GoDaddy API credentials
api_key = os.environ.get("GODADDY_API_KEY")
api_secret = os.environ.get("GODADDY_API_SECRET")

# Set environment variables for the hook scripts
os.environ["DOMAIN"] = args.domain
os.environ["HOSTNAME"] = args.hostname
os.environ["LOGFILENAME"] = args.logfilename
os.environ["LOGLEVEL"] = args.loglevel
os.environ["LOGFILEPATH"] = log_file_path

# Configure logging level
numeric_level = getattr(logging, args.loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError(f"Invalid log level: {args.loglevel}")

# Configure logging
logging.basicConfig(filename=log_file_path, level=numeric_level, format='%(asctime)s %(levelname)s: %(message)s')

def certbot_exec(renew, args):
    command =   [
        "certbot", 
        "renew" if renew else "certonly", 
        "--manual", 
        "--preferred-challenges", "dns",
        "--manual-auth-hook", "python auth-hook.py",
        "--manual-cleanup-hook", "python cleanup-hook.py",
        "--email", args.email,
        "--agree-tos",
    ]
    if not renew:
        command += ["-d", f"{args.hostname}.{args.domain}"]
        for san in args.sans:
            command += ["-d", f"{san}.{args.domain}"]
    if args.dryrun:
        command += ["--dry-run"]
    if args.noroot:
        command += ["--work-dir", work_dir, "--config-dir", config_dir, "--logs-dir", logs_dir]
    
    with open(log_file_path, 'a') as log_file:
        try:
            subprocess.run(command, check=True, stdout=log_file, stderr=log_file)
            logging.info("Certbot command executed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"An error occurred while running Certbot: {e}")
    #return command
    

logging.info("Starting Certbot DNS automation script...")

if args.certonly:
    logging.info(f"Issuing a new certificate for: {args.hostname}.{args.domain}")
    try:
        logging.info("Certbot process for issuing a new certificate completed.")
        certbot_exec(renew=False, args=args)
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while running Certbot: {e}")
else:
    logging.info(f"Renewing certificate...")
    try:
        logging.info("Certbot process for renewing certificates completed.")
        certbot_exec(renew=True, args=args)
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while renewing certificates: {e}")

logging.info("Certbot DNS automation script finished.")