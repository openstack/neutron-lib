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

from unittest import mock

from neutron_lib.api.validators import dns
from neutron_lib.db import constants as db_constants
from neutron_lib.tests import _base as base


class TestDnsValidators(base.BaseTestCase):

    @mock.patch('oslo_config.cfg.CONF')
    def test_validate_dns_name(self, CONF):
        CONF.dns_domain = ''
        msg = dns.validate_dns_name('')
        self.assertIsNone(msg)

        CONF.dns_domain = 'example.org.'
        dns_name = 'host'
        msg = dns.validate_dns_name(dns_name)
        self.assertIsNone(msg)

        invalid_data = 'A' * 256
        max_len = 255
        expected = (f"'{invalid_data}' not a valid PQDN or FQDN. Reason: "
                    f"'{invalid_data}' exceeds the {max_len} character FQDN "
                    "limit")
        msg = dns.validate_dns_name(invalid_data, max_len)
        self.assertEqual(expected, msg)

        invalid_data = '.hostname'
        expected = (f"'{invalid_data}' not a valid PQDN or FQDN. Reason: "
                    "Encountered an empty component")
        msg = dns.validate_dns_name(invalid_data)
        self.assertEqual(expected, msg)

        invalid_data = 'hostname-'
        expected = (f"'{invalid_data}' not a valid PQDN or FQDN. Reason: "
                    f"Name '{invalid_data}' must not start or end with a "
                    "hyphen")
        msg = dns.validate_dns_name(invalid_data)
        self.assertEqual(expected, msg)

        invalid_data = 'hostname@host'
        expected = (f"'{invalid_data}' not a valid PQDN or FQDN. Reason: "
                    f"Name '{invalid_data}' must be 1-63 characters long, "
                    "each of which can only be alphanumeric or a "
                    "hyphen")
        msg = dns.validate_dns_name(invalid_data)
        self.assertEqual(expected, msg)
        invalid_suffix = '1234'
        invalid_data = 'hostname.' + invalid_suffix
        expected = (f"'{invalid_data}' not a valid PQDN or FQDN. Reason: "
                    f"TLD '{invalid_suffix}' must not be all "
                    "numeric")
        msg = dns.validate_dns_name(invalid_data)
        self.assertEqual(expected, msg)

        # len(dns_name + dns_domain) > 255
        invalid_domain = 'A' * 250 + '.org.'
        CONF.dns_domain = invalid_domain
        dns_name = 'hostname'
        expected = ("The dns_name passed is a PQDN and its size is "
                    f"'{len(dns_name)}'. The dns_domain option in "
                    f"neutron.conf is set to {invalid_domain}, with a "
                    f"length of '{len(invalid_domain) + 1}'. When the two are "
                    "concatenated to form a FQDN (with a '.' at the end), "
                    "the resulting length exceeds the maximum size "
                    f"of '{db_constants.FQDN_FIELD_SIZE}'"
                    )
        msg = dns.validate_dns_name(dns_name)
        self.assertEqual(expected, msg)

        dns_name = 'host.'
        dns_domain = 'example.com.'
        CONF.dns_domain = dns_domain
        expected = ("The dns_name passed is a FQDN. Its higher level labels "
                    "must be equal to the dns_domain option in neutron.conf, "
                    f"that has been set to '{dns_domain}'. It must also "
                    "include one or more valid DNS labels to the left "
                    f"of '{dns_domain}'")
        msg = dns.validate_dns_name(dns_name)
        self.assertEqual(expected, msg)

    def test_validate_fip_dns_name(self):
        # Don't run tests duplicated to validate_dns_name()

        msg = dns.validate_fip_dns_name('')
        self.assertIsNone(msg)

        msg = dns.validate_fip_dns_name('host')
        self.assertIsNone(msg)

        invalid_data = 1234
        expected = f"'{invalid_data}' is not a valid string"
        msg = dns.validate_fip_dns_name(invalid_data)
        self.assertEqual(expected, msg)

        invalid_data = 'host.'
        expected = (f"'{invalid_data}' is a FQDN. It should be a relative "
                    "domain name")
        msg = dns.validate_fip_dns_name(invalid_data)
        self.assertEqual(expected, msg)

        length = 10
        invalid_data = 'a' * length
        max_len = 12
        expected = (f"'{invalid_data}' contains {length} characters. Adding a "
                    "domain name will cause it to exceed the maximum length "
                    f"of a FQDN of '{max_len}'")
        msg = dns.validate_fip_dns_name(invalid_data, max_len)
        self.assertEqual(expected, msg)

    def test_validate_dns_domain(self):
        # Don't run tests duplicated to validate_dns_name()

        msg = dns.validate_dns_domain('')
        self.assertIsNone(msg)

        msg = dns.validate_dns_domain('example.com.')
        self.assertIsNone(msg)

        invalid_data = 1234
        expected = f"'{invalid_data}' is not a valid string"
        msg = dns.validate_dns_domain(invalid_data)
        self.assertEqual(expected, msg)

        invalid_data = 'example.com'
        expected = f"'{invalid_data}' is not a FQDN"
        msg = dns.validate_dns_domain(invalid_data)
        self.assertEqual(expected, msg)

        length = 9
        invalid_data = 'a' * length + '.'
        max_len = 11
        expected = (f"'{invalid_data}' contains {length + 1} characters. "
                    "Adding a sub-domain will cause it to exceed the maximum "
                    f"length of a FQDN of '{max_len}'")
        msg = dns.validate_dns_domain(invalid_data, max_len)
        self.assertEqual(expected, msg)
