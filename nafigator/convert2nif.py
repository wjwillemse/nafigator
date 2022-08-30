# -*- coding: utf-8 -*-

from rdflib import Graph, URIRef, Literal
import rdflib
from lxml import etree
import logging
import iribaker
import uuid

from .nafdocument import NafDocument
from .convert2rdf import UD2OLIA_mappings, mapobject

RDF = rdflib.namespace.RDF
RDFS = rdflib.namespace.RDFS
XSD = rdflib.namespace.XSD
DCTERMS = rdflib.namespace.DCTERMS
NIF = rdflib.Namespace('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#')
NIF_ONTOLOGY = 'http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core/2.1'
OLIA = rdflib.Namespace("http://purl.org/olia/olia.owl#")

class NifBase(object):

    def __init__(self, uri: str=None):
        self._uri = uri

    @property
    def uri(self):
        if self._uri is not None:
            return URIRef(iribaker.to_iri(self._uri))
        else:
            return None

    def set_uri(self, uri: str=None):
        self._uri = uri

class NifString(NifBase):

    def __init__(self,
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 anchorOf: str=None,
                 offsetBasedString: bool=True,
                 uri: str=None):
        self.beginIndex = beginIndex
        self.endIndex = endIndex
        self.referenceContext = referenceContext
        self.anchorOf = anchorOf
        self.offsetBasedString = offsetBasedString
        if offsetBasedString:
            super().__init__(uri=uri+"#offset_"+str(beginIndex)+"_"+str(endIndex))
        else:
            super().__init__(uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            if self.offsetBasedString:
                yield (self.uri, RDF.type, NIF.OffsetBasedString)
            else:
                yield (self.uri, RDF.type, NIF.String)
            if self.beginIndex is not None:
                yield (self.uri, NIF.beginIndex, Literal(self.beginIndex, datatype=XSD.nonNegativeInteger))
            if self.endIndex is not None:
                yield (self.uri, NIF.endIndex, Literal(self.endIndex, datatype=XSD.nonNegativeInteger))
            if self.referenceContext is not None:
                yield (self.uri, NIF.referenceContext, self.referenceContext.uri)
            if self.anchorOf is not None:
                yield (self.uri, NIF.anchorOf, Literal(self.anchorOf, datatype=XSD.string))


class NifContext(NifString):

    def __init__(self,
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 anchorOf: str=None,
                 isString: str=None,
                 offsetBasedString: bool=True,
                 uri: str=None):
        self.isString = isString
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext, 
                         anchorOf=anchorOf, 
                         offsetBasedString=offsetBasedString,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Context)
            if self.isString is not None:
                yield (self.uri, NIF.isString, Literal(self.isString, datatype=XSD.string))
            for triple in super().triples():
                yield triple


class NifStructure(NifString):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 anchorOf: str=None,
                 offsetBasedString: bool=True,
                 uri: str=None):
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         offsetBasedString=offsetBasedString,
                         anchorOf=anchorOf,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            for triple in super().triples():
                yield triple

class NifPhrase(NifStructure):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 offsetBasedString: bool=True,
                 anchorOf: str=None,
                 uri: str=None):
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         offsetBasedString=offsetBasedString,
                         anchorOf=anchorOf,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Phrase)
            for triple in super().triples():
                yield triple


class NifSentence(NifStructure):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 offsetBasedString: bool=True,
                 anchorOf: str=None,
                 nextSentence: str=None,
                 previousSentence: str=None,
                 uri: str=None):
        self.nextSentence = nextSentence
        self.previousSentence = previousSentence
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         offsetBasedString=offsetBasedString,
                         anchorOf=anchorOf,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Sentence)
            for triple in super().triples():
                yield triple
            if self.nextSentence is not None:
                yield (self.uri, NIF.nextSentence, self.nextSentence.uri)
            if self.previousSentence is not None:
                yield (self.uri, NIF.previousSentence, self.previousSentence.uri)

