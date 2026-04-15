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

# This role is used only for communication between services, it shouldn't be
# used by human users
SERVICE = 'rule:service_api'

# For completion of the phase 1
# https://governance.openstack.org/tc/goals/selected/consistent-and-secure-rbac.html#phase-1
# there is now ADMIN role
ADMIN = "rule:admin_only"

# This check string is the primary use case for the project's manager who is
# more privileged user then typical MEMBER of the project.
PROJECT_MANAGER = 'role:manager and project_id:%(project_id)s'

# This check string is the primary use case for typical end-users, who are
# working with resources that belong to a project (e.g., creating ports and
# routers).
PROJECT_MEMBER = 'role:member and project_id:%(project_id)s'

# This check string should only be used to protect read-only project-specific
# resources. It should not be used to protect APIs that make writable changes
# (e.g., updating a router or deleting a port).
PROJECT_READER = 'role:reader and project_id:%(project_id)s'

# The following are common composite check strings that are useful for
# protecting APIs designed to operate with multiple scopes (e.g.,
# an administrator should be able to delete any router in the deployment, a
# project member should only be able to delete routers in their project).
ADMIN_OR_SERVICE = (
    '(' + ADMIN + ') or (' + SERVICE + ')')
ADMIN_OR_PROJECT_MANAGER = (
    '(' + ADMIN + ') or (' + PROJECT_MANAGER + ')')
ADMIN_OR_PROJECT_MEMBER = (
    '(' + ADMIN + ') or (' + PROJECT_MEMBER + ')')
ADMIN_OR_PROJECT_READER = (
    '(' + ADMIN + ') or (' + PROJECT_READER + ')')

# In some cases we need to check owner of the parent resource, it's like that
# for example for QoS rules (check owner of QoS policy rule belongs to) or
# Floating IP port forwarding (check owner of FIP which PF is using). It's like
# that becasue those resources (QOS rules, FIP PFs) don't have project_id
# attribute at all and they belongs to the same project as parent resource (QoS
# policy, FIP).
RULE_PARENT_OWNER = 'rule:ext_parent_owner'
PARENT_OWNER_MANAGER = 'role:manager and ' + RULE_PARENT_OWNER
PARENT_OWNER_MEMBER = 'role:member and ' + RULE_PARENT_OWNER
PARENT_OWNER_READER = 'role:reader and ' + RULE_PARENT_OWNER
ADMIN_OR_PARENT_OWNER_MANAGER = (
    '(' + ADMIN + ') or (' + PARENT_OWNER_MANAGER + ')')
ADMIN_OR_PARENT_OWNER_MEMBER = (
    '(' + ADMIN + ') or (' + PARENT_OWNER_MEMBER + ')')
ADMIN_OR_PARENT_OWNER_READER = (
    '(' + ADMIN + ') or (' + PARENT_OWNER_READER + ')')
