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

import copy

from contrail_api_cli.client import SessionLoader
from contrail_api_cli.context import Context
from contrail_api_cli.schema import DummySchema
from contrail_api_cli.resource import Collection
from keystoneauth1.exceptions.connection import ConnectFailure

from rally.common import logging
from rally import exceptions

LOG = logging.getLogger(__file__)


class ContrailCredential(dict):
    """Credential for Contrail."""

    def __init__(self, host, port, timeout, **kwargs):
        if kwargs:
            raise TypeError("%s" % kwargs)
        super(ContrailCredential, self).__init__([
            ('host', host),
            ('port', port),
            ('timeout', timeout),
        ])

    def __getattr__(self, attr, default=None):
        return self.get(attr, default)

    def to_dict(self):
        return dict(self)

    def __deepcopy__(self, memodict=None):
        return self.__class__(**copy.deepcopy(self.to_dict()))

    def verify_connection(self):
        Context.session = SessionLoader().make(
            host=self.host,
            port=self.port,
            os_username="fake",
            os_password="fake",
            os_cacert=None,
            os_cert=None,
            os_key=None,
            insecure=False,
            timeout=self.timeout,
            collect_timing=None,
        )
        Context().schema = DummySchema()

        try:
            Collection('', fetch=True)
        except ConnectFailure as e:
            if logging.is_debug():
                LOG.exception(e)
            raise exceptions.RallyException("Unable to connect %s on port %s."
                                            % (self.host, self.port))
