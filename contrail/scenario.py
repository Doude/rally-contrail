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

import functools
import random

from rally.task import scenario

configure = functools.partial(scenario.configure, namespace="contrail")


class ContrailScenario(scenario.Scenario):
    """Base class for all Contrail scenarios."""

    def __init__(self, context=None):
        super(ContrailScenario, self).__init__(context)

        if context:
            self._choose_project(context)
            # self._get_api_session(context)

    def _choose_project(self, context):
        """Choose one project from projects context

        We are choosing on each iteration one project

        """
        if context["project_choice_method"] == "random":
            project = random.choice(context["projects"].values())
        else:
            # Second and last case - 'round_robin'.
            projects_amount = len(context["projects"].values())
            iteration = context["iteration"] - 1
            project_index = int(iteration % projects_amount)
            project_id = sorted(context["projects"].keys())[project_index]
            project = context["projects"][project_id]

        context["project"] = project

    # def _get_api_session(self, context):
    #     from contrail_api_cli.client import SessionLoader
    #
    #     creds = context['admin']['credential']
    #     context["session"] = SessionLoader().make(
    #         host=creds.host,
    #         port=creds.port,
    #         os_username="fake",
    #         os_password="fake",
    #         os_cacert=None,
    #         os_cert=None,
    #         os_key=None,
    #         insecure=False,
    #         timeout=creds.timeout,
    #     )
