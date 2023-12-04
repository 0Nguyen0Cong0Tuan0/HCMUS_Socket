from InterfaceLib import *
from MailSender import EmailClient_Send

#---- SEND TAB
class SendTab:
    def __init__(self, parent):
        self.send_email_window = Toplevel(parent)
        self.send_email_window.title("Send Email")
        self.send_email_window.geometry(window_size)
        self.open_send_email_window()
        self.filename_list = []
        self.my_label_attached_file
        self.send_tab = None

    def open(self):
        self.send_tab.filename = filedialog.askopenfilename(
            initialdir="D:", title="Select A File", filetypes=(("*", "*"), ("all files", "*.*"))
        )
        self.filename_list.append(self.send_tab.filename + '  ')
        self.update_label_to()


    def update_label_to(self):
        filenames = ''.join(self.filename_list)
        
        max_display_length = 115
        filenames_with_newlines = '\n'.join([filenames[i:i + max_display_length] for i in range(0, len(filenames), max_display_length)])
        self.my_label_attached_file.config(text=filenames_with_newlines)


    def to_tab(self):
        label_to = tb.Label(self.send_tab, text="TO", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_to.grid(row=0, column=0, padx=30, pady=10, sticky="w")

        label_cc = tb.Label(self.send_tab, text="CC", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_cc.grid(row=1, column=0, padx=30, pady=10, sticky="w")

        label_bcc = tb.Label(self.send_tab, text="BCC", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_bcc.grid(row=2, column=0, padx=30, pady=10, sticky="w")

        label_subject = tb.Label(self.send_tab, text="SUBJECT", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_subject.grid(row=3, column=0, padx=30, pady=10, sticky="w")

        label_content = tb.Label(self.send_tab, text="CONTENT", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_content.grid(row=4, column=0, padx=30, pady=10, sticky="w")

        label_file = tb.Label(self.send_tab, text="ATTACHED\n    FILE", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_file.grid(row=5, column=0, padx=30, pady=10, sticky="w")

        entry_to = tb.Entry(self.send_tab, font=(f'{font_type}', 10), width=100)
        entry_to.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        entry_cc = tb.Entry(self.send_tab, font=(f'{font_type}', 10), width=100)
        entry_cc.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        entry_bcc = tb.Entry(self.send_tab, font=(f'{font_type}', 10), width=100)
        entry_bcc.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        entry_subject = tb.Entry(self.send_tab, font=(f'{font_type}', 10), width=100)
        entry_subject.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        entry_content = ScrolledText(self.send_tab, height=20, width=116, autohide=True, bootstyle='info round')
        entry_content.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        get_file_button = tb.Button(self.send_tab, bootstyle="light, outline, inverse", 
                        text='Select A File', padding=10, command=lambda: self.open)
        get_file_button.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.my_label_attached_file = tb.Label(self.send_tab, text="", bootstyle='light', font=('Helvetica', 10))
        self.my_label_attached_file.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        submit_mail = tb.Button(self.send_tab, bootstyle="info outline", 
                        text='SUBMIT', padding=10, command=lambda: self.submit_and_close(entry_to.get(),
                        entry_cc.get(), entry_bcc.get(), entry_subject.get(), entry_content.get("1.0", "end-1c")))
        submit_mail.grid(row=6, column=2, padx=10, pady=10, sticky="w")

    def submit_and_close(self, to, cc, bcc, subject, content):
        EmailClient_Send.run_send_mail_program(to, cc, bcc, subject, content, self.filename_list)
        
        self.send_email_window.destroy()
    
    def open_send_email_window(self):
        frame_send = tb.Frame(self.send_email_window, bootstyle=f'{color}', width=900, height=500)
        frame_send.grid(padx=100)

        label_sent_program = tb.Label(frame_send, text="SEND", bootstyle=f'inverse {color}',
                                    font=(f'{font_interface}', 25, 'bold'))
        label_sent_program.grid(row=0, column=0, columnspan=3, pady=10, padx=10)

        my_notebook = tb.Notebook(frame_send, bootstyle='success')
        my_notebook.grid(row=1, column=0, padx=5, pady=5, sticky="nsew", rowspan=3)
        
        
        self.send_tab = tb.Frame(my_notebook)

        my_notebook.add(self.send_tab, text="SEND EMAIL")

        self.to_tab()

        self.send_tab.columnconfigure(0, weight=1)
        self.send_tab.columnconfigure(1, weight=1)

