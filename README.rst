django-permanent-helpers
========================

.. image:: https://img.shields.io/pypi/v/django-permanent-helpers.svg
    :target: https://pypi.python.org/pypi/django-permanent-helpers/

.. image:: https://img.shields.io/pypi/dm/django-permanent-helpers.svg
    :target: https://pypi.python.org/pypi/django-permanent-helpers/

.. image:: https://img.shields.io/github/license/bashu/django-permanent-helpers.svg
    :target: https://pypi.python.org/pypi/django-permanent-helpers/

Django admin helper classes for django-permanent_ models.

Authored by `Basil Shubin <http://github.com/bashu>`_, inspired by django-taggit-helpers_

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
        'django_permanent_helpers',
    )


Usage
=====

PermanentModelAdmin
-------------------

An abstract ModelAdmin which will include deleted objects in its listing and enable un-deleting feature.

.. code-block:: python

    from django_permanent_helpers import PermanentModelAdmin
    # For Django 1.9+, use this instead:
    # from django_permanent_helpers.admin import PermanentModelAdmin

    class MyModelAdmin(PermanentModelAdmin):
        pass

PermanentModelListFilter
------------------------

Filter records by their ``PERMANENT_FIELD`` value, use together with ``PermanentModelAdmin`` class.

.. code-block:: python

    from django_permanent_helpers import PermanentModelAdmin, PermanentModelListFilter
    # For Django 1.9+, use this instead:
    # from django_permanent_helpers.admin import PermanentModelAdmin, PermanentModelListFilter

    class MyModelAdmin(PermanentModelAdmin):
        list_filter = [PermanentModelListFilter]

Contributing
============

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-permanent: https://github.com/meteozond/django-permanent
.. _django-taggit-helpers: https://github.com/mfcovington/django-taggit-helpers
