"""Tests for `preprocessprocessor` module"""

import unittest
from nafigator.preprocessprocessor import convert_pdf, convert_docx

unittest.TestLoader.sortTestMethodsUsing = None


# Needed documents: pdf with and without password

def test_convert_pdf():
    """
    This function converts a pdf file into text, html or xml.
    Input:
        path: location of the file to be converted
        format: html, text or xml
        codec: codec to be used to conversion
        password: password to be used for conversion
        params: the general params dict to store results
    Level: 0
    Scenarios:
        conversion to text
        conversion to html
        conversion to xml
    """
    pass


# @TODO: write in later refactoring phase
def test_convert_docx():
    """
    This function converts a docx file into text or xml.
    Input:
        path: location of the file to be converted
        format: text or xml
        codec: codec to be used to conversion
        password: password to be used for conversion
        params: the general params dict to store results
    Level: Out of scope in refactoring phase 1
    """
    pass
