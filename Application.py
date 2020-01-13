from tkinter import filedialog
from tkinter import *
from functools import partial

from DocumentComparator import DocumentComparator
from IOUtils import IOUtils


def browse_button():
    folder_path = filedialog.askdirectory()
    [paths_to_pdf_files, pdf_files_in_dir] = IOUtils.list_pdf_files_in_dir(folder_path)
    label_info['text'] = pdf_files_in_dir
    dc = DocumentComparator()
    button_compare_documents = Button(text="Compare documents", command=partial(dc.compare_documents, paths_to_pdf_files))
    button_compare_documents.grid(row=1, column=1)


window = Tk()
window.title("Document comparator")
window.geometry('800x600')

label_info = Label(window, text="First select directory")
label_info.grid(row=1, column=0)

button_browse = Button(text="Browse for directory", command=browse_button)
button_browse.grid(row=0, column=0)

window.mainloop()