class NifParagraph(NifStructure):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 offsetBasedString: bool=True,
                 anchorOf: str=None,
                 uri: str=None):
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         offsetBasedString=offsetBasedString,
                         anchorOf=anchorOf,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Paragraph)
            for triple in super().triples():
                yield triple

# class NifTitle(NifStructure):

#     def __init__(self, uri: str=None):
#         super().__init__(uri)

class NifWord(NifStructure):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 offsetBasedString: bool=True,
                 nifSentence: str=None,
                 anchorOf: str=None,
                 lemma: str=None,
                 pos: str=None,
                 morphofeat:str=None,
                 nextWord: str=None,
                 previousWord: str=None,
                 uri: str=None):
        self.nifSentence = nifSentence
        self.lemma = lemma
        self.pos = pos
        self.morphofeat = morphofeat
        self.nextWord = nextWord
        self.previousWord = previousWord
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         offsetBasedString=offsetBasedString,
                         anchorOf=anchorOf,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Word)
            if self.nifSentence is not None:
                yield (self.uri, NIF.Sentence, self.nifSentence.uri)
            for triple in super().triples():
                yield triple
            if self.lemma is not None:
                yield (self.uri, NIF.lemma, Literal(self.lemma, datatype=XSD.string))
            if self.pos is not None:
                yield (self.uri, NIF.oliaLink, OLIA[self.pos])
            if self.morphofeat is not None:
                yield (self.uri, NIF.morphofeat, Literal(self.morphofeat, datatype=XSD.string))
            if self.nextWord is not None:
                yield (self.uri, NIF.nextWord, self.nextWord.uri)
            if self.previousWord is not None:
                yield (self.uri, NIF.previousWord, self.previousWord.uri)

class NifContextCollection(NifBase):

    def __init__(self,
                 hasContext: list=[],
                 uri: str=None):
        self.hasContext = hasContext
        super().__init__(uri)

    def add_context(self, context: NifContext=None):
        if context is not None:
            self.hasContext.append(context)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.ContextCollection)
            yield (self.uri, DCTERMS.conformsTo, URIRef(NIF_ONTOLOGY))
            for context in self.hasContext:
                yield (self.uri, NIF.hasContext, context.uri)

