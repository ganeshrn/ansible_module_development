# Write an Ansible module
# 1) To install/uninstall apache.
# 2) Start/stop httpd service.
# Based on the value of state argument which can be either present or absent
# The module should be idempotent and support check module

from ansible.module_utils.basic import AnsibleModule


def handle_present(module, result):
    changed = False
    commands = []

    response = module.run_command('rpm -qi httpd')
    # install httpd
    if "not installed" in response[1]:
        cmd = 'yum install -y httpd'
        if not module.check_mode:
            response = module.run_command(cmd)
        commands.append(cmd)
        changed = True

    # start service
    response = module.run_command('service httpd status')
    if 'inactive' in response[1]:
        cmd = 'service httpd start'
        if not module.check_mode:
            response = module.run_command(cmd)
        commands.append(cmd)
        changed = True

    result['commands'] = commands
    result['changed'] = changed


def handle_absent(module, result):
    changed = False
    commands = []

    response = module.run_command('rpm -qi httpd')

    if 'active (running)' in response[1]:
        cmd = 'service httpd stop'
        if not module.check_mode:
            response = module.run_command(cmd)
        commands.append(cmd)
        changed = True

    if "not installed" not in response[1]:
        cmd = 'yum erase -y httpd'
        if not module.check_mode:
            response = module.run_command(cmd)
        commands.append(cmd)
        changed = True

    result['commands'] = commands
    result['changed'] = changed


def main():
    """ main entry point for module execution
    """

    argument_spec = dict(
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    result = {}

    if module.params['state'] == "present":
        handle_present(module, result)
    else:
        handle_absent(module, result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
