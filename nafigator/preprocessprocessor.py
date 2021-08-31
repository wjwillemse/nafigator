# coding: utf-8

"""Preprocessor module."""

import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, XMLConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

try:
    import pdfplumber
    PDFPLUMBER = True
except
    PDFPLUMBER = False

from io import BytesIO
from datetime import datetime
from .const import ProcessorElement

import docx
import zipfile

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML


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

    if PDFPLUMBER:
        tables = []
        fp = pdfplumber.open(path)
        for page in fp.pages:
            tables.append(page.extract_tables(params.get('pdfplumber_table_extraction', {})))
        params['pdftotables'] = tables

    return None


WORD_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
PARA = WORD_NAMESPACE + "p"
TEXT = WORD_NAMESPACE + "t"


def convert_docx(path, format="text", codec="utf-8", password="", params=None):

    start_time = datetime.now()

    if format == "text":
        document = zipfile.ZipFile(path)
        xml_content = document.read("word/document.xml")
        document.close()
        tree = XML(xml_content)
        paragraphs = []
        for paragraph in tree.iter(PARA):
            texts = [node.text for node in paragraph.iter(TEXT) if node.text]
            if texts:
                paragraphs.append("".join(texts))
        text = "\n\n".join(paragraphs)

    elif format == "xml":
        with open(path, "rb") as f:
            zip = zipfile.ZipFile(f)
            text = zip.read("word/document.xml")
            styles = zip.read("word/styles.xml")  # not used yet

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

    return None
