# Copyright (c) 2017 Juniper Networks, Inc. All rights reserved.
# All Rights Reserved.
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

from unittest import skip

import mock

from rally_contrail import credential


def test_to_dict():
    cred = credential.ContrailCredential("foo_host", 1234, 15)
    assert {"host": "foo_host", "port": 1234, "timeout": 15} == cred.to_dict()


@skip("Mock does not work")
@mock.patch("contrail_api_cli.client.SessionLoader")
@mock.patch("contrail_api_cli.schema.DummySchema")
@mock.patch("contrail_api_cli.resource.Collection")
def test_verify_connection(mock_session_loader, mock_dummy_schema,
                           mock_collection):
    cred = credential.ContrailCredential("foo_host", 1234, 15)
    cred.verify_connection()
    mock_session_loader.make.assert_called_once_with(
        host='foo_host',
        port=1234,
        os_username="fake",
        os_password="fake",
        os_cacert=None,
        os_cert=None,
        os_key=None,
        insecure=False,
        timeout=15,
        collect_timing=None)
    mock_dummy_schema.assert_called_once()
    mock_collection.assert_called_once_with('', fetch=True)
