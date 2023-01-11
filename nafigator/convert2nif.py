# -*- coding: utf-8 -*-

from rdflib import Graph, URIRef, Literal
import rdflib
from lxml import etree
import logging
import iribaker
import uuid
import unidecode

from .nafdocument import NafDocument
from .convert2rdf import UD2OLIA_mappings, mapobject

RDF = rdflib.namespace.RDF
RDFS = rdflib.namespace.RDFS
XSD = rdflib.namespace.XSD
DC = rdflib.namespace.DC
DCTERMS = rdflib.namespace.DCTERMS
NIF = rdflib.Namespace('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#')
NIF_ONTOLOGY = 'http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core/2.1'
OLIA = rdflib.Namespace("http://purl.org/olia/olia.owl#")
ITSRDF = rdflib.Namespace("http://www.w3.org/2005/11/its/rdf#")

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
                 uri: str=None,
                 uri_format: str=None):
        self.beginIndex = beginIndex
        self.endIndex = endIndex
        self.referenceContext = referenceContext
        self.anchorOf = anchorOf
        self.uri_format = uri_format
        if uri_format == "offsetBasedString":
            super().__init__(uri=uri+"#offset_"+str(beginIndex)+"_"+str(endIndex))
        else:
            if uri_format == "RFC5147String":
                super().__init__(uri=uri+"#char="+str(beginIndex)+","+str(endIndex))
            else:
                super().__init__(uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            if self.uri_format == "offsetBasedString":
                yield (self.uri, RDF.type, NIF.OffsetBasedString)
            elif self.uri_format == "RFC5147String":
                yield (self.uri, RDF.type, NIF.RFC5147String)
            yield (self.uri, RDF.type, NIF.String)
            if self.beginIndex is not None:
                yield (self.uri, NIF.beginIndex, Literal(self.beginIndex, datatype=XSD.nonNegativeInteger))
            if self.endIndex is not None:
                yield (self.uri, NIF.endIndex, Literal(self.endIndex, datatype=XSD.nonNegativeInteger))
            if self.referenceContext is not None:
                yield (self.uri, NIF.referenceContext, self.referenceContext.uri)
            if self.anchorOf is not None:
                yield (self.uri, NIF.anchorOf, Literal(self.anchorOf, datatype=XSD.string))
        
                lang = self.referenceContext.dublincore.get('language', "en")
                if lang == "grc":
                    yield (self.uri, NIF.anchorOf_no_accents, Literal(delete_accents(s=self.anchorOf, lang=lang), datatype=XSD.string))
                yield (self.uri, NIF.anchorOf_no_diacritics, Literal(delete_diacritics(s=self.anchorOf, lang=lang), datatype=XSD.string))


class NifContext(NifString):

    def __init__(self,
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 anchorOf: str=None,
                 isString: str=None,
                 uri_format: str=None,
                 firstSentence: str=None,
                 lastSentence: str=None,
                 uri: str=None):
        self.isString = isString
        self.firstSentence = firstSentence
        self.lastSentence = lastSentence
        self.dublincore = {}
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext, 
                         anchorOf=anchorOf, 
                         uri_format=uri_format,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Context)

            for key in self.dublincore.keys():
                if key=="uri":
                    yield (self.uri, DC.source, Literal(self.dublincore[key]))
                elif key=="language":
                    yield (self.uri, DC.language, Literal(self.dublincore[key]))
                else:
                    yield (self.uri, DCTERMS[key], Literal(self.dublincore[key]))
            yield (self.uri, DCTERMS.identifier, Literal(self.uri.split("/")[-1]))

            if self.isString is not None:
                yield (self.uri, NIF.isString, Literal(self.isString, datatype=XSD.string))
            if self.firstSentence is not None:
                yield (self.uri, NIF.firstSentence, self.firstSentence.uri)
            if self.lastSentence is not None:
                yield (self.uri, NIF.lastSentence, self.lastSentence.uri)

            for triple in super().triples():
                yield triple


