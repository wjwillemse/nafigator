# -*- coding: utf-8 -*-

"""Linguistic processor module.

This module contains the linguistic classes for nafigator

"""

try:
    import spacy

    SPACY_IMPORTED = True
except:
    SPACY_IMPORTED = False

try:
    import stanza

    STANZA_IMPORTED = True
except:
    STANZA_IMPORTED = False

if SPACY_IMPORTED:

    class spacyProcessor:
        def __init__(self, nlp=None, lang: str = None) -> None:
            """Initialize spacy processor

            Args:
                nlp: optional NLP processor
                lang: language
            Returns:
                None

            """
            self.lang = lang
            if nlp is None:
                if lang == "en":
                    self.nlp = spacy.load("en_core_web_sm")
                elif lang == "nl":
                    self.nlp = spacy.load("nl_core_web_sm")
            else:
                if isinstance(nlp, dict):
                    if lang in nlp.keys():
                        self.nlp = nlp[lang]
                    else:
                        logging.error("Language not available in nlp dict parameter")
                        self.nlp = None
                else:
                    self.nlp = nlp
            self.model_name = (
                f'spaCy-model_{self.nlp.meta["lang"]}_{self.nlp.meta["name"]}'
            )
            self.model_version = f'spaCy_version-{spacy.__version__}__model_version-{self.nlp.meta["version"]}'

        def processor(self, name):
            """Return processor of each pipeline element

            Args:
                name: name of processor
            Returns:
                dict: dictionary with name of processor

            """
            processors = {proc_name: proc for proc_name, proc in self.nlp.pipeline}

            # where is the tokenizer object in spacy?
            if name == "text":
                processor = processors.get("tagger", None)
            elif name == "entities":
                processor = processors.get("ner", None)
            elif name == "terms":
                processor = processors.get("tagger", None)
            elif name == "deps":
                processor = processors.get("parser", None)
            elif name == "multiwords":
                processor = processors.get("tagger", None)
            elif name == "raw":
                processor = processors.get("tagger", None)

            # need a better solution for this
            return {"model": str(processor.model)}

        def nlp(self, text):
            self.doc = self.nlp(text)
            return self.doc

        def document_sentences(self, doc):
            return doc.sents

        def sentence_tokens(self, sentence):
            return sentence

        def sentence_entities(self, sentence):
            return sentence.ents

        def document_entities(self, doc):
            return doc.ents

        def document_text(self, doc):
            return doc.text

        def token_head(self, sentence, token):
            return token.head

        def token_index(self, token):
            return token.i

        def token_head_index(self, sentence, token):
            return token.head.i

        def token_dependency(self, token):
            return token.dep_

        def token_orth(self, token):
            return token.orth_

        def token_offset(self, token):
            return token.idx

        def offset_token_index(self):
            return 1

        def token_pos(self, token):
            return token.pos_

        def token_lemma(self, token):
            if token.lemma_ == None:
                return token.text
            else:
                return token.lemma_

        def token_tag(self, token):
            return token.tag_

        def entity_span_start(self, entity):
            return entity.start + 1

        def entity_span_end(self, entity):
            return entity.end

        def entity_type(self, entity):
            ent_type_set = {
                token.ent_type_ for token in entity if token.ent_type_ != ""
            }
            return ent_type_set.pop()

        def document_noun_chunks(self, doc):
            return doc.noun_chunks

        def token_reset(self):
            return False


else:

    class spacyProcessor:
        def __init__(self):
            return None


if STANZA_IMPORTED:

    class stanzaProcessor:
        def __init__(
            self,
            nlp=None,
            lang: str = None,
        ):

            if nlp is None:
                self.nlp = stanza.Pipeline(
                    lang=lang,
                    processors="tokenize,pos,lemma,ner,depparse",
                    verbose=False,
                )
            else:
                self.nlp = nlp
            self.lang = lang
            self.model_name = f"stanza-model_{lang}"
            self.model_version = f"stanza_version-{stanza.__version__}"

        def processor(self, name):

            if name == "text":
                processor = self.nlp.processors.get("tokenize")
            elif name == "entities":
                processor = self.nlp.processors.get("ner")
            elif name == "terms":
                processor = self.nlp.processors.get("pos")
            elif name == "deps":
                processor = self.nlp.processors.get("depparse")
            elif name == "multiwords":
                processor = self.nlp.processors.get("tokenize")
            elif name == "raw":
                processor = self.nlp.processors.get("tokenize")

            return {"model": processor._config["model_path"]}

        def nlp(self, text):
            self.doc = self.nlp(text)
            return self.doc

        def document_sentences(self, doc):
            return doc.sentences

        def sentence_tokens(self, sentence):
            return sentence.tokens

        def sentence_entities(self, sentence):
            return sentence.ents

        def document_entities(self, doc):
            return doc.ents

        def document_text(self, doc):
            return doc.text

        def offset_token_index(self):
            return 0

        def token_head(self, sentence, token):
            if token.words[0].head != 0:
                return sentence.words[token.words[0].head - 1].parent
            else:
                return token.id[0]

        def token_reset(self):
            return True

        def token_index(self, token):
            return token.id[0]

        def token_head_index(self, sentence, token):
            if token.words[0].head != 0:
                return sentence.words[token.words[0].head - 1].parent.id[0]
            else:
                return token.id[0]

        def token_dependency(self, token):
            return token.words[0].deprel

        def token_orth(self, token):
            return token.text

        def token_offset(self, token):
            return token.start_char

        def token_pos(self, token):
            if len(token.words) > 0:
                return token.words[0].pos
            else:
                return ""

        def token_lemma(self, token):
            if len(token.words) > 0:
                if token.words[0].lemma == None:
                    return token.words[0].text
                else:
                    return token.words[0].lemma
            else:
                return ""

        def token_tag(self, token):
            if len(token.words) > 0:
                return token.words[0].feats
            else:
                return ""

        def entity_token_start(self, entity):
            return entity.tokens[0]

        def entity_token_end(self, entity):
            return entity.tokens[-1]

        def entity_span_start(self, entity):
            return entity.tokens[0].id[0]

        def entity_span_end(self, entity):
            return entity.tokens[-1].id[0]

        def entity_type(self, entity):
            return entity.type


else:

    class stanzaProcessor:
        def __init__(self):
            return None
