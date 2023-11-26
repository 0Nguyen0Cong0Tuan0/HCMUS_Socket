import os
import csv
import re
import base64
import socket
#--------------
from datetime import datetime
import uuid
#--------------
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb

from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledText
from tkinter import filedialog
#--------------
HEADER = 1024
FORMAT = "utf-8"
BOUNDARY = "------------5sWLTDpPOowcnjH7yr7J87Aq"
MIME_VERSION = "1.0"
USER_AGENT = "Mozilla Thunderbird"
CONTENT_LANGUAGE = "en-US"
BCC_NOTICE = "undisclosed-recipients: ;"
CONTENT_TYPE = "text/plain; charset=UTF-8; format=flowed"
CONTENT_TXT = "text/plain; charset=UTF-8; name="
CONTENT_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document; name="
CONTENT_PDF = "application/pdf; name="
CONTENT_JPG = "image/jpeg; name="
CONTENT_ZIP = "application/x-zip-compressed; name="
CONTENT_TRANSFER_ENCODING = "7bit"
NOTICE = "This is a multi-part message in MIME format."
SEND_CONTENT = False
USERNAME = "Nguyen Cong Tuan"
#--------------
USERNAME = 'nguyencongtuan0810@gmail.com'
PASSWORD = '1234567'
SERVER = '127.0.0.1'
BOUNDARIES = "--------------5sWLTDpPOowcnjH7yr7J87Aq"
POP3_PORT = 3335
SMTP_PORT  = 2225
SAVE_FOLDER = 'saved_emails'
NOTICE_1 = 'Content-Type: multipart/mixed;'
FOLDER_LIST = ['Inbox', 'Project', 'Important', 'Work', 'Spam']
IMPORTANT = ['urgent', 'asap', 'important', 'action required', 'critical',
             'priority', 'attention', 'dealine', 'approval required', 'emergency', 
             'important information', 'right now']
SPAM = ['virus', 'hack', 'crack', 'security alert', 'suspicious activity', 
        'unauthorized access', 'account compromise', 'fraud warning', 'phishing attempt',
        'please confirm your identity', 'click here to reset your password', 'verify your account',
        'unusual login activity', 'your account will be suspended', 'bank account verification',
        'important security upadate', 'win a prize', 'win a lottery']
WORK = ['meeting', 'report', 'project update', 'task', 'collaboration', 'discussion', 'schedule', 
        'feedback', 'assignment']
PROJECT = ['nctuan081004@gmail.com']
#--------------
window_width = 1200
window_height = 700
window_size = str(window_width) + 'x' + str(window_height)
color = "primary"
font_interface = 'GOUDY STOUT'
font_type = 'Arial Greek'