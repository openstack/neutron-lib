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

from neutron_lib.callbacks import manager


# TODO(armax): consider adding locking
_CALLBACK_MANAGER = None


def _get_callback_manager():
    global _CALLBACK_MANAGER
    if _CALLBACK_MANAGER is None:
        _CALLBACK_MANAGER = manager.CallbacksManager()
    return _CALLBACK_MANAGER


def subscribe(callback, resource, event):
    _get_callback_manager().subscribe(callback, resource, event)


def unsubscribe(callback, resource, event):
    _get_callback_manager().unsubscribe(callback, resource, event)


def unsubscribe_by_resource(callback, resource):
    _get_callback_manager().unsubscribe_by_resource(callback, resource)


def unsubscribe_all(callback):
    _get_callback_manager().unsubscribe_all(callback)


# NOTE(boden): This method is deprecated in favor of publish() and will be
# removed in Queens, but not deprecation message to reduce log flooding
def notify(resource, event, trigger, **kwargs):
    _get_callback_manager().notify(resource, event, trigger, **kwargs)


def publish(resource, event, trigger, payload=None):
    _get_callback_manager().publish(resource, event, trigger, payload=payload)


def clear():
    _get_callback_manager().clear()
