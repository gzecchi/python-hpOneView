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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

from hpOneView.resources.resource import Resource, ensure_resource_client
from hpOneView.resources.resource import merge_default_values


class Interconnects(Resource):
    """
    Interconnects API client.

    """

    URI = '/rest/interconnects'

    def __init__(self, connection, options=None):
        super(Interconnects, self).__init__(connection, options)

    @ensure_resource_client
    def get_statistics(self, port_name=''):
        """
        Gets the statistics from an interconnect.

        Args:
            port_name (str): A specific port name of an interconnect.

        Returns:
             dict: The statistics for the interconnect that matches id.
        """
        uri = '{}/statistics'.format(self.data['uri'])

        if port_name:
            uri = uri + "/" + port_name

        return self.do_get(uri)

    @ensure_resource_client
    def get_subport_statistics(self, port_name, subport_number):
        """
        Gets the subport statistics on an interconnect.

        Args:
            port_name (str): A specific port name of an interconnect.
            subport_number (int): The subport.

        Returns:
             dict: The statistics for the interconnect that matches id, port_name, and subport_number.
        """
        uri = self.build_uri(self.data['uri']) + "/statistics/{0}/subport/{1}".format(port_name, subport_number)
        return self.do_get(uri)

    @ensure_resource_client
    def get_name_servers(self):
        """
        Gets the named servers for an interconnect.

        Returns:
             dict: the name servers for an interconnect.
        """
        uri = '{}/nameServers'.format(self.data['uri'])
        return self.do_get(uri)

    def patch(self, operation, path, value, timeout=-1):
        """
        Performs a specific patch operation for the given interconnect.

        There is a limited set of interconnect properties which might be changed.
        They are: 'powerState', 'uidState', and 'deviceResetState'.

        If the interconnect supports the operation, the operation is performed and
        a task is returned through which the results are reported.

        Args:
            operation:
                The type of operation: one of "add", "copy", "move", "remove", "replace", or "test".
            path:
                The JSON path the operation is to use. The exact meaning depends on the type of operation.
            value:
                The value to add or replace for "add" and "replace" operations or the value to compare against
                for a "test" operation. Not used by "copy", "move", or "remove".

        Returns:
            dict
        """
        patch_request_body = [{'op': operation, 'path': path, 'value': value}]

        self.data = self.patch_request(body=patch_request_body,
                                       timeout=timeout)
        return self

    @ensure_resource_client
    def update_port(self, port_information, timeout=-1):
        """
        Updates an interconnect port.

        Args:
            port_information (dict): object to update
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: The interconnect.

        """
        uri = '{}/ports'.format(self.data['uri'])
        return self.do_put(uri, port_information, timeout, None)

    @ensure_resource_client
    def update_ports(self, ports, timeout=-1):
        """
        Updates the interconnect ports.

        Args:
            ports (list): Ports to update.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: The interconnect.

        """
        resources = merge_default_values(ports, {'type': 'port'})

        uri = '{}/update-ports'.format(self.data['uri'])
        return self.do_put(uri, resources, timeout, None)

    @ensure_resource_client
    def reset_port_protection(self, timeout=-1):
        """
        Triggers a reset of port protection.

        Cause port protection to be reset on all the interconnects of the logical interconnect that matches ID.

        Args:
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: The interconnect.

        """
        uri = '{}/resetportprotection'.format(self.data['uri'])
        return self.update_with_zero_body(uri, timeout=timeout)

    @ensure_resource_client
    def reset_statistics(self, timeout=-1):
        """
        Reset the statistics of an interconnect.

        Returns:
             dict: The statistics for the interconnect that matches id.
        """
        uri = '{}/statistics/reset'.format(self.data['uri'])
        return self.update_with_zero_body(uri, timeout=timeout)

    @ensure_resource_client
    def get_ports(self, start=0, count=-1):
        """
        Gets all interconnect ports.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items.
                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.

        Returns:
            list: All interconnect ports.
        """
        uri = self.build_subresource_uri(resource_id_or_uri=self.data['uri'], subresource_path="ports")
        return self.get_all(start, count, uri=uri)

    @ensure_resource_client
    def get_port(self, port_id_or_uri):
        """
        Gets an interconnect port.

        Args:
            port_id_or_uri: The interconnect port id or uri.

        Returns:
            dict: The interconnect port.
        """
        uri = self.build_subresource_uri(self.data['uri'], port_id_or_uri, "ports")
        return self.do_get(uri)

    @ensure_resource_client
    def get_pluggable_module_information(self):
        """
        Gets all the pluggable module information.

        Returns:
            array: dicts of the pluggable module information.
        """
        uri = '{}/pluggableModuleInformation'.format(self.data['uri'])
        return self.do_get(uri)

    @ensure_resource_client
    def update_configuration(self, timeout=-1):
        """
        Reapplies the appliance's configuration on the interconnect. This includes running the same configure steps
        that were performed as part of the interconnect add by the enclosure.

        Args:
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Interconnect
        """
        uri = '{}/configuration'.format(self.data['uri'])
        return self.update_with_zero_body(uri, timeout=timeout)
