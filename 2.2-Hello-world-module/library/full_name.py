# Write an Ansible print_name module to print full name as task output.
# 1) The module should have first, middle (optional), last as arguments
# 2) Should return complete name in module result.
# 3) If first or last arguments is not received as input from user module should throw an error.

from ansible.module_utils.basic import AnsibleModule


def main():
    """ main entry point for module execution
    """
    required_together = [['first', 'last']]

    argument_spec = dict(
        first=dict(type='str', required=True),
        middle=dict(type='str'),
        last=dict(type='str')
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           required_together=required_together,
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
