# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from collections.abc import Callable, Iterable
from typing import TypedDict, TypeAlias


AttributeValidator = TypedDict(
    'AttributeValidator',
    {
        'type:allowed_address_pairs': None,
        'type:availability_zone_hint_list': None,
        'type:boolean': None,
        'type:dict': dict[str, object] | None,
        'type:dict_or_none': dict[str, object] | None,
        'type:dict_or_empty': dict[str, object] | None,
        'type:dict_or_nodata': dict[str, object] | None,
        'type:dns_domain_name': int | None,
        'type:dns_host_name': int | None,
        'type:fip_dns_host_name': int | None,
        'type:fixed_ips': None,
        'type:hostroutes': None,
        'type:ip_address': None,
        'type:ip_address_or_none': None,
        'type:ip_pools': None,
        'type:ip_or_subnet_or_none': None,
        'type:list_of_any_key_specs_or_none': list[dict[str, object]] | None,
        'type:list_of_dict_or_nodata': dict[str, object] | None,
        'type:list_of_regex_or_none': str | None,
        'type:list_of_subnet_service_types': None,
        'type:list_of_subnets_or_none': None,
        'type:mac_address': None,
        'type:nameservers': None,
        'type:name_string': int | None,
        'type:name_string_or_none': int | None,
        'type:network_segments': None,
        'type:not_empty_name_string': None,
        'type:non_negative': None,
        'type:port_range': tuple[int, int] | None,
        'type:range': tuple[int, int],
        'type:range_or_none': tuple[int, int],
        'type:regex_or_none': str | None,
        'type:service_plugin_type': None,
        'type:string': int | None,
        'type:string_or_none': int | None,
        'type:subnetpool_id_or_none': None,
        'type:subnet': None,
        'type:subnet_list': None,
        'type:subnet_or_none': None,
        'type:subports': None,
        'type:uuid': None,
        'type:uuid_list': None,
        'type:uuid_list_non_empty': None,
        'type:uuid_or_none': None,
        'type:values': Iterable[object],
    },
    total=False,
)


class ResourceAttributeMapItem(TypedDict, total=False):
    allow_post: bool
    allow_put: bool
    convert_to: Callable[[object], object]
    convert_list_to: Callable[[object], object]
    default: object
    default_overrides_none: bool
    dict_populate_defaults: bool
    enforce_policy: bool
    is_visible: bool
    is_filter: bool
    is_sort_key: bool
    required_by_policy: bool
    primary_key: bool
    validate: AttributeValidator


ResourceAttributeMap: TypeAlias = dict[
    str, dict[str, ResourceAttributeMapItem]
]


class SubResourceParent(TypedDict):
    collection_name: str
    member_name: str


class SubResourceAttributeMapItem(TypedDict, total=False):
    parent: SubResourceParent
    parameters: dict[str, ResourceAttributeMapItem]


SubResourceAttributeMap: TypeAlias = dict[str, SubResourceAttributeMapItem]
