"""Utils for PyMap."""

def get_netmiko_device_type(vendor, operating_system):
    if vendor == 'Cisco' and operating_system == 'IOS':
        response = 'cisco_ios'
    else:
        response = 'cisco_ios'
    return response
