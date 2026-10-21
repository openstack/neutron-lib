neutron-lib Style Commandments
==============================

- Step 1: Read the OpenStack Style Commandments
  https://docs.openstack.org/hacking/latest/
- Step 2: Read on

Neutron Library Specific Commandments
-------------------------------------

- [N521] Validate that jsonutils module is used instead of json
- [N529] Method's default argument shouldn't be mutable
- [N530] No importing of neutron; should be ignored in neutron itself
- [N532] Validate that LOG.warning is used instead of LOG.warn. The latter is deprecated.
- [N534] Exception messages should be translated
- [N535] Usage of Python eventlet module not allowed
- [N536] DEPRECATED: Use assertIsNone/assertIsNotNone rather than assertEqual/assertIs to check None values.
- [N537] Don't translate logs.

Type Annotations
----------------

- New code must be fully annotated: every parameter and return value of new
  or modified functions and methods should have a type annotation.
- Modules that are already fully annotated are listed in the
  ``[[tool.mypy.overrides]]`` sections of ``pyproject.toml`` and are enforced
  by ``tox -e mypy`` (which is also run as part of ``tox -e pep8``). Do not
  remove a module from those lists; when you finish annotating a module, add
  it.
- Avoid ``Any`` in public signatures where a more specific type is available.
- Annotations must not change runtime behaviour.
