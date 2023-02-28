import re
import csv
import codecs
from tempfile import TemporaryDirectory
from os import path, makedirs
from pypdf import PdfWriter
from md2pdf.core import md2pdf
from tkinter import filedialog

def process_csv(in_file, tmp_path, out_file_path):
    if not in_file: return        
    csvreader = csv.reader(in_file)
    headers = csvreader.__next__()

    pdf = PdfWriter()

    for rownum, row in enumerate(csvreader, start=1):
        row_text = '\n\n'.join([f'## ID: {rownum}'] + [
            f'**{headers[i]}** {elt}'
            for i, elt in enumerate(row)
            if elt != '' and headers[i][0] != '-'
        ])
        pdf_path = path.join(tmp_path, f'{rownum}.pdf') # Use a named file in a temp directory to avoid potential weirdness with closing and re-opening
        md2pdf(pdf_file_path=pdf_path, md_content=row_text)
        
        pdf.append(pdf_path)
        if len(pdf.pages) % 2 != 0:
            pdf.add_blank_page()

    pdf.write(out_file_path)


with filedialog.askopenfile(title='Open CSV file', filetypes=[('CSV', '.csv')]) as in_file, \
        TemporaryDirectory() as tmp_path:
    out_file_path = filedialog.asksaveasfilename(title='Save final PDF', filetypes=[('PDF', '.pdf')])
    process_csv(in_file, tmp_path, out_file_path)
