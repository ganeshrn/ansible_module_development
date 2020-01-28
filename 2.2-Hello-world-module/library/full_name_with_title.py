# Extend Ansible print_name module to print full name with title as task output.
# 1) Add a new argument title
# 2) The accepted values of title are Mr, Mrs, Ms.
# 3) The title argument and middle argument should be mutually exculsive, that is if
#    user inputs both title and middle argument module should throw an error.

from ansible.module_utils.basic import AnsibleModule


def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        title=dict(type='str', choices=["Mr", "Mrs", "Ms"]),
        first=dict(type='str', required=True),
        middle=dict(type='str'),
        last=dict(type='str')
    )

    required_together = [['first', 'last']]
    mutually_exclusive = [['title', 'middle']]

    module = AnsibleModule(argument_spec=argument_spec,
                           required_together=required_together,
                           mutually_exclusive=mutually_exclusive)

    result = {}
    title = module.params['title']
    first = module.params['first']
    middle = module.params['middle']
    last = module.params['last']

    if middle:
        full_name = first + ' ' + middle + ' ' + last
    else:
        full_name = first + ' ' + last

    if title:
        full_name = title + ' ' + full_name

    result['stdout'] = full_name
    result['msg'] = "Name is %s" % full_name

    module.exit_json(**result)


if __name__ == "__main__":
    main()
