# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
from django.db.models import Q, F
#from services.oaibbu.models import OAIBBUService, OAIBBUTenant
from synchronizers.new_base.modelaccessor import *
from synchronizers.new_base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible

parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

class SyncOAIBBUTenant(SyncInstanceUsingAnsible):

    # Used by XOSObserver : sync_steps to determine dependencies.
    provides = [OAIBBUTenant]

    # The Tenant that is synchronized.
    observes = OAIBBUTenant

    requested_interval = 0

    # Name of the ansible playbook to run.
    template_name = "oaibbutenant_playbook.yaml"

    # Path to the SSH key used by Ansible.
    service_key_name = "/opt/xos/configurations/mcord/mcord_private_key"

    def __init__(self, *args, **kwargs):
        super(SyncOAIBBUTenant, self).__init__(*args, **kwargs)

    def get_network_id(self, network_name):
        network = Network.objects.filter(name=network_name).first()

        return network.id

    def get_instance_object(self, instance_id):
        instance = Instance.objects.filter(id=instance_id).first()

        return instance

    def get_information(self, o):
        fields = {}

        # not sure if this part need to modify, need to check further network setting

        collect_network = [
           {'name': 'HSS_PRIVATE_IP', 'net_name': 'vhss_network'}
        ]

        instance = self.get_instance_object(o.instance_id)

        for data in collect_network:
            network_id = self.get_network_id(data['net_name'])
            port = filter(lambda x: x.network_id == network_id, instance.ports.all())[0]
            fields[data['name']] = port.ip

        return fields

    def get_extra_attributes(self, o):
        fields = self.get_information(o)

        return fields
