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


DB Model Query
==============

The implementation in ``neutron_lib.db.model_query`` is intended to be used as a
stepping stone for existing consumers using standard database models/tables.
Moving forward new database implementations should all use neutron's Versioned
Object approach, while existing model based implementations should begin
migrating to Versioned Objects.


Registering Hooks
-----------------

The ``neutron_lib.db.model_query.register_hook`` function allows hooks to be
registered for invocation during a respective database query.

Each hook has three components:

- "query": used to build the query expression
- "filter": used to build the filter expression
- "result_filters": used for final filtering on the query result

Query hooks take as input the query being built and return a transformed
query expression. For example::

    def mymodel_query_hook(context, original_model, query):
        augmented_query = ...
        return augmented_query

Filter hooks take as input the filter expression being built and return
a transformed filter expression. For example::

    def mymodel_filter_hook(context, original_model, filters):
        refined_filters = ...
        return refined_filters

Result filter hooks take as input the query expression and the filter
expression, and return a final transformed query expression. For example::

    def mymodel_result_filter_hook(query, filters):
        final_filters = ...
        return query.filter(final_filters)

