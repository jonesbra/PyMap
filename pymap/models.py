"""Representation of Netbox Data Models."""

import json
import random
import requests
import time
import urllib


class NetboxTransport():
    """Define the transport mechanism between script and Netbox API."""
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def post(self, obj):
        """Post the object to Netbox instance."""
        headers = {'Authorization': 'Token {}'.format(self.token)}
        print(obj.json_repr())
        response = requests.post(self.url + obj.post_url, json=obj.dict_repr(), headers=headers)
        print(response.text)
        for key, value in response.json().items():
            if key not in CLASS_MAPPER:
                obj.repr[key] = value
        print('Request Complete')
        print('\n\n')
        time.sleep(5)
        obj.alive = True


class NetboxObject():
    """Representation of a Netbox object."""
    def __init__(self):
        self.alive = False  # Whether or not the device is "alive" on Netbox

        self.repr = dict()

        # Make sure all arguments that represent other Netbox objects are correct type.
        for field in self.__dict__:
            if field in CLASS_MAPPER:
                assert isinstance(getattr(self, field), CLASS_MAPPER[field])

    def json_repr(self):
        """Get a JSON representation of the object."""
        response = dict()
        for key, value in self.repr.items():
            if key in CLASS_MAPPER:
                # Must get the ID value of other Netbox Objects.
                response[key] = self.repr.get(key).get_id()
            else:
                response[key] = value
        return json.dumps(response)

    def dict_repr(self):
        """Get a dict representation of the object."""
        return json.loads(self.json_repr())

    def get_id(self):
        """Get the Netbox ID of the object."""
        if self.alive:
            return self.dict_repr().get('id')
        raise Exception('Can not get id of object.')


class Device(NetboxObject):
    """Class representation of a Netbox Device."""
    def __init__(self, hostname, device_type, device_role, site, primary_ip):
        super().__init__()
        self.repr = {
            'name': hostname,
            'display_name': hostname,
            'device_type': device_type,
            'device_role': device_role,
            'site': site,
            'primary_ip': primary_ip
        }

        self.post_url = '/dcim/devices/'
        self.get_url = '/dcim/devices/{id}'


class DeviceType(NetboxObject):
    """Class representation of a Netbox Device Type."""
    def __init__(self, name, manufacturer, model):
        super().__init__()
        self.repr = {
            'display_name': name,
            'slug': name,
            'manufacturer': manufacturer,
            'model': model
        }

        self.post_url = '/dcim/device-types/'
        self.get_url = '/dcim/device-types/{id}'


class DeviceRole(NetboxObject):
    """Class representation of a Netbox Device Role."""
    def __init__(self, name):
        super().__init__()
        self.repr = {
            'name': name,
            'slug': name,
            'color': "%06x" % random.randint(0, 0xFFFFFF)
        }

        self.post_url = '/dcim/device-roles/'
        self.get_url = '/dcim/device-roles/{id}'


class Site(NetboxObject):
    """Class representation of a Netbox Site."""
    def __init__(self, name, description):
        super().__init__()
        self.repr = {
            'name': name,
            'slug': name,
            'description': description
        }

        self.post_url = '/dcim/sites/'
        self.get_url = '/dcim/sites/{id}'


class Manufacturer(NetboxObject):
    """Class representation of a Netbox Manufacturer."""
    def __init__(self, name):
        super().__init__()
        self.repr = {
            'name': name,
            'slug': name
        }

        self.post_url = '/dcim/manufacturers/'
        self.get_url = '/dcim/manufacturers/{id}'


CLASS_MAPPER = {
    'device_type': DeviceType,
    'device_role': DeviceRole,
    'site': Site,
    'manufacturer': Manufacturer
}
