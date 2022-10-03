# -*- coding: utf-8 -*-

"""Termbase processor module.

This module contains the termbase processor classes for nafigator

"""

from .nafdocument import NafDocument
from .utils import sublist_indices
from .const import EntityElement
from lxml import etree
from collections import defaultdict

NAMESPACES = {
    None: "urn:iso:std:iso:30042:ed-2",
}

XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

def QName(prefix: str = None, name: str = None):
    """ """
    if prefix is None:
        qname = etree.QName("{urn:iso:std:iso:30042:ed-2}" + name, name)
    else:
        qname = etree.QName("{" + namespaces[prefix] + "}" + name, name)
    return qname


def normalize_term_text(term_text: str = ""):
    return term_text.lower().replace("’", "'").replace("‘", "'").replace("”", '"').replace("“", '"')


def find_term_in_text(sub, full):
    """ Faster variant than in utils.sublist_indices"""
    return [list(range(idx, idx+len(sub))) for idx in range(len(full) - len(sub) + 1) if full[idx : idx + len(sub)] == sub]

class TermbaseProcessor(object):

    def __init__(self, termbase: etree._ElementTree = None):

        if termbase is None:
            logging.info("No termbase to process.")
            return None

        self.termbase = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        for concept in termbase.findall("text/body/conceptEntry", namespaces=NAMESPACES):
            concept_id = concept.attrib["id"]
            for langSec in concept:
                if langSec.tag == QName(name="langSec"):
                    language = langSec.attrib[XML_LANG]
                    for termSec in langSec:
                        term_text = ""
                        term_type = ""
                        term_lemma = ""
                        for item in termSec:
                            if item.tag == QName(name="term"):
                                term_text = item.text
                            if item.tag == QName(name="termNote") and item.attrib['type']=='termType':
                                term_type = item.text
                            if item.tag == QName(name="termNote") and item.attrib['type']=='termLemma':
                                term_lemma = item.text
                        if term_text != "":
                            if term_lemma != "":
                                # if the lowercase lemma is available then it is used
                                key = normalize_term_text(term_lemma)
                            else:
                                # otherwise the lowercase plain text is used
                                key = normalize_term_text(term_text)
                            term_length = len(key.split(" "))
                            self.termbase[language][term_length][key].append(concept_id)

    def process(self, 
                doc: NafDocument=None,
                remove_all_existing_terms: bool=True):

        if doc is None:
            logging.info("No naf document to process termbase.")
            return None

        if remove_all_existing_terms:
            for term in doc.xpath("//entity[@type=\'Term\']"):
                term.getparent().remove(term)

        doc_word_id = {word['id']: word for word in doc.text}
        doc_terms = doc.terms
        for term in doc_terms:
            term['text'] = " ".join([doc_word_id[s['id']]['text'] for s in term['span']])

        num_entities = len(doc.entities)
        entities_data = []

        # we check terms in the document language and English
        for language in [doc.language.lower(), "en"]:

            # termbase dictionary is structured on length of terms
            for term_length in self.termbase[language].keys():

                # loop over all words in the document
                if term_length <= len(doc_terms):
                    for idx, t in enumerate(doc_terms[0:-term_length]+[doc_terms[-term_length]]):

                        # key for termbase dictionary is concatenated words
                        key = " ".join([d.get('lemma', 'text') for d in doc_terms[idx:idx+term_length]])

                        # strange lemmatization error
                        # der versicherungstechnischen Rückstellungen -> 
                        # versicherungstechnischen Rückstellungen -> 
                        if language=="de":
                            if "versicherungstechnisch" in key:
                                key = key.replace("versicherungstechnisch", "versicherungstechnische")
                        print(key)
                        ext_ref = self.termbase[language][term_length].get(key.lower(), None)
                        if  ext_ref is not None:
                            entity_data = EntityElement(
                                id="e"+str(num_entities+1),
                                type="Term", # for now we introduce a new type
                                status=None,
                                source=None,
                                span=[doc_terms[idx+s]['id'] for s in range(term_length)],
                                ext_refs=[{"reference": ref} for ref in ext_ref],
                                comment=[key],
                            )
                            num_entities += 1
                            entities_data.append(entity_data)
                        else:
                            for last_word_idx in range(2, len(doc_terms[idx+term_length-1]['lemma'])):
                                last_word = doc_terms[idx+term_length-1]['lemma'][:last_word_idx]
                                key = " ".join([d.get('lemma', 'text') for d in doc_terms[idx:idx+term_length-1]]+[doc_terms[idx+term_length-1]['lemma'][:last_word_idx]])
                                ext_ref = self.termbase[language][term_length].get(key.lower(), None)
                                if  ext_ref is not None:
                                    entity_data = EntityElement(
                                        id="e"+str(num_entities+1),
                                        type="Term", # for now we introduce a new type
                                        status=None,
                                        source=None,
                                        span=[doc_terms[idx+s]['id'] for s in range(term_length)],
                                        ext_refs=[{"reference": ref} for ref in ext_ref],
                                        comment=[key],
                                    )
                                    num_entities += 1
                                    entities_data.append(entity_data)

        for entity_data in entities_data:
            doc.add_entity_element(data = entity_data,
                                   naf_version = doc.version,
                                   comments = entity_data.comment)


