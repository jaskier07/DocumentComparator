import tkinter
from tkinter import filedialog, ttk
from tkinter import *
from functools import partial
from tkinter.ttk import *
from _thread import start_new_thread
from tkinter import font
from PIL import Image

from PIL import ImageTk

from DocumentComparator import DocumentComparator
from GraphDrawer import GraphDrawer
from IOUtils import IOUtils

def compare_documents(paths_to_pdf_files, pdf_names):
    dc = DocumentComparator()

    label_info_progressbar = Label(window, text='Comparing...')
    label_info_progressbar.grid(row=3, column=0)

    bar = Progressbar(window, length=200)
    bar.grid(row=4, column=0)

    arr = dc.compare_documents(paths_to_pdf_files, bar, pdf_names)
    label_info_progressbar['text'] = 'Comparing completed.'

    drawer = GraphDrawer()
    drawer.draw(arr, pdf_names)

    im = Image.open("appdata/compare_result.png")
    resized = im.resize((700, 700), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(resized)
    img_placeholder['image'] = photo
    img_placeholder.image = photo


def browse_button():
    folder_path = filedialog.askdirectory()
    [paths_to_pdf_files, pdf_files_in_dir, pdf_names] = IOUtils.list_pdf_files_in_dir(folder_path)
    label_content['text'] = pdf_files_in_dir
    label_header_info['text'] = 'PDFs found in directory:'
    button_compare_documents = Button(text="Compare documents",
                                      command=partial(compare_documents, paths_to_pdf_files, pdf_names))
    button_compare_documents.grid(row=2, column=0)


def configure_styles():
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=12)
    window.option_add("*Font", default_font)


window = Tk()
window.title("Document comparator")
window.geometry('1100x900')

configure_styles()

label_header_info = Label(window, text='First select directory')
label_header_info.configure(font=('calibri', 15))
label_header_info.grid(row=0, column=0)

label_content = Label(window)
label_content.grid(row=1, column=0, sticky="NW")

button_browse = Button(text="Browse for directory", command=browse_button)
button_browse.grid(row=0, column=1, sticky="W")

img_placeholder = Label(window)
img_placeholder.grid(row=1, column=1)

window.mainloop()
