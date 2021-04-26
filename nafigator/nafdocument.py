# coding: utf-8

"""naf document."""

from lxml import etree
from .const import DependencyRelation
from .const import WordformElement
from .const import EntityElement
from .const import TermElement
from .const import ChunkElement
from .utils import time_in_correct_format
from .utils import load_dtd_as_file_object
# import json
import logging

FILEDESC_LAYER_TAG = "fileDesc"
PUBLIC_LAYER_TAG = "public"

TERMS_LAYER_TAG = "terms"
TERM_OCCURRENCE_TAG = "term"

DEPS_LAYER_TAG = "deps"
DEP_OCCURENCE_TAG = "dep"

TEXT_LAYER_TAG = "text"
TEXT_OCCURENCE_TAG = "wf"

ENTITIES_LAYER_TAG = "entities"
ENTITY_OCCURENCE_TAG = "entity"

CHUNKS_LAYER_TAG = "chunks"
CHUNK_OCCURENCE_TAG = "chunk"

RAW_LAYER_TAG = "raw"
FORMATS_LAYER_TAG = "formats"
NAF_HEADER = "nafHeader"

SPAN_OCCURRENCE_TAG = "span"
TARGET_OCCURENCE_TAG = "target"

PREPROCESSOR_LAYER_TAG = "preProcessors"
PREPROCESSOR_OCCURENCE_TAG = "pp"

LINGUISTIC_LAYER_TAG = "linguisticProcessors"
LINGUISTIC_OCCURENCE_TAG = "lp"

PREFIX_DC = "dc"
PREFIX_NAF_BASE = "naf-base"


def QName(prefix: str, name: str):
    return name
    # qname = etree.QName('{'+namespaces[prefix]+'}'+name, name)
    # return qname


