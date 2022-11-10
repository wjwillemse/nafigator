# from nafigator.nafdocument import NafDocument
from nafigator.postprocessor.highlighter import Highlighter
from lxml import etree
import fitz
import os
from nafigator import NafDocument, parse2naf
import unittest

unittest.TestLoader.sortTestMethodsUsing = None


class TestHighlighter(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """

    doc = NafDocument().open('tests/tests/example_copy.naf.xml')
    highlighter = Highlighter('tests/tests/example.pdf', doc)

    def test_highlight_box_in_pdf(self):
        bbox = {'x0': 203.963, 'y0': 771.408, 'x1': 221.964, 'y1': 783.408}
        path_highlighted_pdf = 'tests/tests/example_highlighted.pdf'
        page_nr = 1

        origin_bl = True
        self.highlighter.highlight_box_in_pdf(bbox, path_highlighted_pdf, page_nr, origin_bl)
        # check if document has been highlighted and saved
        filepath = "tests/tests/example_highlighted.pdf"
        doc = fitz.open(filepath)
        page = doc[0]

        # list of words on page
        wordlist = page.get_text("words")
        # sort on ascending y, then x
        wordlist.sort(key=lambda w: (w[3], w[0]))
        annot = page.firstAnnot
        # check which word corresponds with highlight in pdf
        points = annot.vertices
        r = fitz.Quad(points[0: 4]).rect
        word = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
        actual = word[0][4]
        os.remove("tests/tests/example_highlighted.pdf")
        assert actual == 'you'

    def test_retreive_subelements_by_tag(self):
        tag_path = "page/textbox/textline/text"
        actual = self.highlighter.retreive_subelements_by_tag(self.highlighter.root_xml, tag_path)
        assert len(actual) == 221  # this is less than the offset, as it does not contain spaces
        assert actual[14].attrib == {
            'font': 'CIDFont+F1', 'bbox': '138.746,771.408,144.062,783.408',
            'size': '12.000', 'length': '1', 'offset': '16'}
        assert actual[14].text == 'c'
        # @TODO: assertions below belong to the refactored formats layer, i.e. format_copy
        # assert len(actual) == 265
        # assert actual[14].attrib == {'font': 'CIDFont+F1', 'bbox': '127.419,771.408,133.419,783.408',
        #                              'colourspace': 'DeviceGray', 'ncolour': '(0.0, 0.0, 0.0)', 'size': '12.000'}
        # assert actual[14].text == 'p'

    def test__get_char_bbox(self):
        char_str = ('<text font="CIDFont+F1" bbox="56.760,771.408,64.080,783.408" colourspace="DeviceGray" '
                    'ncolour="(0.0, 0.0, 0.0)" size="12.000">T</text>\n')
        char_element = etree.fromstring(char_str)
        actual = self.highlighter._get_char_bbox(char_element)
        exp_output = (56.76, 771.408, 64.08, 783.408)
        assert actual == exp_output

    def test_get_word_bbox(self):
        actual = self.highlighter.get_word_bbox(word_id='w5')
        exp_output = {'text': 'you', 'id': 'w5', 'sent': '1', 'para': '1', 'page': '1',
                      'offset': '29', 'length': '3',
                      'bbox': {'x0': 203.963, 'y0': 771.408, 'x1': 221.964, 'y1': 783.408}}
        # get bbox of character 29 and 31, here a deduction of 4 is applied due to the missing spaces.
        # In the refactored formats layer this deduction can be removed.
        exp_output_bbox_ru = self.highlighter.root_xml[0][0][0][29-4].attrib['bbox'].split(',')
        exp_output_bbox_bl = self.highlighter.root_xml[0][0][0][31-4].attrib['bbox'].split(',')
        assert actual == exp_output
        # check if bbox also corresponds with the naf xml
        assert actual['bbox']['x0'] == float(exp_output_bbox_ru[0])
        assert actual['bbox']['y1'] == float(exp_output_bbox_ru[3])
        assert actual['bbox']['y0'] == float(exp_output_bbox_bl[1])
        assert actual['bbox']['x1'] == float(exp_output_bbox_bl[2])
