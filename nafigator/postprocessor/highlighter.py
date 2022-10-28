from nafigator.nafdocument import NafDocument
import ast
import fitz
from lxml import etree
from copy import deepcopy
import logging


class Highlighter:
    def __init__(self, path_input_pdf: str, doc: NafDocument) -> None:
        """
        Initialize the Highlighter

        args
        path_input_pdf: the path of the pdf file to be highlighed. This must correspond with the doc.
        doc: the naf file

        returns
        None
        """
        # @TODO rewrite, so that filename retreived from naf is used directly, giving error if no file found
        if doc.header['fileDesc']['filename'] != path_input_pdf:
            logging.warning("The source of the naf file does not seem to correspond to the given path_input_pdf. \n"
                            "The source document registered in the naf file is "
                            f"{doc.header['fileDesc']['filename']}, \n"
                            f"while {path_input_pdf} has been passed. \n"
                            "This may lead to incorrect highlights. \n\n"
                            "Construction of the Highlighter continues...")

        self.path_input_pdf = path_input_pdf
        self.doc = doc
        self.root_xml = doc.find("formats_copy")

    def highlight_box_in_pdf(self, bbox: dict, path_highlighted_pdf: str, page_nr: int = 1,
                             origin_bl: bool = True,
                             ):
        """
        Highlights a box in a pdf file

        args
        bbox: the coordinates of the box to be highlighted
        path_highlighted_pdf: the path of the highlighted pdf file
        page_nr: page number on which to highlight the box
        page_height: height of page
        origin_bl: a boolean. specifying the origin of the coordinate system.
        If True it is bottem left, if False it is top left.

        return
        a saved pdf file with the highlighted box
        """

        page_bbox = ast.literal_eval(self.root_xml[page_nr-1].attrib['bbox'])
        page_height = page_bbox[3]

        # define coordinates
        x0 = bbox['x0']
        x1 = bbox['x1']
        if origin_bl:  # convert coordination system
            y0 = page_height - bbox['y1']
            y1 = page_height - bbox['y0']
        else:
            y0 = bbox['y0']
            y1 = bbox['y1']

        # check if realistic coordinates were passed
        if (x0 > x1) or (y0 > y1):
            logging.error("No valid coordinates or wrong coordinate system origin is passed. \n"
                          f"x0 ({x0}) can not be larger than x1 ({x1}) and \n"
                          f"y0 ({y0}) can not be larger than y1 ({y1}). \n"
                          "Also check if the right coordination system origin was passed. \n")

        doc = fitz.open(self.path_input_pdf)

        # check if passed page number is within the bound
        if page_nr > len(doc):
            logging.error(f"The passed page is out of bound. \n")
            raise IndexError(f"The document contains {len(doc)} page(s). Page {page_nr} is passed.")

        page = doc[page_nr - 1]
        rectangle = [fitz.Quad((fitz.Point(x0, y0), fitz.Point(x1, y0),
                                fitz.Point(x0, y1), fitz.Point(x1, y1)))]
        page.add_highlight_annot(rectangle)

        try:
            doc.save(path_highlighted_pdf, garbage=4, deflate=True, clean=True)
            logging.info(f"Highlighted document {path_highlighted_pdf} saved succesfully.")
        except(Exception):
            logging.warning(f"Some issue occured. Highlighted {path_highlighted_pdf} document could not be saved.")

        return None

    def retreive_subelements_by_tag(self, node: etree._Element, tag_path: str) -> etree._Element:
        """
        retreive all subelements of the same tag.

        arg
        node: an lxml tree from which the subelements are retreived
        tag_path: the tag path to the subelement to be retreived

        returns
        a lxml root with all the subelements of the same tag
        """

        # make a copy to preserve the original lxml structure
        orig_node = deepcopy(node)
        new_root = etree.Element("root")
        for element_tag in orig_node.findall(tag_path):
            new_root.append(element_tag)

        if new_root is None:
            logging.warning("None will be returned. \n"
                            f"the tag path {tag_path} has been past and may not exist.")
        return new_root

    def _get_char_bbox(self, char_element: etree._Element) -> tuple:
        """
        retreive the bbox from a character element

        args
        char_element: a character lxml element

        returns
        the bbox of the character as a tuple
        """
        char_bbox_str = char_element.attrib['bbox']
        char_bbox_tuple = ast.literal_eval(char_bbox_str)
        return char_bbox_tuple

    def get_word_bbox(self, word_id: str, page_nr: int) -> dict:

        # lookup the word
        word_position = int(word_id[1:])

        # check if word position is within bound of the document
        if (word_position > len(self.doc.text)) and self.doc.text[-1]['id']:
            logging.error(f"the word_id {word_id} is out of bound. \n"
                          "The last word id in the document is {self.doc.text[-1]['id']}. \n"
                          "Check if the right id is being used.")

        word_dict = self.doc.text[word_position - 1]

        # determine start and end of word
        word_start = int(word_dict["offset"])
        length = int(word_dict["length"])
        word_end = word_start + length - 1

        # check if passed page number is within the bound
        if page_nr > len(self.root_xml):
            logging.error(f"The passed page is out of bound. \n")
            raise IndexError(f"The document contains {len(self.root_xml)} page(s). Page {page_nr} is passed.")

        # create root chars
        page = self.root_xml[page_nr - 1]
        tag_path = "textbox/textline/text"
        root_chars = self.retreive_subelements_by_tag(page, tag_path)

        # look up bbox in root_chars
        bbox_first_char = self._get_char_bbox(root_chars[word_start])
        bbox_last_char = self._get_char_bbox(root_chars[word_end])

        # convert to word coordinates
        bbox = (bbox_first_char[0], bbox_last_char[1], bbox_last_char[2], bbox_first_char[3])

        # return word id, offset, length, bbox, word
        bbox_keys = ('x0', 'y0', 'x1', 'y1')
        bbox_dict = {bbox_keys[i]: bbox[i] for i, _ in enumerate(bbox)}
        word_dict['bbox'] = bbox_dict

        return word_dict
