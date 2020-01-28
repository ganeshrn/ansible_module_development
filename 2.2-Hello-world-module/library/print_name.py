# Write an Ansible module to print full name as task output.
# The module should have first, middle (optional), last as arguments
# and should return complete name in module result.
# If first or last arguments is not given as input from user
# module should throw an error.

from ansible.module_utils.basic import AnsibleModule


def main():
    """ main entry point for module execution
    """
    required_together = [['first', 'last']]
    mutually_exclusive = [['name', 'aggregate']]

    argument_spec = dict(
        first=dict(type='str', required=True),
        middle=dict(type='str'),
        last=dict(type='str')
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           mutually_exclusive=mutually_exclusive,
                           supports_check_mode=True)

    result = {}
    first = module.params['first']
    middle = module.params['middle']
    last = module.params['last']

    if middle:
        full_name = first + ' ' + middle + ' ' + last
    else:
        full_name = first + ' ' + last

    result['stdout'] = full_name
    result['msg'] = "Name is %s" % full_name

    module.exit_json(**result)


if __name__ == "__main__":
    main()
