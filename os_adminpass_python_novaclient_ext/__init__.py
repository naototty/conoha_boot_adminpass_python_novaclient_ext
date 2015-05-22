# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
admin Password extension
"""

from novaclient import utils
from novaclient.v1_1 import servers
from novaclient.v1_1 import shell

API_ADMIN_PASS = "OS-DCF:adminPass"

# This function was removed from python-novaclient, so we are defining it here
# So the add_args() function will work again.

def add_arg(f, *args, **kwargs):
    """Bind CLI arguments to a shell.py `do_foo` function."""

    if not hasattr(f, 'arguments'):
        f.arguments = []

    # NOTE(sirp): avoid dups that can occur when the module is shared across
    # tests.
    if (args, kwargs) not in f.arguments:
        # Because of the semantics of the decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        f.arguments.insert(0, (args, kwargs))

def add_args():
    add_arg(shell.do_boot,
        '--admin-password',
        default=None,
        metavar='<your_input_root_admin_password>',
        help="When you setup root(admin) password for OS to primary boot disk."
             " This overrides the value inherited from image.")


def bind_args_to_resource_manager(args):
    def add_admin_password(args):
        return dict(admin_password=args.admin_password)

    utils.add_resource_manager_extra_kwargs_hook(
            shell.do_boot, add_admin_password)


def add_modify_body_hook():
    def modify_body_for_create(body, **kwargs):
        admin_password = kwargs.get('admin_password')
        if admin_password:
            ## disk_config = disk_config.upper()

            # if admin_password in ('AUTO', 'MANUAL'):
            if not admin_password == '':
                #body["server"][API_DISK_CONFIG] = disk_config
                body["server"][API_ADMIN_PASS] = admin_password
            else:
                raise Exception("Unrecognized admin_password '%s'" % admin_password)

    servers.ServerManager.add_hook(
            'modify_body_for_create', modify_body_for_create)


def __pre_parse_args__():
    add_args()


def __post_parse_args__(args):
    bind_args_to_resource_manager(args)
    add_modify_body_hook()
