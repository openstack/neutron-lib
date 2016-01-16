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


API Converters
==============

Defintions for REST API attributes, can include conversion methods
to help normalize user input or transform the input into a form that
can be used.


Defining A Converter Method
---------------------------

By convention, the name should start with ``convert_to_``, and will
take a single argument for the data to be converted. The method
should return the converted data (which, if the input is None,
and no conversion is performed, the implicit None returned by the
method may be used). If the conversion is impossible, an
InvalidInput exception should be raised, indicating what is wrong.
For example, here is one that converts a variety of user inputs
to a boolean value.
::

   def convert_to_boolean(data):
        if isinstance(data, six.string_types):
            val = data.lower()
            if val == "true" or val == "1":
                return True
            if val == "false" or val == "0":
                return False
        elif isinstance(data, bool):
            return data
        elif isinstance(data, int):
            if data == 0:
                return False
            elif data == 1:
                return True
        msg = _("'%s' cannot be converted to boolean") % data
        raise n_exc.InvalidInput(error_message=msg)


Using Validators
----------------

In client code, the conversion can be used in a REST API
definition, by specifying the name of the method as a value for
the 'convert_to' key on an attribute. For example:

::

  'admin_state_up': {'allow_post': True, 'allow_put': True,
                     'default': True,
                     'convert_to': conversions.convert_to_boolean,
                     'is_visible': True},

Here, the admin_state_up is a boolean, so the converter is used to
take user's (string) input and transform it to a boolean.


Test The Validator
------------------

Do the right thing, and make sure you've created a unit test for any
converter that you add to verify that it works as expected.

