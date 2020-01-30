#!/usr/bin/python
# Copyright: (c) 2020, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
module: user_info
short_description: Get User information from Flask-JWT server
description:
    - Get user id from Flask-JWT server
version_added: "2.10"
author:
    - Abhijeet Kasurde (@Akasurde)
'''

RETURN = '''
info:
    description: User metadata
    type: dict
    returned: success
    sample: {
        "user_id": 123,
    }
'''

EXAMPLES = '''
- name: Check if GitHub pull request is closed or not
  user_info:
  register: r

- name: Take action depending upon pr status
  debug:
    msg: Do something when pr 23642 is open
  when: r.info
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection


def main():
    argument_spec = dict()
    module = AnsibleModule(argument_spec=argument_spec)
    connection = Connection(module._socket_path)

    url = "/api/v1/private"
    ret, data = connection.send_request(url, {}, method='GET')
    module.exit_json(info=data)


if __name__ == '__main__':
    main()
