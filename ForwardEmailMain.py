import discord
import imaplib
import email
import asyncio
import os
from email.header import decode_header
from datetime import datetime, timedelta


# Discord bot token
TOKEN = 'MTE1NTc0Mjg4NDk5NDI0MDU1Mg.G5k0xV.H7MPIW0gHS_EvYoTinjBksoR8PL9rRUEIQsOds'
# Connect to Discord
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
client = discord.Client(intents=intents)


async def fetch_emails(IMAP_SERVER, EMAIL, PASSWORD, CHANNEL_ID):
    channel = client.get_channel(CHANNEL_ID)
    
    # Connect to the email server and fetch emails from the past 24 hours
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%d-%b-%Y')
    status, email_ids = mail.search(None, f'(SINCE "{yesterday}")', 'UNSEEN')
    email_ids = email_ids[0].split()

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        email_content = msg_data[0][1]
        msg = email.message_from_bytes(email_content)
        
        # Extract sender's name and email
        from_header = email.utils.parseaddr(msg['From'])
        sender_name = from_header[0]
        sender_email = from_header[1]

        # Extract and decode the subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        # Extract the email body and truncate for a short description (let's say first 100 characters)
        body = ""
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                break  # Get only the first text/plain part

        short_description = body[:300] + '...' if len(body) > 300 else body
        await channel.send("\n---------------------------------------------------------------------------------------------------------")

        # Create the formatted message
        formatted_message = f"{sender_name} <{sender_email}>\n{subject}\n{short_description}\n"
        await channel.send(formatted_message)


        
        image_count = 0
        # If there are any images, send them as well
        for part in msg.walk():
            if part.get_content_type().startswith("image/"):
                image_data = part.get_payload(decode=True)
                image_filename = part.get_filename()
                if image_filename:
                    with open(image_filename, "wb") as f:
                        f.write(image_data)
                    with open(image_filename, "rb") as f:
                        await channel.send(file=discord.File(f))
                    os.remove(image_filename)  # Delete the image file after sending


                image_count += 1
                if image_count >= 3:  # Only take the first three images
                    break

        await channel.send("---------------------------------------------------------------------------------------------------------\n")



        mail.store(email_id, '+FLAGS', '\\Seen')
        
    mail.logout()

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    # enable IMAP settings for all of the following emails 
    while True:  # This loop makes the email checking semi-continuous
        # IMAP SERVER_ADDRESS , email, app password or email password, channel id of the channel you want those emails fed into 
        await fetch_emails('imap.mail.yahoo.com','example@yahoo.com', 'REDACTED APP PASSWORD', 1158110758492704930) # yahoo uses app passwords
        await fetch_emails('outlook.office365.com','example@outlook.com', 'REDACTED EMAIL PASSWORD', 1158188122186731551) # outlook accounts can use 
        await fetch_emails('imap.gmail.com','example@gmail.com', 'REDACTED APP PASSWORD', 1158188178432340089) # app passwords
        await asyncio.sleep(300)  # Wait for 5 minutes (300 seconds) before checking again

client.run(TOKEN)
