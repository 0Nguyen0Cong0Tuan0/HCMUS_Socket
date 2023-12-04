import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import ttkbootstrap as tb
from ttkbootstrap import Style
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox

import socket

HEADER = 1024

window_width = 1200
window_height = 800
window_size = str(window_width) + 'x' + str(window_height)
color = "primary"
font_interface = 'GOUDY STOUT'
font_type = 'Arial Greek'