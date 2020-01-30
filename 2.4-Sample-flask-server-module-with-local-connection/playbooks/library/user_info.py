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
short_description: Get user id information
description:
    - View User information for the Flask server.
version_added: "2.10"
options:
    username:
        description:
        - Username for login.
        type: str
        required: True
    password:
        description:
        - Password for the given user.
        type: str
        required: True
    servername:
        description:
        - Name of server
        type: str
    port:
        description:
        - Port to access on server
        type: int
        default: 8042
author:
    - Abhijeet Kasurde (@Akasurde)
'''

RETURN = '''
info:
    description: User metadata
    type: dict
    returned: success
    sample: {
        "user_id": 123
    }
'''

EXAMPLES = '''
- name: Get User
  user_info:
    username: user1
    password: Secret123
  register: r

- name: Take action depending upon user
  debug:
    msg: Do something user exists
  when: r.info is defined
'''

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def main():
    # Create AnsibleModule to accept user data to work on
    module = AnsibleModule(
        argument_spec=dict(
            servername=dict(),
            username=dict(required=True),
            password=dict(required=True, no_log=True),
            port=dict(type=int, default=8042)
        ),
        supports_check_mode=True,
    )

    # Get all user defined parameters
    username = module.params['username']
    password = module.params['password']
    servername = module.params['servername']
    port = module.params['port']

    # Define datastructure to return
    result = dict()

    # Headers for
    headers = {
        'Content-Type': 'application/json',
    }

    # GitHub url to fetch information about PR
    base_url = "http://%s:%s" % (servername, port)

    login_url = "%s/auth" % base_url

    # Use Ansible fetch_url API
    data = json.dumps({
        'username': username,
        'password': password,
    })

    response, info = fetch_url(module, login_url, headers=headers, method='POST', data=data)
    # Sanity check
    if not (200 <= info['status'] < 400):
        if info['status'] == 404:
            module.fail_json(msg="Failed to login")
        module.fail_json(msg="Failed to send request to %s: %s" % (login_url, info['msg']))

    # Get access token from successful login
    user_token = json.loads(response.read())['access_token']

    # Get user details
    headers.update({
        "Authorization": "JWT %s" % user_token
    })

    # Get protected contents
    protected_url = "%s/api/v1/private" % base_url
    response, info = fetch_url(module, protected_url, headers=headers, method='GET')
    # Sanity check
    if not (200 <= info['status'] < 400):
        if info['status'] == 404:
            module.fail_json(msg="Failed to login")
        module.fail_json(msg="Failed to send request to %s: %s" % (login_url, info['msg']))

    user_info = json.loads(response.read())
    # Check if user is running ansible command in check mode or not
    if module.check_mode:
        result.update(changed=True)
    else:
        # Return the pull request information
        result.update(changed=True, info=user_info)

    # Exit module
    module.exit_json(**result)


if __name__ == '__main__':
    main()
