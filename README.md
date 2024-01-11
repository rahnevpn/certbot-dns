# Certbot DNS Automation Script

## Introduction
This project provides a script to automate the process of obtaining or renewing SSL/TLS certificates using Certbot with DNS challenges. It is specifically designed for integration with GoDaddy DNS. The script simplifies the certificate management process, making it accessible even to those with minimal programming experience.

# Disclaimer
My programming skills are close to 0 :-) these scripts were created with the heavy usage of ChatGPT and GitHub co-pilot.

## Table of Contents
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Options](#options)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Requirements
- Python 3 (version 3.12 recommended)
- `requests` library (version 2.31.0)
- `python-dotenv` library (version 1.0.0)
- [Certbot](https://certbot.eff.org/)
- Access to [GoDaddy API](https://developer.godaddy.com/) (API Key and Secret required)

## Setup
### Python Virtual Environment
1. Download `certbot-dns.py`, `auth-hook.py`, and `cleanup-hook.py` to your chosen folder.
2. Navigate to the folder:
   ```
   cd /path/to/folder
   ```
3. Create a Python virtual environment:
   ```
   /path/to/python3.12 -m venv .
   source bin/activate
   ```
4. Install required libraries:
   ```
   pip install requests python-dotenv
   ```

## Usage
Run the script with the necessary arguments:

1. For issuing of a new certificate run:
	
	```
	python certbot-dns.py --domain <your_domain> --hostname 	<your_hostname> --email <your_email> [options]
	```

	Alternatively, make the scripts executable and run:
	
	```
	chmod +x certbot-dns.py auth-hook.py cleanup-hook.py
	./certbot-dns.py --domain <your_domain> --hostname <your_hostname> --	email <your_email> [options]
	```
2. For renewing of existing certificates run:
	
	```
	python certbot-dns.py
	```
	Alternatively, make the scripts executable and run:
	
	```
	chmod +x certbot-dns.py auth-hook.py cleanup-hook.py
	./certbot-dns.py
	```


## Configuration
Set up the `config.env` file with your GoDaddy API credentials and optional local folder settings for Certbot when running with the `--noroot` option:

```
GODADDY_API_KEY=your_api_key_here
GODADDY_API_SECRET=your_api_secret_here
CERTBOT_CONFIG_DIR=/path/to/certbot/config
CERTBOT_WORK_DIR=/path/to/certbot/work
CERTBOT_LOGS_DIR=/path/to/certbot/logs
```
###Important Reminder
If you populate config.env with real API credentials, remember to add this file to your .gitignore to prevent accidentally committing sensitive data to your public repository. To do this, simply add the line config.env to your .gitignore file.

## Options
- `--certonly`: Issue a new certificate instead of renewing an existing one.
-  `--domain`: The base domain for the certificate.
- `--hostname`: The primary hostname for the certificate.
- `--sans`: add an additional hostname if you wish your certificate to have one or more Subject Alternative Name/s (SAN). Provide each SAN separated by a space. LE supports up to 100 names per certificate: [Rate Limits](https://letsencrypt.org/docs/rate-limits/)
- `--email`: Email address for registration and recovery contact with Let's Encrypt.
- `--dryrun`: Perform a test run without saving the certificates.
- `--noroot`: Run Certbot without root privileges using specified directories.
- `--logfilename`: Custom log file name (default: `certbot-dns.log`).
- `--loglevel`: Logging level (INFO, WARNING, ERROR, DEBUG).


## Logging
Logs are written to `certbot-dns.log` by default. Customize the log file name and level through command-line options or environment variables.

## Troubleshooting

If you run this script with unprivileged user certbot will produce an error that it cannot write in the default directories. The solution is to run it either with elevated permissions or with the `--noroot` option. Running the script with the `-noroot` option requires specifying the folders in the user homedir where certbot can write logs and certificates. You have to create the folders and then configure the full path in the `config.env` file.

## Contributing

Contributions to this project are welcome and appreciated. If you have ideas for improvements or have found issues, here's how you can contribute:

1. **Fork the Repository:** Create a fork of this repository on GitHub. This allows you to make changes to your own copy of the project.

2. **Create a Branch:** Once you have forked the repository, create a branch for your changes. A good branch name could be related to the feature or fix you're working on.

3. **Make Your Changes:** Implement your changes, improvements, or fixes in your branch. Ensure your code is well-documented and follows the project's coding style and standards.

4. **Test Your Changes:** Before submitting, thoroughly test your changes to ensure they are functioning as expected and do not introduce any new issues.

5. **Submit a Pull Request:** Once your changes are ready and tested, submit a pull request to the main repository. In your pull request, provide a clear description of the changes and any additional information that might be helpful for understanding your contributions.

6. **Code Review:** After submitting, your pull request will be reviewed. Be open to feedback and engage in discussions if there are comments or suggestions.

**Guidelines**
Ensure your code is clean, readable, and well-commented.
Update the documentation, including README, if your changes require it.
Respect the project's existing coding style and conventions.
Keep pull requests focused on a single feature or fix to simplify review and merging.

We greatly appreciate any contributions you make to this project!



## License
Copyright 2024 Peter Rahnev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
## Acknowledgments
- Developed with the assistance of OpenAI's ChatGPT and GitHub Co-pilot.

