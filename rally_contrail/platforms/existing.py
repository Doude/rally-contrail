# Copyright (c) 2019 Juniper Networks, Inc. All rights reserved.
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

import json
import traceback

from rally.common import logging
from rally.env import platform
from rally import exceptions

from rally_contrail import credential


LOG = logging.getLogger(__name__)


@platform.configure(name="existing", platform="contrail")
class Contrail(platform.Platform):
    """Default plugin for Contrail platform

    It may be used to test any existing Contrail VNC API compatible cloud.
    """
    VERSION_SCHEMA = {
        "anyOf": [
            {"type": "string", "description": "a string-like version."},
            {"type": "number", "description": "a number-like version."}
        ]
    }

    CONFIG_SCHEMA = {
        "type": "object",
        "properties": {
            "host": {"type": "string"},
            "port": {"type": "integer"},
        },
        "additionalProperties": False
    }

    def create(self):
        platform_data = {
            "host": '127.0.0.1',
            "port": 8082,
            "timeout": 10,
        }
        platform_data.update(self.spec)
        return platform_data, {}

    def destroy(self):
        pass

    def cleanup(self, task_uuid=None):
        return {
            "message": "Coming soon!",
            "discovered": 0,
            "deleted": 0,
            "failed": 0,
            "resources": {},
            "errors": []
        }

    def check_health(self):
        """Check whatever platform is alive."""
        try:
            credential.ContrailCredential(**self.platform_data)
        except exceptions.RallyException as e:
            return {"available": False, "message": e.format_message(),
                    # traceback is redundant here. Remove as soon as min
                    #   required rally version will be updated
                    #   More details here:
                    #       https://review.openstack.org/597197
                    "traceback": traceback.format_exc()}
        except Exception:
            if logging.is_debug():
                LOG.exception("Something unexpected had happened while "
                              "validating Contrail credentials.")
            return {
                "available": False,
                "message": (
                    "Failed to connect Contrail deployment:\n%s" %
                    json.dumps(self.platform_data, indent=2, sort_keys=True)),
                "traceback": traceback.format_exc()
            }

        return {"available": True}

    def info(self):
        """Return information about deployment as dict."""
        return {
            "info": {
                "services": [
                    {"type": "networking", "name": "Contrail"}
                ]
            }
        }

    @classmethod
    def create_spec_from_sys_environ(cls, sys_environ):
        """Create a spec based on system environment.

        .. envvar:: CONTRAIL_API_HOST
            Contrail API host to connect to

        .. envvar:: CONTRAIL_API_PORT
            Contrail API port to connect to
        """

        required_env_vars = ["CONTRAIL_API_HOST", "CONTRAIL_API_PORT"]
        missing_env_vars = [v for v in required_env_vars if
                            v not in sys_environ]
        if missing_env_vars:
            return {"available": False,
                    "message": "The following variable(s) are missed: %s" %
                               missing_env_vars}
        spec = {
            "host": sys_environ.get("CONTRAIL_API_HOST"),
            "port": sys_environ.get("CONTRAIL_API_PORT"),
        }

        return {"spec": spec, "available": True, "message": "Available"}

    def _get_validation_context(self):
        return {"existing_users@contrail": {}}
