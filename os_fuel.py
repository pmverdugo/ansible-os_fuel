#!/usr/bin/python
# coding=utf-8

# Copyright (c) 2017, Pedro Verdugo <pmverdugo at dit.upm.es>
# Copyright (c) 2017 Grupo de Internet de Nueva Generación (GING), ETSIT, UPM
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {'status': [''],
                    'supported_by': '',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: os_fuel
short_description: Manages an OpenStack Fuel environment
version_added: "2.2"
author: "Pedro Verdugo"
description:
   - Manages an OpenStack Fuel environment.
options:
   action:
     description:
        - Action to be performed by the fuel cli.
     required: true
   env:
     description:
        - Environment to deploy the action in.
     required: false
     default: false
'''

RETURN = '''
os_fuel:
    description: Dictionary describing the fuel state.
    returned: On success when I(state) is 'present'.
    type: dictionary
    contains:
        env:
            description: Environment ID.
            type: string
            sample: "1"
        status:
            description: A string with the execution output
            returned: success
            type: string
'''


def main():
    argument_spec = dict(
        action=dict(default='list', choices=['list']),
        env=dict(required=False),
    )
    module = AnsibleModule(argument_spec)
    action = module.params['action']
    env = module.params['env']
    fuel_cmd = module.get_bin_path('fuel', True)
    result = {
        'env': env,
        'changed': False,
        'status': {},
    }
    try:
        (rc, out, err) = module.run_command("%s %s --env %s" % (fuel_cmd, action, env))
        if rc != 0:
            module.fail_json(msg='failure %d during fuel execution: %s' % (rc, err))
        else:
            result['changed'] = True
            result['status'] = out
        module.exit_json(msg=result)
    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