class NifStructure(NifString):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 anchorOf: str=None,
                 uri_format: str=None,
                 uri: str=None):
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         uri_format=uri_format,
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
                 taIdentRef: str=None,
                 taClassRef: str=None,
                 taConfidence: float=None,
                 uri_format: str=None,
                 anchorOf: str=None,
                 entityOccurrence: bool=False,
                 termOccurrence: bool=False,
                 uri: str=None):
        self.taIdentRef = taIdentRef
        self.taClassRef = taClassRef
        self.taConfidence = taConfidence
        self.entityOccurrence = entityOccurrence
        self.termOccurrence = termOccurrence
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         uri_format=uri_format,
                         anchorOf=anchorOf,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Phrase)
            if self.entityOccurrence:
                yield (self.uri, RDF.type, NIF.entityOccurrence)
            if self.termOccurrence:
                yield (self.uri, RDF.type, NIF.termOccurrence)
            if self.taClassRef is not None:
                yield (self.uri, ITSRDF.taClassRef, URIRef(self.taClassRef))
            if self.taIdentRef is not None:
                yield (self.uri, ITSRDF.taIdentRef, URIRef(self.taIdentRef))
            if self.taConfidence is not None:
                yield (self.uri, ITSRDF.taConfidence, Literal(self.taConfidence, datatype=XSD.decimal))
            for triple in super().triples():
                yield triple


class NifSentence(NifStructure):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 uri_format: str=None,
                 anchorOf: str=None,
                 nextSentence: str=None,
                 previousSentence: str=None,
                 firstWord: str=None,
                 lastWord: str=None,
                 uri: str=None):
        self.nextSentence = nextSentence
        self.previousSentence = previousSentence
        self.firstWord = firstWord
        self.lastWord = lastWord
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         uri_format=uri_format,
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
            if self.firstWord is not None:
                yield (self.uri, NIF.firstWord, self.firstWord.uri)
            if self.lastWord is not None:
                yield (self.uri, NIF.lastWord, self.lastWord.uri)

class NifParagraph(NifStructure):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 uri_format: str=None,
                 anchorOf: str=None,
                 uri: str=None):
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         uri_format=uri_format,
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

class NifPage(NifStructure):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 uri_format: str=None,
                 anchorOf: str=None,
                 uri: str=None):
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         uri_format=uri_format,
                         anchorOf=anchorOf,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Page)
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
                 uri_format: str=None,
                 nifsentence: str=None,
                 anchorOf: str=None,
                 lemma: str=None,
                 pos: str=None,
                 morphofeats:list=[],
                 nextWord: str=None,
                 previousWord: str=None,
                 uri: str=None):
        self.nifsentence = nifsentence
        self.lemma = lemma
        self.pos = pos
        self.morphofeats = morphofeats
        self.nextWord = nextWord
        self.previousWord = previousWord
        self.dependency = []
        self.dependencyRelationType = None
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         uri_format=uri_format,
                         anchorOf=anchorOf,
                         uri=uri)

    def add_dependency(self, dependency: str=None):
        self.dependency.append(dependency)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Word)
            if self.nifsentence is not None:
                yield (self.uri, NIF.sentence, self.nifsentence.uri)
            for triple in super().triples():
                yield triple
            if self.lemma is not None:
                yield (self.uri, NIF.lemma, Literal(self.lemma, datatype=XSD.string))
                lang = self.referenceContext.dublincore.get('language', "en")
                if lang == "grc":
                    yield (self.uri, NIF.lemma_no_accents, Literal(delete_accents(s=self.lemma, lang=lang), datatype=XSD.string))
                yield (self.uri, NIF.lemma_no_diacritics, Literal(delete_diacritics(s=self.lemma, lang=lang), datatype=XSD.string))
            if self.pos is not None:
                yield (self.uri, NIF.oliaLink, OLIA[self.pos])
            if self.morphofeats is not None and self.morphofeats != []:
                for morphofeat in self.morphofeats:
                    yield (self.uri, NIF.oliaLink, OLIA[morphofeat])
            if self.nextWord is not None:
                yield (self.uri, NIF.nextWord, self.nextWord.uri)
            if self.previousWord is not None:
                yield (self.uri, NIF.previousWord, self.previousWord.uri)
            if self.dependencyRelationType is not None:
                yield (self.uri, NIF.dependencyRelationType, Literal(self.dependencyRelationType, datatype=XSD.string))
            for dep in self.dependency:
                yield (self.uri, NIF.dependency, dep.uri)

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

