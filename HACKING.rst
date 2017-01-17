neutron-lib Style Commandments
===============================================

- Step 1: Read the OpenStack Style Commandments
  http://docs.openstack.org/developer/hacking/
- Step 2: Read on

Neutron Library Specific Commandments
-------------------------------------

- [N521] Validate that jsonutils module is used instead of json
- [N523] DEPRECATED. Enforce namespace-less imports for oslo libraries
- [N524] Prevent use of deprecated contextlib.nested.
- [N525] Python 3: Do not use xrange.
- [N526] Python 3: do not use basestring.
- [N527] Python 3: do not use dict.iteritems.
- [N529] Method's default argument shouldn't be mutable
- [N530] No importing of neutron; should be ignored in neutron itself
- [N531] Validate that LOG messages, except debug ones, have translations
- [N532] Validate that LOG.warning is used instead of LOG.warn. The latter is deprecated.
- [N533] Validate that debug level logs are not translated
- [N534] Exception messages should be translated
- [N535] Usage of Python eventlet module not allowed
- [N536] Use assertIsNone/assertIsNotNone rather than assertEqual/assertIs to check None values.
