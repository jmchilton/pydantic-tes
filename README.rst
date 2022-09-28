
pydantic-tes
---------------------

.. image:: https://badge.fury.io/py/pydantic-tes.svg
   :target: https://pypi.python.org/pypi/pydantic-tes/
   :alt: pydantic-tes on the Python Package Index (PyPI)

A collection of pydantic_ models for `GA4GH Task Execution Service`_.

In addition to the models, this package contains a lightweight client for TES based
on them using requests_ and utilities for working and testing it against Funnel_ - 
a the TES implementation.

This Python project can be installed from PyPI using ``pip``.

::

    $ python3 -m venv .venv
    $ . .venv/bin/activate
    $ pip install pydantic-tes

Checkout `py-tes`_ for an alternative set of Python models and an API client based on the
more lightweight attrs_ package.

.. _Funnel: https://ohsu-comp-bio.github.io/funnel/
.. _requests: https://requests.readthedocs.io/en/latest/
.. _GA4GH Task Execution Service: https://github.com/ga4gh/task-execution-schemas
.. _pydantic: https://pydantic-docs.helpmanual.io/
.. _py-tes: https://github.com/ohsu-comp-bio/py-tes
.. _attrs: https://www.attrs.org/en/stable/
