# coding: utf-8

"""naf document."""

from lxml import etree
from .const import ProcessorElement
from .const import DependencyRelation
from .const import WordformElement
from .const import EntityElement
from .const import TermElement
from .const import MultiwordElement
from .const import ComponentElement
from .const import ChunkElement
from .const import RawElement
from .utils import time_in_correct_format
from .utils import load_dtd_as_file_object
import datetime

# import json
import logging

FILEDESC_ELEMENT_TAG = "fileDesc"
PUBLIC_ELEMENT_TAG = "public"

TERMS_LAYER_TAG = "terms"
TERM_OCCURRENCE_TAG = "term"

DEPS_LAYER_TAG = "deps"
DEP_OCCURRENCE_TAG = "dep"

TEXT_LAYER_TAG = "text"
TEXT_OCCURRENCE_TAG = "wf"

ENTITIES_LAYER_TAG = "entities"
ENTITY_OCCURRENCE_TAG = "entity"

CHUNKS_LAYER_TAG = "chunks"
CHUNK_OCCURRENCE_TAG = "chunk"

MULTIWORDS_LAYER_TAG = "multiwords"
MULTIWORD_OCCURRENCE_TAG = "mw"

COMPONENTS_LAYER_TAG = "components"
COMPONENT_OCCURRENCE_TAG = "component"

RAW_LAYER_TAG = "raw"
FORMATS_LAYER_TAG = "formats"
NAF_HEADER = "nafHeader"

SPAN_OCCURRENCE_TAG = "span"
TARGET_OCCURRENCE_TAG = "target"

LINGUISTIC_LAYER_TAG = "linguisticProcessors"
LINGUISTIC_OCCURRENCE_TAG = "lp"

PREFIX_DC = "dc"
PREFIX_NAF_BASE = "naf-base"


def QName(prefix: str, name: str):
    # currently no namespaces used
    return name
    # qname = etree.QName('{'+namespaces[prefix]+'}'+name, name)
    # return qname


namespaces = {
    PREFIX_DC: "http://purl.org/dc/elements/1.1/",
    # PREFIX_NAF_BASE: "https://dnb.nl/naf-Base/elements/1.0/",
}


