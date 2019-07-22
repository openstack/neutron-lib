..
      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.


      Convention for heading levels in Neutron devref:
      =======  Heading 0 (reserved for the title in a document)
      -------  Heading 1
      ~~~~~~~  Heading 2
      +++++++  Heading 3
      '''''''  Heading 4
      (Avoid deeper levels because they do not render well.)


API Extensions
==============

API extensions provide a standardized way of introducing new API functionality.
While the ``neutron-lib`` project itself does not serve an API, the ``neutron``
project does and leverages the API extension framework from ``neutron-lib``.

API extensions consist of the following high-level constructs:

- API definitions that specify the extension's static metadata. This metadata
  includes basic details about the extension such as its name, description,
  alias, etc. as well as its extended resources/sub-resources and
  required/optional extensions. These definitions live in the
  ``neutron_lib.api.definitions`` package.
- API reference documenting the APIs/resources added/modified by the extension.
  This documentation is in ``rst`` format and is used to generate the
  `OpenStack Networking API reference
  <https://docs.openstack.org/api-ref/network/>`_.
  The API reference lives under the ``api-ref/source/v2``
  directory of the ``neutron-lib`` project repository.
- An extension descriptor class that must be defined in an extension directory
  for ``neutron`` or other sub-project that supports extensions. This concrete
  class provides the extension's metadata to the API server. These extension
  classes reside outside of ``neutron-lib``, but leverage the base classes
  from ``neutron_lib.api.extensions``. For more details see the section below
  on using neutron-lib's extension classes.
- The API extension plugin implementation itself. This is the code that
  implements the extension's behavior and should carry out the operations
  defined by the extension. This code resides under its respective project
  repository, not in ``neutron-lib``. For more details see the `neutron api
  extension dev-ref <https://docs.openstack.org/neutron/latest/contributor/
  internals/api_extensions.html>`_.


Using neutron-lib's base extension classes
------------------------------------------

The ``neutron_lib.api.extensions`` module provides a set of base extension
descriptor classes consumers can use to define their extension descriptor(s).
For those extensions that have an API definition in
``neutron_lib.api.definitions``, the ``APIExtensionDescriptor`` class can
be used. For example::

    from neutron_lib.api.definitions import provider_net
    from neutron_lib.api import extensions


    class Providernet(extensions.APIExtensionDescriptor):
        api_definition = provider_net
        # nothing else needed if default behavior is acceptable


For extensions that do not yet have a definition in
``neutron_lib.api.definitions``, they can continue to use the
``ExtensionDescriptor`` as has been done historically.
