# coding: utf-8

"""Main module."""

import sys
import click
from .nafdocument import NafDocument
from .const import MultiwordElement
from .const import ProcessorElement


@click.command()
@click.option(
    "--input", default="data/example.naf", prompt="input file", help="The input file"
)
def opennaf(input: str):
    """ """
    naf = NafDocument().open(input)
    # print(naf.header)
    # print(naf.version)
    # print(naf.raw)
    # print(naf.text)
    # print(naf.terms)
    # print(naf.entities)
    # print(naf.deps)
    # print(naf.formats)
    print(naf.multiwords)
    naf.remove_layer_elements("multiwords")
    print(naf.multiwords)

    recommendations = {
        'id': "recommendation1",
        'subjectivity': "0.5",
        'targets': list()
        }

    lp = ProcessorElement(
        name="processorname",
        version="1.0",
        timestamp=None,
        beginTimestamp=None,
        endTimestamp=None,
        hostname=None)

    naf.add_processor_element("recommendations", lp)

    naf.add_layer_element(data=recommendations,
                          layer_tag="recommendations",
                          occurrence_tag="recommendation")

    print(naf.recommendations)
    print(naf.header)

    # print(naf.sentences)

if __name__ == "__main__":
    sys.exit(opennaf())
