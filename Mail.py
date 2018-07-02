# import necessary packages

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# create message object instance
msg = MIMEMultipart()

message = "Bonjour Monsieur/Madame X, \n\n" \
          "Je me dois de vous prévenir que vous n'avez pas pris le bon médicament. \n" \
          "Je ne suis pas sur que le fait de prendre une deuxieme fois le médicament pour la tension \n" \
          "en moins de deux heures soit une bonne idée...\n" \
          "Bon courage pour la suite :)\n\n" \
          "Bien cordialement, \n" \
          "Ton pilulier\n"  #le corps du message

# setup the parameters of the message
password = "@azerty$"
msg['From'] = "RemMeds@outlook.fr"
msg['To'] = "koceila.haddouch@edu.itescia.fr"
msg['Subject'] = "Rappel !" # L'objet du mail

# add in the message body
msg.attach(MIMEText(message, 'plain'))

# create server
server = smtplib.SMTP('smtp-mail.outlook.com: 587')

server.starttls()

# Login Credentials for sending the mail
server.login(msg['From'], password)

# send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())

server.quit()

print ("successfully sent email to %s:" % (msg['To']))