class NafDocument:

    def __init__(self, params: dict):

        self.namespaces = {PREFIX_DC: "http://purl.org/dc/elements/1.1/",
                           PREFIX_NAF_BASE: "https://dnb.nl/naf-Base/elements/1.0/"}

        uri = params['public']['uri']
        if uri[-3:].lower() == 'naf':
            with open(uri, "r", encoding='utf-8') as f:
                self.tree = etree.parse(f)
            self.root = self.tree.getroot()
            self.naf_version = self.root.get("version")
            self.language = self.root.get('{http://www.w3.org/XML/1998/namespace}lang')
        else:
            self.tree = etree.ElementTree()
            self.root = etree.Element("NAF", nsmap=self.namespaces)
            self.tree._setroot(self.root)
            self.engine = params['engine']

            self.naf_version = params['naf_version']
            self.root.set('version', self.naf_version)

            self.language = params['language']
            self.root.set('{http://www.w3.org/XML/1998/namespace}lang', self.language)

            etree.SubElement(self.root, QName(PREFIX_NAF_BASE, NAF_HEADER))

            self.add_filedesc_data(params.get('fileDesc', None))
            self.add_public_data(params.get('public', None))
            self.add_preprocess_data(params.get('preprocess_layers', None), params)
            self.add_linguistic_data(params.get('linguistic_layers', None), params)

    def __getattr__(self, name):

        if name == "nafHeader":
            header = dict()
            prep_proc = list()
            ling_proc = list()
            for child in self.root.find(NAF_HEADER):
                if child.tag == "fileDesc":
                    header_data = dict(child.attrib)
                    header['fileDesc'] = header_data
                if child.tag == "public":
                    header_data = dict(child.attrib)
                    header['public'] = header_data
                if child.tag == PREPROCESSOR_LAYER_TAG:
                    header_data = dict(child.attrib)
                    pp = list()
                    for child2 in child:
                        if child2.tag == PREPROCESSOR_OCCURENCE_TAG:
                            pp.append(child2.attrib)
                    header_data['pp'] = pp
                    prep_proc.append(header_data)
                if child.tag == LINGUISTIC_LAYER_TAG:
                    header_data = dict(child.attrib)
                    lp = list()
                    for child2 in child:
                        if child2.tag == LINGUISTIC_OCCURENCE_TAG:
                            lp.append(child2.attrib)
                    header_data['lps'] = lp
                    ling_proc.append(header_data)
            header[PREPROCESSOR_LAYER_TAG] = prep_proc
            header[LINGUISTIC_LAYER_TAG] = ling_proc
            return header

        if name == "formats_layer":
            pages = list()
            for child in self.root.find(FORMATS_LAYER_TAG):
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
                                            text_data['text'] = child4.text
                                            texts.append(text_data)
                                    textline_data['texts'] = texts
                                    textlines.append(textline_data)
                            textbox_data['textlines'] = textlines
                            textboxes.append(textbox_data)
                        # elif child2.tag == "layout":
                        elif child2.tag == "figure":
                            textbox_data = dict(child2.attrib)
                            texts = list()
                            for child3 in child2:
                                if child3.tag == "text":
                                    text_data = dict(child3.attrib)
                                    text_data['text'] = child3.text
                                    texts.append(text_data)
                            textbox_data['texts'] = texts
                            textboxes.append(textbox_data)
                    pages_data['textboxes'] = textboxes
                    pages.append(pages_data)
            return pages


        # if raw_layer is requested return text
        if name == "raw_layer":
            return self.root.find(RAW_LAYER_TAG).text

        # if deps_layer is requested return list of deps
        if name == "deps_layer":
            deps = list()
            for child in self.root.find(DEPS_LAYER_TAG):
                if child.tag == DEP_OCCURENCE_TAG:
                    dep_data = dict(child.attrib)
                    deps.append(dep_data)
            return deps

        # if text_layer is requested return list of wfs
        if name == "text_layer":
            wfs = list()
            for child in self.root.find(TEXT_LAYER_TAG):
                if child.tag == TEXT_OCCURENCE_TAG:
                    wf_data = dict({"text": child.text}, **dict(child.attrib))
                    wfs.append(wf_data)
            return wfs

        if name == "terms_layer":
            terms = list()
            for child in self.root.find(TERMS_LAYER_TAG):
                if child.tag == TERM_OCCURRENCE_TAG:
                    term_data = dict(child.attrib)
                    for child2 in child:
                        if child2.tag == SPAN_OCCURRENCE_TAG:
                            targets = list()
                            for child3 in child2:
                                if child3.tag == TARGET_OCCURENCE_TAG:
                                    targets.append(child3.attrib.get("id", None))
                        term_data['targets'] = targets
                    terms.append(term_data)
            return terms

        if name == "entities_layer":
            entities = list()
            for child in self.root.find(ENTITIES_LAYER_TAG):
                if child.tag == ENTITY_OCCURENCE_TAG:
                    entity_data = dict(child.attrib)
                    for child2 in child:
                        if child2.tag == SPAN_OCCURRENCE_TAG:
                            targets = list()
                            for child3 in child2:
                                if child3.tag == TARGET_OCCURENCE_TAG:
                                    targets.append(child3.attrib.get("id", None))
                        entity_data['targets'] = targets
                    entities.append(entity_data)
            return entities

        raise("Error: "+name+" not available.")

    def write(self, output, output_type):
        self.tree.write(output,
                        encoding='utf-8',
                        pretty_print=True,
                        xml_declaration=True)
        # if output_type == 'json':
        #     with open(output) as xml_file:
        #         data_dict = xmltodict.parse(xml_file.read())
        #         xml_file.close()
        #     json_data = json.dumps(data_dict)
        #     with open(output, "w") as json_file:
        #         json_file.write(json_data)
        #         json_file.close()

    def validate(self):
        """
        """

        NAF_VERSION_TO_DTD = {
            'v3': load_dtd_as_file_object('data/naf_v3.dtd'),
            'v3.1': load_dtd_as_file_object('data/naf_v3_1.dtd')}

        dtd = NAF_VERSION_TO_DTD[self.naf_version]

        success = dtd.validate(self.root)
        if not success:
            logging.error("DTD error log:")
            for error in dtd.error_log.filter_from_errors():
                logging.error(str(error))
            return success
        return success

    def tree2string(self,
                    byte: bool = False):
        """
        """
        xml_string = etree.tostring(self.tree,
                                    pretty_print=True,
                                    xml_declaration=True,
                                    encoding='utf-8')
        if byte:
            return xml_string
        else:
            return xml_string.decode('utf-8')

    def add_filedesc_data(self,
                          filedesc_data: dict):
        """
        """
        naf_header = self.root.find(NAF_HEADER)
        filedesc_layer = self.root.find(FILEDESC_LAYER_TAG)
        if filedesc_layer is None:
            filedesc_layer = etree.SubElement(naf_header, QName(PREFIX_NAF_BASE, FILEDESC_LAYER_TAG))
        for key in filedesc_data.keys():
            if key == 'creationtime':
                filedesc_layer.set(key, time_in_correct_format(filedesc_data['creationtime']))
            else:
                if filedesc_data[key] is not None:
                    filedesc_layer.set(key, str(filedesc_data[key]))

    def add_public_data(self,
                        public_data: dict):
        """
        """
        naf_header = self.root.find(NAF_HEADER)
        public_layer = self.root.find(PUBLIC_LAYER_TAG)
        if public_layer is None:
            public_layer = etree.SubElement(naf_header, QName(PREFIX_NAF_BASE, PUBLIC_LAYER_TAG))
        for key in public_data.keys():
            qname = etree.QName('{http://purl.org/dc/elements/1.1/}'+key, key)
            public_layer.set(qname, public_data[key])

    def add_preprocess_data(self,
                            preprocess_layers: dict,
                            params: dict):
        """
        """
        if preprocess_layers is not None:
            for layer in preprocess_layers:
                self.add_preprocessors(layer, params)

    def add_preprocessors(self,
                          layer: str,
                          params: dict):
        """
        """
        naf_header = self.root.find(NAF_HEADER)
        proc = etree.SubElement(naf_header, QName(PREFIX_NAF_BASE, PREPROCESSOR_LAYER_TAG))
        proc.set("layer", layer)
        pp = etree.SubElement(proc, QName(PREFIX_NAF_BASE, PREPROCESSOR_OCCURENCE_TAG))
        pp.set("beginTimestamp", time_in_correct_format(params['preprocess_start_time']))
        pp.set('endTimestamp', time_in_correct_format(params['preprocess_end_time']))
        pp.set('name', params['preprocess_name'])
        if params['preprocess_version'] is not None:
            pp.set('version', params['preprocess_version'])

    def add_linguistic_data(self,
                            linguistic_layers: dict,
                            params: dict):
        """
        """
        if params['add_mws']:
            linguistic_layers.append('multiwords')
        if linguistic_layers is not None:
            for layer in linguistic_layers:
                self.add_linguistic_processors(layer, params)

    def add_linguistic_processors(self,
                                  layer: str,
                                  params: dict):
        """
        """
        naf_header = self.root.find(NAF_HEADER)
        ling_proc = etree.SubElement(naf_header, QName(PREFIX_NAF_BASE, LINGUISTIC_LAYER_TAG))
        ling_proc.set("layer", layer)
        lp = etree.SubElement(ling_proc, QName(PREFIX_NAF_BASE, LINGUISTIC_OCCURENCE_TAG))
        lp.set("beginTimestamp", time_in_correct_format(params['start_time']))
        lp.set('endTimestamp', time_in_correct_format(params['end_time']))
        lp.set('name', self.engine.model_name)
        lp.set('version', self.engine.model_version)

    def prepare_comment_text(self, text: str):
        """
        """
        text = text.replace('--', 'DOUBLEDASH')
        if text.endswith('-'):
            text = text[:-1] + 'SINGLEDASH'
        return text

    def get_mws_layer(self):
        """
        """
        mws_layer = self.root.find('multiwords')
        if mws_layer is None:
            mws_layer = etree.SubElement(self.root, 'multiwords')
        return mws_layer

    def get_next_mw_id(self):
        """
        """
        mws_layer = self.get_mws_layer(self.root)
        mw_ids = [int(mw_el.get('id')[2:])
                  for mw_el in mws_layer.xpath('mw')]
        if mw_ids:
            next_mw_id = max(mw_ids) + 1
        else:
            next_mw_id = 1
        return f'mw{next_mw_id}'

    def add_multi_words(self,
                        naf_version: str,
                        language: str):
        """
        """
        if naf_version == 'v3':
            logging.info('add_multi_words function only applies to naf version 4')

        supported_languages = {'nl', 'en'}
        if language not in supported_languages:
            logging.info(f'add_multi_words function only implemented for {supported_languages}, not for supplied {language}')

        # dictionary from tid -> term_el
        tid_to_term = {term_el.get('id'): term_el
                       for term_el in self.root.xpath('terms/term')}

        num_of_compound_prts = 0

        # loop deps el
        for dep in self.root.findall('deps/dep'):

            if dep.get('rfunc') == 'compound:prt':

                mws_layer = self.get_mws_layer()
                next_mw_id = self.get_next_mw_id()

                idverb = dep.get('from')
                idparticle = dep.get('to')
                num_of_compound_prts += 1

                verb_term_el = tid_to_term[idverb]
                verb = verb_term_el.get('lemma')
                verb_term_el.set('component_of', next_mw_id)

                particle_term_el = tid_to_term[idparticle]
                particle = particle_term_el.get('lemma')
                particle_term_el.set('component_of', next_mw_id)

                separable_verb_lemma = self.create_separable_verb_lemma(verb,
                                                                        particle,
                                                                        language)
                attributes = [('id', next_mw_id),
                              ('lemma', separable_verb_lemma),
                              ('pos', 'VERB'),
                              ('type', 'phrasal')]

                mw_element = etree.SubElement(mws_layer, 'mw')
                for attr, value in attributes:
                    mw_element.set(attr, value)

                # add component elements
                components = [
                    (f'{next_mw_id}.c1', idverb),
                    (f'{next_mw_id}.c2', idparticle)
                ]
                for c_id, t_id in components:
                    component = etree.SubElement(mw_element,
                                                 'component',
                                                 attrib={'id': c_id})
                    span = etree.SubElement(component, 'span')
                    etree.SubElement(span,
                                     'target',
                                     attrib={'id': t_id})

    def create_separable_verb_lemma(verb, particle, language):
        """
        """
        if language == 'nl':
            lemma = particle+verb
        if language == 'en':
            lemma = f'{verb}_{particle}'
        return lemma

    def add_wf_element(self,
                       data: WordformElement,
                       cdata: bool):
        """
        """
        layer = self.root.find(TEXT_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(self.root, 
                                     QName(PREFIX_NAF_BASE, 
                                           TEXT_LAYER_TAG))
        wf_attrib = dict()
        if data.page != 0:
            wf_attrib["page"] = data.page
        if data.sent != 0:
            wf_attrib["sent"] = data.sent
        wf_attrib["id"] = data.id
        wf_attrib["length"] = data.length
        wf_attrib["offset"] = data.offset
        wf = etree.SubElement(layer,
                              QName(PREFIX_NAF_BASE, 
                                    TEXT_OCCURENCE_TAG),
                              wf_attrib)
        if cdata:
            wf.text = etree.CDATA(data.wordform)
        else:
            wf.text = data.wordform

    def add_raw_text_element(self,
                             cdata: bool):
        """
        """
        layer = self.root.find(RAW_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(self.root, 
                                     QName(PREFIX_NAF_BASE, 
                                           RAW_LAYER_TAG))
        wfs = self.root.findall(TEXT_LAYER_TAG+'/wf')
        tokens = [wfs[0].text]
        for prev_wf, cur_wf in zip(wfs[:-1], wfs[1:]):
            prev_start = int(prev_wf.get('offset'))
            prev_end = prev_start + int(prev_wf.get('length'))
            cur_start = int(cur_wf.get('offset'))
            delta = cur_start - prev_end  # how many characters are between current token and previous token?
            # no chars between two token (for example with a dot .)
            if delta == 0:
                trailing_chars = ''
            elif delta >= 1:
                # 1 or more characters between tokens -> n spaces added
                trailing_chars = ' '*delta
            elif delta < 0:
                raise AssertionError(f'please check the offsets of {prev_wf.text} and {cur_wf.text} (delta of {delta})')
            tokens.append(trailing_chars + cur_wf.text)
        raw_text = ''.join(tokens)
        if cdata:
            layer.text = etree.CDATA(raw_text)
        else:
            layer.text = raw_text
        # verify alignment between raw and token layer
        for wf in self.root.xpath('text/wf'):
            start = int(wf.get('offset'))
            end = start + int(wf.get('length'))
            token = layer.text[start:end]
            assert wf.text == token, f'mismatch in alignment of wf element {wf.text} ({wf.get("id")}) with raw layer (expected length {wf.get("length")}'

    def add_formats_element(self, formats: str):

        """
        """
        formats = bytes(bytearray(formats, encoding='utf-8'))
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        formats_root = etree.fromstring(formats, parser=parser)

        layer = self.root.find(FORMATS_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(self.root,
                                     QName(PREFIX_NAF_BASE,
                                           FORMATS_LAYER_TAG))

        def add_element(el, tag):
            c = etree.SubElement(el, tag)
            for item in el.attrib.keys():
                if item not in ['bbox', 'colourspace', 'ncolour']:
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
            return {item: el2.attrib[item] for item in el2.keys() if item not in ['bbox', 'colourspace', 'ncolour']}

        offset = 0
        for page in formats_root:
            page_element = add_element(layer, "page")
            page_length = 0
            for page_item in page:

                if page_item.tag == 'textbox':

                    page_item_element = add_element(page_element, page_item.tag)
                    for textline in page_item:
                        textline_element = add_element(page_item_element, textline.tag)
                        if len(textline) > 0:
                            previous_text = textline[0].text
                            previous_attrib = copy_dict(textline[0])
                            for idx, char in enumerate(textline[1:]):
                                char_attrib = copy_dict(char)

                                if (previous_attrib == char_attrib):
                                    previous_text += char.text
                                    if idx == len(textline) - 1:
                                        add_text_element(textline_element, char.tag, previous_text, previous_attrib, offset)
                                        page_length += len(previous_text)
                                        offset += len(previous_text)

                                else:  # -> previous_attrib != char_attrib

                                    add_text_element(textline_element, char.tag, previous_text, previous_attrib, offset)
                                    page_length += len(previous_text)
                                    offset += len(previous_text)

                                    previous_text = char.text
                                    previous_attrib = char_attrib
                                    if idx == len(textline) - 1:
                                        add_text_element(textline_element, char.tag, previous_text, previous_attrib, offset)
                                        page_length += len(previous_text)
                                        offset += len(previous_text)
                        page_length += 1
                        offset += 1

                    page_length += 1
                    offset += 1

                elif page_item.tag == 'layout':
                    page_length += 1
                    offset += 1
                elif page_item.tag == 'figure':
                    page_item_element = add_element(page_element,
                                                    page_item.tag)
                    previous_text = textline[0].text
                    previous_attrib = copy_dict(textline[0])
                    for idx, char in enumerate(page_item):
                        if char.tag == 'text':
                            char_attrib = copy_dict(char)
                            if previous_attrib == char_attrib:
                                previous_text += char.text
                                if idx == len(textline) - 1:
                                    add_text_element(page_item_element,
                                                     char.tag,
                                                     previous_text,
                                                     previous_attrib,
                                                     offset)
                                    page_length += len(previous_text)
                                    offset += len(previous_text)
                            else:  # -> previous_attrib != char_attrib
                                add_text_element(page_item_element,
                                                 char.tag,
                                                 previous_text,
                                                 previous_attrib,
                                                 offset)
                                page_length += len(previous_text)
                                offset += len(previous_text)
                                if idx < len(textline) - 1:
                                    previous_text = char.text
                                    previous_attrib = char_attrib
                                else:
                                    add_text_element(page_item_element,
                                                     char.tag,
                                                     char.text,
                                                     char_attrib,
                                                     offset)
                                    page_length += len(char.text)
                                    offset += len(char.text)
            page_element.set("length", str(page_length))
            page_element.set("offset", str(offset-page_length))

    def add_dependency_element(self,
                               data: DependencyRelation,
                               comments: bool):
        """
        """
        layer = self.root.find(DEPS_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(self.root, QName(PREFIX_NAF_BASE,
                                                      DEPS_LAYER_TAG))

        if comments:
            comment = data.rfunc + '(' + data.from_orth + ',' + data.to_orth + ')'
            comment = self.prepare_comment_text(comment)
            layer.append(etree.Comment(comment))

        dep_attrib = {
            "from": data.from_term,
            "to": data.to_term,
            "rfunc": data.rfunc}

        etree.SubElement(layer,
                         QName(PREFIX_NAF_BASE, DEP_OCCURENCE_TAG),
                         dep_attrib)

    def add_entity_element(self,
                           data: EntityElement,
                           naf_version: str,
                           comments: str):
        """
        """
        layer = self.root.find(ENTITIES_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(self.root,
                                     QName(PREFIX_NAF_BASE,
                                           ENTITIES_LAYER_TAG))
        entity_attrib = {
            "id": data.id,
            "type": data.type}

        entity = etree.SubElement(layer,
                                  QName(PREFIX_NAF_BASE, ENTITY_OCCURENCE_TAG),
                                  entity_attrib)

        if naf_version == 'v3':
            references = etree.SubElement(entity, "references")
            span = etree.SubElement(references, SPAN_OCCURRENCE_TAG)
        elif naf_version == 'v3.1':
            span = etree.SubElement(entity, SPAN_OCCURRENCE_TAG)

        if comments:
            text = ' '.join(data.text)
            text = self.prepare_comment_text(text)
            span.append(etree.Comment(text))
        for target in data.targets:
            target_el = etree.SubElement(span, TARGET_OCCURENCE_TAG)
            target_el.set("id", target)

        assert type(data.ext_refs) == list, f'ext_refs should be a list of dictionaries (can be empty)'

        ext_refs_el = etree.SubElement(entity, 'externalReferences')
        for ext_ref_info in data.ext_refs:
            one_ext_ref_el = etree.SubElement(ext_refs_el, 'externalRef')
            one_ext_ref_el.set('reference', ext_ref_info['reference'])
            for optional_attr in ['resource', 'source', 'timestamp']:
                if optional_attr in ext_ref_info:
                    one_ext_ref_el.set(optional_attr,
                                       ext_ref_info[optional_attr])

    def add_term_element(self,
                         data: TermElement,
                         layer_to_attributes_to_ignore: dict,
                         comments: bool):
        """
        """
        layer = self.root.find(TERMS_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(self.root, QName(PREFIX_NAF_BASE,
                                                      TERMS_LAYER_TAG))

        term = etree.SubElement(layer, QName(PREFIX_NAF_BASE,
                                             TERM_OCCURRENCE_TAG))

        attrs = ['id', 'lemma', 'pos', 'type', 'morphofeat']
        for attr in attrs:
            if attr not in layer_to_attributes_to_ignore.get('terms', set()):
                term.set(attr, getattr(data, attr))

        span = etree.SubElement(term, SPAN_OCCURRENCE_TAG)
        if comments:
            text = ' '.join(data.text)
            text = self.prepare_comment_text(text)
            span.append(etree.Comment(text))
        for target in data.targets:
            target_el = etree.SubElement(span, TARGET_OCCURENCE_TAG)
            target_el.set("id", target)

    def add_chunk_element(self,
                          data: ChunkElement,
                          comments: bool):
        """
        """
        layer = self.root.find(CHUNKS_LAYER_TAG)
        if layer is None:
            layer = etree.SubElement(self.root,
                                     QName(PREFIX_NAF_BASE,
                                           CHUNKS_LAYER_TAG))

        chunk = etree.SubElement(layer, CHUNK_OCCURENCE_TAG)
        chunk.set("id", data.cid)
        chunk.set("head", data.head)
        chunk.set("phrase", data.phrase)
        span = etree.SubElement(chunk, SPAN_OCCURRENCE_TAG)
        if comments:
            text = data.text
            text = self.prepare_comment_text(text)
            span.append(etree.Comment(text))
