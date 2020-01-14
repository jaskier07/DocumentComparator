from tkinter import filedialog
from tkinter import *
from functools import partial
from tkinter.ttk import *
from _thread import start_new_thread

from DocumentComparator import DocumentComparator
from IOUtils import IOUtils


def browse_button():
    folder_path = filedialog.askdirectory()
    [paths_to_pdf_files, pdf_files_in_dir] = IOUtils.list_pdf_files_in_dir(folder_path)
    label_info['text'] = pdf_files_in_dir
    dc = DocumentComparator()
    bar = Progressbar(window, length=200)
    bar.grid(row=0, column=1)
    button_compare_documents = Button(text="Compare documents", command=partial(dc.compare_documents, paths_to_pdf_files, bar))
    button_compare_documents.grid(row=1, column=1)


window = Tk()
window.title("Document comparator")
window.geometry('800x600')

label_info = Label(window, text="First select directory")
label_info.grid(row=1, column=0)

button_browse = Button(text="Browse for directory", command=browse_button)
button_browse.grid(row=0, column=0)

window.mainloop()
