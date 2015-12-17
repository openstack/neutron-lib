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


API Validators
==============

For the REST API, attributes may have custom validators defined. Each
validator will have a method to perform the validation, and a type
definition string, so that the validator can be referenced.


Defining A Validator Method
---------------------------

The validation method will have a positional argument for the data to
be validated, and may have additional (optional) keyword arguments that
can be used during validation.  The method must handle any exceptions
and either return None (success) or a i18n string indicating the
validation failure message. By convention, the method name is prefixed
with ``validate_`` and then includes the data type. For example:

::

   def validate_uuid(data, valid_values=None):
      if not uuidutils.is_uuid_like(data):
          msg = _("'%s' is not a valid UUID") % data
          LOG.debug(msg)
          return msg

There is a validation dictionary that maps the method to a validation
type that can be referred to in REST API definitions. An entry in the
dictionary would look like the following:

::

  'type:uuid': validate_uuid,


Using Validators
----------------

In client code, the valdiator can be used in a REST API by using the
dictionary key for the validator. For example:

::

  RESOURCE_ATTRIBUTE_MAP = {
      NETWORKS: {
          'id': {'allow_post': False, 'allow_put': False,
                 'validate': {'type:uuid': None},
                 'is_visible': True,
                 'primary_key': True},
          'name': {'allow_post': True, 'allow_put': True,
                   'validate': {'type:string': NAME_MAX_LEN},
                   'default': '', 'is_visible': True},

Here, the networks resource has an 'id' attribute with a UUID validator,
as seen by the 'validate' key containing a dictionary with a key of
'type:uuid'.

Any addition arguments for the validator can be specified as values for
the dictionary entry (None in this case, NAME_MAX_LEN in the 'name'
attribute that uses a string validator). In a IP version attribute, one
could have a validator defined as follows:

::

   'ip_version': {'allow_post': True, 'allow_put': False,
                  'convert_to': conversions.convert_to_int,
                  'validate': {'type:values': [4, 6]},
                  'is_visible': True},

Here, the valdiate_values() method will take the list of values as the
allowable values that can be specified for this attribute.

Test The Validator
------------------

Do the right thing, and make sure you've created a unit test for any
validator that you add to verify that it works as expected, even for
simple validators.

