Exercise-1
==========

Write an Ansible module
* To install/uninstall apache.
* Start/stop httpd service.
Based on the value of state argument which can be either present or absent

.. note:: The module should be idempotent and support check mode.


Module debugging steps
======================
Run the playbook

.. code::

$ ANSIBLE_KEEP_REMOTE_FILES=1 ansible-playbook test_playbook_apache.yml


Login to remote host

.. code::

$ python <full temporary path>/manage_server.py explode
Module expanded into:
<full temporary path>/debug_dir


Edit module file in temporary location and rerun the module

.. code::

$ python <full temporary path>/manage_server.py execute
