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

Then create a new deployment with the ``contrail`` Credential:

    $ rally deployment create --name my-contrail-cluster --filemame samples/deployments/contail.json

And run scenario test as samples provided:

    $ rally task start samples/plugins/scenario/test_create_and_list_virtual_networks.yaml

That command outputs a summary of the test result and you could also `generate
and compare reports <http://docs.xrally.xyz/projects/openstack/en/latest/task/index.html#html-reports>`_.