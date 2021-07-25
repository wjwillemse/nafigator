# coding: utf-8

"""Preprocessor module."""

import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, XMLConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
from datetime import datetime
from .const import ProcessorElement

import docx
import zipfile

def convert_pdf(path, format="text", codec="utf-8", password="", params=None):

    start_time = datetime.now()

    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    laparams = LAParams()
    if format == "text":
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    elif format == "html":
        device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    elif format == "xml":
        device = XMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    else:
        raise ValueError("provide format, either text, html or xml!")
    fp = open(path, "rb")
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    maxpages = 0
    caching = True
    pagenos = set()
    pages = 0
    for page in PDFPage.get_pages(
        fp,
        pagenos,
        maxpages=maxpages,
        password=password,
        caching=caching,
        check_extractable=False,
    ):
        interpreter.process_page(page)
        pages += 1

    fp.close()
    device.close()

    text = retstr.getvalue().decode()
    retstr.close()

    end_time = datetime.now()
    params["fileDesc"]["pages"] = pages

    pp = ProcessorElement(
        name="pdfminer-pdf2" + format,
        version=f"pdfminer_version-{pdfminer.__version__}",
        model=None,
        timestamp=None,
        beginTimestamp=start_time,
        endTimestamp=end_time,
        hostname=None,
    )

    params["tree"].add_processor_element("pdfto" + format, pp)

    params["pdfto" + format] = text

    return text

def convert_docx(path, format="text", codec="utf-8", password="", params=None):

    start_time = datetime.now()

    if format == "text":
        document = docx.Document(path)
        text = ""
        for para in document.paragraphs:
            text += para.text
    elif format == "xml":
        with open(path, "rb") as f:
            zip = zipfile.ZipFile(f)
            text = zip.read('word/document.xml')

    end_time = datetime.now()

    pp = ProcessorElement(
        name="python-docx2" + format,
        version=f"python-docx_version-{docx.__version__}",
        model=None,
        timestamp=None,
        beginTimestamp=start_time,
        endTimestamp=end_time,
        hostname=None,
    )

    params["tree"].add_processor_element("docxto" + format, pp)

    params["docxto" + format] = text