def process_termbase(doc: NafDocument = None, 
                     termbase: etree._ElementTree = None, 
                     remove_all_existing_terms: bool = True,
                     params: dict = {}):
    """
    General function to add terms from a termbase to a NafDocument

    """
    if termbase is None:
        logging.info("No termbase to process.")
        return None

    if doc is None:
        logging.info("No naf document to process termbase.")
        return None

    if remove_all_existing_terms:
        for term in doc.xpath("//entity[@type=\'Term\']"):
            term.getparent().remove(term)

    doc_word_id = {word['id']: word for word in doc.text}
    doc_terms = doc.terms
    for term in doc_terms:
        term['text'] = " ".join([doc_word_id[s['id']]['text'] for s in term['span']])
    term_ids = [term['id'] for term in doc_terms]

    num_entities = len(doc.entities)
    
    entities_data = dict()
    for concept in termbase.findall("text/body/conceptEntry", namespaces=NAMESPACES):
        concept_id = concept.attrib["id"]
        for langSec in concept:
            if langSec.tag == QName(name="langSec"):
                language = langSec.attrib[XML_LANG]
                if language.lower() in [doc.language.lower(), "en"]:
                    for termSec in langSec:
                        term_text = ""
                        term_type = ""
                        term_lemma = ""
                        for item in termSec:
                            if item.tag == QName(name="term"):
                                term_text = item.text
                            if item.tag == QName(name="termNote") and item.attrib['type']=='termType':
                                term_type = item.text
                            if item.tag == QName(name="termNote") and item.attrib['type']=='termLemma':
                                term_lemma = item.text
                        if term_text != "":
                            if term_lemma != "":
                                # if the lowercase lemma is available then it is used
                                sub = normalize_term_text(term_lemma).split(" ")
                                full = [normalize_term_text(term['lemma']) for term in doc_terms]
                            else:
                                # otherwise the lowercase plain text is used
                                sub = normalize_term_text(term_text).split(" ")
                                full = [normalize_term_text(term['text']) for term in doc_terms]
                            spans = [[term_ids[i] for i in item] for item in find_term_in_text(sub, full)]

                            # spans contains all occurrences of the term in the document
                            for span in spans:
                                ext_refs = [{"reference": concept_id}]
                                if str(span) in entities_data.keys():
                                    entities_data[str(span)] = entities_data[str(span)]._replace(ext_refs=entities_data[str(span)].ext_refs+ext_refs)
                                else:
                                    entity_data = EntityElement(
                                        id="e"+str(num_entities+1),
                                        type="Term", # for now we introduce a new type
                                        status=None,
                                        source=None,
                                        span=span,
                                        ext_refs=ext_refs,
                                        comment=[term_text],
                                    )
                                    num_entities += 1
                                    entities_data[str(span)] = entity_data

    for entity_data in entities_data.values():                                
        doc.add_entity_element(data = entity_data,
                               naf_version = doc.version,
                               comments = term_text)

    return None
