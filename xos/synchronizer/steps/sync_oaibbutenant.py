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

    def get_oaibbuservice(self, o):
        if not o.owner:
            return None

        oaibbuservice = OAIBBUService.objects.filter(id=o.owner.id)

        if not oaibbuservice:
            return None

        return oaibbuservice[0]

    # Gets the attributes that are used by the Ansible template but are not
    # part of the set of default attributes.
    def get_extra_attributes(self, o):
        fields = {}
        fields['tenant_message'] = o.tenant_message
        oaibbuservice = self.get_oaibbuservice(o)
        fields['service_message'] = oaibbuservice.service_message

        if o.foreground_color:
            fields["foreground_color"] = o.foreground_color.html_code

        if o.background_color:
            fields["background_color"] = o.background_color.html_code

        images=[]
        for image in o.embedded_images.all():
            images.append({"name": image.name,
                           "url": image.url})
        fields["images"] = images

        return fields

    def delete_record(self, port):
        # Nothing needs to be done to delete an oaibbuservice; it goes away
        # when the instance holding the oaibbuservice is deleted.
        pass