def delete_accents(s: str = None, lang: str = "en"):
    if lang == "grc":
        replacements = {
            'ἒ': 'ἐ', 'ἓ': 'ἑ', 'ἔ': 'ἐ', 'ἕ': 'ἑ', 'έ': 'ε', 'ὲ': 'ε', 'έ': 'ε',
            'ἂ': 'ἀ', 'ἃ': 'ἁ', 'ἄ': 'ἀ', 'ἅ': 'ἁ', 'ά': 'α', 'ὰ': 'α', 'ά': 'α',
            'ᾂ': 'ᾀ', 'ᾄ': 'ᾀ', 'ᾃ': 'ᾁ', 'ᾅ': 'ᾁ', 'ᾲ': 'ᾳ', 'ᾴ': 'ᾳ',
            'ί': 'ι', 'ἲ': 'ἰ', 'ἳ': 'ἱ', 'ἴ': 'ἰ', 'ἵ': 'ἱ', 'ῒ': 'ϊ', 'ΐ': 'ϊ', 'ὶ': 'ι', 'ί': 'ι',
            'ή': 'η', 'ἢ': 'ἠ', 'ἣ': 'ἡ', 'ἤ': 'ἠ', 'ἥ': 'ἡ', 'ὴ': 'η', 'ή': 'η',
            'ΰ': 'ϋ', 'ύ': 'υ', 'ὒ': 'ὐ', 'ὓ': 'ὑ', 'ὔ': 'ὐ', 'ὕ': 'ὑ', 'ὺ': 'υ', 'ύ': 'υ', 'ῢ': 'ϋ', 'ΰ': 'ϋ',
            'ὢ': 'ὠ', 'ὣ': 'ὡ', 'ὤ': 'ὠ', 'ὥ': 'ὡ', 'ὼ': 'ω', 'ώ': 'ω',
            'ό': 'ο', 'ὂ': 'ὀ', 'ὃ': 'ὁ', 'ὄ': 'ὀ', 'ὅ': 'ὁ', 'ὸ': 'ο', 'ό': 'ο',
            'ᾢ': 'ᾠ', 'ᾣ': 'ᾡ', 'ᾤ': 'ᾠ', 'ᾥ': 'ᾡ', 'ῲ': 'ῳ', 'ῴ': 'ῳ'
        }
        for replacement in replacements.keys():
            s = s.replace(replacement, replacements[replacement])
    else:
        s = unidecode(s)
    return s

