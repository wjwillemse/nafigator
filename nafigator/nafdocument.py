# coding: utf-8

"""naf document."""

from lxml import etree

class NafDocument:

    TERMS_LAYER_TAG = "terms"
    TERM_OCCURRENCE_TAG = "term"

    def __init__(self, tree):
        self.tree = tree
        self.root = self.tree.getroot()


    def write(self, output):
        self.tree.write(output, 
                        encoding='utf-8',
                        pretty_print=True,
                        xml_declaration=True)

    def validate(self, dtd: etree.DTD):
        """
        """
        success = dtd.validate(self.root)
        if not success:
            logging.error("DTD error log:")
            for error in dtd.error_log.filter_from_errors():
                logging.error(str(error))
            return success
        return success


    def get_terms(self):
        """ Return all the words in the document"""
        terms = self.root.findall(
            "{0}/{1}".format(self.TERMS_LAYER_TAG, self.TERM_OCCURRENCE_TAG))

        return terms

    def get_term(self, termId):
        """ Get the term.
        :param termId: Id of the Term node wanted.
        """
        return self.root.xpath(
            "//{0}[@id='{1}']".format(self.TERM_OCCURRENCE_TAG, termId))[0]
