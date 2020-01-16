from functools import partial
from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter.ttk import *
from tkinter import messagebox

from PIL import Image
from PIL import ImageTk

from SimilarityTable import SimilarityTable
from DocumentComparator import DocumentComparator
from GraphDrawer import GraphDrawer
from IOUtils import IOUtils

def compare_documents(paths_to_pdf_files, pdf_names):
    bar['value'] = 0
    bar.update()

    label_info_progressbar['text'] = 'Comparing...'
    label_info_progressbar.update()
    bar.grid(row=4, column=0)

    dc = DocumentComparator()
    arr = dc.compare_documents(paths_to_pdf_files, bar)

    label_info_progressbar['text'] = 'Comparing completed.'
    label_info_progressbar.update()

    SimilarityTable().create(arr, pdf_names, window)

    drawer = GraphDrawer()
    drawer.draw(arr, pdf_names)


def browse_files():
    folder_path = filedialog.askopenfilenames(filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
    if folder_path != '':
        [paths_to_pdf_files, pdf_names] = IOUtils.list_pdf_files_in_dir(folder_path)

        if len(pdf_names) < 2:
            messagebox.showerror('Wrong directory', 'Select two or more PDF files.')
        else:
            listbox.delete(0, END)
            for (i, elem) in enumerate(pdf_names):
                listbox.insert(i, elem)

            label_header_info['text'] = 'PDFs select:'
            button_compare_documents = Button(text="Compare documents",
                                              command=partial(compare_documents, paths_to_pdf_files, pdf_names))
            button_compare_documents.grid(column=0, row=2, sticky="S", padx=(5, 5))


def configure_styles():
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=12)
    window.option_add("*Font", default_font)


window = Tk()
window.title("Document comparator")
window.geometry('660x400')

configure_styles()

label_program_name = Label(window, text='Document comparator')
label_program_name.configure(font=('calibri', 20, "bold"), foreground="#3d423a")
label_program_name.grid(row=0, column=0, padx=(5, 5))

label_header_info = Label(window, text='First select PDF files...')
label_header_info.configure(font=('calibri', 15))
label_header_info.grid(row=0, column=1, padx=(5, 5), sticky=W, columnspan=3)

listbox = Listbox(window)
listbox.yview()
listbox.grid(row=1, column=1, sticky=N + W, rowspan=14, columnspan=3)
listbox.configure(width=40, height=15)

scroll_vertical = Scrollbar(window, orient=VERTICAL)
scroll_vertical.config(command=listbox.yview)
scroll_vertical.grid(row=1, column=4, sticky=N + S, rowspan=14)

scroll_horizontal = Scrollbar(window, orient=HORIZONTAL)
scroll_horizontal.config(command=listbox.xview)
scroll_horizontal.grid(row=15, column=1, sticky=E + W, columnspan=3)

listbox.config(yscrollcommand=scroll_vertical.set, xscrollcommand=scroll_horizontal.set)

label_info_progressbar = Label(window, text='')
label_info_progressbar.grid(row=3, column=0, sticky="S")

bar = Progressbar(window, length=200)

button_browse = Button(text="Select files", command=browse_files)
button_browse.grid(row=1, column=0, sticky="S", padx=(5, 5))

window.mainloop()
