import imaplib, ssl
import base64
import os
import email
from pathlib import Path

FOLDER_PATH = r'D:\Socket\HCMUS_Socket'

email_user = 'nguyencongtuan0810@gmail.com'  # input('Email: ')
email_pass = '1234567'  # input('Password: ')
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
mail = imaplib.IMAP4_SSL("smtp.neilolander.name", port=2225, ssl_context=context)

mail.login(email_user, email_pass)

mail.select('Inbox')

type, data = mail.search(None, 'ALL')
mail_ids = data[0]
id_list = mail_ids.split()
# print(data[0].decode('utf8').split(' '))
# print(id_list)
mylist = []
# for i in mail.list()[1]:
#   print(i)

for response_part in data:
    if isinstance(response_part, tuple):
        msg = email.message_from_string(response_part[1].decode('utf-8'))
        email_subject = msg['subject']
        email_from = msg['from']
        print('From : ' + email_from + '\n')
        print('Subject : ' + email_subject + '\n')
        print(msg.get_payload(decode=True))

for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)')
    raw_email = data[0][1]
    # converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    # downloading attachments
    for part in email_message.walk():
        # this part comes from the snipped I don't understand yet...
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        print(num)
        if num in mylist:
            pass
        else:
            mylist.append(num)
        if bool(fileName):
            sender = email_message['From']
            sender = sender.replace('<', '')
            sender = sender.replace('>', '')
            tpath = FOLDER_PATH + '/' + str(sender)
            Path(tpath).mkdir(parents=True, exist_ok=True)
            filePath = os.path.join(tpath, fileName)
            if not os.path.isfile(filePath):
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
            print(tpath)
            print('Downloaded "{file}" from email titled "{subject}".'.format(file=fileName,
                                                                              subject=subject))  # , uid=mail.uid.decode('utf-8')))
for i in mylist:
    mail.copy(i, 'INBOX.Processed')
    mail.store(i, '+FLAGS', '\\Deleted')
mail.expunge()
