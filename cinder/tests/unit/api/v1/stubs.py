# Copyright 2010 OpenStack Foundation
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

import datetime
import iso8601

from cinder import exception as exc
from cinder import objects
from cinder.tests.unit import fake_volume

FAKE_UUID = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
FAKE_UUIDS = {}

DEFAULT_VOL_TYPE = "vol_type_name"


def stub_volume(id, **kwargs):
    volume = {
        'id': id,
        'user_id': 'fakeuser',
        'project_id': 'fakeproject',
        'host': 'fakehost',
        'size': 1,
        'availability_zone': 'fakeaz',
        'attached_mode': 'rw',
        'status': 'fakestatus',
        'migration_status': None,
        'attach_status': 'attached',
        'bootable': False,
        'name': 'vol name',
        'display_name': 'displayname',
        'display_description': 'displaydesc',
        'updated_at': datetime.datetime(1900, 1, 1, 1, 1, 1,
                                        tzinfo=iso8601.iso8601.Utc()),
        'created_at': datetime.datetime(1900, 1, 1, 1, 1, 1,
                                        tzinfo=iso8601.iso8601.Utc()),
        'snapshot_id': None,
        'source_volid': None,
        'volume_type_id': '3e196c20-3c06-11e2-81c1-0800200c9a66',
        'volume_admin_metadata': [{'key': 'attached_mode', 'value': 'rw'},
                                  {'key': 'readonly', 'value': 'False'}],
        'volume_type': fake_volume.fake_db_volume_type(name=DEFAULT_VOL_TYPE),
        'volume_attachment': [],
        'multiattach': False,
        'readonly': 'False'}

    volume.update(kwargs)
    if kwargs.get('volume_glance_metadata', None):
        volume['bootable'] = True
    if kwargs.get('attach_status') == 'detached':
        del volume['volume_admin_metadata'][0]
    return volume


def stub_volume_create(self, context, size, name, description, snapshot,
                       **param):
    vol = stub_volume('1')
    vol['size'] = size
    vol['display_name'] = name
    vol['display_description'] = description
    vol['source_volid'] = None
    try:
        vol['snapshot_id'] = snapshot['id']
    except (KeyError, TypeError):
        vol['snapshot_id'] = None
    vol['availability_zone'] = param.get('availability_zone', 'fakeaz')
    return vol


def stub_volume_api_create(self, context, *args, **kwargs):
    vol = stub_volume_create(self, context, *args, **kwargs)
    return fake_volume.fake_volume_obj(context, **vol)


def stub_volume_create_from_image(self, context, size, name, description,
                                  snapshot, volume_type, metadata,
                                  availability_zone):
    vol = stub_volume('1')
    vol['status'] = 'creating'
    vol['size'] = size
    vol['display_name'] = name
    vol['display_description'] = description
    vol['bootable'] = False
    vol['availability_zone'] = 'cinder'
    return vol


def stub_volume_update(self, context, *args, **param):
    pass


def stub_volume_delete(self, context, *args, **param):
    pass


def stub_volume_get(self, context, volume_id, viewable_admin_meta=False):
    if viewable_admin_meta:
        return stub_volume(volume_id)
    else:
        volume = stub_volume(volume_id)
        del volume['volume_admin_metadata']
        return volume


def stub_volume_get_notfound(self, context,
                             volume_id, viewable_admin_meta=False):
    raise exc.VolumeNotFound(volume_id)


def stub_volume_get_db(context, volume_id):
    if context.is_admin:
        return stub_volume(volume_id)
    else:
        volume = stub_volume(volume_id)
        del volume['volume_admin_metadata']
        return volume


def stub_volume_api_get(self, context, volume_id, viewable_admin_meta=False):
    vol = stub_volume(volume_id)
    return fake_volume.fake_volume_obj(context, **vol)


def stub_volume_api_get_all_by_project(self, context, marker, limit,
                                       sort_keys=None, sort_dirs=None,
                                       filters=None,
                                       viewable_admin_meta=False,
                                       offset=None):
    vol = stub_volume_get(self, context, '1',
                          viewable_admin_meta=viewable_admin_meta)
    vol_obj = fake_volume.fake_volume_obj(context, **vol)
    return objects.VolumeList(objects=[vol_obj])


def stub_volume_get_all(context, search_opts=None, marker=None, limit=None,
                        sort_keys=None, sort_dirs=None, filters=None,
                        viewable_admin_meta=False, offset=None):
    return [stub_volume(100, project_id='fake'),
            stub_volume(101, project_id='superfake'),
            stub_volume(102, project_id='superduperfake')]


def stub_volume_get_all_by_project(self, context, marker, limit,
                                   sort_keys=None, sort_dirs=None,
                                   filters=None,
                                   viewable_admin_meta=False, offset=None):
    return [stub_volume_get(self, context, '1', viewable_admin_meta=True)]


def stub_snapshot(id, **kwargs):
    snapshot = {'id': id,
                'volume_id': 12,
                'status': 'available',
                'volume_size': 100,
                'created_at': None,
                'display_name': 'Default name',
                'display_description': 'Default description',
                'project_id': 'fake',
                'snapshot_metadata': []}

    snapshot.update(kwargs)
    return snapshot


def stub_snapshot_get_all(context, filters=None, marker=None, limit=None,
                          sort_keys=None, sort_dirs=None, offset=None):
    return [stub_snapshot(100, project_id='fake'),
            stub_snapshot(101, project_id='superfake'),
            stub_snapshot(102, project_id='superduperfake')]


def stub_snapshot_get_all_by_project(context, project_id, filters=None,
                                     marker=None, limit=None, sort_keys=None,
                                     sort_dirs=None, offset=None):
    return [stub_snapshot(1)]


def stub_snapshot_update(self, context, *args, **param):
    pass


def stub_service_get_all_by_topic(context, topic, disabled=None):
    return [{'availability_zone': "zone1:host1", "disabled": 0}]


def stub_volume_type_get(context, id, *args, **kwargs):
    return {'id': id,
            'name': 'vol_type_name',
            'description': 'A fake volume type',
            'is_public': True,
            'projects': [],
            'extra_specs': {},
            'created_at': None,
            'deleted_at': None,
            'updated_at': None,
            'deleted': False}
