import smtplib  # for actual sending
from email.mime.text import MIMEText # Import the email modules we'll need

# Usage:
# from send_email import sendEmail
# sendEmail("ATTN","all hands onboard","buchmann@zew.de")

def sendEmail(subj,msgBody,address):
	try:
		sender     = address
		recipients = address
		body = '%s\n(end of message body)\n' % (msgBody)
		msg = MIMEText(body)  # ascii only
		msg['Subject'] = '%s (subject line)' % (subj[:40])
		msg['From'] = sender
		msg['To']   = recipients

		# Send the message via our own SMTP server.
		# But don't include the envelope header.
		# s = smtplib.SMTP('localhost')
		s = smtplib.SMTP('hermes.zew-private.de',timeout=4)
		s.sendmail(sender, [recipients], msg.as_string())
		s.quit()
	except Exception as e:
		print("Exception while sending Email")
		print(str(e))

