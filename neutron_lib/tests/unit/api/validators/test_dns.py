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
        expected = ("'%(data)s' not a valid PQDN or FQDN. Reason: "
                    "'%(data)s' exceeds the %(maxlen)s character FQDN "
                    "limit") % {'data': invalid_data, 'maxlen': max_len}
        msg = dns.validate_dns_name(invalid_data, max_len)
        self.assertEqual(expected, msg)

        invalid_data = '.hostname'
        expected = ("'%(data)s' not a valid PQDN or FQDN. Reason: "
                    "Encountered an empty component") % {'data': invalid_data}
        msg = dns.validate_dns_name(invalid_data)
        self.assertEqual(expected, msg)

        invalid_data = 'hostname-'
        expected = ("'%(data)s' not a valid PQDN or FQDN. Reason: "
                    "Name '%(data)s' must not start or end with a "
                    "hyphen") % {'data': invalid_data}
        msg = dns.validate_dns_name(invalid_data)
        self.assertEqual(expected, msg)

        invalid_data = 'hostname@host'
        expected = ("'%(data)s' not a valid PQDN or FQDN. Reason: "
                    "Name '%(data)s' must be 1-63 characters long, each of "
                    "which can only be alphanumeric or a "
                    "hyphen") % {'data': invalid_data}
        msg = dns.validate_dns_name(invalid_data)
        self.assertEqual(expected, msg)
        invalid_suffix = '1234'
        invalid_data = 'hostname.' + invalid_suffix
        expected = ("'%(data)s' not a valid PQDN or FQDN. Reason: "
                    "TLD '%(suffix)s' must not be all "
                    "numeric") % {'data': invalid_data,
                                  'suffix': invalid_suffix}
        msg = dns.validate_dns_name(invalid_data)
        self.assertEqual(expected, msg)

        # len(dns_name + dns_domain) > 255
        invalid_domain = 'A' * 250 + '.org.'
        CONF.dns_domain = invalid_domain
        dns_name = 'hostname'
        expected = ("The dns_name passed is a PQDN and its size is "
                    "'%(dns_name_len)s'. The dns_domain option in "
                    "neutron.conf is set to %(dns_domain)s, with a "
                    "length of '%(higher_labels_len)s'. When the two are "
                    "concatenated to form a FQDN (with a '.' at the end), "
                    "the resulting length exceeds the maximum size "
                    "of '%(fqdn_max_len)s'"
                    ) % {'dns_name_len': len(dns_name),
                         'dns_domain': invalid_domain,
                         'higher_labels_len': len(invalid_domain) + 1,
                         'fqdn_max_len': db_constants.FQDN_FIELD_SIZE}
        msg = dns.validate_dns_name(dns_name)
        self.assertEqual(expected, msg)

        dns_name = 'host.'
        dns_domain = 'example.com.'
        CONF.dns_domain = dns_domain
        expected = ("The dns_name passed is a FQDN. Its higher level labels "
                    "must be equal to the dns_domain option in neutron.conf, "
                    "that has been set to '%(dns_domain)s'. It must also "
                    "include one or more valid DNS labels to the left "
                    "of '%(dns_domain)s'") % {'dns_domain': dns_domain}
        msg = dns.validate_dns_name(dns_name)
        self.assertEqual(expected, msg)

    def test_validate_fip_dns_name(self):
        # Don't run tests duplicated to validate_dns_name()

        msg = dns.validate_fip_dns_name('')
        self.assertIsNone(msg)

        msg = dns.validate_fip_dns_name('host')
        self.assertIsNone(msg)

        invalid_data = 1234
        expected = "'%s' is not a valid string" % invalid_data
        msg = dns.validate_fip_dns_name(invalid_data)
        self.assertEqual(expected, msg)

        invalid_data = 'host.'
        expected = ("'%s' is a FQDN. It should be a relative domain "
                    "name") % invalid_data
        msg = dns.validate_fip_dns_name(invalid_data)
        self.assertEqual(expected, msg)

        length = 10
        invalid_data = 'a' * length
        max_len = 12
        expected = ("'%(data)s' contains %(length)s characters. Adding a "
                    "domain name will cause it to exceed the maximum length "
                    "of a FQDN of '%(max_len)s'") % {"data": invalid_data,
                                                     "length": length,
                                                     "max_len": max_len}
        msg = dns.validate_fip_dns_name(invalid_data, max_len)
        self.assertEqual(expected, msg)

    def test_validate_dns_domain(self):
        # Don't run tests duplicated to validate_dns_name()

        msg = dns.validate_dns_domain('')
        self.assertIsNone(msg)

        msg = dns.validate_dns_domain('example.com.')
        self.assertIsNone(msg)

        invalid_data = 1234
        expected = "'%s' is not a valid string" % invalid_data
        msg = dns.validate_dns_domain(invalid_data)
        self.assertEqual(expected, msg)

        invalid_data = 'example.com'
        expected = "'%s' is not a FQDN" % invalid_data
        msg = dns.validate_dns_domain(invalid_data)
        self.assertEqual(expected, msg)

        length = 9
        invalid_data = 'a' * length + '.'
        max_len = 11
        expected = ("'%(data)s' contains %(length)s characters. Adding a "
                    "sub-domain will cause it to exceed the maximum length "
                    "of a FQDN of '%(max_len)s'") % {"data": invalid_data,
                                                     "length": length + 1,
                                                     "max_len": max_len}
        msg = dns.validate_dns_domain(invalid_data, max_len)
        self.assertEqual(expected, msg)
