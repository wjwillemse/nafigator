# coding: utf-8

"""Convert2rdf module."""

import sys
import click
from io import StringIO, BytesIO

from .nafdocument import NafDocument


@click.command()
@click.option(
    "--input", default="data/example.naf", prompt="input file", help="The input file"
)
@click.option(
    "--output", default="data/example.ttl", prompt="output file", help="The output file"
)

def opennaf(input: str, output: str):
    """ """
    naf = NafDocument().open(input)

    params: dict = dict()
    params['namespaces']: dict = dict()
    params['provenanceNumber']: int = 0

    addNamespace("dc", "http://purl.org/dc/elements/1.1/", params)

    params['out']: StringIO = StringIO()

    params['prefix'] = printNamespaces(params)

    processNaf(naf, params)

    file_content: StringIO = StringIO()
    file_content.write("# RDF triples (turtle syntax)\n\n")
    file_content.write("# NAF URI  '"+input+"'\n")
    file_content.write("\n")
    file_content.write(params['prefix'])
    file_content.write("\n\n")
    file_content.write(params['out'].getvalue().replace('\u2264', ''))
    
    if output:
        fh = open(output, "w", encoding='utf-8')
        fh.write(file_content.getvalue())
        fh.close()


def addNamespace(prefix, uri, params):
    namespaces = params['namespaces']
    found = namespaces.get(uri, None)
    if found:
        if prefix != found:
            return -1
        del namespaces[uri]
    namespaces[uri] = prefix
    return 0


def printNamespaces(params):
    namespaces = params['namespaces']
    res: str = ''
    for uri in namespaces:
        if uri[-1] != "#":
            res += "@prefix "+namespaces[uri]+": <"+uri+"#>.\n"
        else:
            res += "@prefix "+namespaces[uri]+": <"+uri+">.\n"
    return res


def processNaf(naf, params):
    provenance = genProvenanceName(params)

def processEntities(naf, params):

    entity_id = context.attrib.get('id', None)
    output = params['out']
    output.write("_:entity_"+entity_id+"\n")
    output.write("    xl:type naf-base:entity ;\n")
    output.write("    naf-base:type bla .\n")


def genProvenanceName(params: dict) -> str:
    output = params['out']
    params['provenanceNumber'] += 1
    name: str = "_:provenance"+str(params['provenanceNumber'])
    output.write("# provenance for data from same naf-file\n")
    output.write(name+" \n")
    return name


if __name__ == "__main__":
    sys.exit(opennaf())