class naf2nif(object):

    def __init__(self,
                 uri: str=None,
                 collection_uri: str=None,
                 doc: NafDocument=None):
        self.graph = Graph()
        self.graph.bind("nif", NIF)
        self.graph.bind("olia", "http://purl.org/olia/olia.owl#")

        doc_uri = doc.header['public']['{http://purl.org/dc/elements/1.1/}uri']

        doc_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, doc_uri))

        nif_context = NifContext(beginIndex=0,
                       endIndex=len(doc.raw),
                       isString=doc.raw,
                       offsetBasedString=False,
                       uri=uri+"/"+doc_uuid)
        nif_context.referenceContext = nif_context

        nif_collection = NifContextCollection(uri=collection_uri)
        nif_collection.add_context(nif_context)

        words = {word['id']: word for word in doc.text}
        terms = {term['id']: term for term in doc.terms}

        nif_sentences = []
        nif_words = []
        nif_terms = []
        for sentence in doc.sentences:
            beginIndex = int(words[sentence['span'][0]['id']]['offset'])
            endIndex = (int(words[sentence['span'][-1]['id']]['offset'])+
                       int(words[sentence['span'][-1]['id']]['length']))
            anchorOf = " ".join([words[s['id']]['text'] for s in sentence['span']])
            nif_sentence = NifSentence(beginIndex=beginIndex,
                                       endIndex=endIndex,
                                       referenceContext=nif_context,
                                       offsetBasedString=True,
                                       anchorOf=anchorOf,
                                       # annotation reference missing
                                       uri=uri+"/"+doc_uuid)
            sentence['nif'] = nif_sentence
            nif_sentences.append(nif_sentence)

            for word_id in sentence['span']:
                word = words[word_id['id']]
                beginIndex = int(word['offset'])
                endIndex = (int(word['offset'])+int(word['length']))
                anchorOf = word['text']
                nif_word = NifWord(beginIndex=beginIndex,
                                   endIndex=endIndex,
                                   referenceContext=nif_context,
                                   offsetBasedString=True,
                                   anchorOf=anchorOf,
                                   nifSentence=nif_sentence,
                                   # annotation reference missing
                                   uri=uri+"/"+doc_uuid)
                word['nif'] = nif_word
                nif_words.append(nif_word)

            # Add nextWord and previousWord to make graph traversable
            for idx, word_id in enumerate(sentence['span']):
                word = words[word_id['id']]
                if idx < len(sentence['span']) - 1:
                    word['nif'].nextWord = words[sentence['span'][idx + 1]['id']]['nif']
                if idx > 0:
                    word['nif'].previousWord = words[sentence['span'][idx - 1]['id']]['nif']

            for term in sentence['terms']:
                term_words = [s['id'] for s in terms[term['id']]['span']]
                beginIndex = int(words[term_words[0]]['offset'])
                endIndex = (int(words[term_words[-1]]['offset'])+
                            int(words[term_words[-1]]['length']))
                term_lemma = terms[term['id']].get('lemma', None)
                term_pos = terms[term['id']].get('pos', None)
                term_pos = mapobject("pos", term_pos.lower()).replace("olia:", "")
                term_morphofeat = terms[term['id']].get('morphofeat', None)
                nif_term = NifWord(beginIndex=beginIndex,
                                   endIndex=endIndex,
                                   offsetBasedString=True,
                                   lemma=term_lemma,
                                   pos=term_pos,
                                   morphofeat=term_morphofeat,
                                   # annotation reference missing
                                   uri=uri+"/"+doc_uuid)
                terms[term['id']]['nif'] = nif_term
                nif_terms.append(nif_term)

        # Add nextSentence and previousSentence to make graph traversable
        for idx, nif_sentence in enumerate(nif_sentences):
            if idx < len(nif_sentences) - 1:
                nif_sentence.nextSentence = nif_sentences[idx + 1]
            if idx > 0:
                nif_sentence.previousSentence = nif_sentences[idx - 1]

        nif_paragraphs = []
        for paragraph in doc.paragraphs:
            beginIndex = int(words[paragraph['span'][0]['id']]['offset'])
            endIndex = (int(words[paragraph['span'][-1]['id']]['offset'])+
                       int(words[paragraph['span'][-1]['id']]['length']))
            anchorOf = " ".join([words[s['id']]['text'] for s in paragraph['span']])
            nif_paragraph = NifParagraph(beginIndex=beginIndex,
                                         endIndex=endIndex,
                                         referenceContext=nif_context,
                                         offsetBasedString=True,
                                         anchorOf=anchorOf,
                                         # annotation reference missing
                                         uri=uri+"/"+doc_uuid)
            nif_paragraphs.append(nif_paragraph)

        for triple in nif_context.triples():
            self.graph.add(triple)

        for triple in nif_collection.triples():
            self.graph.add(triple)

        for nif_sentence in nif_sentences:
            for triple in nif_sentence.triples():
                self.graph.add(triple)

        for nif_paragraph in nif_paragraphs:
            for triple in nif_paragraph.triples():
                self.graph.add(triple)

        for nif_word in nif_words + nif_terms:
            for triple in nif_word.triples():
                self.graph.add(triple)

#         lemon_header = LemonHeader(uri=uri+'/header',
#                                    dct_type=dct_type,
#                                    tbx_sourcedesc=tbx_sourcedesc)

#         languages = set()

#         lemon_concepts = list()
#         lemon_entries = list()
#         lemon_lexicons = dict()
#         for concept in termbase.findall("text/body/conceptEntry", namespaces=NAMESPACES):