class NafDocument(etree._ElementTree):
    def generate(self, params: dict):
        self._setroot(etree.Element("NAF", nsmap=namespaces))
        self.set_version(params["naf_version"])
        self.set_language(params["language"])
        self.add_nafHeader()
        self.add_filedesc_element(params["fileDesc"])
        self.add_public_element(params["public"])

    def open(self, input):
        with open(input, "r", encoding="utf-8") as f:
            self._setroot(etree.parse(f).getroot())
        return self

    def write(self, output):
        super().write(output, encoding="utf-8", pretty_print=True, xml_declaration=True)

    def __getattr__(self, name):

        if name == "version":
            return self.getroot().get("version")

        if name == "language":
            return self.getroot().get("{http://www.w3.org/XML/1998/namespace}lang")

        if name == "header":
            header = dict()
            ling_proc = list()
            for child in self.find(NAF_HEADER):
                if child.tag == "fileDesc":
                    header["fileDesc"] = dict(child.attrib)
                if child.tag == "public":
                    header["public"] = dict(child.attrib)
                if child.tag == LINGUISTIC_LAYER_TAG:
                    header_data = dict(child.attrib)
                    lp = list()
                    for child2 in child:
                        if child2.tag == LINGUISTIC_OCCURRENCE_TAG:
                            lp.append(child2.attrib)
                    header_data["lps"] = lp
                    ling_proc.append(header_data)
            header[LINGUISTIC_LAYER_TAG] = ling_proc
            return header

        if name == "formats":
            pages = list()
            for child in self.find(FORMATS_LAYER_TAG):
                if child.tag == "page":
                    pages_data = dict(child.attrib)
                    textboxes = list()
                    for child2 in child:
                        if child2.tag == "textbox":
                            textbox_data = dict(child2.attrib)
                            textlines = list()
                            for child3 in child2:
                                if child3.tag == "textline":
                                    textline_data = dict(child3.attrib)
                                    texts = list()
                                    for child4 in child3:
                                        if child4.tag == "text":
                                            text_data = dict(child4.attrib)
                                            text_data["text"] = child4.text
                                            texts.append(text_data)
                                    textline_data["texts"] = texts
                                    textlines.append(textline_data)
                            textbox_data["textlines"] = textlines
                            textboxes.append(textbox_data)
                        # elif child2.tag == "layout":
                        elif child2.tag == "figure":
                            textbox_data = dict(child2.attrib)
                            texts = list()
                            for child3 in child2:
                                if child3.tag == "text":
                                    text_data = dict(child3.attrib)
                                    text_data["text"] = child3.text
                                    texts.append(text_data)
                            textbox_data["texts"] = texts
                            textboxes.append(textbox_data)
                    pages_data["textboxes"] = textboxes
                    pages.append(pages_data)
            return pages

        if name == "raw":
            return self.find(RAW_LAYER_TAG).text

        if name == "deps":
            return [
                dep.attrib
                for dep in self.findall(DEPS_LAYER_TAG + "/" + DEP_OCCURRENCE_TAG)
            ]
        if name == "text":
            return [
                dict({"text": wf.text}, **dict(wf.attrib))
                for wf in self.findall(TEXT_LAYER_TAG + "/" + TEXT_OCCURRENCE_TAG)
            ]

        if name == "terms":
            terms = list()
            for child in self.findall(TERMS_LAYER_TAG + "/" + TERM_OCCURRENCE_TAG):
                term_data = dict(child.attrib)
                for child2 in child:
                    if child2.tag == SPAN_OCCURRENCE_TAG:
                        targets = [
                            child3.attrib
                            for child3 in child2
                            if child3.tag == TARGET_OCCURRENCE_TAG
                        ]
                    term_data["targets"] = targets
                terms.append(term_data)
            return terms

        if name == "multiwords":
            mw = list()
            for child in self.findall(
                MULTIWORDS_LAYER_TAG + "/" + MULTIWORD_OCCURRENCE_TAG
            ):
                mw_data = dict(child.attrib)
                com = list()
                for child2 in child:
                    if child2.tag == COMPONENT_OCCURRENCE_TAG:
                        com_data = dict(child2.attrib)
                        for child3 in child2:
                            if child3.tag == SPAN_OCCURRENCE_TAG:
                                targets = [
                                    child4.attrib
                                    for child4 in child3
                                    if child4.tag == TARGET_OCCURRENCE_TAG
                                ]
                                com_data["targets"] = targets
                        com.append(com_data)
                mw_data["components"] = com
                mw.append(mw_data)
            return mw

        if name == "entities":
            entities = list()
            for child in self.findall(ENTITIES_LAYER_TAG + "/" + ENTITY_OCCURRENCE_TAG):
                entity_data = dict(child.attrib)
                for child2 in child:
                    if child2.tag == SPAN_OCCURRENCE_TAG:
                        targets = list()
                        for child3 in child2:
                            if child3.tag == TARGET_OCCURRENCE_TAG:
                                targets.append(child3.attrib)
                    entity_data["targets"] = targets
                entities.append(entity_data)
            return entities

        return super().name

    def set_language(self, language: str):
        """ """
        self.getroot().set("{http://www.w3.org/XML/1998/namespace}lang", language)

    def set_version(self, version):
        """ """
        self.getroot().set("version", version)

    def validate(self):
        """ """
        NAF_VERSION_TO_DTD = {
            "v3": load_dtd_as_file_object("data/naf_v3.dtd"),
            "v3.1": load_dtd_as_file_object("data/naf_v3_1.dtd"),
        }
        dtd = NAF_VERSION_TO_DTD[self.get_version()]
        success = dtd.validate(self.getroot())
        if not success:
            logging.error("DTD error log:")
            for error in dtd.error_log.filter_from_errors():
                logging.error(str(error))
            return success
        return success

    def tree2string(self, byte: bool = False):
        """ """
        xml_string = etree.tostring(
            self, pretty_print=True, xml_declaration=True, encoding="utf-8"
        )
        if byte:
            return xml_string
        else:
            return xml_string.decode("utf-8")

    def get_attributes(self, data, namespace=None, exclude=list()):
        """ """
        if not isinstance(data, dict):
            data = data._asdict()
        for key, value in dict(data).items():
            if value is None:
                del data[key]
            if isinstance(value, datetime.datetime):
                data[key] = time_in_correct_format(value)
            if isinstance(value, list):
                del data[key]
        if namespace:
            for key, value in dict(data).items():
                qname = etree.QName("{" + namespace + "}" + key, key)
                del data[key]
                data[qname] = value
        for key in dict(data).keys():
            if key in exclude:
                del data[key]
        return data

    def add_nafHeader(self):
        """ """
        etree.SubElement(self.getroot(), QName(PREFIX_NAF_BASE, NAF_HEADER))

    def add_filedesc_element(self, data: dict):
        """
        <!-- FILEDESC ELEMENT -->
        <!--
            <fileDesc> is an empty element containing information about the
              computer document itself. It has the following attributes:

              - title: the title of the document (optional).
              - author: the author of the document (optional).
              - creationtime: when the document was created. In ISO 8601. (optional)
              - filename: the original file name (optional).
              - filetype: the original format (PDF, HTML, DOC, etc) (optional).
              - pages: number of pages of the original document (optional).
              -->

        <!ELEMENT fileDesc EMPTY>
        <!ATTLIST fileDesc
                  title CDATA #IMPLIED
                  author CDATA #IMPLIED
                  creationtime CDATA #IMPLIED
                  filename CDATA #IMPLIED
                  filetype CDATA #IMPLIED
                  pages CDATA #IMPLIED>
        """
        naf_header = self.find(NAF_HEADER)
        filedesc_element = self.find(FILEDESC_ELEMENT_TAG)
        if filedesc_element is None:
            filedesc_element = etree.SubElement(
                naf_header,
                QName(PREFIX_NAF_BASE, FILEDESC_ELEMENT_TAG),
                self.get_attributes(data),
            )

    def add_public_element(self, data: dict):
        """
        <!-- PUBLIC ELEMENT -->
        <!--
             <public> is an empty element which stores public information about
               the document, such as its URI. It has the following attributes:

               - publicId: a public identifier (for instance, the number inserted by the capture server) (optional).
               - uri: a public URI of the document (optional).

               -->

        <!ELEMENT public EMPTY>
        <!ATTLIST public
                  publicId CDATA #IMPLIED
                  uri CDATA #IMPLIED>

        Difference to NAF: here all attributes are mapped to the Dublic Core
        """
        naf_header = self.find(NAF_HEADER)
        public_element = self.find(PUBLIC_ELEMENT_TAG)
        if public_element is None:
            public_element = etree.SubElement(
                naf_header,
                QName(PREFIX_NAF_BASE, PUBLIC_ELEMENT_TAG),
                self.get_attributes(data, "http://purl.org/dc/elements/1.1/"),
            )

    def add_processor_element(self, layer: str, data: ProcessorElement):
        """
        <!-- LINGUISTICPROCESSORS ELEMENT -->
        <!--
              <linguisticProcessors> elements store the information about which linguistic processors
                produced the NAF document. There can be several <linguisticProcessors> elements, one
                  per NAF layer. NAF layers correspond to the top-level elements of the
                  documents, such as "text", "terms", "deps" etc.

                  -->

        <!ELEMENT linguisticProcessors (lp)+>
        <!ATTLIST linguisticProcessors
                  layer CDATA #REQUIRED>

        <!-- LP ELEMENT -->
        <!--
             <lp> elements describe one specific linguistic processor. <lp> elements
                 have the following attributes:

                 - name: the name of the processor
                 - version: processor's version
                 - timestamp: a timestamp, denoting the date/time at which the processor was
                 launched. The timestamp follows the XML Schema xs:dateTime type (See
                 http://www.w3.org/TR/xmlschema-2/#isoformats). In summary, the date is
                 specified following the form "YYYY-MM-DDThh:mm:ss" (all fields
                 required). To specify a time zone, you can either enter a dateTime in UTC
                 time by adding a "Z" behind the time ("2002-05-30T09:00:00Z") or you can
                 specify an offset from the UTC time by adding a positive or negative time
                 behind the time ("2002-05-30T09:00:00+06:00").
                 - beginTimestamp (optional): a timestamp, denoting the date/time at
                 which the processor started the process. It follows the XML Schema
                 xs:dateTime format.
                 - endTimestamp (optional): a timestamp, denoting the date/time at
                 which the processor ended the process. It follows the XML Schema
                 xs:dateTime format.

                 -->

        <!ELEMENT lp EMPTY>
        <!ATTLIST lp
                  name CDATA #REQUIRED
                  version CDATA #REQUIRED
                  timestamp CDATA #IMPLIED
                  beginTimestamp CDATA #IMPLIED
                  endTimestamp CDATA #IMPLIED
                  hostname CDATA #IMPLIED>
        """
        naf_header = self.find(NAF_HEADER)
        proc = etree.SubElement(
            naf_header, QName(PREFIX_NAF_BASE, LINGUISTIC_LAYER_TAG)
        )
        proc.set("layer", layer)
        lp = etree.SubElement(
            proc,
            QName(PREFIX_NAF_BASE, LINGUISTIC_OCCURRENCE_TAG),
            self.get_attributes(data),
        )

    def add_wf_element(self, data: WordformElement, cdata: bool):
        """
        <!-- WORDFORM ELEMENT -->
        <!--
            <wf> elements describe and contain all word foorms generated after the tokenization step
              <wf> elements have the following attributes:
                - id: the id of the word form (REQUIRED and UNIQUE)
                - sent: sentence id of the word form (optional)
                - para: paragraph id of the word form (optional)
                - page: page id of the word form (optional)
                - offset: the offset (in characters) of the word form (optional)
                - length: the length (in characters) of the word form (optional)
                - xpath: in case of source xml files, the xpath expression identifying the original word form (optional)

                -->
        <!ELEMENT wf (#PCDATA|subtoken)*>
        <!ATTLIST wf
                  id ID #REQUIRED
                  sent CDATA #IMPLIED
                  para CDATA #IMPLIED
                  page CDATA #IMPLIED
                  offset CDATA #REQUIRED
                  length CDATA #REQUIRED
                  xpath CDATA #IMPLIED>
        """
        layer = self.find(TEXT_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(
                self.getroot(), QName(PREFIX_NAF_BASE, TEXT_LAYER_TAG)
            )
        wf = etree.SubElement(
            layer,
            QName(PREFIX_NAF_BASE, TEXT_OCCURRENCE_TAG),
            self.get_attributes(data, exclude=["wordform"]),
        )
        if cdata:
            wf.text = etree.CDATA(data.wordform)
        else:
            wf.text = data.wordform

    def add_raw_text_element(self, data: RawElement):
        """
        <!-- RAW ELEMENT -->
        <!ELEMENT raw (#PCDATA)>
        """
        layer = self.find(RAW_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(
                self.getroot(), QName(PREFIX_NAF_BASE, RAW_LAYER_TAG)
            )
        layer.text = data.text

    def add_dependency_element(self, data: DependencyRelation, comments: bool):
        """
        <!-- DEPS ELEMENT -->
        <!ELEMENT deps (dep)+>

        <!-- DEP ELEMENT -->
        <!--
            The <dep> elements have the following attributes:
            -   from: term id of the source element (REQUIRED)
            -   to: term id of the target element (REQUIRED)
            -   rfunc: relational function.(REQUIRED)
            -       case: declension case (optional)
          -->
        <!ELEMENT dep EMPTY>
        <!ATTLIST dep
                  from IDREF #REQUIRED
                  to IDREF #REQUIRED
                  rfunc CDATA #REQUIRED
                  case CDATA #IMPLIED>
        """
        layer = self.find(DEPS_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(
                self.getroot(), QName(PREFIX_NAF_BASE, DEPS_LAYER_TAG)
            )
        if comments:
            comment = data.rfunc + "(" + data.from_orth + "," + data.to_orth + ")"
            comment = self.prepare_comment_text(comment)
            layer.append(etree.Comment(comment))
        dep_el = etree.SubElement(
            layer, QName(PREFIX_NAF_BASE, DEP_OCCURRENCE_TAG), self.get_attributes(data)
        )

    def add_entity_element(self, data: EntityElement, naf_version: str, comments: str):
        """
        <!-- ENTITY ELEMENT -->
        <!--
            A named entity element has the following attributes:
            -   id: the id for the named entity (REQUIRED)
            -   type:  type of the named entity. (IMPLIED) Currently, 8 values are possible:
            -   Person
            -   Organization
            -   Location
            -   Date
            -   Time
            -   Money
            -   Percent
            -   Misc
          -->
        <!ELEMENT entity (span|externalReferences)+>
        <!ATTLIST entity
                  id ID #REQUIRED
                  type CDATA #IMPLIED
                  status CDATA #IMPLIED
                  source CDATA #IMPLIED>
        """
        layer = self.find(ENTITIES_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(
                self.getroot(), QName(PREFIX_NAF_BASE, ENTITIES_LAYER_TAG)
            )
        entity = etree.SubElement(
            layer,
            QName(PREFIX_NAF_BASE, ENTITY_OCCURRENCE_TAG),
            self.get_attributes(data),
        )
        self.add_span_element(
            element=entity, data=data, comments=comments, naf_version=naf_version
        )

        self.add_external_reference_element(element=entity, ext_refs=data.ext_refs)

    def add_term_element(
        self, data: TermElement, layer_to_attributes_to_ignore: dict, comments: bool
    ):
        """
        <!-- TERM ELEMENT -->
        <!--
            attributes of term elements
            id: unique identifier (REQUIRED AND UNIQUE)
            type: type of the term. (IMPLIED) Currently, 3 values are possible:
            open: open category term
            close: close category term
            lemma: lemma of the term (IMPLIED).
            pos: part of speech. (IMPLIED)
            Users are encourage to provide URIs to part of speech values to dereference these them.
            more complex pos attributes may be formed by concatenating values separated
            by a dot ".".
            morphofeat: morphosyntactic feature encoded as a single attribute.
            case: declension case of the term (optional).
            head: if the term is a compound, the id of the head component (optional).
            component_of: if the term is part of multiword, i.e., referenced by a multiwords/mw element
            than this attribute can be used to make reference to the multiword.
            compound_type: endocentric or exocentric
          -->
        <!ELEMENT term (sentiment?|span|externalReferences|component)+>
        <!ATTLIST term
                  id ID #REQUIRED
                  type CDATA #IMPLIED
                  lemma CDATA #IMPLIED
                  pos CDATA #IMPLIED
                  morphofeat CDATA #IMPLIED
                  netype CDATA #IMPLIED
                  case CDATA #IMPLIED
                  head CDATA #IMPLIED
                  component_of IDREF #IMPLIED
                  compound_type CDATA #IMPLIED>
        """
        layer = self.find(TERMS_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(
                self.getroot(), QName(PREFIX_NAF_BASE, TERMS_LAYER_TAG)
            )
        term = etree.SubElement(
            layer,
            QName(PREFIX_NAF_BASE, TERM_OCCURRENCE_TAG),
            self.get_attributes(
                data, exclude=layer_to_attributes_to_ignore.get("terms", list())
            ),
        )
        self.add_span_element(element=term, data=data, comments=comments)

        self.add_external_reference_element(element=term, ext_refs=data.ext_refs)

    def add_span_element(self, element, data, comments=False, naf_version: str = None):
        """
        <!-- SPAN ELEMENT -->
        <!ELEMENT span (target)+>
        <!ATTLIST span
                  primary CDATA #IMPLIED
                  status CDATA #IMPLIED>
        """
        if (naf_version is not None) and naf_version == "v3":
            references = etree.SubElement(element, "references")
            span = etree.SubElement(references, SPAN_OCCURRENCE_TAG)
        else:
            span = etree.SubElement(element, SPAN_OCCURRENCE_TAG)

        if comments:
            text = " ".join(data.text)
            text = self.prepare_comment_text(text)
            span.append(etree.Comment(text))

        for target in data.targets:
            target_el = etree.SubElement(span, TARGET_OCCURRENCE_TAG, {"id": target})

    def add_external_reference_element(self, element, ext_refs: list):
        """
        <!-- EXTERNALREFERENCES ELEMENT -->
        <!--
            The <externalReferences> element is used to associate terms to
            external resources, such as elements of a Knowledge base, an ontology,
            etc. It consists of several <externalRef> elements, one per
            association.
          -->
        <!ELEMENT externalReferences (externalRef)+>
        <!-- EXTERNALREF ELEMENT -->
        <!--
             <externalRef> elements have the following attributes:- resource: indicates the identifier of the resource referred to.
               - reference: code of the referred element. If the element is a
               synset of some version of WordNet, it follows the pattern:
               [a-z]{3}-[0-9]{2}-[0-9]+-[nvars]
               which is a string composed by four fields separated by a dash.
               The four fields are the following:
               - Language code (three characters).
               - WordNet version (two digits).
               - Synset identifier composed by digits.
               - POS character:
               n noun
               v verb
               a adjective
               r adverb
               examples of valid patterns are: ``ENG-20-12345678-n'',
               ``SPA-16-017403-v'', etc.
               - confidence: a floating number between 0 and 1. Indicates the confidence weight of the association
               -->
        <!ELEMENT externalRef (sentiment|externalRef)*>
        <!ATTLIST externalRef
                  resource CDATA #IMPLIED
                  reference CDATA #REQUIRED
                  reftype CDATA #IMPLIED
                  status CDATA #IMPLIED
                  source CDATA #IMPLIED
                  confidence CDATA #IMPLIED
                  timestamp CDATA #IMPLIED>
        """
        if not isinstance(ext_refs, list):
            logging.info("ext_refs should be a list of dictionaries (can be empty)")

        ext_refs_el = etree.SubElement(element, "externalReferences")
        for ext_ref in ext_refs:
            ext_ref_el = etree.SubElement(
                ext_refs_el, "externalRef", {"reference": ext_ref["reference"]}
            )
            for optional_attr in ["resource", "source", "timestamp"]:
                if optional_attr in ext_ref:
                    ext_ref_el.set(optional_attr, ext_ref[optional_attr])

    def add_chunk_element(self, data: ChunkElement, comments: bool):
        """
        <!-- CHUNKS ELEMENT -->
        <!ELEMENT chunks (chunk)+>
        <!-- CHUNK ELEMENT -->
        <!--
            The <chunk> elements have the following attributes:
            -   id: unique identifier (REQUIRED)
            -   head: the chunk head’s term id  (REQUIRED)
            -   phrase: type of the phrase (REQUIRED)
            -   case: declension case (optional)
          -->
        <!ELEMENT chunk (span)+>
        <!ATTLIST chunk
                  id ID #REQUIRED
                  head IDREF #REQUIRED
                  phrase CDATA #REQUIRED
                  case CDATA #IMPLIED>
        """
        layer = self.find(CHUNKS_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(
                self.getroot(), QName(PREFIX_NAF_BASE, CHUNKS_LAYER_TAG)
            )
        chunk = etree.SubElement(layer, CHUNK_OCCURRENCE_TAG, self.get_attributes(data))

        self.add_span_element(element=chunk, data=data, comments=comments)

    def add_formats_element(self, formats: str):

        """ """
        formats = bytes(bytearray(formats, encoding="utf-8"))
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding="utf-8")
        formats_root = etree.fromstring(formats, parser=parser)

        layer = self.find(FORMATS_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(
                self.getroot(), QName(PREFIX_NAF_BASE, FORMATS_LAYER_TAG)
            )

        def add_element(el, tag):
            c = etree.SubElement(el, tag)
            for item in el.attrib.keys():
                if item not in ["bbox", "colourspace", "ncolour"]:
                    c.attrib[item] = el.attrib[item]
            return c

        def add_text_element(el, tag, text, attrib, offset):
            text_element = etree.SubElement(el, tag)
            for item in attrib.keys():
                text_element.attrib[item] = attrib[item]
            text_element.text = text
            text_element.set("length", str(len(text)))
            text_element.set("offset", str(offset))

        def copy_dict(el2):
            return {
                item: el2.attrib[item]
                for item in el2.keys()
                if item not in ["bbox", "colourspace", "ncolour"]
            }

        offset = 0
        for page in formats_root:
            page_element = add_element(layer, "page")
            page_length = 0
            for page_item in page:

                if page_item.tag == "textbox":

                    page_item_element = add_element(page_element, page_item.tag)
                    for textline in page_item:
                        textline_element = add_element(page_item_element, textline.tag)
                        if len(textline) > 0:
                            previous_text = textline[0].text
                            previous_attrib = copy_dict(textline[0])
                            for idx, char in enumerate(textline[1:]):
                                char_attrib = copy_dict(char)

                                if previous_attrib == char_attrib:
                                    previous_text += char.text
                                    if idx == len(textline) - 1:
                                        add_text_element(
                                            textline_element,
                                            char.tag,
                                            previous_text,
                                            previous_attrib,
                                            offset,
                                        )
                                        page_length += len(previous_text)
                                        offset += len(previous_text)

                                else:  # -> previous_attrib != char_attrib

                                    add_text_element(
                                        textline_element,
                                        char.tag,
                                        previous_text,
                                        previous_attrib,
                                        offset,
                                    )
                                    page_length += len(previous_text)
                                    offset += len(previous_text)

                                    previous_text = char.text
                                    previous_attrib = char_attrib
                                    if idx == len(textline) - 1:
                                        add_text_element(
                                            textline_element,
                                            char.tag,
                                            previous_text,
                                            previous_attrib,
                                            offset,
                                        )
                                        page_length += len(previous_text)
                                        offset += len(previous_text)
                        page_length += 1
                        offset += 1

                    page_length += 1
                    offset += 1

                elif page_item.tag == "layout":
                    page_length += 1
                    offset += 1
                elif page_item.tag == "figure":
                    page_item_element = add_element(page_element, page_item.tag)
                    previous_text = textline[0].text
                    previous_attrib = copy_dict(textline[0])
                    for idx, char in enumerate(page_item):
                        if char.tag == "text":
                            char_attrib = copy_dict(char)
                            if previous_attrib == char_attrib:
                                previous_text += char.text
                                if idx == len(textline) - 1:
                                    add_text_element(
                                        page_item_element,
                                        char.tag,
                                        previous_text,
                                        previous_attrib,
                                        offset,
                                    )
                                    page_length += len(previous_text)
                                    offset += len(previous_text)
                            else:  # -> previous_attrib != char_attrib
                                add_text_element(
                                    page_item_element,
                                    char.tag,
                                    previous_text,
                                    previous_attrib,
                                    offset,
                                )
                                page_length += len(previous_text)
                                offset += len(previous_text)
                                if idx < len(textline) - 1:
                                    previous_text = char.text
                                    previous_attrib = char_attrib
                                else:
                                    add_text_element(
                                        page_item_element,
                                        char.tag,
                                        char.text,
                                        char_attrib,
                                        offset,
                                    )
                                    page_length += len(char.text)
                                    offset += len(char.text)
            page_element.set("length", str(page_length))
            page_element.set("offset", str(offset - page_length))

    def prepare_comment_text(self, text: str):
        """ """
        text = text.replace("--", "DOUBLEDASH")
        if text.endswith("-"):
            text = text[:-1] + "SINGLEDASH"
        return text

    def add_multiword_element(self, data: MultiwordElement):
        """
        <!-- MULTIWORDS ELEMENT -->
        <!ELEMENT multiwords (mw)+>

        <!-- MW ELEMENT -->
        <!--
            attributes of mw elements
            id: unique identifier (REQUIRED AND UNIQUE)
            lemma: lemma of the term (IMPLIED).
            pos: part of speech. (IMPLIED)
            morphofeat: morphosyntactic feature encoded as a single attribute. (IMPLIED)
            case: declension case (IMPLIED)
            status: manual | system | deprecated
            type: phrasal, idiom
          -->

        <!ELEMENT mw (component|externalReferences)+>
        <!ATTLIST mw
                  id ID #REQUIRED
                  lemma CDATA #IMPLIED
                  pos CDATA #IMPLIED
                  morphofeat CDATA #IMPLIED
                  case CDATA #IMPLIED
                  status CDATA #IMPLIED
                  type CDATA #REQUIRED>
        """
        layer = self.find(MULTIWORDS_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(
                self.getroot(), QName(PREFIX_NAF_BASE, MULTIWORDS_LAYER_TAG)
            )
        mw = etree.SubElement(
            layer, MULTIWORD_OCCURRENCE_TAG, self.get_attributes(data)
        )
        for component in data.components:
            com = etree.SubElement(
                mw, COMPONENT_OCCURRENCE_TAG, self.get_attributes(component)
            )
            self.add_span_element(element=com, data=component)

    def get_mws_layer(self):
        """ """
        layer = self.find("multiwords")
        if layer is None:
            layer = etree.SubElement(
                self.getroot(), QName(PREFIX_NAF_BASE, "multiwords")
            )
        return layer

    def get_next_mw_id(self):
        """ """
        layer = self.find("multiwords")
        if layer is None:
            layer = etree.SubElement(
                self.getroot(), QName(PREFIX_NAF_BASE, "multiwords")
            )
        mw_ids = [int(mw_el.get("id")[2:]) for mw_el in layer.xpath("mw")]
        if mw_ids:
            next_mw_id = max(mw_ids) + 1
        else:
            next_mw_id = 1
        return f"mw{next_mw_id}"

    def add_multi_words(self, naf_version: str, language: str):
        """
        <!-- MULTIWORDS ELEMENT -->
        <!ELEMENT multiwords (mw)+>
        <!-- MW ELEMENT -->
        <!--
            attributes of mw elements
            id: unique identifier (REQUIRED AND UNIQUE)
            lemma: lemma of the term (IMPLIED).
            pos: part of speech. (IMPLIED)
            morphofeat: morphosyntactic feature encoded as a single attribute. (IMPLIED)
            case: declension case (IMPLIED)
            status: manual | system | deprecated
            type: phrasal, idiom
          -->
        <!ELEMENT mw (component|externalReferences)+>
        <!ATTLIST mw
                  id ID #REQUIRED
                  lemma CDATA #IMPLIED
                  pos CDATA #IMPLIED
                  morphofeat CDATA #IMPLIED
                  case CDATA #IMPLIED
                  status CDATA #IMPLIED
                  type CDATA #REQUIRED>
        """

        # dictionary from tid -> term_el
        tid_to_term = {
            term.get("id"): term for term in self.getroot().xpath("terms/term")
        }

        num_of_compound_prts = 0

        # loop deps el
        for dep in self.findall(DEPS_LAYER_TAG + "/" + DEP_OCCURRENCE_TAG):

            if dep.get("rfunc") == "compound:prt":

                mws_layer = self.get_mws_layer()
                next_mw_id = self.get_next_mw_id()

                idverb = dep.get("from_term")
                idparticle = dep.get("to_term")
                num_of_compound_prts += 1

                verb_term_el = tid_to_term[idverb]
                verb = verb_term_el.get("lemma")
                verb_term_el.set("component_of", next_mw_id)

                particle_term_el = tid_to_term[idparticle]
                particle = particle_term_el.get("lemma")
                particle_term_el.set("component_of", next_mw_id)

                separable_verb_lemma = self.create_separable_verb_lemma(
                    verb, particle, language
                )
                attributes = [
                    ("id", next_mw_id),
                    ("lemma", separable_verb_lemma),
                    ("pos", "VERB"),
                    ("type", "phrasal"),
                ]

                mw_element = etree.SubElement(mws_layer, "mw", attributes)

                # add component elements
                components = [
                    (f"{next_mw_id}.c1", idverb),
                    (f"{next_mw_id}.c2", idparticle),
                ]
                for c_id, t_id in components:
                    component = etree.SubElement(
                        mw_element, "component", attrib={"id": c_id}
                    )
                    span = etree.SubElement(component, "span")
                    etree.SubElement(span, "target", attrib={"id": t_id})
