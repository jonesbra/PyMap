"""Representation of Netbox Data Models."""

import json
import random
import requests
import time
import urllib


class NetboxTransport():
    """Define the transport mechanism between script and Netbox API."""
    def __init__(self, url, token):
        print('- Creating Netbox Transport object with URL: ' + url)
        self.url = url
        self.token = token
        self.headers = {
            'Authorization': 'Token {}'.format(self.token),
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def post(self, obj):
        """Post the object to Netbox instance."""
        print('- Issuing POST: ' + self.url + obj.api_route)
        print('\tData:')
        print(obj.dict_repr())
        print('\n')
        response = requests.post(self.url + obj.api_route, json=obj.dict_repr(),
                                 headers=self.headers)
        print('Response:')
        print(response.json())
        print('\n')
        for key, value in response.json().items():
            if key not in CLASS_MAPPER:
                obj.repr[key] = value
        time.sleep(3)
        obj.alive = True

    def get(self, obj):
        """Get the object's URL from Netbox instance."""
        print('- Issuing GET: ' + self.url + obj.api_route)
        response = requests.get(self.url + obj.api_route, headers=self.headers)
        print('Response:')
        print(response.json())
        return response


class NetboxObject():
    """Representation of a Netbox object."""
    def __init__(self, transport, representation, api_route):
        print('\n- Creating Netbox object: ' + type(self).__name__)
        self.transport = transport
        self.repr = representation
        self.api_route = api_route
        self.alive = False  # Whether or not the device is "alive" on Netbox

        # Make sure all arguments that represent other Netbox objects are correct type.
        for field in self.__dict__:
            if field in CLASS_MAPPER:
                assert isinstance(getattr(self, field), CLASS_MAPPER[field])

        self.validate_alive() # Determine if the object is already alive on Netbox

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

    def validate_alive(self):
        """Determine if device is already alive on Netbox."""
        print('- Determining if {} object already lives on Netbox.'.format(type(self).__name__))
        response = self.transport.get(self)
        if isinstance(response.json().get('results'), list):
            # Determine if all object properties already exist in some object in response.
            for response_obj in response.json().get('results'):
                print('Comparing response with self')
                print('Response: ')
                print(response_obj)
                print('\n')
                print('Self:')
                print(self.dict_repr())
                print('\n')
                if all(item in response_obj.items() for item in self.dict_repr().items()):
                    print('- Self is a subset of response.')
                    self.repr = response_obj
                    self.alive = True
                else:
                    print('- Self is NOT a subset of response.')
        if not self.alive:
            print('- Object isnt currently alive on Netbox.')
            self.transport.post(self)


class Device(NetboxObject):
    """Class representation of a Netbox Device."""
    def __init__(self, transport, hostname, device_type, device_role, site, primary_ip):
        representation = {
            'name': hostname,
            'display_name': hostname,
            'device_type': device_type,
            'device_role': device_role,
            'site': site,
            'primary_ip': primary_ip
        }
        super().__init__(transport, representation, '/dcim/devices/')


class DeviceType(NetboxObject):
    """Class representation of a Netbox Device Type."""
    def __init__(self, transport, name, manufacturer, model):
        representation = {
            'display_name': name,
            'slug': name,
            'manufacturer': manufacturer,
            'model': model
        }
        super().__init__(transport, representation, '/dcim/device-types/')


class DeviceRole(NetboxObject):
    """Class representation of a Netbox Device Role."""
    def __init__(self, transport, name):
        representation = {
            'name': name,
            'slug': name,
            'color': "%06x" % random.randint(0, 0xFFFFFF)
        }
        super().__init__(transport, representation, '/dcim/device-roles/')


class Site(NetboxObject):
    """Class representation of a Netbox Site."""
    def __init__(self, transport, name, description):
        representation = {
            'name': name,
            'slug': name,
            'description': description
        }
        super().__init__(transport, representation, '/dcim/sites/')


class Manufacturer(NetboxObject):
    """Class representation of a Netbox Manufacturer."""
    def __init__(self, transport, name):
        representation = {
            'name': name,
            'slug': name
        }
        super().__init__(transport, representation, '/dcim/manufacturers/')


CLASS_MAPPER = {
    'device_type': DeviceType,
    'device_role': DeviceRole,
    'site': Site,
    'manufacturer': Manufacturer
}
