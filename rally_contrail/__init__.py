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

from rally.common import cfg
from rally.common import opts as global_opts


OPTS = {"contrail": [
    cfg.IntOpt("projects_context_resource_management_workers",
               default=20,
               help="The number of concurrent threads to use for serving "
                    "projects context."),
    cfg.StrOpt("project_domain",
               default="default-domain",
               help="Domain name in which projects will be created."),
]}
global_opts.register()
global_opts.register_opts(OPTS.items())