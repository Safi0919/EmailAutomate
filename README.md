# Tutoring Email Automation

## Overview

This project automates fetching tutoring appointment requests from unread emails, extracting relevant details, and sending confirmation emails to attendees. It uses IMAP to read emails, regex to extract information, and SMTP to send responses.

## Features

- Fetch unread emails from Gmail.
- Extract appointment details (date, time, modality, location, topic, attendees, comments) from the email body.
- Send confirmation emails to attendees with extracted details.
- CC the confirmation email to the desired email address.
- Interactive prompt to confirm before sending emails.

## Prerequisites

- A Gmail account with IMAP access enabled.
- Google App Password (if using Gmail, as Google blocks less secure apps).
- Python 3 installed.

## Installation

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies (if any):
   ```sh
   pip install -r requirements.txt  # If using external dependencies
   ```
3. Enable IMAP for your Gmail account:
   - Go to Gmail settings -> See all settings -> Forwarding and POP/IMAP.
   - Enable IMAP.

## Configuration

Modify the script with your email credentials:

```python
EMAIL_USER = "your email address"
EMAIL_PASS = "your Google apps password"
```

## Usage

Run the script:

```sh
python script.py
```

- The script fetches unread emails.
- Extracts details from tutoring requests.
- Asks for confirmation before sending an email.
- Sends a formatted confirmation email if confirmed.

## Security Notice

- Do **NOT** store your email password directly in the script. Use environment variables or a configuration file.
- If using Gmail, generate an **App Password** instead of using your actual password.

## License

This project is open-source and available under the MIT License.

## Author

Safiullah Saif

