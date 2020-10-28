# Copyright (c) 2012 OpenStack Foundation.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from neutron_lib.api.definitions import port
from neutron_lib import constants


# The type of vnic that this port should be attached to
VNIC_TYPE = 'binding:vnic_type'
# The service will return the vif type for the specific port.
VIF_TYPE = 'binding:vif_type'
# The service may return a dictionary containing additional
# information needed by the interface driver. The set of items
# returned may depend on the value of VIF_TYPE.
VIF_DETAILS = 'binding:vif_details'
# In some cases different implementations may be run on different hosts.
# The host on which the port will be allocated.
HOST_ID = 'binding:host_id'
# The profile will be a dictionary that enables the application running
# on the specific host to pass and receive vif port specific information to
# the plugin.
PROFILE = 'binding:profile'

# The keys below are used in the VIF_DETAILS attribute to convey
# information to the VIF driver.

# TODO(rkukura): Replace CAP_PORT_FILTER, which nova no longer
# understands, with the new set of VIF security details to be used in
# the VIF_DETAILS attribute.
#
#  - port_filter : Boolean value indicating Neutron provides port filtering
#                  features such as security group and anti MAC/IP spoofing
#  - ovs_hybrid_plug: Boolean used to inform Nova that the hybrid plugging
#                     strategy for OVS should be used
CAP_PORT_FILTER = 'port_filter'
OVS_HYBRID_PLUG = 'ovs_hybrid_plug'
VIF_DETAILS_VLAN = 'vlan'
VIF_DETAILS_MACVTAP_SOURCE = 'macvtap_source'
VIF_DETAILS_MACVTAP_MODE = 'macvtap_mode'
VIF_DETAILS_PHYSICAL_INTERFACE = 'physical_interface'
VIF_DETAILS_BRIDGE_NAME = 'bridge_name'
VIF_DETAILS_CONNECTIVITY = 'connectivity'
VIF_DETAILS_BOUND_DRIVERS = 'bound_drivers'

# OVS bridge datapath type: String value used to define if the bridge uses
# kernel or userspace datapath.
OVS_DATAPATH_TYPE = 'datapath_type'

# The keys below are used in the VIF_DETAILS attribute to convey
# information related to the configuration of the vhost-user VIF driver.

# - vhost_user_mode: String value used to declare the mode of a
#                    vhost-user socket
VHOST_USER_MODE = 'vhostuser_mode'
# - server: socket created by hypervisor
VHOST_USER_MODE_SERVER = 'server'
# - client: socket created by vswitch
VHOST_USER_MODE_CLIENT = 'client'
# - vhostuser_socket String value used to declare the vhostuser socket name
VHOST_USER_SOCKET = 'vhostuser_socket'
# - vhost_user_ovs_plug: Boolean used to inform Nova that the ovs plug
#                        method should be used when binding the
#                        vhost-user vif.
VHOST_USER_OVS_PLUG = 'vhostuser_ovs_plug'

# VIF_TYPE: vif_types are required by Nova to determine which vif_driver to
#           use to attach a virtual server to the network

# - vhost-user:  The vhost-user interface type is a standard virtio interface
#                provided by qemu 2.1+. This constant defines the neutron side
#                of the vif binding type to provide a common definition
#                to enable reuse in multiple agents and drivers.
VIF_TYPE_VHOST_USER = 'vhostuser'

VIF_TYPE_UNBOUND = 'unbound'
VIF_TYPE_BINDING_FAILED = 'binding_failed'
VIF_TYPE_DISTRIBUTED = 'distributed'
VIF_TYPE_OVS = 'ovs'
VIF_TYPE_BRIDGE = 'bridge'
VIF_TYPE_OTHER = 'other'
VIF_TYPE_TAP = 'tap'
# vif_type_macvtap: Tells Nova that the macvtap vif_driver should be used to
#                   create a vif. It does not require the VNIC_TYPE_MACVTAP,
#                   which is defined further below. E.g. Macvtap agent uses
#                   vnic_type 'normal'.
VIF_TYPE_MACVTAP = 'macvtap'
# vif_type_agilio_ovs: Tells Nova that the Agilio OVS vif_driver should be
#                      used to create a vif. In addition to the normal OVS
#                      vif types exposed, VNIC_DIRECT and
#                      VNIC_VIRTIO_FORWARDER are supported.
VIF_TYPE_AGILIO_OVS = 'agilio_ovs'
# SR-IOV VIF types
VIF_TYPE_HW_VEB = 'hw_veb'
VIF_TYPE_HOSTDEV_PHY = 'hostdev_physical'

