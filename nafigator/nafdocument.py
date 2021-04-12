# coding: utf-8

"""naf document."""

from lxml import etree
from .const import DependencyRelation
from .const import WordformElement
from .const import EntityElement
from .const import TermElement
from .const import ChunkElement
from .utils import time_in_correct_format

class NafDocument:

    TERMS_LAYER_TAG = "terms"
    TERM_OCCURRENCE_TAG = "term"

    def __init__(self, params: dict):
        self.tree = etree.ElementTree()
        nsmap = {"dc":  "http://purl.org/dc/elements/1.1/"}
        self.root = etree.Element("NAF", nsmap = nsmap)
        self.tree._setroot(self.root)
        self.deps_layer = None
        self.text_layer = None
        self.entities_layer = None
        self.terms_layer = None
        self.xml_layer = None
        self.naf_header = None
        self.raw_layer = None
        self.add_naf_tree(params)

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


    def add_naf_tree(self, 
                     params: dict):
        """
        """
        self.root.set('{http://www.w3.org/XML/1998/namespace}lang', params['language'])
        self.root.set('version', params['naf_version'])

        self.naf_header = etree.SubElement(self.root, "nafHeader")

        filedesc_el = etree.SubElement(self.naf_header, 'fileDesc')
        filedesc_el.set('creationtime', time_in_correct_format(params['creationtime']))
        if params['title'] is not None:
            filedesc_el.set('title', params['title'])

        # add public child to nafHeader
        public_el = etree.SubElement(self.naf_header, 'public')
        if params['uri'] is not None:
            uri_qname = etree.QName('{http://purl.org/dc/elements/1.1/}uri', 'uri')
            public_el.set(uri_qname, params['uri'])

        layers = params['preprocess_layers']
        for layer in layers:
            self.add_pre_processors(layer, params)
        if 'xml' in layers:
            self.xml_layer = etree.SubElement(self.root, 'xml')

        self.raw_layer = etree.SubElement(self.root, 'raw')

        layers = params['linguistic_layers']
        if params['add_mws']:
            layers.append('multiwords')
        for layer in layers:
            self.add_linguistic_processors(layer, params)


    def add_pre_processors(self, 
                           layer: str, 
                           params: dict):
        """
        """
        proc = etree.SubElement(self.naf_header, "Preprocessors")
        proc.set("layer", layer)
        pp = etree.SubElement(proc, "pp")
        pp.set("beginTimestamp", time_in_correct_format(params['preprocess_start_time']))
        pp.set('endTimestamp', time_in_correct_format(params['preprocess_end_time']))
        pp.set('name', params['preprocess_name'])
        if params['preprocess_version'] is not None:
            pp.set('version', params['preprocess_version'])

    def add_linguistic_processors(self,
                                  layer: str, 
                                  params: dict):
        """
        """
        ling_proc = etree.SubElement(self.naf_header, "linguisticProcessors")
        ling_proc.set("layer", layer)
        lp = etree.SubElement(ling_proc, "lp")
        lp.set("beginTimestamp", time_in_correct_format(params['start_time']))
        lp.set('endTimestamp', time_in_correct_format(params['end_time']))
        lp.set('name', params['engine'].model_name)
        lp.set('version', params['engine'].model_version)


    def prepare_comment_text(self, text: str):
        """
        """
        text = text.replace('--','DOUBLEDASH')
        if text.endswith('-'):
            text = text[:-1] + 'SINGLEDASH'
        return text

    def add_wf_element(self, 
                       data: WordformElement, 
                       params: dict):
        """
        """
        if self.text_layer is None:
            self.text_layer = etree.SubElement(self.root, "text")

        wf_attrib = {
            "id": data.wid,
            "length": data.length,
            "offset": data.offset}

        if data.page != 0:
            wf_attrib["page"] = data.page
        if data.sent != 0:
            wf_attrib["sent"] = data.sent

        wf = etree.SubElement(self.text_layer, "wf", wf_attrib)

        if params['cdata']:
            wf.text = etree.CDATA(data.wordform)
        else:
            wf.text = data.wordform


    def add_dependency_element(self, 
                               data: DependencyRelation,
                               params: dict):
        """
        """
        if self.deps_layer is None:
            self.deps_layer = etree.SubElement(self.root, "deps")

        if params['comments']:
            comment = data.rfunc + '(' + data.from_orth + ',' + data.to_orth + ')'
            comment = self.prepare_comment_text(comment)
            self.deps_layer.append(etree.Comment(comment))

        dep_attrib = {
            "from": data.from_term,
            "to": data.to_term,
            "rfunc": data.rfunc}

        dep_el = etree.SubElement(self.deps_layer, "dep", dep_attrib)

    def add_entity_element(self, 
                           data: EntityElement, 
                           params: dict):
        """
        """
        if self.entities_layer is None:
            self.entities_layer = etree.SubElement(self.root, "entities")

        ent_attrib = {
            "id": data.id,
            "type": data.type}

        entity = etree.SubElement(self.entities_layer, "entity", ent_attrib)

        if params['naf_version'] == 'v3':
            references_el = etree.SubElement(entity, "references")
            span = etree.SubElement(references, "span")
        elif params['naf_version'] == 'v3.1':
            span = etree.SubElement(entity, "span")

        if params['comments']:
            text = ' '.join(data.text)
            text = self.prepare_comment_text(text)
            span.append(etree.Comment(text))
        for target in data.targets:
            target_el = etree.SubElement(span, "target")
            target_el.set("id", target)

        assert type(data.ext_refs) == list, f'ext_refs should be a list of dictionaries (can be empty)'

        ext_refs_el = etree.SubElement(entity, 'externalReferences')
        for ext_ref_info in data.ext_refs:
            one_ext_ref_el = etree.SubElement(ext_refs_el, 'externalRef')
            one_ext_ref_el.set('reference', ext_ref_info['reference'])
            for optional_attr in ['resource', 'source', 'timestamp']:
                if optional_attr in ext_ref_info:
                    one_ext_ref_el.set(optional_attr, ext_ref_info[optional_attr])

    def add_term_element(self, 
                         data: TermElement, 
                         params: dict):
        """
        """
        if self.terms_layer is None:
            self.terms_layer = etree.SubElement(self.root, "terms")

        term = etree.SubElement(self.terms_layer, "term")

        attrs = ['id', 'lemma', 'pos', 'type', 'morphofeat']
        for attr in attrs:
            if attr not in params['layer_to_attributes_to_ignore'].get('terms', set()):
                term.set(attr, getattr(data, attr))

        span = etree.SubElement(term, "span")
        if params['comments']:
            text = ' '.join(data.text)
            text = self.prepare_comment_text(text)
            span.append(etree.Comment(text))
        for target in data.targets:
            target_el = etree.SubElement(span, "target")
            target_el.set("id", target)

    def add_chunk_element(self, 
                          data: ChunkElement, 
                          params: dict):
        """
        """
        if self.chunks_layer is None:
            self.chunks_layer = etree.SubElement(self.root, "chunks")

        chunk = etree.SubElement(self.chunks_layer, "chunk")
        chunk.set("id", data.cid)
        chunk.set("head", data.head)
        chunk.set("phrase", data.phrase)
        span = etree.SubElement(chunk, "span")
        if params['comments']:
            text = data.text
            text = self.prepare_comment_text(text)
            span.append(etree.Comment(text))

