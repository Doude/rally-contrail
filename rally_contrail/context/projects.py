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

import collections

from contrail_api_cli.resource import Resource
from contrail_api_cli.exceptions import SystemResource
from contrail_api_cli.exceptions import BackRefsExists
from rally.common import cfg
from rally.common import broker
from rally import consts
from rally import exceptions
from rally.common import logging
from rally.task import context

from rally_contrail import credential


LOG = logging.getLogger(__name__)
CONF = cfg.CONF
RESOURCE_MANAGEMENT_WORKERS_DESCR = ("The number of concurrent threads to use "
                                     "for serving project context.")
PROJECT_DOMAIN_DESCR = "Name of domain in which projects will be created."


@context.configure(name="projects", platform="contrail", order=100)
class ProjectGenerator(context.Context):
    """Context class for generating temporary projects for benchmarks."""

    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": consts.JSON_SCHEMA,
        "additionalProperties": False,
        "properties": {
            "projects": {
                "type": "integer",
                "minimum": 1,
                "description": "The number of project to create."
            },
            "resource_management_workers": {
                "type": "integer",
                "minimum": 1,
                "description": RESOURCE_MANAGEMENT_WORKERS_DESCR,

            },
            "project_domain": {
                "type": "string",
                "description": PROJECT_DOMAIN_DESCR
            },
            "project_choice_method": {
                "enum": ["random", "round_robin"],
                "description": "The mode of balancing usage of project "
                               "between scenario iterations."
            },
        },
    }

    DEFAULT_CONFIG = {
        "projects": 1,
        "resource_management_workers":
            cfg.CONF.contrail.projects_context_resource_management_workers,
        "project_domain": "default-domain",
        "project_choice_method": "random",
    }

    def __init__(self, context):
        super(ProjectGenerator, self).__init__(context)
        self.context["credential"] = credential.ContrailCredential(
            **self.env["platforms"]["contrail"])
        self.context["credential"].verify_connection()

    def _create_projects(self):
        threads = self.config["resource_management_workers"]

        projects = collections.deque()

        def publish(queue):
            domain = Resource('domain',
                              fq_name=self.config['project_domain'],
                              fetch=True)
            for _ in range(self.config["projects"]):
                queue.append(domain)

        def consume(cache, domain):
            fq_name = "%s:%s" % (domain.fq_name, self.generate_random_name())
            LOG.debug("Creating projects %s" % fq_name)
            project = Resource('project', parent=domain, fq_name=fq_name)
            project.save()
            projects.append(project)

        broker.run(publish, consume, threads)

        projects_dict = {}
        for t in projects:
            projects_dict[t["uuid"]] = t

        return projects_dict

    def _get_back_refs(self, resource, back_refs):
        resource.fetch()
        if resource in back_refs:
            back_refs.remove(resource)
        back_refs.append(resource)
        for back_ref in resource.back_refs:
            if back_ref in back_refs and back_ref.uuid == resource.parent.uuid:
                continue
            back_refs = self._get_back_refs(back_ref, back_refs)
        for children in resource.children:
            back_refs = self._get_back_refs(children, back_refs)
        return back_refs

    def _delete_projects(self):
        threads = self.config["resource_management_workers"]

        def publish(queue):
            for _, project in self.context["projects"].items():
                queue.append(project)

        def consume(cache, project):
            LOG.debug("Deleting projects %s" % project.fq_name)
            resources_to_delete = self._get_back_refs(project, [])
            for resource in reversed(resources_to_delete):
                LOG.debug("Deleting %s %s" % (resource.type, resource.fq_name))
                try:
                    resource.delete()
                except SystemResource as e:
                    # Ignore failure on system resources
                    LOG.debug('Failed to delete system resource %s: %s' %
                              (resource, str(e)))
                    pass
                except BackRefsExists:
                    # Ignore deleting default project APS as it have a backref
                    # to the project. It will be removed by the API server when
                    # project will be deleted
                    if resource.type == 'application-policy-set':
                        pass

        broker.run(publish, consume, threads)

        self.context["projects"] = {}

    def setup(self):
        """Create projects, using the broker pattern."""
        self.context["projects"] = {}
        self.context["project_choice_method"] =\
            self.config["project_choice_method"]

        threads = self.config["resource_management_workers"]

        LOG.debug("Creating %(projects)d projects using %(threads)s threads" %
                  {"projects": self.config["projects"], "threads": threads})
        self.context["projects"] = self._create_projects()

        if len(self.context["projects"]) < self.config["projects"]:
            raise exceptions.ContextSetupFailure(
                ctx_name=self.get_name(),
                msg="Failed to create the requested number of projects.")

    def cleanup(self):
        """Delete projects, using the broker pattern."""
        self._delete_projects()
