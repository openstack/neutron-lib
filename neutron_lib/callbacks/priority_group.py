# Copyright (c) 2018 Intel Corporation.
# Copyright (c) 2018 Isaku Yamahata <isaku.yamahata at intel com>
#                                   <isaku.yamahata at gmail com>
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


# NOTE(yamahata):smallest one is called first.
# we are using a big enough number for default that can
# be manipulated to increase or decrease the priorities.
# for all the callbacks, to reduce the priority division
# can be used for reducing that number for higher priority.
# each resources would want to define their own symbolic values for their use.

PRIORITY_DEFAULT = 55550000


# For l3 plugin and flavor
PRIORITY_ROUTER_EXTENDED_ATTRIBUTE = PRIORITY_DEFAULT - 100
# DEFAULT is reserved for third party which may not know priority yet
PRIORITY_ROUTER_DEFAULT = PRIORITY_DEFAULT
PRIORITY_ROUTER_CONTROLLER = PRIORITY_DEFAULT + 100
PRIORITY_ROUTER_DRIVER = PRIORITY_DEFAULT + 200
