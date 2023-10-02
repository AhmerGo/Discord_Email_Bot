# Discord_Email_Bot

Email-to-Discord Forwarder
This script fetches unread emails from specified email accounts and forwards them to a Discord channel. The fetched emails include the sender's name, their email address, the email subject, a short description of the email, and up to three images if present.

Prerequisites
Python 3.x
pip3
Dependencies
The script uses the following libraries:

discord
imaplib
email
datetime
bs4 (BeautifulSoup)


To install these libraries, run:
pip3 install discord beautifulsoup4
(Note: imaplib and email are part of Python's standard library, so there's no need to install them separately.)

Configuration
Before running the script:

Set up the Email Account:

Replace the IMAP_SERVER, EMAIL, and PASSWORD variables with your email server's IMAP address and your email credentials.
Set up Discord Bot:

Create a new bot on Discord's Developer Portal and copy its token.
Replace the TOKEN variable with your bot's token.
Replace the discord_channel_id variable with the ID of the Discord channel where you want the emails to be forwarded.
Running the Script
Run the script with the command:

python3 your-script-name.py
Deployment on AWS EC2
For continuous 24/7 operation, consider deploying this script on an AWS EC2 instance. Detailed steps on setting up and running the script on EC2 can be found in a separate guide.

Security Considerations
Be cautious about sharing your email credentials. Only deploy this script on trusted and secure environments.
It's advisable to use app-specific passwords or enable 2FA for added email account security.
Ensure you have the necessary permissions and are complying with Discord's terms of service when forwarding emails.
Contributing
If you'd like to contribute or suggest improvements, feel free to fork the repository and submit pull requests or create issues.

