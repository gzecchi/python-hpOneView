# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.resources.networking.fcoe_networks import FcoeNetworks
from hpOneView.resources.resource import ResourceClient


class FcoeNetworksTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._fcoe_networks = FcoeNetworks(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._fcoe_networks.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_given_values(self, mock_create):
        resource = {
            'name': 'vsan1',
            'vlanId': '201',
            'connectionTemplateUri': None,
            'type': 'fcoe-networkV2',
        }
        mock_create.return_value = {}

        self._fcoe_networks.create(resource, False)
        mock_create.assert_called_once_with(resource, False)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_default_values(self, mock_create):
        resource = {
            'name': 'OneViewSDK Test FCoE Network',
        }
        resource_with_default_values = {
            'name': 'OneViewSDK Test FCoE Network',
            'type': 'fcoe-network',
        }
        mock_create.return_value = {}

        self._fcoe_networks.create(resource)

        mock_create.assert_called_once_with(resource_with_default_values, True)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_given_values(self, mock_update):
        resource = {
            'name': 'vsan1',
            'vlanId': '201',
            'connectionTemplateUri': None,
            'type': 'fcoe-networkV2',
        }
        mock_update.return_value = {}

        self._fcoe_networks.update(resource, False)
        mock_update.assert_called_once_with(resource, False)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_default_values(self, mock_update):
        resource = {
            'name': 'OneViewSDK Test FCoE Network',
        }
        resource_with_default_values = {
            'name': 'OneViewSDK Test FCoE Network',
            'type': 'fcoe-network',
        }
        mock_update.return_value = {}

        self._fcoe_networks.update(resource)

        mock_update.assert_called_once_with(resource_with_default_values, True)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._fcoe_networks.delete(id, force=False, blocking=True)

        mock_delete.assert_called_once_with(id, force=False, blocking=True)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._fcoe_networks.get_by('name', 'OneViewSDK Test FCoE Network')

        mock_get_by.assert_called_once_with('name', 'OneViewSDK Test FCoE Network')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._fcoe_networks.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with('3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/fcoe-networks/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._fcoe_networks.get(uri)

        mock_get.assert_called_once_with(uri)