VIF_UNPLUGGED_TYPES = (VIF_TYPE_BINDING_FAILED, VIF_TYPE_UNBOUND)

# VNIC_TYPE: It's used to determine which mechanism driver to use to bind a
#            port. It can be specified via the Neutron API. Default is normal,
#            used by OVS and LinuxBridge agent.
VNIC_NORMAL = 'normal'
VNIC_DIRECT = 'direct'
VNIC_MACVTAP = 'macvtap'
VNIC_BAREMETAL = 'baremetal'
VNIC_DIRECT_PHYSICAL = 'direct-physical'
VNIC_VIRTIO_FORWARDER = 'virtio-forwarder'
VNIC_SMARTNIC = 'smart-nic'
# - vdpa:  The vHost-vdpa transport is a new vHost backend type introduced
#          in qemu 5.1. vHost-vdpa leverages the vdpa framework introduced in
#          kernel 5.7 to implement  a vhost offload of a standard virtio-net
#          interface to a software or hardware backend.
VNIC_VHOST_VDPA = 'vdpa'

VNIC_TYPES = [VNIC_NORMAL, VNIC_DIRECT, VNIC_MACVTAP, VNIC_BAREMETAL,
              VNIC_DIRECT_PHYSICAL, VNIC_VIRTIO_FORWARDER, VNIC_SMARTNIC,
              VNIC_VHOST_VDPA]

# VIF_DETAILS_CONNECTIVITY: Indicates what kind of connectivity the network
#                           back-end provides: L2, L3 or not specified.
CONNECTIVITY_L2 = 'l2'
CONNECTIVITY_L3 = 'l3'
CONNECTIVITY_LEGACY = 'legacy'

# The alias of the extension.
ALIAS = 'binding'

# Whether or not this extension is simply signaling behavior to the user
# or it actively modifies the attribute map.
IS_SHIM_EXTENSION = False

# Whether the extension is marking the adoption of standardattr model for
# legacy resources, or introducing new standardattr attributes. False or
# None if the standardattr model is adopted since the introduction of
# resource extension.
# If this is True, the alias for the extension should be prefixed with
# 'standard-attr-'.
IS_STANDARD_ATTR_EXTENSION = False

# The name of the extension.
NAME = 'Port Binding'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource.
API_PREFIX = ''

# The description of the extension.
DESCRIPTION = "Expose port bindings of a virtual port to external application"

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2014-02-03T10:00:00-00:00"

# The name of the resource.
RESOURCE_NAME = port.RESOURCE_NAME

# The plural for the resource.
COLLECTION_NAME = port.COLLECTION_NAME

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        VIF_TYPE: {'allow_post': False, 'allow_put': False,
                   'default': constants.ATTR_NOT_SPECIFIED,
                   'enforce_policy': True,
                   'is_visible': True},
        VIF_DETAILS: {'allow_post': False, 'allow_put': False,
                      'default': constants.ATTR_NOT_SPECIFIED,
                      'enforce_policy': True,
                      'is_visible': True},
        VNIC_TYPE: {'allow_post': True, 'allow_put': True,
                    'default': VNIC_NORMAL,
                    'is_visible': True,
                    'validate': {'type:values': VNIC_TYPES},
                    'enforce_policy': True},
        HOST_ID: {'allow_post': True, 'allow_put': True,
                  'default': constants.ATTR_NOT_SPECIFIED,
                  'is_visible': True,
                  'is_filter': True,
                  'enforce_policy': True},
        PROFILE: {'allow_post': True, 'allow_put': True,
                  'default': constants.ATTR_NOT_SPECIFIED,
                  'enforce_policy': True,
                  'validate': {'type:dict_or_none': None},
                  'is_visible': True},
    }
}

# The subresource attribute map for the extension. It adds child resources
# to main extension's resource. The subresource map must have a parent and
# a parameters entry. If an extension does not need such a map, None can
# be specified (mandatory).
SUB_RESOURCE_ATTRIBUTE_MAP = None

# The action map: it associates verbs with methods to be performed on
# the API resource. For example:
#
# ACTION_MAP = {
#     RESOURCE_NAME: {
#        'add_my_foo_bars': 'PUT',
#        'remove_my_foo_bars': 'PUT',
#        'get_my_foo_bars': 'GET'
#    }
# }
ACTION_MAP = {
}

# The action status.
ACTION_STATUS = {
}

# The list of required extensions.
REQUIRED_EXTENSIONS = [
]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = [
]
