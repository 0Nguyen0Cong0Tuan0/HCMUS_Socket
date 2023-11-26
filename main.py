from MailSender import EmailClient_Send
from MailReceiver import EmailClient_Download

def main():
    client = EmailClient_Send()
    client.run()

    # Client = EmailClient_Download()
    # Client.run_download_mail_program()

if __name__ == "__main__":
    main()