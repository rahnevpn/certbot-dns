# Certbot DNS Automation Script

This script automates the process of obtaining or renewing SSL/TLS certificates using Certbot with DNS challenges, specifically tailored for use with GoDaddy DNS.

# Disclaimer
My programming skills are close to 0 :-) these scripts were created with the heavy usage of ChatGPT and GitHub co-pilot.

## Requirements
- Python 3 (I used 3.12)
- `requests` library
- Certbot
- Access to GoDaddy API (API Key and Secret)

### Setup python virtual environment

Download the files certbot-dns.py, auth-hook.py and cleanup-hook.py to a folder of your choice. The go to that folder:

`cd /path/to/folder`

The execute the following to create python virtual environment:

`/path/to/python3.12 -m venv .`

`source bin/activate`

## Usage
Run the script with the required arguments:
```
python certbot-dns.py --domain <your_domain> --hostname <your_hostname> --email <your_email> [options]
```
or:<br>
`chmod +x certbot-dns.py auth-hook.py cleanup-hook.py`

Then change the "shebang" line in the beginning of the three files to match the path to python executable in your venv. and then run:

```
certbot-dns.py --domain <your_domain> --hostname <your_hostname> --email <your_email> [options]
```

### Options
- `--domain`: The base domain for the certificate.
- `--hostname`: The primary hostname for the certificate.
- `--email`: Email address for registration and recovery contact with Let's Encrypt.
- `--certonly`: Issue a new certificate instead of renewing an existing one.
- `--dryrun`: Perform a test run without saving the certificates.
- `--sans`: Additional Subject Alternative Names (SANs). Provide each SAN separated by a space.
- `--noroot`: Run Certbot without root privileges, using specified directories.
- `--logfilename`: Custom log file name (default: `certbot-dns.log`).
- `--loglevel`: Logging level (INFO, WARNING, ERROR, DEBUG).

### Environment Variables
Set the following environment variables for GoDaddy API and logging:
- `GODADDY_API_KEY`
- `GODADDY_API_SECRET`
- `LOGFILENAME` (optional)
- `LOGLEVEL` (optional)
- `LOGFILEPATH` (optional)

### Script Functions
- `certbot_exec()`: Constructs and executes the Certbot command based on the provided arguments and options.

## Logging
Logs are written to the specified log file (`certbot-dns.log` by default) with the chosen log level.

## Notes
- Ensure that you have the necessary permissions to write to the specified log and config directories.
- The script handles both issuance and renewal of certificates, including configuring DNS records via GoDaddy's API.
