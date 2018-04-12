# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutron_lib.utils import runtime


NEUTRON_OBJECT_NAMESPACE = 'neutron.objects'
_REGISTRY = runtime.NamespacedPlugins(NEUTRON_OBJECT_NAMESPACE)


def load_class(object_class_name):
    """Return the versioned object for the given class name.

    :param object_class_name: The class name of the versioned object to
        get.
    :returns: A reference to the class for the said object_class_name.
    """
    return _REGISTRY.get_plugin_class(object_class_name)


def new_instance(object_class_name, *inst_args, **inst_kwargs):
    """Create a new instance of a versioned object.

    :param object_class_name: The name of the versioned object's class to
        instantiate.
    :param inst_args: Any args pass onto the constructor of the versioned
        object when creating it.
    :param inst_kwargs: Any kwargs to pass onto the constructor of the object
        when creating it.
    :returns: A new instance of the versioned object.
    """
    return _REGISTRY.new_plugin_instance(
        object_class_name, *inst_args, **inst_kwargs)


def contains(object_class_name):
    """Determine if a given versioned object is loaded.

    :param object_class_name: The class name of the versioned object to check
        for.
    :returns: True if the versioned object is loaded, and False otherwise.
    """
    return object_class_name in _REGISTRY.loaded_plugin_names
