# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

import unittest

import mock

from hpOneView.connection import connection
from hpOneView.resources.networking.interconnects import Interconnects
from hpOneView.resources.resource import Resource


class InterconnectsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._interconnects = Interconnects(self.connection)
        self._interconnects.data = {'uri': '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20'}

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_get')
    def test_get_statistics(self, mock_get, load_resource):
        self._interconnects.get_statistics()

        uri = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/statistics'

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_get')
    def test_get_statistics_with_port_name(self, mock_get, load_resource):
        self._interconnects.get_statistics('d1')

        uri = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/statistics/d1'

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_get')
    def test_get_interconnect_name_servers(self, mock_get, load_resource):
        uri = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/nameServers'

        self._interconnects.get_name_servers()
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_get')
    def test_get_statistics_with_port_name_and_subport(self, mock_get, load_resource):
        self._interconnects.get_subport_statistics('d1', 1)

        uri = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/statistics/d1/subport/1'

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_interconnect_by_uri(self, mock_get):
        uri = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20'

        self._interconnects.get_by_uri(uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'get_by')
    def test_get_interconnect_by_key(self, mock_get_by):
        field = 'name'
        value = 'fakeName'

        self._interconnects.get_by(field, value)
        mock_get_by.assert_called_once_with(field, value)

    @mock.patch.object(Resource, 'get_by_name')
    def test_get_interconnect_by_name(self, mock_get_by_name):
        name = 'fakeName'

        self._interconnects.get_by_name(name)
        mock_get_by_name.assert_called_once_with(name)

    @mock.patch.object(Resource, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._interconnects.get_all(2, 5, filter, sort)
        mock_get_all.assert_called_once_with(2, 5, filter, sort)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'patch_request')
    def test_patch_interconnect_should_return_the_task(self, mock_patch, load_resource):
        operation = 'replace'
        path = '/powerState'
        value = 'On'
        timeout = 10
        patch_request_body = [{'op': operation, 'path': path, 'value': value}]
        self._interconnects.patch(operation, path, value, timeout)
        mock_patch.assert_called_once_with(body=patch_request_body, timeout=timeout)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_put')
    def test_update_interconnect_port(self, mock_put, load_resource):
        url = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/ports'
        information = {
            "type": "port",
            "bayNumber": 1,
        }
        self._interconnects.update_port(information)
        mock_put.assert_called_once_with(url, information, -1, None)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'update_with_zero_body')
    def test_reset_port_protection(self, mock_update, load_resource):
        url = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/resetportprotection'
        self._interconnects.reset_port_protection()
        mock_update.assert_called_once_with(url, timeout=-1)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'update_with_zero_body')
    def test_reset_statistics(self, mock_update, load_resource):
        url = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/statistics/reset'
        self._interconnects.reset_statistics()
        mock_update.assert_called_once_with(url, timeout=-1)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_put')
    def test_update_ports(self, mock_put, load_resource):
        url = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/update-ports'

        port1 = {
            "type": "port2",
            "portName": "d1",
            "enabled": False,
            "portId": "5v8f3ec0-52t4-475a-84g4-c4iod72d2c20:d1"
        }
        port2 = {
            "portName": "d2",
            "enabled": False,
            "portId": "5v8f3ec0-52t4-475a-84g4-c4iod72d2c20:d2"
        }
        ports = [port1, port2]

        clone = port2.copy()
        clone["type"] = "port"
        expected_ports = [port1, clone]

        self._interconnects.update_ports(ports)
        mock_put.assert_called_once_with(url, expected_ports, -1, None)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'get_all')
    def test_get_ports_called_once(self, mock_get_all, load_resource):
        uri = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/ports'

        self._interconnects.get_ports(2, 5)

        mock_get_all.assert_called_once_with(2, 5, uri=uri)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'get_all')
    def test_get_ports_called_once_with_defaults(self, mock_get_all, load_resource):
        uri = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/ports'

        self._interconnects.get_ports(0, -1)

        mock_get_all.assert_called_once_with(0, -1, uri=uri)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_get')
    def test_get_ports_should_return_the_ports(self, mock_get, load_resource):
        port_id = "88888"

        ports = [{"mock": "value"}, {"mock": "value2"}]
        mock_get.return_value = ports

        result = self._interconnects.get_port(port_id)

        self.assertEqual(result, ports)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_get')
    def test_get_port_called_once(self, mock_get, load_resource):
        port_id = "88888"
        uri = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/ports/88888'

        self._interconnects.get_port(port_id)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_get')
    def test_get_port_should_return_the_port(self, mock_get, load_resource):
        port_id = "88888"

        mock_get.return_value = {"mock": "value"}

        result = self._interconnects.get_port(port_id)

        self.assertEqual(result, {"mock": "value"})

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'update_with_zero_body')
    def test_update_configuration_by_uri(self, mock_update_with_zero_body, load_resource):
        uri_rest_call = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/configuration'
        self._interconnects.update_configuration()

        mock_update_with_zero_body.assert_called_once_with(uri_rest_call, timeout=-1)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_get')
    def test_get_pluggable_module_information(self, mock_get, load_resource):
        self._interconnects.get_pluggable_module_information()

        uri = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/pluggableModuleInformation'

        mock_get.assert_called_once_with(uri)
