neutron-lib Style Commandments
===============================================

- Step 1: Read the OpenStack Style Commandments
  http://docs.openstack.org/developer/hacking/
- Step 2: Read on

Neutron Specific Commandments
-----------------------------

- [N521] Validate that jsonutils module is used instead of json
- [N523] Enforce namespace-less imports for oslo libraries
- [N524] Prevent use of deprecated contextlib.nested.
- [N525] Python 3: Do not use xrange.
- [N526] Python 3: do not use basestring.
- [N527] Python 3: do not use dict.iteritems.
- [N529] Method's default argument shouldn't be mutable
- [N530] No importing of neutron; should be ignored in neutron itself