def delete_diacritics(s: str = None, lang: str = "en"):
    if lang == "grc":
        replacements = {
            'Ά': 'Α', 'Ᾰ': 'Α', 'Ᾱ': 'Α', 'Ὰ': 'Α', 'Ά': 'Α', 'Έ': 'Ε', 'Ὲ': 'Ε', 'Έ': 'Ε', 'Ή': 'Η', 'Ὴ': 'Η', 'Ή': 'Η', 'Ί': 'Ι', 'Ϊ': 'Ι', 'Ό': 'Ο', 'Ὸ': 'Ο', 'Ό': 'Ο', 'Ύ': 'Υ', 'Ϋ': 'Υ', 'Ώ': 'Ω', 
            'ϓ': 'ϒ', 'ϔ': 'ϒ', 'Ὑ': 'ϒ', 'Ὓ': 'ϒ', 'Ὕ': 'ϒ', 'Ὗ': 'ϒ', 'Ῠ': 'ϒ', 'Ῡ': 'ϒ', 'Ὺ': 'ϒ', 'Ύ': 'ϒ', 
            'ἀ': 'α', 'ἁ': 'α', 'ἂ': 'α', 'ἃ': 'α', 'ἄ': 'α', 'ἅ': 'α', 'ἆ': 'α', 'ἇ': 'α', 'ά': 'α', 'ὰ': 'α', 'ά': 'α', 'ᾰ': 'α', 'ᾱ': 'α', 'ᾶ': 'α', 
            'Ἀ': 'Α', 'Ἁ': 'Α', 'Ἂ': 'Α', 'Ἃ': 'Α', 'Ἄ': 'Α', 'Ἅ': 'Α', 'Ἆ': 'Α', 'Ἇ': 'Α',
            'ἐ': 'ε', 'ἑ': 'ε', 'ἒ': 'ε', 'ἓ': 'ε', 'ἔ': 'ε', 'ἕ': 'ε', 'έ': 'ε', 'ὲ': 'ε', 'έ': 'ε', 
            'Ἐ': 'Ε', 'Ἑ': 'Ε', 'Ἒ': 'Ε', 'Ἓ': 'Ε', 'Ἔ': 'Ε', 'Ἕ': 'Ε',
            'ἠ': 'η', 'ἡ': 'η', 'ἢ': 'η', 'ἣ': 'η', 'ἤ': 'η', 'ἥ': 'η', 'ἦ': 'η', 'ἧ': 'η', 'ή': 'η', 'ὴ': 'η', 'ή': 'η', 'ῆ': 'η',
            'Ἠ': 'Η', 'Ἡ': 'Η', 'Ἢ': 'Η', 'Ἣ': 'Η', 'Ἤ': 'Η', 'Ἥ': 'Η', 'Ἦ': 'Η', 'Ἧ': 'Η',
            'ἰ': 'ι', 'ἱ': 'ι', 'ἲ': 'ι', 'ἳ': 'ι', 'ἴ': 'ι', 'ἵ': 'ι', 'ἶ': 'ι', 'ἷ': 'ι', 'ΐ': 'ι', 'ϊ': 'ι', 'ί': 'ι', 'ὶ': 'ι', 'ί': 'ι', 'ῐ': 'ι', 'ῑ': 'ι', 'ῒ': 'ι', 'ΐ': 'ι', 'ῖ': 'ι', 'ῗ': 'ι',
            'ΰ': 'υ', 'ϋ': 'υ', 'ύ': 'υ', 'ὐ': 'υ', 'ὑ': 'υ', 'ὒ': 'υ', 'ὓ': 'υ', 'ὔ': 'υ', 'ὕ': 'υ', 'ὖ': 'υ', 'ὗ': 'υ', 'ὺ': 'υ', 'ύ': 'υ', 'ῠ': 'υ', 'ῡ': 'υ', 'ῢ': 'υ', 'ΰ': 'υ', 'ῦ': 'υ', 'ῧ': 'υ', 
            'ό': 'ο', 'ὀ': 'ο', 'ὁ': 'ο', 'ὂ': 'ο', 'ὃ': 'ο', 'ὄ': 'ο', 'ὅ': 'ο', 'ὸ': 'ο', 'ό': 'ο',
            'ώ': 'ω', 'ὠ': 'ω', 'ὡ': 'ω', 'ὢ': 'ω', 'ὣ': 'ω', 'ὤ': 'ω', 'ὥ': 'ω', 'ὦ': 'ω', 'ὧ': 'ω', 'ὼ': 'ω', 'ώ': 'ω', 'ῶ': 'ω',
            'Ἰ': 'Ι', 'Ἱ': 'Ι', 'Ἲ': 'Ι', 'Ἳ': 'Ι', 'Ἴ': 'Ι', 'Ἵ': 'Ι', 'Ἶ': 'Ι', 'Ἷ': 'Ι', 'Ῐ': 'Ι', 'Ῑ': 'Ι', 'Ὶ': 'Ι', 'Ί': 'Ι', 
            'Ὀ': 'Ο', 'Ὁ': 'Ο', 'Ὂ': 'Ο', 'Ὃ': 'Ο', 'Ὄ': 'Ο', 'Ὅ': 'Ο', 
            'Ὠ': 'Ω', 'Ὡ': 'Ω', 'Ὢ': 'Ω', 'Ὣ': 'Ω', 'Ὤ': 'Ω', 'Ὥ': 'Ω', 'Ὦ': 'Ω', 'Ὧ': 'Ω', 
            'ᾀ': 'ᾳ', 'ᾁ': 'ᾳ', 'ᾂ': 'ᾳ', 'ᾃ': 'ᾳ', 'ᾄ': 'ᾳ', 'ᾅ': 'ᾳ', 'ᾆ': 'ᾳ', 'ᾇ': 'ᾳ', 'ᾲ': 'ᾳ', 'ᾴ': 'ᾳ', 'ᾷ': 'ᾳ',
            'ᾈ': 'ᾼ', 'ᾉ': 'ᾼ', 'ᾊ': 'ᾼ', 'ᾋ': 'ᾼ', 'ᾌ': 'ᾼ', 'ᾍ': 'ᾼ', 'ᾎ': 'ᾼ', 'ᾏ': 'ᾼ',
            'ᾐ': 'ῃ', 'ᾑ': 'ῃ', 'ᾒ': 'ῃ', 'ᾓ': 'ῃ', 'ᾔ': 'ῃ', 'ᾕ': 'ῃ', 'ᾖ': 'ῃ', 'ᾗ': 'ῃ', 'ῂ': 'ῃ', 'ῄ': 'ῃ', 'ῇ': 'ῃ',
            'ᾘ': 'ῌ', 'ᾙ': 'ῌ', 'ᾚ': 'ῌ', 'ᾛ': 'ῌ', 'ᾜ': 'ῌ', 'ᾝ': 'ῌ', 'ᾞ': 'ῌ', 'ᾟ': 'ῌ', 
            'ᾠ': 'ῳ', 'ᾡ': 'ῳ', 'ᾢ': 'ῳ', 'ᾣ': 'ῳ', 'ᾤ': 'ῳ', 'ᾥ': 'ῳ', 'ᾦ': 'ῳ', 'ᾧ': 'ῳ', 'ῲ': 'ῳ', 'ῴ': 'ῳ', 'ῷ': 'ῳ',
            'ᾨ': 'ῼ', 'ᾩ': 'ῼ', 'ᾪ': 'ῼ', 'ᾫ': 'ῼ', 'ᾬ': 'ῼ', 'ᾭ': 'ῼ', 'ᾮ': 'ῼ', 'ᾯ': 'ῼ', 
            'ῤ': 'ρ', 'ῥ': 'ρ',
            'Ῥ': 'Ρ', 
            'Ὼ': 'Ω', 'Ώ': 'Ω', 'ꭥ': 'Ω'}
        for replacement in replacements.keys():
            s = s.replace(replacement, replacements[replacement])
    else:
        s = unidecode(s)
    return s


