=======
History
=======

0.1.0 (2021-03-13)
------------------

* First release on PyPI.

0.1.1 to 0.1.41 (2022-3-1)
--------------------------

* A lot of small changes

0.1.42 (2022-4-6)
-----------------

* Added first version of termbase processor

0.1.43 (2022-4-29)
------------------

* Fix for get_context_rows

0.1.45 (2022-4-29)
------------------

* Added sent ids to doc.sentences and doc.paragraphs

0.1.47 (2022-8-22)
------------------

* Table extraction improvements 
* Fix to align enumeration of sentences and paragraphs

0.1.48 (2022-8-30)
------------------

* Added first version of nif conversion

0.1.49 (2022-9-2)
-----------------

* Improved version of nif conversion
* Optimized TermbaseProcessor

0.1.50 (2022-9-5)
-----------------

* Morphological features in nif
* Bugfix TermbaseProcessor
* NIF example added to README.rst

0.1.52 (2022-10-19)
-------------------

* Formats layer now contains a deep copy of pdfminer output in xml

0.1.53 (2022-11-11)
-------------------

* Added coordinates to formats layer as an option
* Added highlighter feature for words
* Separated TableFormatter and Highlighter into 2 different modules
* Bugfix in formats layer

0.1.54 (2022-11-17)
-------------------

* Added PyMuPDF to requirements

0.1.55 (2022-11-21)
-------------------

* Added iribaker and Unidecode to requirements

0.1.57 (2022-11-30)
-------------------

* Added possibility to use stream instead of opening a file
* Added naf2nif function to convert naf to rdflid.Graph in NIF format 
* Added parameter "include pdf xml" to include the original xml output of pdfminer to the naf document

0.1.58 (2022-12-08)
-------------------
* Version bump for new build to check if this solves the installation version of 0.1.57

0.1.59 (2022-12-08)
-------------------
* Added PyMuPDF==1.21.0 to requirements

0.1.60 (2022-12-12)
-------------------
* Add outline unittests
* Bugfix Lemma error
* Part 1 bugfix referencing error

0.1.61 (2022-01-09)
-------------------
* Add option for streams input
* Remove unused imports

