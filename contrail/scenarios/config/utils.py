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

from contrail_api_cli.resource import Collection
from contrail_api_cli.resource import Resource
from oslo_config import cfg

from rally.common import logging
from rally.task import atomic

from contrail import scenario

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class ContrailScenario(scenario.ContrailScenario):
    """Base class for Contrail scenarios with basic atomic actions."""

    @atomic.action_timer("config.create_virtual_network")
    def _create_virtual_network(self, virtual_network_create_args):
        """Create contrail virtual network.
        :param virtual_network_create_args: dict, POST /virtual-networks
                                            request options
        :returns: contrail virtual network dict
        """

        project = self.context['project']
        virtual_network = Resource(
            'virtual-network',
            # session=self.context['session'],
            parent=project,
            fq_name=list(project.fq_name) + [self.generate_random_name()],
            **virtual_network_create_args
        )
        virtual_network.save()
        return virtual_network

    @atomic.optional_action_timer("config.list_virtual_networks")
    def _list_virtual_networks(self, **kwargs):
        """Return project virtual networks list.
        :param atomic_action: True if this is an atomic action. added
                              and handled by the optional_action_timer()
                              decorator
        :param kwargs: virtual network list options
        """

        return Collection(
            'virtual-network',
            # session=self.context['session'],
            **kwargs
        )
