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
module: github_pr_info
short_description: View GitHub Pull request information.
description:
    - View GitHub pull request information for the given repository and organization.
version_added: "2.10"
options:
  repo:
    description:
      - Name of repository from which pull request needs to be retrieved.
    required: true
    type: str
  organization:
    description:
      - Name of the GitHub organization in which the repository is hosted.
    required: true
    type: str
  pull_request:
    description:
      - Pull request number for which information is required.
    required: true
    aliases: ['pr']
    type: str
author:
    - Abhijeet Kasurde (@Akasurde)
'''

RETURN = '''
pull_request_info:
    description: GitHub Pull Request metadata
    type: dict
    returned: success
    sample: {
       "_links": {
                "comments": {
                    "href": "https://api.github.com/repos/ansible/ansible/issues/61006/comments"
                },
                "commits": {
                    "href": "https://api.github.com/repos/ansible/ansible/pulls/61006/commits"
                },
        }
    }
'''

EXAMPLES = '''
- name: Check if GitHub pull request is closed or not
  github_pr:
    organization: ansible
    repo: ansible
    pr: 23642
  register: r

- name: Take action depending upon pr status
  debug:
    msg: Do something when pr 23642 is open
  when: r.pull_request_info.state == 'open'
'''

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def main():
    # Create AnsibleModule to accept user data to work on
    module = AnsibleModule(
        argument_spec=dict(
            organization=dict(required=True),
            repo=dict(required=True),
            pull_request=dict(type='int', required=True, aliases=['pr']),
        ),
        supports_check_mode=True,
    )

    # Get all user defined parameters
    organization = module.params['organization']
    repo = module.params['repo']
    pr = module.params['pull_request']

    # Define datastructure to return
    result = dict()

    # Headers for
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.github.v3+json',
    }

    # GitHub url to fetch information about PR
    url = "https://api.github.com/repos/%s/%s/pulls/%s" % (organization, repo, pr)

    # Use Ansible fetch_url API
    response, info = fetch_url(module, url, headers=headers)
    # Sanity check
    if not (200 <= info['status'] < 400):
        if info['status'] == 404:
            module.fail_json(msg="Failed to find pr %s" % pr)
        module.fail_json(msg="Failed to send request to %s: %s" % (url, info['msg']))

    # Modify response in json format
    gh_obj = json.loads(response.read())

    # Check if user is running ansible command in check mode or not
    if module.check_mode:
        result.update(changed=True)
    else:
        # Return the pull request information
        result.update(changed=True, pull_request_info=gh_obj)

    # Exit module
    module.exit_json(**result)


if __name__ == '__main__':
    main()
