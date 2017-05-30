# Copyright (c) 2017 Juniper Networks, Inc. All rights reserved.
#
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

from contrail import scenario
from rally.task import validation

import utils


@validation.add("required_platform", platform="contrail", admin=True)
@scenario.configure(name='config.create_and_list_virtual_networks')
class CreateAndListVirtualNetworks(utils.ContrailScenario):

    def run(self, virtual_network_create_args=None):
        """Create and list all virtual networks.

        Measure Contrail config API listing virtual networks performance.
        If you have only 1 user in your context, you will
        add 1 network on every iteration. So you will have more
        and more networks and will be able to measure the
        performance of listing virtual networks depending on
        the number of networks owned by users.

        :param virtual_network_create_args: dict, POST /virtual-networks
                                                  request options
        """
        self._create_virtual_network(virtual_network_create_args or {})
        self._list_virtual_networks()
