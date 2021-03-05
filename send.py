import os
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

SENDER = ""
RECIPIENT = ""


# The subject line for the email.
SUBJECT = "Send Attachment by AWS SES"

# The full path to the file that will be attached to the email.
ATTACHMENT = "corgi.pdf"

# The email body for recipients with non-HTML email clients.
with open("email.txt", "r") as file:
    BODY_TEXT = file.read()

# The HTML body of the email.
with open("email.html", "r") as file:
    BODY_HTML = file.read()

# The character encoding for the email.
CHARSET = "utf-8"

# Create a new SES resource and specify a region.
client = boto3.client("ses")

# Create a multipart/mixed parent container.
msg = MIMEMultipart("mixed")

# Add subject, from and to lines.
msg["Subject"] = SUBJECT
msg["From"] = SENDER
msg["To"] = RECIPIENT

# Create a multipart/alternative child container.
msg_body = MIMEMultipart("alternative")

# Encode the text and HTML content and set the character encoding. This step is
# necessary if you"re sending a message with characters outside the ASCII range.
text_part = MIMEText(BODY_TEXT.encode(CHARSET), "plain", CHARSET)
html_part = MIMEText(BODY_HTML.encode(CHARSET), "html", CHARSET)

# Add the text and HTML parts to the child container.
msg_body.attach(text_part)
msg_body.attach(html_part)

# Define the attachment part and encode it using MIMEApplication.
att = MIMEApplication(open(ATTACHMENT, "rb").read())

# Add a header to tell the email client to treat this part as an attachment,
# and to give the attachment a name.
att.add_header("Content-Disposition", "attachment", filename=os.path.basename(ATTACHMENT))

# Attach the multipart/alternative child container to the multipart/mixed
# parent container.
msg.attach(msg_body)

# Add the attachment to the parent container.
msg.attach(att)
try:
    response = client.send_raw_email(
        Source=SENDER,
        Destinations=[
            RECIPIENT
        ],
        RawMessage={
            "Data": msg.as_string(),
        }
    )
    print("Email sent! Message ID: ", response["MessageId"])
except Exception as e:
    print(e)
