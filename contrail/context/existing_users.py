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

from rally.task import context


@context.configure(name="existing_users", namespace="contrail", order=99,
                   hidden=True)
class ExistingUsers(context.Context):
    """This context supports using existing users in Rally."""

    def setup(self):
        super(ExistingUsers, self).setup()
        self.context["users"] = []

    def cleanup(self):
        """These users are not managed by Rally, so don't touch them."""
