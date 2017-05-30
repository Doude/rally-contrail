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

from contrail_api_cli.client import SessionLoader
from contrail_api_cli.context import Context
from contrail_api_cli.schema import DummySchema
from contrail_api_cli.resource import Collection

from rally.common import logging
from rally.deployment import credential
from rally import exceptions

LOG = logging.getLogger(__file__)


@credential.configure("contrail")
class ContrailCredential(credential.Credential):
    """Credential for Contrail."""

    def __init__(self, host, port, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout

    def to_dict(self):
        return {
            "host": self.host,
            "port": self.port,
            "timeout": self.timeout,
        }

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
        )
        Context().schema = DummySchema()

        from keystoneauth1.exceptions.connection import ConnectFailure
        try:
            Collection('', fetch=True)
        except ConnectFailure as e:
            if logging.is_debug():
                LOG.exception(e)
            raise exceptions.RallyException("Unable to connect %s on port %s."
                                            % (self.host, self.port))


@credential.configure_builder("contrail")
class ContrailCredentialBuilder(credential.CredentialBuilder):
    """Builds credentials provided by existing Cloud config."""

    CONFIG_SCHEMA = {
        "type": "object",
        "properties": {
            "host": {"type": "string"},
            "port": {"type": "integer"},
            "timeout": {"type": "integer"},
        },
        "required": ["host"],
        "additionalProperties": False,
    }

    def build_credentials(self):
        cred = ContrailCredential(
            self.config["host"],
            self.config.get("port", 8082),
            self.config.get("timeout", 10),
        )
        return {"admin": cred.to_dict(), "users": [cred.to_dict()]}
