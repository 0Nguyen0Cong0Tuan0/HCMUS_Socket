from InterfaceLib import *
from MailSender import EmailClient_Send

#---- SEND TAB
class SendTab:
    @staticmethod
    def open(send_file):
        send_file.filename = filedialog.askopenfilename(
            initialdir="D:", title="Select A File", filetypes=(("*", "*"), ("all files", "*.*"))
        )
        filename_list.append(send_file.filename + '  ')
        SendTab.update_label_to(send_file)

    @staticmethod
    def update_label_to(send_file):
        filenames = ''.join(filename_list)
        
        max_display_length = 115
        filenames_with_newlines = '\n'.join([filenames[i:i + max_display_length] for i in range(0, len(filenames), max_display_length)])

        if send_file is send_to_tab:
            my_label_to.config(text=filenames_with_newlines)
        elif send_file is send_cc_tab:
            my_label_cc.config(text=filenames_with_newlines)
        elif send_file is send_bcc_tab:
            my_label_bcc.config(text=filenames_with_newlines)

    @staticmethod
    def to_tab(send_to_tab, send_email_window):
        # TO LABEL
        label_to = tb.Label(send_to_tab, text="TO", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_to.grid(row=0, column=0, padx=30, pady=10, sticky="w")

        label_subject = tb.Label(send_to_tab, text="SUBJECT", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_subject.grid(row=1, column=0, padx=30, pady=10, sticky="w")

        label_content = tb.Label(send_to_tab, text="CONTENT", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_content.grid(row=2, column=0, padx=30, pady=10, sticky="w")

        label_file = tb.Label(send_to_tab, text="ATTACHED\n    FILE", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_file.grid(row=3, column=0, padx=30, pady=10, sticky="w")

        # TO ENTRY
        global entry_to, entry_subject, entry_content
        entry_to = tb.Entry(send_to_tab, font=(f'{font_type}', 10), width=100)
        entry_to.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        entry_subject = tb.Entry(send_to_tab, font=(f'{font_type}', 10), width=100)
        entry_subject.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        entry_content = ScrolledText(send_to_tab, height=20, width=116, autohide=True, bootstyle='info round')
        entry_content.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        get_file_button = tb.Button(send_to_tab, bootstyle="light, outline, inverse", 
                        text='Select A File', padding=10, command=lambda: SendTab.open(send_to_tab))
        get_file_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        global my_label_to
        my_label_to = tb.Label(send_to_tab, text="", bootstyle='light', font=('Helvetica', 10))
        my_label_to.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        submit_mail = tb.Button(send_to_tab, bootstyle="info outline", 
                        text='SUBMIT', padding=10, command=lambda: SendTab.submit_and_close_to(send_email_window, entry_to.get(),
                         entry_subject.get(), entry_content.get("1.0", "end-1c")))
        submit_mail.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    @staticmethod
    def cc_tab(send_cc_tab, send_email_window):
        # CC LABEL
        label_cc = tb.Label(send_cc_tab, text="CC", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_cc.grid(row=0, column=0, padx=30, pady=10, sticky="w")

        label_subject_cc = tb.Label(send_cc_tab, text="SUBJECT", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_subject_cc.grid(row=1, column=0, padx=30, pady=10, sticky="w")

        label_content_cc = tb.Label(send_cc_tab, text="CONTENT", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_content_cc.grid(row=2, column=0, padx=30, pady=10, sticky="w")

        label_file_cc = tb.Label(send_cc_tab, text="ATTACHED\n    FILE", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_file_cc.grid(row=3, column=0, padx=30, pady=10, sticky="w")

        # CC ENTRY
        global entry_cc, entry_subject_cc, entry_content_cc
        entry_cc = tb.Entry(send_cc_tab, font=(f'{font_type}', 10), width=100)
        entry_cc.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        entry_subject_cc = tb.Entry(send_cc_tab, font=(f'{font_type}', 10), width=100)
        entry_subject_cc.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        entry_content_cc = ScrolledText(send_cc_tab, height=20, width=116, autohide=True, bootstyle='info round')
        entry_content_cc.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        get_file_button_cc = tb.Button(send_cc_tab, bootstyle="light, outline, inverse", 
                        text='Select A File', padding=10, command=lambda: SendTab.open(send_cc_tab))
        get_file_button_cc.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        global my_label_cc
        my_label_cc = tb.Label(send_cc_tab, text="", bootstyle='light', font=('Helvetica', 10))
        my_label_cc.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        submit_mail = tb.Button(send_cc_tab, bootstyle="info outline", 
                        text='SUBMIT', padding=10, command=lambda: SendTab.submit_and_close_cc(send_email_window, entry_cc.get(),\
                         entry_subject_cc.get(), entry_content_cc.get("1.0", "end-1c")))
        submit_mail.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    @staticmethod
    def bcc_tab(send_bcc_tab, send_email_window):
        # BCC LABEL
        label_bcc = tb.Label(send_bcc_tab, text="BCC", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_bcc.grid(row=0, column=0, padx=30, pady=10, sticky="w")

        label_subject_bcc = tb.Label(send_bcc_tab, text="SUBJECT", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_subject_bcc.grid(row=1, column=0, padx=30, pady=10, sticky="w")

        label_content_bcc = tb.Label(send_bcc_tab, text="CONTENT", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_content_bcc.grid(row=2, column=0, padx=30, pady=10, sticky="w")

        label_file_bcc = tb.Label(send_bcc_tab, text="ATTACHED\n    FILE", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_file_bcc.grid(row=3, column=0, padx=30, pady=10, sticky="w")

        # BCC ENTRY
        global entry_bcc, entry_subject_bcc, entry_content_bcc
        entry_bcc = tb.Entry(send_bcc_tab, font=(f'{font_type}', 10), width=100)
        entry_bcc.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        entry_subject_bcc = tb.Entry(send_bcc_tab, font=(f'{font_type}', 10), width=100)
        entry_subject_bcc.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        entry_content_bcc = ScrolledText(send_bcc_tab, height=20, width=116, autohide=True, bootstyle='info round')
        entry_content_bcc.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        get_file_button_bcc = tb.Button(send_bcc_tab, bootstyle="light, outline, inverse", 
                        text='Select A File', padding=10, command=lambda: SendTab.open(send_bcc_tab))
        get_file_button_bcc.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        global my_label_bcc
        my_label_bcc = tb.Label(send_bcc_tab, text="", bootstyle='light', font=('Helvetica', 10))
        my_label_bcc.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        submit_mail = tb.Button(send_bcc_tab, bootstyle="info outline", 
                        text='SUBMIT', padding=10, command=lambda: SendTab.submit_and_close_bcc(send_email_window, entry_bcc.get(),\
                                 entry_subject_bcc.get(), entry_content_bcc.get("1.0", "end-1c")))
        submit_mail.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    @staticmethod
    def submit_and_close_to(window, to, subject, content):
        EmailClient_Send.run_send_mail_program(to, None, None, subject, content, filename_list)
        window.destroy()

    @staticmethod
    def submit_and_close_cc(window, cc, subject, content):
        EmailClient_Send.run_send_mail_program(None, cc, None, subject, content, filename_list)
        window.destroy()

    @staticmethod
    def submit_and_close_bcc(window, bcc, subject, content):
        EmailClient_Send.run_send_mail_program(None, None, bcc, subject, content, filename_list)
        window.destroy()

    @staticmethod
    def open_send_email_window(parent):
        send_email_window = Toplevel(parent)
        send_email_window.title("Send Email")
        send_email_window.geometry(window_size)

        global filename_list
        filename_list = []
        
        frame_send = tb.Frame(send_email_window, bootstyle=f'{color}', width=900, height=500)
        frame_send.grid(padx=100)

        label_sent_program = tb.Label(frame_send, text="SEND", bootstyle=f'inverse {color}',
                                    font=(f'{font_interface}', 25, 'bold'))
        label_sent_program.grid(row=0, column=0, columnspan=3, pady=10, padx=10)

        my_notebook = tb.Notebook(frame_send, bootstyle='success')
        my_notebook.grid(row=1, column=0, padx=5, pady=5, sticky="nsew", rowspan=3)
        
        global send_to_tab
        global send_cc_tab
        global send_bcc_tab
        send_to_tab = tb.Frame(my_notebook)
        send_cc_tab = tb.Frame(my_notebook)
        send_bcc_tab = tb.Frame(my_notebook)

        my_notebook.add(send_to_tab, text="TO")
        my_notebook.add(send_cc_tab, text="CC")
        my_notebook.add(send_bcc_tab, text="BCC")

        SendTab.to_tab(send_to_tab, send_email_window)
        SendTab.cc_tab(send_cc_tab, send_email_window)
        SendTab.bcc_tab(send_bcc_tab, send_email_window)

        # Configure column weights to make them expand evenly
        send_to_tab.columnconfigure(0, weight=1)
        send_to_tab.columnconfigure(1, weight=1)
        send_cc_tab.columnconfigure(0, weight=1)
        send_cc_tab.columnconfigure(1, weight=1)
        send_bcc_tab.columnconfigure(0, weight=1)
        send_bcc_tab.columnconfigure(1, weight=1)
