==============================
Contrail API Rally tests suite
==============================

What is it?
===========
This OpenStack Rally plugin adds a new Credential plugin to Rally that directly
requesting Contrail VNC API. This Credential plugin does not allow to use
Keystone authentication on the VNC config API.

How to use it
=============
Just `install Rally <http://docs.xrally.xyz/projects/openstack/en/latest/quick_start/tutorial/step_0_installation.html>`_
and clone that repository in ``/opt/rally/plugins`` or ``~/.rally/plugins``
directory (or its subdirectories) or by specifying the path from command lines
as described in the `Rally documentation <http://docs.xrally.xyz/projects/openstack/en/latest/plugins/index.html#placement>`_.
::

  $ mkdir -p ~/.rally/plugins
  $ git clone https://github.com/Doude/rally-contrail-plugin
  Cloning into 'rally-contrail-plugin'...
  remote: Counting objects: 28, done.
  remote: Compressing objects: 100% (19/19), done.
  remote: Total 28 (delta 4), reused 25 (delta 4), pack-reused 0
  Unpacking objects: 100% (28/28), done.
  Checking connectivity... done.
  $ cd

Activate the Rally python environment and add ``contrail-api-cli`` python library
dependency:
::

  $ source ~/rally/bin/activate
  (rally)$ pip install git+https://github.com/eonpatapon/contrail-api-cli
  Collecting git+https://github.com/eonpatapon/contrail-api-cli
  Cloning https://github.com/eonpatapon/contrail-api-cli to /tmp/pip-lWkGU4-build
  ...

