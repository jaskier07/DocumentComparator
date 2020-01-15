from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import os


class IOUtils:

    @staticmethod
    def pdf_to_text(pdf_name):
        # PDFMiner boilerplate
        resource_manager = PDFResourceManager()
        sio = StringIO()
        device = TextConverter(resource_manager, sio, laparams=LAParams())
        interpreter = PDFPageInterpreter(resource_manager, device)
        fp = open(pdf_name, 'rb')
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
        fp.close()
        text = sio.getvalue()
        device.close()
        sio.close()

        return text

    @staticmethod
    def list_pdf_files_in_dir(directory):
        paths_to_pdf_files = []
        pdf_files_in_dir = ''
        pdf_names = []
        for filename in os.listdir(directory):
            if filename.endswith('.pdf'):
                pdf_files_in_dir += filename + '\n'
                pdf_names.append(filename)
                paths_to_pdf_files.append(directory + '/' + filename)
        return [paths_to_pdf_files, pdf_files_in_dir, pdf_names]