class naf2nif(object):

    def __init__(self,
                 doc: NafDocument=None,
                 base_uri: str=None,
                 base_prefix: str=None,
                 uri_format: str="offsetBasedString"):

        self.graph = Graph()
        self.graph.bind("itsrdf", ITSRDF)
        self.graph.bind("dcterms", DCTERMS)
        self.graph.bind("dc", DC)
        self.graph.bind("nif", NIF)
        self.graph.bind("olia", OLIA)

        doc_uri = doc.header['public']['{http://purl.org/dc/elements/1.1/}uri']
        doc_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, doc_uri).hex)

        self.graph.bind(base_prefix, base_uri)

        # create nif:context
        if doc.raw is None:
            doc_raw = ""
        else:
            doc_raw = doc.raw
        nif_context = NifContext(
            beginIndex=0,
            endIndex=len(doc_raw),
            isString=doc_raw,
            uri_format=None,
            uri=base_uri+doc_uuid)
        nif_context.referenceContext = nif_context

        nif_context.dublincore = {
            "uri": doc.header['public'].get('{http://purl.org/dc/elements/1.1/}uri', ""),
            "format": doc.header['public'].get('{http://purl.org/dc/elements/1.1/}format', ""),
            "creator": doc.header['public'].get('{http://purl.org/dc/elements/1.1/}creator', ""),
            "coverage": doc.header['public'].get('{http://purl.org/dc/elements/1.1/}coverage', ""),
            "language": doc.language,
            "created": doc.header['fileDesc']['creationtime'],
            "provenance": doc.header['fileDesc']['filename']}

        # create nif:collection (containing the context)
        nif_collection = NifContextCollection(uri=base_uri+"collection")
        nif_collection.add_context(nif_context)

        # create nif:sentence and nif:word
        words = {word['id']: word for word in doc.text}
        terms = {term['id']: term for term in doc.terms}
        entities = {entity['id']: entity for entity in doc.entities}

        nif_sentences = []
        nif_words = []
        nif_terms = []
        doc_sentences = doc.sentences
        for sent_idx, sentence in enumerate(doc_sentences):
            beginIndex = int(words[sentence['span'][0]['id']]['offset'])
            endIndex = (int(words[sentence['span'][-1]['id']]['offset'])+
                       int(words[sentence['span'][-1]['id']]['length']))
            anchorOf = " ".join([words[s['id']]['text'] for s in sentence['span']])
            nif_sentence = NifSentence(
                beginIndex=beginIndex,
                endIndex=endIndex,
                referenceContext=nif_context,
                uri_format=uri_format,
                anchorOf=anchorOf,
                # annotation reference missing
                uri=base_uri+doc_uuid)
            sentence['nif'] = nif_sentence
            nif_sentences.append(nif_sentence)

            if sent_idx == 0:
                nif_context.firstSentence = nif_sentence
            if sent_idx == len(doc_sentences) - 1:
                nif_context.lastSentence = nif_sentence

            for word_idx, word_id in enumerate(sentence['span']):
                word = words[word_id['id']]
                beginIndex = int(word['offset'])
                endIndex = (int(word['offset'])+int(word['length']))
                anchorOf = word['text']
                nif_word = NifWord(
                    beginIndex=beginIndex,
                    endIndex=endIndex,
                    referenceContext=nif_context,
                    uri_format=uri_format,
                    anchorOf=anchorOf,
                    nifsentence=nif_sentence,
                    # annotation reference missing
                    uri=base_uri+doc_uuid)
                word['nif'] = nif_word
                nif_words.append(nif_word)

            # Add nextWord and previousWord
            for word_idx, word_id in enumerate(sentence['span']):
                word = words[word_id['id']]
                # add firstWord to sentence
                if word_idx == 0:
                    nif_sentence.firstWord = word['nif']
                # add lastWord to sentence
                if word_idx == len(sentence['span']) - 1:
                    nif_sentence.lastWord = word['nif']
                if word_idx < len(sentence['span']) - 1:
                    word['nif'].nextWord = words[sentence['span'][word_idx + 1]['id']]['nif']
                if word_idx > 0:
                    word['nif'].previousWord = words[sentence['span'][word_idx - 1]['id']]['nif']

            for term in sentence['terms']:
                term_words = [s['id'] for s in terms[term['id']]['span']]
                beginIndex = int(words[term_words[0]]['offset'])
                endIndex = (int(words[term_words[-1]]['offset'])+
                            int(words[term_words[-1]]['length']))
                term_lemma = terms[term['id']].get('lemma', None)
                term_pos = terms[term['id']].get('pos', None)
                term_pos = mapobject("pos", term_pos.lower()).replace("olia:", "")

                term_morphofeats = []
                morphofeats = terms[term['id']].get('morphofeat', None)
                if morphofeats is not None:
                    for feat in morphofeats.split("|"):

                        if (
                            feat.split("=")[0] in ["Foreign", "Reflex", "Poss", "Abbr"]
                            and feat.split("=")[1] == "Yes"
                        ):
                            olia_term = (feat.split("=")[0].replace("Poss", "PossessivePronoun")
                                                           .replace("Abbr", "Abbreviation")
                                                           .replace("Reflex", "ReflexivePronoun"))
                            term_morphofeats.append(olia_term)
                        else:
                            term_morphofeats.append(mapobject(feat.split("=")[0], feat.split("=")[1]).replace("olia:", ""))

                nif_term = NifWord(
                    beginIndex=beginIndex,
                    endIndex=endIndex,
                    referenceContext=nif_context,
                    uri_format=uri_format,
                    lemma=term_lemma,
                    pos=term_pos,
                    morphofeats=term_morphofeats,
                    # annotation reference missing
                    uri=base_uri+doc_uuid)
                terms[term['id']]['nif'] = nif_term
                nif_terms.append(nif_term)

        # create nif:page
        nif_pages = []
        if len(doc.text) > 0:
            page_number = int(doc.text[0]['page'])
            page_start = int(doc.text[0]['offset'])
            page_end = int(doc.text[0]['offset'])
        else:
            page_number = 1
            page_start = 0
            page_end = 0
        for word in doc.text:
            if int(word['page']) != page_number:
                nif_page = NifPage(
                    beginIndex=page_start,
                    endIndex=page_end,
                    referenceContext=nif_context,
                    uri_format=uri_format,
                    uri=base_uri+doc_uuid)
                page_start = int(word['offset'])
                page_end = int(word['offset']) + int(word['length'])
                nif_pages.append(nif_page)
                page_number += 1
            page_end = int(word['offset']) + int(word['length'])
        nif_page = NifPage(
            beginIndex=page_start,
            endIndex=page_end,
            referenceContext=nif_context,
            uri_format=uri_format,
            uri=base_uri+doc_uuid)
        nif_pages.append(nif_page)

        # add collection of sentences to nif:Context
        seq_element = rdflib.term.BNode()
        self.graph.add((nif_context.uri, NIF.hasSentences, seq_element))
        rdflib.collection.Collection(self.graph, seq_element, [sentence['nif'].uri for sentence in doc_sentences])

        # add collection of words to each nif:Sentence
        for sentence in doc_sentences:
            seq_element = rdflib.term.BNode()
            self.graph.add((sentence['nif'].uri, NIF.hasWords, seq_element))
            rdflib.collection.Collection(self.graph, seq_element, [words[word_id['id']]['nif'].uri for word_id in sentence['span']])

        # create nif:phrases
        nif_phrases = []
        for entity in doc.entities:
            taClassRef = "https://stanfordnlp.github.io/stanza#"+entity.get('type', 'unknown')
            entity_words = [ss['id'] for s in entity['span'] for ss in terms[s['id']]['span']]
            beginIndex = int(words[entity_words[0]]['offset'])
            endIndex = (int(words[entity_words[-1]]['offset'])+
                        int(words[entity_words[-1]]['length']))
            anchorOf = " ".join([words[s]['text'] for s in entity_words])
            nif_phrase = NifPhrase(
                beginIndex=beginIndex,
                endIndex=endIndex,
                referenceContext=nif_context,
                uri_format=uri_format,
                taClassRef=taClassRef,
                anchorOf=anchorOf,
                entityOccurrence=True,
                uri=base_uri+doc_uuid)
            nif_phrases.append(nif_phrase)

        # Add dependencies:
        for dep in doc.deps:
            from_term = terms[dep['from_term']]
            to_term = terms[dep['to_term']]
            rfunc = dep['rfunc']
            if "nif" in from_term.keys() and "nif" in to_term.keys():
                from_term['nif'].add_dependency(to_term['nif'])
                from_term['nif'].dependencyRelationType = rfunc
            else:
                if "nif" not in from_term.keys():
                    print("Not found:\n" + str(from_term))
                if "nif" not in to_term.keys():
                    print("Not found:\n" + str(to_term))

        # Add nextSentence and previousSentence to make graph traversable
        for sent_idx, nif_sentence in enumerate(nif_sentences):
            if sent_idx < len(nif_sentences) - 1:
                nif_sentence.nextSentence = nif_sentences[sent_idx + 1]
            if sent_idx > 0:
                nif_sentence.previousSentence = nif_sentences[sent_idx - 1]

        # create nif:paragraph
        nif_paragraphs = []
        for paragraph in doc.paragraphs:
            if paragraph['span']!=[]:
                beginIndex = int(words[paragraph['span'][0]['id']]['offset'])
                endIndex = (int(words[paragraph['span'][-1]['id']]['offset'])+
                        int(words[paragraph['span'][-1]['id']]['length']))
                anchorOf = " ".join([words[s['id']]['text'] for s in paragraph['span']])
                nif_paragraph = NifParagraph(
                    beginIndex=beginIndex,
                    endIndex=endIndex,
                    referenceContext=nif_context,
                    uri_format=uri_format,
                    # annotation reference missing
                    uri=base_uri+doc_uuid)
                nif_paragraphs.append(nif_paragraph)

        # store triples of all nif elements in graph
        for triple in nif_context.triples():
            self.graph.add(triple)

        for triple in nif_collection.triples():
            self.graph.add(triple)

        for nif_page in nif_pages:
            for triple in nif_page.triples():
                self.graph.add(triple)

        for nif_sentence in nif_sentences:
            for triple in nif_sentence.triples():
                self.graph.add(triple)

        for nif_paragraph in nif_paragraphs:
            for triple in nif_paragraph.triples():
                self.graph.add(triple)

        for nif_element in nif_words + nif_terms + nif_phrases:
            for triple in nif_element.triples():
                self.graph.add(triple)