Then create a new deployment with the ``contrail`` Credential (you probably need
to edit the sample file accordingly to your deployment):
::

  (rally)$ rally deployment create --name my-contrail-cluster --filename ~/.rally/plugins/rally-contrail-plugin/samples/deployments/contrail.json
  2017-06-15 14:54:13.142 14259 WARNING rally.task.validation [-] Plugin 'NeutronSecurityGroup.create_and_list_security_group_rules' uses validator 'rally.task.validation.required_services' which is deprecated in favor of 'required_services' (it should be used via new decorator 'rally.common.validation.add') in Rally v0.10.0.
  2017-06-15 14:54:14.257 14259 INFO rally.common.plugin.discover [-] Loading plugins from directories /home/cloud/.rally/plugins/*
  2017-06-15 14:54:14.259 14259 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/__init__.py
  2017-06-15 14:54:14.259 14259 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/__init__.py
  2017-06-15 14:54:14.409 14259 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/credential.py
  2017-06-15 14:54:14.410 14259 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/scenario.py
  2017-06-15 14:54:14.410 14259 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/cfg/__init__.py
  2017-06-15 14:54:14.410 14259 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/scenarios/__init__.py
  2017-06-15 14:54:14.411 14259 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/scenarios/config/utils.py
  2017-06-15 14:54:14.411 14259 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/scenarios/config/__init__.py
  2017-06-15 14:54:14.414 14259 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/scenarios/config/virtual_network.py
  2017-06-15 14:54:14.415 14259 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/context/projects.py
  2017-06-15 14:54:14.415 14259 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/context/__init__.py
  2017-06-15 14:54:14.416 14259 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/context/existing_users.py
  2017-06-15 14:54:14.471 14259 INFO rally.deployment.engines.existing [-] Save deployment 'my-contrail-cluster' (uuid=544a0fd6-63ee-48fb-8087-cc5114f2af68) with 'contrail' platform.
  +--------------------------------------+---------------------+---------------------+------------------+--------+
  | uuid                                 | created_at          | name                | status           | active |
  +--------------------------------------+---------------------+---------------------+------------------+--------+
  | 544a0fd6-63ee-48fb-8087-cc5114f2af68 | 2017-06-15T14:54:14 | my-contrail-cluster | deploy->finished |        |
  +--------------------------------------+---------------------+---------------------+------------------+--------+
  Using deployment: 544a0fd6-63ee-48fb-8087-cc5114f2af68

And run scenario test like samples provided:
::

  (rally)$ rally task start ~/.rally/plugins/rally-contrail-plugin/samples/plugins/scenario/test_create_and_list_virtual_networks.yaml
  2017-06-15 15:01:18.394 14506 WARNING rally.task.validation [-] Plugin 'NeutronSecurityGroup.create_and_list_security_group_rules' uses validator 'rally.task.validation.required_services' which is deprecated in favor of 'required_services' (it should be used via new decorator 'rally.common.validation.add') in Rally v0.10.0.
  2017-06-15 15:01:19.496 14506 INFO rally.common.plugin.discover [-] Loading plugins from directories /home/cloud/.rally/plugins/*
  2017-06-15 15:01:19.499 14506 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/__init__.py
  2017-06-15 15:01:19.499 14506 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/__init__.py
  2017-06-15 15:01:19.649 14506 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/credential.py
  2017-06-15 15:01:19.650 14506 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/scenario.py
  2017-06-15 15:01:19.651 14506 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/cfg/__init__.py
  2017-06-15 15:01:19.651 14506 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/scenarios/__init__.py
  2017-06-15 15:01:19.652 14506 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/scenarios/config/utils.py
  2017-06-15 15:01:19.653 14506 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/scenarios/config/__init__.py
  2017-06-15 15:01:19.656 14506 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/scenarios/config/virtual_network.py
  2017-06-15 15:01:19.657 14506 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/context/projects.py
  2017-06-15 15:01:19.657 14506 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/context/__init__.py
  2017-06-15 15:01:19.658 14506 INFO rally.common.plugin.discover [-]      Loaded module with plugins: /home/cloud/.rally/plugins/rally-contrail-plugin/contrail/context/existing_users.py
  --------------------------------------------------------------------------------
  Preparing input task
  --------------------------------------------------------------------------------

  Task is:
  ---
    config.create_and_list_virtual_networks:
      -
        args:
          virtual_network_create_args: {}
        runner:
          type: "constant"
          times: 100
          concurrency: 10
        context:
          projects:
            projects: 10
        sla:
          failure_rate:
            max: 0

  Task syntax is correct :)
  Running Rally version 0.9.1~dev348
  --------------------------------------------------------------------------------
  Task  e202bc32-9aea-4201-8967-dd27e96d2a50: started
  --------------------------------------------------------------------------------

  Benchmarking... This can take a while...

  To track task status use:

          rally task status
          or
          rally task detailed

  Using task: e202bc32-9aea-4201-8967-dd27e96d2a50
  2017-06-15 15:01:19.767 14506 INFO rally.task.engine [-] Task e202bc32-9aea-4201-8967-dd27e96d2a50 | Starting:  Task validation.
  2017-06-15 15:01:19.778 14506 INFO rally.task.engine [-] Task e202bc32-9aea-4201-8967-dd27e96d2a50 | Starting:  Task validation of syntax.
  2017-06-15 15:01:19.787 14506 INFO rally.task.engine [-] Task e202bc32-9aea-4201-8967-dd27e96d2a50 | Completed: Task validation of syntax.
  2017-06-15 15:01:19.787 14506 INFO rally.task.engine [-] Task e202bc32-9aea-4201-8967-dd27e96d2a50 | Starting:  Task validation of required platforms.
  2017-06-15 15:01:19.792 14506 INFO rally.task.engine [-] Task e202bc32-9aea-4201-8967-dd27e96d2a50 | Completed: Task validation of required platforms.
  2017-06-15 15:01:19.792 14506 INFO rally.task.engine [-] Task e202bc32-9aea-4201-8967-dd27e96d2a50 | Starting:  Task validation of semantic.
  ...
  +----------------------------------------------------------------------------------------------------------------------------------+
  |                                                       Response Times (sec)                                                       |
  +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
  | Action                        | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
  +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
  | config.create_virtual_network | 0.198     | 0.227        | 0.287        | 0.291        | 0.319     | 0.235     | 91.0%   | 100   |
  | config.list_virtual_networks  | 0.0       | 0.0          | 0.0          | 0.0          | 0.0       | 0.0       | 100.0%  | 91    |
  | total                         | 0.199     | 0.228        | 0.288        | 0.292        | 0.32      | 0.236     | 91.0%   | 100   |
  +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+

  Load duration: 10.228579
  Full duration: 16.453507

  HINTS:
  * To plot HTML graphics with this data, run:
          rally task report 53b385d7-b496-4172-b7d9-84ab03cd6d0a --out output.html

  * To generate a JUnit report, run:
          rally task report 53b385d7-b496-4172-b7d9-84ab03cd6d0a --junit --out output.xml

  * To get raw JSON output of task results, run:
          rally task results 53b385d7-b496-4172-b7d9-84ab03cd6d0a

That command outputs a summary of the test result and you could also `generate
and compare reports <http://docs.xrally.xyz/projects/openstack/en/latest/task/index.html#html-reports>`_.
