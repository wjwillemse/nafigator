import unittest
import pandas as pd
import numpy as np


unittest.TestLoader.sortTestMethodsUsing = None


class TestNafDocument(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """

    def test_generate(self):
        """
        This function tests whether the naf document initalization is done correctly
        input: etree._ElementTree + dict
        level: 2
        scenarios: check added features vs input
        """
        pass

    def test_subelement(self):
        """
        This function tests whether subelement is added correctly
        input: etree._ElementTree OPTIONAL: [etree._Element, tag-string, data-dict, ignore-list]
        level: 0
        scenarios: check element input and ignore list
        """
        pass

    def test_add_processor_Element(self):
        """
        This function tests whether processor element is added correctly
        input: etree._ElementTree + str + ProcessorElement
        level: 1
        scenarios: check element input and ignore list
        """
        pass

    def test_header(self):
        """
        test header output
        input: etree._ElementTree
        level: 0
        scenarios: test generated header
        """
        pass

    def test_terms(self):
        """
        test terms output
        input: etree._ElementTree
        level: 0
        scenarios: test generated terms
        """
        pass

    def test_multiwords(self):
        """
        test multiwords output
        input: etree._ElementTree
        level: 0
        scenaris: test generated multiwords
        """
        pass

    def test_entities(self):
        """
        test entities output
        input: etree._ElementTree
        level: 0
        """
        pass

    def test_sentences(self):
        """
        test sentences output
        input: etree._ElementTree
        level: 0
        scenarios: test sentences vs input
        """
        pass

    def test_paragraphs(self):
        """
        test paragraphs output
        input: etree._ElementTree
        level: 0
        scenarios: test paragraphs vs input
        """
        pass

    def test_formats_copy(self):
        """
        test formats_copy output
        input: etree._ElementTree
        level: 0
        scenarios: copy vs input
        """
        pass

    def test_formats(self):
        """
        test formats output
        input: etree._ElementTree
        level: 0
        scenarios: test formats vs input
        """
        pass

    def test_validate(self):
        """
        test validate output
        input:etree._ElementTree
        level: 1 (uses utilsfunction load_dtd)
        scenarios: check xml string
        """
        pass

    def test_get_attributes(self):
        """
        test data of attributes output
        input: etree._ElementTree + dictlike OPTIONAL = [namespace-str, exclude-list]
        level: 0
        scenarios: check attributes vs input
        """
        pass

    def test_layer(self):
        """
        test layer output
        input: etree._ElementTree + str
        level: 0
        scenarios: check layer output
        """
        pass

    def test_add_filedesc_element(self):
        """
        test added filedescription element
        input: etree._ElementTree + dict
        level: 1
        scenarios: test elements vs input
        """
        pass

    def test_add_public_element(self):
        """
        test added public element
        input: etree._ElementTree + dict
        level: 1
        scenarios: test elements vs input
        """
        pass

    def test_add_raw_text_element(self):
        """
        test added raw text element
        input: etree._ElementTree + RawElement
        level: 1
        """
        pass

    def test_add_wf_element(self):
        """
        test added wf element
        input: etree._ElementTree + wordform element + boolean
        level: 1
        scenarios: test elements vs input
        """
        pass

    def test_add_raw_text_element(self):
        """
        test added wf element
        input: etree._ElementTree + DependencyRelation + boolean
        level: 1
        scenarios: test elements vs input
        """
        pass

    def test_add_entity_element(self):
        """
        test added entity element
        input: etree._ElementTree + EntityElement + str + boolean
        level: 1
        scenarios: test elements vs input
        """
        pass

    def test_add_term_element(self):
        """
        test added term element
        input: etree._ElementTree + TermElement + str + boolean
        level: 2
        scenarios: test elements vs input
        """
        pass

    def test_add_chunk_element(self):
        """
        test added chunk element
        input: etree._ElementTree + ChunkElement + boolean
        level: 2
        scenarios: test elements vs input
        """
        pass

    def test_add_span_element(self):
        """
        test added span element
        input: etree._ElementTree + tree._ElementTree(2) + dictlike OPTIONAL [comments-boolean, naf_version str]
        level: 1
        scenarios: test elements vs input
        """
        pass

    def test_add_external_reference_element(self):
        """
        test added external reference element
        input: etree._ElementTree + tree._ElementTree(2) + list
        level: 1
        scenarios: test elements vs input
        """
        pass

    def test_add_multiword_element(self):
        """
        test added multiword element
        input: etree._ElementTree + MultiwordElement
        level: 1
        scenarios: test elements vs input
        """
        pass

    def test_add_formats_copy_element(self):
        """
        test added formats copy element
        input: etree._ElementTree + src str + formats str
        level: 0
        scenarios: test elements vs input
        """
        pass

    def test_add_formats_element(self):
        """
        test added formats element
        input: etree._ElementTree + src str + formats str + bool Optional: [camelot.core.TableList]
        level: 1
        scenarios: test elements vs input
        """
        pass
