from InterfaceLib import *
from MailLib import *
from MailReceiver import EmailShow, EmailGetter, EmailManager, EmailDownloader, EmailFilter
from manageInfo import ManagerInfoUser

#---- RECEIVE TAB AND DOWNLOAD TAB
class EmailView:
    def __init__ (self, root):
        self.root = root
        self.root.title("Email Viewer")
        self.root.geometry(window_size)

        self.style = Style(theme='darkly')

        self.tree = ttk.Treeview(self.root, style="Treeview", 
                                columns=("Sender", "Message ID", "Status"))
        self.tree.heading("#0", text="Folder", anchor=tk.W)
        self.tree.heading("Sender", text="Sender", anchor=tk.W)
        self.tree.heading("Message ID", text="Message ID", anchor=tk.W)
        self.tree.heading("Status", text="Status", anchor=tk.W)
        self.tree.pack(expand=tb.YES, fill=tb.BOTH)

        for font in FOLDER_LIST:
            self.insert_folder(font)

        global emails_list
        emails_list = EmailShow.show_download_mail()
        
        for email in emails_list:
            self.insert_email(email)

        # Bind double-click event to show email content
        self.tree.bind("<Double-1>", self.show_mail_content)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def path_to_sub_folder(self, folder_name):
        config = ManagerInfoUser.load_config()
        path = os.path.join(f"{SAVE_FOLDER}_{config['EMAIL']}", folder_name)
        return path

    def take_email(self, folder_path, file_name):
        response = b""
        path_file = os.path.join(folder_path, file_name)

        with open(path_file, 'rb') as file:
            response = file.read()
        
        return response, EmailGetter.get_sender(response.decode(FORMAT)), \
            EmailGetter.get_subject_email(response.decode(FORMAT)),\
            EmailGetter.get_email_content(response.decode(FORMAT))
    
    def save_attachments(self, response, email_id, folder, new_win):
        config = ManagerInfoUser.load_config()
        mail_folder = os.path.join(f"{SAVE_FOLDER}_{config['EMAIL']}", folder)
        mail_path = os.path.join(mail_folder, f"{email_id} attachment")
        os.makedirs(mail_path, exist_ok=True)

        attachment_pattern = re.compile(rb'Content-Disposition:.*?attachment; filename="(.*?)"', re.DOTALL)
        attachments = re.finditer(attachment_pattern, response)

        for match in attachments:
            attachment_filename = match.group(1).decode(FORMAT)
            attachment_path = os.path.join(mail_path, f"{attachment_filename}")

            attachment_start = response.find(b'\r\n\r\n', match.end()) + 4
            attachment_end = response.find(b'\r\n\r\n', attachment_start)
            
            with open(attachment_path, 'wb') as attachment_file:
                attachment_data = response[attachment_start:attachment_end]
                encoded_data = base64.b64decode(attachment_data)
                attachment_file.write(encoded_data)
        
        new_win.destroy()

    def show_mail(self, response, sender, subject, content, email_id, folder):
        EmailManager.update_status_of_mail(email_id, emails_list)

        new_win = Toplevel()
        new_win.title('Content of the mail')

        frame_show_content = tb.Label(new_win, bootstyle=f'{color} ', width=900)
        frame_show_content.pack()

        label_sender = tb.Label(frame_show_content, text=f"From: {sender}", bootstyle='light',
                            font=('Helvetica', 10, 'bold'))
        label_sender.grid(row=0, column=0, sticky='W')

        label_subject = tb.Label(frame_show_content, text=f"Subject: {subject}", bootstyle='light',
                            font=('Helvetica', 10, 'bold'))
        label_subject.grid(row=1, column=0, sticky='W')

        label_content = tb.Label(frame_show_content, text=f"Content: \n\n{content}", bootstyle='light',
                            font=('Helvetica', 10, 'bold'))
        label_content.grid(row=2, column=0, sticky='W')

        close_button = tb.Button(frame_show_content, text="Close", command=new_win.destroy,
                             bootstyle='info', width=10)
        close_button.grid(row=3, column=0, pady=10, padx = 10, sticky='W')
        
        if NOTICE.encode() in response:
            save_attach_button = tb.Button(frame_show_content, text="Save file", bootstyle='info', width=10,
                                           command=lambda: self.save_attachments(response, email_id, folder, new_win))
            save_attach_button.grid(row=3, column=0, pady=10, padx = 10, sticky='E')

        selected_item = self.tree.selection()
        if selected_item:
            for email in emails_list:
                if email['mes_id'] == email_id:
                    email['status'] = 'read'

        self.tree.item(selected_item, values=(sender, email_id, 'read'))

        new_win.update_idletasks()
        new_win.geometry(f"{frame_show_content.winfo_reqwidth()}x{frame_show_content.winfo_reqheight()}")


        mainloop()

    def insert_folder(self, folder_name):
        self.tree.insert("", "end", folder_name, text=folder_name)

    def insert_email(self, email):
        self.tree.insert(email['folder'], "end", text="", values=(email['sender'], email['mes_id'], email['status']))

    def show_mail_content(self, event):
        item = self.tree.selection()[0]
        if not self.tree.parent(item):  
            return
        folder_name = self.tree.parent(item)
        folder_path = self.path_to_sub_folder(folder_name)

        email_sender = self.tree.item(item, "values")[0]
        email_id = self.tree.item(item, 'value')[1]
        file_name = f"{email_sender}, {email_id}"

        response, sender, subject, content = self.take_email(folder_path, file_name)
        self.show_mail(response, sender, subject, content, email_id, folder_name)
    
    def on_close(self):
        EmailManager.update_all_mail(emails_list)
        self.root.destroy()

    @staticmethod
    def download_tab():
        EmailFilter.create_filter_folder()
        EmailDownloader.download_emails_pop3()
    
    def run_received_tab():
        root = tk.Tk()
        app = EmailView(root)
        root.mainloop()
        