#             concept_id = concept.attrib["id"]

#             if "http" not in concept_id:

#                 subjectField = None
#                 for element in concept:
#                     if element.tag==QName(name="descrip") and element.attrib.get("type", "")=="subjectField":
#                         subjectField = element.text

#                 lemon_concepts.append(LemonConcept(uri=uri+"/"+concept_id,
#                                                    subjectField=subjectField))

#                 references = []
#                 for element in concept:
#                     if element.tag==QName(name="ref"):
#                         if element.attrib.get("match")=="fullMatch":
#                             references.append(element.text)

#                 for langSec in concept:
#                     if langSec.tag==QName(name="langSec"):
#                         lang = langSec.attrib.get(XML_LANG, None)

#                         if lang not in lemon_lexicons.keys():
#                             lemon_lexicons[lang] = LemonLexicon(uri=uri+"/lexicon/"+lang, language=lang)

#                         for termSec in langSec:

#                             lexicalEntry = LemonLexicalEntry(lexicon=lemon_lexicons[lang])

#                             # set references for lexical senses
#                             lexicalEntry.references = [uri+"/"+concept_id] + references

#                             for element in termSec:
#                                 if element.tag==QName(name="term"):
#                                     lemon_entry_uri = uri+"/"+"+".join(element.text.split(" "))+"-"+lang
#                                     lexicalEntry.set_uri(lemon_entry_uri)
#                                     lexicalEntry.term = element.text
#                                 elif element.tag==QName(name="termNote"):
#                                     termnote_type = element.attrib.get("type", None)
#                                     if termnote_type=="termType":
#                                         lexicalEntry.termType = element.text
#                                     elif termnote_type=="termLemma":
#                                         lexicalEntry.termLemma = element.text
#                                     elif termnote_type=="partOfSpeech":
#                                         lexicalEntry.partOfSpeech = element.text
#                                     # administrativeStatus not yet done
#                                 elif element.tag==QName(name="descrip"):
#                                     descrip_type = element.attrib.get("type", None)
#                                     if descrip_type=="reliabilityCode":
#                                         lexicalEntry.reliabilityCode = element.text
#                                     else:
#                                         logging.warning("descrip type not found: " + descrip_type)
#                                 else:
#                                     logging.warning("termSec element not found: " + element.tag)
#                             lemon_entries.append(lexicalEntry)

#                             components = lexicalEntry.term.split(" ")
#                             if len(components) > 1:
#                                 component_list = LemonComponentList(
#                                     # uri=lexicalEntry.uri+"#ComponentList",
#                                     uri=lexicalEntry.uri,
#                                     lexicalEntry=lexicalEntry)
#                                 for idx, component in enumerate(components):
#                                     component_lexicalEntry = LemonLexicalEntry(
#                                         uri=uri+"/"+component+"-"+lang,
#                                         lexicon=lemon_lexicons[lang],
#                                         term=component,
#                                         partOfSpeech=lexicalEntry.partOfSpeech.split(", ")[idx] if lexicalEntry.partOfSpeech is not None else None)
#                                     lemon_component = LemonComponent(
#                                         uri=lexicalEntry.uri+"#component"+str(idx+1),
#                                         term=component,
#                                         lexicalEntry=component_lexicalEntry)
#                                     component_list.components.append(lemon_component)
#                                 lemon_entries.append(component_list)
#                     elif langSec.tag not in [QName(name="descrip"), QName(name="ref")]:
#                         logging.warning("conceptEntry element not found: " + langSec.tag)


#         for triple in lemon_header.triples():
#             self.graph.add(triple)

#         for lexicon in lemon_lexicons.values():
#             for triple in lexicon.triples():
#                 self.graph.add(triple)

#         for concept in lemon_concepts:
#             for triple in concept.triples():
#                 self.graph.add(triple)

#         for entry in lemon_entries:
#             for triple in entry.triples():
#                 self.graph.add(triple)

#         # to do: abbreviations
