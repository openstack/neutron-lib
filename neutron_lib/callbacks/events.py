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

# String literals representing events associated to data store operations
BEFORE_CREATE = 'before_create'
BEFORE_READ = 'before_read'
BEFORE_UPDATE = 'before_update'
BEFORE_DELETE = 'before_delete'

PRECOMMIT_CREATE = 'precommit_create'
PRECOMMIT_UPDATE = 'precommit_update'
PRECOMMIT_DELETE = 'precommit_delete'
PRECOMMIT_ADD_ASSOCIATION = 'precommit_add_association'
PRECOMMIT_DELETE_ASSOCIATIONS = 'precommit_delete_associations'

AFTER_CREATE = 'after_create'
AFTER_READ = 'after_read'
AFTER_UPDATE = 'after_update'
AFTER_DELETE = 'after_delete'

# String literals representing events associated to API operations
BEFORE_RESPONSE = 'before_response'
AFTER_REQUEST = 'after_request'

# String literals representing events associated to process operations
BEFORE_INIT = 'before_init'
BEFORE_SPAWN = 'before_spawn'  # sent per process
AFTER_SPAWN = 'after_spawn'  # sent per process
AFTER_INIT = 'after_init'  # sent per worker

# String literals representing events associated to error conditions
ABORT_CREATE = 'abort_create'
ABORT_READ = 'abort_read'
ABORT_UPDATE = 'abort_update'
ABORT_DELETE = 'abort_delete'

ABORT = 'abort_'
BEFORE = 'before_'
PRECOMMIT = 'precommit_'

OVS_RESTARTED = 'ovs_restarted'


class EventPayload(object):
    """Base event payload object.

    This class is intended to be the super class for all event payloads. As
    such, it defines common attributes many events are likely to use in their
    payload. Note that event attributes are passed by reference; no copying
    of states, metadata or request_body is performed and thus consumers should
    not modify payload references.

    For more information, see the callbacks dev-ref documentation for this
    project.
    """

    def __init__(self, context, metadata=None, request_body=None,
                 states=None, resource_id=None):
        # the event context
        self.context = context

        # NOTE(boden): longer term we should consider removing metadata
        # optional 'unstructured' (key,value) pairs for special needs
        self.metadata = metadata if metadata else {}

        # the request body associated to the resource
        self.request_body = request_body

        # an iterable of states for the resource from the newest to the oldest
        # for example db states or api request/response
        # the actual object type for states will vary depending on event caller
        self.states = states if states else []

        # a unique ID for the event resource; may be None if the resource
        # isn't created yet
        self.resource_id = resource_id

    @property
    def has_states(self):
        """Determines if this event payload has any states.

        :returns: True if this event payload has states, otherwise False.
        """
        return len(self.states) > 0

    @property
    def latest_state(self):
        """Returns the latest state for the event payload.

        :returns: The last state of this event payload if has_state else None.
        """
        return self.states[-1] if self.has_states else None


class DBEventPayload(EventPayload):
    """The payload for data store events payloads."""

    def __init__(self, context, metadata=None, request_body=None,
                 states=None, resource_id=None, desired_state=None):

        super().__init__(
            context, metadata=metadata, request_body=request_body,
            states=states, resource_id=resource_id)

        # the model object to be persisted in pre create/commit payloads
        self.desired_state = desired_state

    @property
    def is_persisted(self):
        """Determine if the resource for this event payload is persisted.

        :returns: True if this payload's resource is persisted, otherwise
            False.
        """
        return self.resource_id is not None and self.has_states

    @property
    def is_to_be_committed(self):
        """"Determine if the event payload resource is to be committed.

        :returns:  True if the desired state has been populated, else False.
        """
        return self.desired_state is not None

    @property
    def latest_state(self):
        """Returns the latest state for the event payload resource.

        :returns: If this payload has a desired_state its returned, otherwise
            latest_state is returned.
        """
        return (self.desired_state or super().latest_state)


class APIEventPayload(EventPayload):
    """The payload for API events."""

    def __init__(self, context, method_name, action,
                 metadata=None, request_body=None, states=None,
                 resource_id=None, collection_name=None):

        super().__init__(
            context, metadata=metadata, request_body=request_body,
            states=states, resource_id=resource_id)

        self.method_name = method_name
        self.action = action
        self.collection_name = collection_name
