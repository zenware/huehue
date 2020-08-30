import urllib3
import logging
import json
from decouple import config
import decouple
import sys
import time
# TODO: SSDP instead of polling outside for the hue bridge ip


logging.captureWarnings(True)

http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)


def hue_request_username(bridge_ip, identifier):
    PAYLOAD = {
        "devicetype": identifier
    }
    API_ENDPOINT = f"https://{bridge_ip}/api"
    r = http.request(
        'POST',
        API_ENDPOINT,
        body=json.dumps(PAYLOAD).encode('utf-8'),
        headers={'Content-Type': 'application/json'})

    data = json.loads(r.data.decode('utf-8'))[0]
    if "error" in data:
        print(data)
        if data["error"]["type"] == 101:
            # TODO: Colorama this red.
            print("Press the Link Button First")
            sys.exit(1)
        raise ValueError
    return data["success"]["username"]



def hue_request_bridge_ip():
    # TODO: Add Error Handling
    HUE_API_DISCOVERY = 'https://discovery.meethue.com/'
    r = http.request('GET', HUE_API_DISCOVERY)

    data = json.loads(r.data.decode('utf-8'))[0]

    return data['internalipaddress']



def hue_get_all_data(config):
    r = http.request(
        'GET',
        config['API_ROOT'])
    data = json.loads(r.data.decode('utf-8'))
    # Top Level keys are API Endpoints
    return data

"""
TODO: Implement Modules for the following.
lights
groups
config
schedules
scenes
rules
sensors
resourceLinks
"""


def hue_list_api_endpoints(config):
    # ['lights', 'groups', 'config', 'schedules', 'scenes', 'rules', 'sensors', 'resourcelinks']
    return hue_get_all_data(config).keys()


def turn_all_lights_off(config):
    LIGHTS_API = f"{config['API_ROOT']}/lights"
    
    r = http.request('GET',
        LIGHTS_API)
    lights_data = json.loads(r.data.decode('utf-8'))
    OFF_PAYLOAD = {
        "on": False
    }
    for num in lights_data.keys():
        print(f"Attempting to turn off light {num}")
        LIGHTS_STATE_API = f"{LIGHTS_API}/{num}/state"
        r = http.request('PUT',
            LIGHTS_STATE_API,
            body=json.dumps(OFF_PAYLOAD).encode('utf-8'),
            headers={'Content-Type': 'application/json'})

def toggle_light(config, light):
    LIGHTS_API = f"{config['API_ROOT']}lights/{light}"
    
    r = http.request('GET',
        LIGHTS_API)
    light_data = json.loads(r.data.decode('utf-8'))
    
    TOGGLE_PAYLOAD = json.dumps({ "on": not light_data["state"]["on"] }).encode('utf-8')
    r = http.request('PUT',
        f"{LIGHTS_API}/state",
        body=TOGGLE_PAYLOAD,
        headers={'Content-Type': 'application/json'})


def hue_adjust_all_lights(config, payloads):
    LIGHTS_API = f"{config['API_ROOT']}lights"
    
    r = http.request('GET',
        LIGHTS_API)
    lights_data = json.loads(r.data.decode('utf-8'))
    # {"on":true, "sat":254, "bri":254,"hue":10000}
    for payload in payloads:
        for num in lights_data:  # .keys()?
            print(f"Adjusting light {num} with payload {payload}")
            LIGHTS_STATE_API = f"{LIGHTS_API}/{num}/state"
            r = http.request('PUT',
                LIGHTS_STATE_API,
                body=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'})


def hue_rainbow_all_lights(config):
    """TODO: Convert to setting colorloop"""
    payloads = ({"hue": hue} for hue in range(65535))
    hue_adjust_all_lights(config, payloads)


def hue_adjust_lights(config, lights, payloads, delay=0.1):
    """
    TODO: The lights are off-sync even at 1/10th of a second. Is there a better way to update them all?
    
    TODO: There should be a payload analyzer that validates payloads.
    For instance, the 'effect' state can only be either 'none' or 'colorloop'
    """
    for payload in payloads:
        for light in lights:
            time.sleep(delay)
            #print(f"Sending {payload} to light {light}")
            API_LIGHTS_STATE = f"lights/{light}/state"
            r = http.request('PUT',
                f"{config['API_ROOT']}{API_LIGHTS_STATE}",
                body=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'})
            # Sometimes I don't get data back here...
            # data = json.loads(r.data.decode('utf-8'))
            #print(f'Light {light} responded with {data}')


def config_write_option(key, value):
    # TODO: Add Debug Logging
    with open(".env", "a") as f:
        f.write(f"{key}={value}\n")


def config_get_username(bridge_ip, app_id):
    try:
        HUE_USERNAME = config('HUE_USERNAME')
    except decouple.UndefinedValueError:
        HUE_USERNAME = hue_request_username(bridge_ip, app_id)
        config_write_option('HUE_USERNAME', HUE_USERNAME)
        print(f"Stored Username in config: {HUE_USERNAME}")
    return HUE_USERNAME


def config_get_bridge_ip():
    try:
        HUE_BRIDGE_IP = config('HUE_BRIDGE_IP')
    except decouple.UndefinedValueError:
        HUE_BRIDGE_IP = hue_request_bridge_ip()
        config_write_option('HUE_BRIDGE_IP', HUE_BRIDGE_IP)
    return HUE_BRIDGE_IP


def modular_range(start, stop, step):
    """Generator that goes forever, restarting at start after it passes stop."""
    i = start
    while True:
        if i > stop:
            i = i % stop
        yield i
        i += step


def config_get():
    """Builds and returns a config object"""
    config = {
        'ip': config_get_bridge_ip(),
    }
    config['username'] = config_get_username(config['ip'], "huehue#zenware")
    config['API_ROOT'] = f"https://{config['ip']}/api/{config['username']}/"
    return config


config = config_get()
print(f"Local Hue IP is: {config['ip']}")
print(f"CLIP API Debugger URL is: https://{config['ip']}/debug/clip.html")


bedroom_lights = [1, 2, 4]
living_room_lights = [5, 6]
if __name__=='__main__':
    # TODO: Configure "Actions" -- Multi-Part Transitions
    # TODO: Configure "Sensors" -- IP/WebRequest Sensors
    # TODO: Turn this into a "Debug log level"
    #print(hue_get_all_data(local_bridge, HUE_USERNAME))
    #turn_all_lights_off(local_bridge, HUE_USERNAME)
    #hue_adjust_all_lights(local_bridge, HUE_USERNAME, {'on': True})
    #hue_rainbow_all_lights(local_bridge, HUE_USERNAME)

    # {"on":true, "sat":254, "bri":254,"hue":10000}
    # TODO: Transition Time: https://developers.meethue.com/develop/application-design-guidance/watch-that-transition-time/
    try: 
        hue_adjust_lights(
            config,
            living_room_lights,
            # EACH COMPONENT OF STATE INCREASES LATENCY
            #https://developers.meethue.com/develop/application-design-guidance/hue-system-performance/
            #({'on': True, 'sat': 254, 'bri': 254, 'hue': hue} for hue in modular_range(0, 65535, 4096)),
            ({'hue': hue, 'transitiontime': 0} for hue in modular_range(0, 65535, 4096)),
            #[{'effect': 'none'}],
            delay=0.01
        )
    except KeyboardInterrupt:
        print("Thanks for playing")
