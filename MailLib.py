import os
import csv
import re
import base64
import socket
from datetime import datetime
import uuid
import json
#-----
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
BOUNDARIES = "--------------5sWLTDpPOowcnjH7yr7J87Aq"
SAVE_FOLDER = 'saved_emails'
NOTICE_1 = 'Content-Type: multipart/mixed;'
FOLDER_LIST = ['INBOX', 'PROJECT', 'IMPORTANT', 'WORK', 'SPAM']
CONFIG_FILE = 'account.json'