Standard query parameters are supported on the URI.
For more information, see `Filtering and Column Selection <#filtering>`__.

Use the ``fields`` query parameter to control which fields are returned
in the response body.
For more information, see `Fields <#fields>`__.

Pagination query parameters are supported if Neutron configuration supports
it by overriding ``allow_pagination=false``.
For more information, see `Pagination <#pagination>`__.

Sorting query parameters are supported if Neutron configuration supports
it with ``allow_sorting=true``.
For more information, see `Sorting <#sorting>`__.
