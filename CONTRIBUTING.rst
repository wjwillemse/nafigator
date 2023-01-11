.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/denederlandschebank/nafigator/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Nafigator could always use more documentation, whether as part of the
official nafigator docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/denederlandschebank/nafigator/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `nafigator` for local development.

1. Fork the `nafigator` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/nafigator.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv nafigator
    $ cd nafigator/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ flake8 nafigator tests
    $ python setup.py test or pytest
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

We work with a main and a dev branch. To add new functionality, make a new branch, add the new functionality and submit a pull request to the dev branch. When needed we will merge the dev branch with the main branch and provide a new version of the package.

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.6, 3.7 and 3.8, and for PyPy. 
   Make sure that the tests pass for all supported Python versions.


Pushing a new version to pypi.org
---------------------------------

If you want to upload a new version to pypi.org then take the following steps

1. Merge pull requests with your changes
2. If not yet done, update the version number in *setup.py* and *nafigator/__init__.py*
3. If not yet done, update *HISTORY.rst* with your changes
4. Build the new version with::

  python setup.py bdist_wheel --universal

5. Upload the new version::

  twine upload dist/*

6. If you get errors when uploading then you can find errors with::

  twine check dist/nafigator-version-py2.py3-none-any.whl


Tips
----

To run a subset of tests::


    $ python -m unittest tests.test_nafigator

