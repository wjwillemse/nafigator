# coding: utf-8

"""Preprocessor module."""

import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, XMLConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO

from datetime import datetime

def convert_pdf(path, format='text', codec='utf-8', password='', params = None):

    params['preprocess_name'] = f'pdfminer-pdf2'+format
    params['preprocess_version'] = f'pdfminer_version-{pdfminer.__version__}'
    params['preprocess_start_time'] = datetime.now()

    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    laparams = LAParams()
    if format == 'text':
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    elif format == 'html':
        device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    elif format == 'xml':
        device = XMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    else:
        raise ValueError('provide format, either text, html or xml!')
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)

    fp.close()
    device.close()

    text = retstr.getvalue().decode()
    retstr.close()
    
    params['preprocess_end_time'] = datetime.now()

    return text