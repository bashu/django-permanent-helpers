Changes
-------

2.0.0 (2026-08-14)
~~~~~~~~~~~~~~~~~~

* Fixed a ``ValueError`` in ``PermanentModelListFilter.queryset()`` on Django 5+ (``__isnull`` requires a strict ``bool``).
* Fixed ``log_restore()`` to use ``LogEntry.objects.log_actions()`` (``log_action()`` is removed in Django 6.0).
* Dropped Python 2.7/3.6–3.9 support; now requires Python 3.10–3.14.
* Dropped Django <5.2 support; now requires Django 5.2–6.1.


1.0.1 (2021-11-29)
~~~~~~~~~~~~~~~~~~

* Updated ru translation.

1.0.0 (2021-11-29)
~~~~~~~~~~~~~~~~~~

* Added Django 3+ support.
* Dropped Python 2.7 support.
* Dropped Django 1.10 / 1.11 support.
