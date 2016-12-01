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

from oslo_db.sqlalchemy import enginefacade


context_manager = enginefacade.transaction_context()
context_manager.configure(sqlite_fk=True)


# TODO(akamyshnikova): when all places in the code, which use sessions/
# connections will be updated, this won't be needed
def get_session(autocommit=True, expire_on_commit=False, use_slave=False):
    """Helper method to grab session."""
    return context_manager.get_legacy_facade().get_session(
        autocommit=autocommit, expire_on_commit=expire_on_commit,
        use_slave=use_slave)
