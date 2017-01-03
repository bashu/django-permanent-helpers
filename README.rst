django-permanent-helpers
========================

Django admin helper classes for django-permanent_ models.

Authored by `Basil Shubin <http://github.com/bashu>`_, inspired by django-taggit-helpers_

.. image:: https://img.shields.io/pypi/v/django-permanent-helpers.svg
    :target: https://pypi.python.org/pypi/django-permanent-helpers/

.. image:: https://img.shields.io/pypi/dm/django-permanent-helpers.svg
    :target: https://pypi.python.org/pypi/django-permanent-helpers/

.. image:: https://img.shields.io/github/license/bashu/django-permanent-helpers.svg
    :target: https://pypi.python.org/pypi/django-permanent-helpers/

.. image:: https://landscape.io/github/bashu/django-permanent-helpers/develop/landscape.svg?style=flat
    :target: https://landscape.io/github/bashu/django-permanent-helpers/develop

Installation
============

First install the module, preferably in a virtual environment. It can be installed from PyPI:

.. code-block:: shell

    pip install django-permanent-helpers

Configuration
-------------

First make sure the project is configured for django-permanent_.

Then add the following settings:

.. code-block:: python

    INSTALLED_APPS += (
        'permanent_helpers',
    )


Usage
=====

Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-permanent: https://github.com/meteozond/django-permanent
.. _django-taggit-helpers: https://github.com/mfcovington/django-taggit-helpers
