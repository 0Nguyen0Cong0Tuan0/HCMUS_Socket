from MailLib import *

class EmailViewerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Viewer")
        self.root.geometry("600x400")

        # Create Treeview
        self.tree = tb.Treeview(self.root, columns=("Folder", "Sender", "Message ID", "Status"), show="headings")
        self.tree.heading("Folder", text="Folder")
        self.tree.heading("Sender", text="Sender")
        self.tree.heading("Message ID", text="Message ID")
        self.tree.heading("Status", text="Status")
        self.tree.pack(expand=tb.YES, fill=tb.BOTH)

        # Bind double-click event to show email content
        self.tree.bind("<Double-1>", self.show_email_content)

    def insert_email(self, folder, sender, mes_id, status):
        self.tree.insert("", "end", values=(folder, sender, mes_id, status))

    def show_email_content(self, event):
        item = self.tree.selection()[0]
        folder = self.tree.item(item, "values")[0]
        sender = self.tree.item(item, "values")[1]
        mes_id = self.tree.item(item, "values")[2]
        status = self.tree.item(item, "values")[3]

        # You can implement logic to fetch and display the content of the selected email
        print(f"Selected email in folder {folder} - Sender: {sender} - Message ID: {mes_id} - Status: {status}")

class EmailGetter:
    @staticmethod
    def take_email(files, choice, folder_path):
        response = b""
        path_file = os.path.join(folder_path, files[choice - 1])
        
        with open(path_file, 'rb') as file:
            response = file.read()
        
        return response, EmailGetter.get_email_content(response.decode(FORMAT)) 

    @staticmethod
    def get_email_content(response):
        start_marker = "Content-Transfer-Encoding: 7bit"
        dot = "."

        start_index = response.find(start_marker)
        end_index_boundary = response.find(BOUNDARIES, start_index)
        end_index_dot = response.find(dot, start_index)

        if start_index != -1 and end_index_boundary != -1:
            return response[start_index + len(start_marker):end_index_boundary].strip()
        elif start_index != -1 and end_index_dot != -1:
            return response[start_index + len(start_marker):end_index_dot].strip() 

class EmailSelector:
    @staticmethod
    def choose_folder():
        return int(input("Choose the folder number you want to read: "))

class EmailCreator:
    @staticmethod
    def list_folder():
        sub_folders = [folder.name for folder in os.scandir(SAVE_FOLDER) if folder.is_dir()]
        return sub_folders
    
    @staticmethod
    def path_to_sub_folder(sub_folders, choice):
        path = os.path.join(SAVE_FOLDER, sub_folders[choice - 1])
        return path

    @staticmethod
    def list_file(path):
        files = [file.name for file in os.scandir(path) if file.is_file()]
        return files

class EmailShow:
    @staticmethod
    def show_download_mail():
        email_list = []
        csv_path = os.path.join(SAVE_FOLDER, "students.csv")

        if os.path.exists(csv_path):
            with open(csv_path) as file:
                for line in file:
                    folder, sender, mes_id, status = line.strip().split(',')
                    email = {'folder': folder, 'sender': sender, 'mes_id': mes_id, 'status': status}
                    email_list.append(email)

        return email_list    
    
    @staticmethod
    def show_list_folders(sub_folders):
        for index, sub_folder in enumerate(sub_folders, start=1):
            print(f"{index}_{sub_folder}")

    @staticmethod
    def show_list_files(files):
        for index, file in enumerate(files, start=1):
            print(f"{index}_{file}")

    @staticmethod
    def show_mail_content(content):
        print(f"Content: {content}")

class EmailManager:
    @staticmethod
    def update_all_mail(email_list):
        csv_path = os.path.join(SAVE_FOLDER, "students.csv")
        if os.path.exists(csv_path):
            with open(csv_path, 'w', newline='') as file:
                writer = csv.writer(file)
                for element in email_list:
                    content = [element['folder'], element['sender'], element['mes_id'], element['status']]
                    writer.writerow(content)

    @staticmethod
    def update_status_of_mail(files, choice_file, emails_list):
        global mes_ID, matching_emails
        mes_ID = files[choice_file - 1].split(', ')[1]
        matching_emails = [email for email in emails_list if email.get('mes_id') == mes_ID]
            
        if matching_emails:
            for matching_email in matching_emails:
                matching_email['status'] = "read"
    
    @staticmethod
    def show_email_viewer(email_list):
        root = tk.Tk()
        email_viewer = EmailViewerGUI(root)

        for email in email_list:
            email_viewer.insert_email(email['folder'], email['sender'], email['mes_id'], email['status'])

        root.mainloop()

class EmailDownloader:
    @staticmethod
    def notice_download_attachment(response):
        if NOTICE.encode() in response:
            while True:
                ans = input(f"The {mes_ID} has attached files. Do you want to download it? ")
                if ans.lower() == 'y' or ans.lower() == 'yes':
                    EmailDownloader.save_attachments(response, mes_ID, matching_emails[0]['folder'])
                    break
                elif ans.lower() == 'n' or ans.lower() == 'no':
                    break
                else:
                    print("Invalid Value!!! Try again")

def run_download_mail_program(): 
    emails_list = EmailShow.show_download_mail()
    EmailManager.show_email_viewer(emails_list)

    while True:
        sub_folders = EmailCreator.list_folder()
        EmailShow.show_list_folders(sub_folders)

        choice_folder = EmailSelector.choose_folder()
        folder_path = EmailCreator.path_to_sub_folder(sub_folders, choice_folder)
        
        files = EmailCreator.list_file(folder_path)
        EmailShow.show_list_files(files)

        choice_file = EmailSelector.choose_file()

        response, content = EmailGetter.take_email(files, choice_file, folder_path)
        EmailShow.show_mail_content(content)

        EmailManager.update_status_of_mail(files, choice_file, emails_list)

        EmailDownloader.notice_download_attachment(response)


        choice_continuing = EmailSelector.ask_for_continuing()
        if choice_continuing == 'y':
            continue
        elif choice_continuing == 'n':
            break
    
    EmailManager.update_all_mail(emails_list)

run_download_mail_program()