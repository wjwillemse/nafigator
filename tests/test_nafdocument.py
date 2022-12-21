import unittest
import pandas as pd
import numpy as np


unittest.TestLoader.sortTestMethodsUsing = None


class TestNafDocument(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """

    def test_generate():
        '''
        This function tests whether the naf document initalization is done correctly
        input: etree._ElementTree + dict
        level: 2
        scenarios: check added features vs input
        '''

    def test_subelement():
        '''
        This function tests whether subelement is added correctly
        input: etree._ElementTree OPTIONAL: [etree._Element, tag-string, data-dict, ignore-list]
        level: 0
        scenarios: check element input and ignore list
        '''

    def test_add_processor_Element():
        '''
        This function tests whether processor element is added correctly
        input: etree._ElementTree + str + ProcessorElement
        level: 1
        scenarios: check element input and ignore list
        '''

    def test_header():
        '''
        test header output
        input: etree._ElementTree
        level: 0
        scenarios: test generated header
        '''

    def test_terms():
        '''
        test terms output
        input: etree._ElementTree
        level: 0
        scenarios: test generated terms
        '''

    def test_multiwords():
        '''
        test multiwords output
        input: etree._ElementTree
        level: 0
        scenaris: test generated multiwords
        '''

    def test_entities():
        '''
        test entities output
        input: etree._ElementTree
        level: 0
        '''

    def test_sentences():
        '''
        test sentences output
        input: etree._ElementTree
        level: 0
        scenarios: test sentences vs input
        '''

    def test_paragraphs():
        '''
        test paragraphs output
        input: etree._ElementTree
        level: 0
        scenarios: test paragraphs vs input
        '''

    def test_formats_copy():
        '''
        test formats_copy output
        input: etree._ElementTree
        level: 0
        scenarios: copy vs input
        '''

    def test_formats():
        '''
        test formats output
        input: etree._ElementTree
        level: 0
        scenarios: test formats vs input
        '''

    def test_validate():
        '''
        test validate output
        input:etree._ElementTree
        level: 1 (uses utilsfunction load_dtd)
        scenarios: check xml string
        '''

    def test_get_attributes():
        '''
        test data of attributes output
        input: etree._ElementTree + dictlike OPTIONAL = [namespace-str, exclude-list]
        level: 0
        scenarios: check attributes vs input
        '''

    def test_layer():
        '''
        test layer output
        input: etree._ElementTree + str
        level: 0
        scenarios: check layer output
        '''

    def test_add_filedesc_element():
        '''
        test added filedescription element
        input: etree._ElementTree + dict
        level: 1
        scenarios: test elements vs input
        '''

    def test_add_public_element():
        '''
        test added public element
        input: etree._ElementTree + dict
        level: 1
        scenarios: test elements vs input
        '''

    def test_add_raw_text_element():
        '''
        test added raw text element
        input: etree._ElementTree + RawElement
        level: 1
        '''

    def test_add_wf_element():
        '''
        test added wf element
        input: etree._ElementTree + wordform element + boolean
        level: 1
        scenarios: test elements vs input
        '''

    def test_add_raw_text_element():
        '''
        test added wf element
        input: etree._ElementTree + DependencyRelation + boolean
        level: 1
        scenarios: test elements vs input
        '''

    def test_add_entity_element():
        '''
        test added entity element
        input: etree._ElementTree + EntityElement + str + boolean
        level: 1
        scenarios: test elements vs input
        '''

    def test_add_term_element():
        '''
        test added term element
        input: etree._ElementTree + TermElement + str + boolean
        level: 2
        scenarios: test elements vs input
        '''

    def test_add_chunk_element():
        '''
        test added chunk element
        input: etree._ElementTree + ChunkElement + boolean
        level: 2
        scenarios: test elements vs input
        '''

    def test_add_span_element():
        '''
        test added span element
        input: etree._ElementTree + tree._ElementTree(2) + dictlike OPTIONAL [comments-boolean, naf_version str]
        level: 1
        scenarios: test elements vs input
        '''

    def test_add_external_reference_element():
        '''
        test added external reference element
        input: etree._ElementTree + tree._ElementTree(2) + list
        level: 1
        scenarios: test elements vs input
        '''

    def test_add_multiword_element():
        '''
        test added multiword element
        input: etree._ElementTree + MultiwordElement
        level: 1
        scenarios: test elements vs input
        '''

    def test_add_formats_copy_element():
        '''
        test added formats copy element
        input: etree._ElementTree + src str + formats str
        level: 0
        scenarios: test elements vs input
        '''

    def test_add_formats_element():
        '''
        test added formats element
        input: etree._ElementTree + src str + formats str + bool Optional: [camelot.core.TableList]
        level: 1
        scenarios: test elements vs input
        '''
