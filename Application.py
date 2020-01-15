from functools import partial
from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter.ttk import *
from tkinter import messagebox

from PIL import Image
from PIL import ImageTk

from DocumentComparator import DocumentComparator
from GraphDrawer import GraphDrawer
from IOUtils import IOUtils


def compare_documents(paths_to_pdf_files, pdf_names):
    dc = DocumentComparator()

    label_info_progressbar = Label(window, text='Comparing...')
    label_info_progressbar.grid(row=3, column=0, sticky="S")

    bar.grid(row=4, column=0)

    arr = dc.compare_documents(paths_to_pdf_files, bar)
    label_info_progressbar['text'] = 'Comparing completed.'

    drawer = GraphDrawer()
    drawer.draw(arr, pdf_names)


def browse_button():
    folder_path = filedialog.askdirectory()
    [paths_to_pdf_files, pdf_files_in_dir, pdf_names] = IOUtils.list_pdf_files_in_dir(folder_path)

    bar['value'] = 0
    label_header_info['text']
    bar.update()

    if len(pdf_names) == 0:
         messagebox.showerror('Wrong directory', 'No PDFs found in this directory!')
    elif len(pdf_names) == 1:
        messagebox.showerror('Wrong directory', 'Only 1 PDF found in this directory!')
    else:
        listbox.delete(0, END)
        for (i, elem) in enumerate(pdf_files_in_dir):
            listbox.insert(i, elem)

        label_header_info['text'] = 'PDFs found in directory:'
        button_compare_documents = Button(text="Compare documents",
                                          command=partial(compare_documents, paths_to_pdf_files, pdf_names))
        button_compare_documents.grid(column=0, row=2, sticky="N", padx=(5, 5))


def configure_styles():
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=12)
    window.option_add("*Font", default_font)


window = Tk()
window.title("Document comparator")
window.geometry('800x640')

configure_styles()

label_program_name = Label(window, text='Document comparator')
label_program_name.configure(font=('calibri', 20))
label_program_name.grid(row=0, column=0)

label_header_info = Label(window, text='First select a directory')
label_header_info.configure(font=('calibri', 15))
label_header_info.grid(row=0, column=1, padx=(5, 5), columnspan=3)

listbox = Listbox(window)
listbox.yview()
listbox.grid(row=1, column=1, sticky=N+W, rowspan=14, columnspan=3)
listbox.configure(width=40, height=20)

scroll_vertical = Scrollbar(window, orient=VERTICAL)
scroll_vertical.config(command=listbox.yview)
scroll_vertical.grid(row=1, column=4, sticky=N+S, rowspan=3)

scroll_horizontal = Scrollbar(window, orient=HORIZONTAL)
scroll_horizontal.config(command=listbox.xview)
scroll_horizontal.grid(row=15, column=1, sticky=E+W, columnspan=3)

listbox.config(yscrollcommand=scroll_vertical.set, xscrollcommand=scroll_horizontal.set)

label_info_progressbar = Label(window, text='Comparing...')

bar = Progressbar(window, length=200)

button_browse = Button(text="Browse for directory", command=browse_button)
button_browse.grid(row=1, column=0, sticky="N", padx=(5, 5))

window.mainloop()
