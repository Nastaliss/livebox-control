import requests

class Livebox:

    session = None
    ip = None
    context_id = None

    def __init__(self, password, ip, user="admin"):
        """
        Logs in to the livebox api.
        """
        self.ip = ip

        self.session = requests.Session()
        login_request = None
        login_request = self.session.post(f'http://{ip}/ws', json={
            "service":"sah.Device.Information",
            "method":"createContext",
            "parameters": {
                "applicationName": "webui",
                "username": user,
                "password": password
                }
            },
            headers= {
                "Authorization":  "X-Sah-Login",
            },
            timeout=3,
        )

        login_request.raise_for_status()
        self.context_id = login_request.json()['data']['contextID']

    def _perform_request(self, json_body, timeout_seconds=3):
        """
        Performs all requests to the livebox api except for the login request.
        The Authorization and Content-Type headers seem to be the only mandatory headers.
        Errors will always return a 200 status code, so we have to check the status field in the response.
        """
        request = self.session.post(
            f'http://{self.ip}/ws',
            json=json_body,
            timeout=timeout_seconds,
            headers={
                'Authorization': f'X-Sah {self.context_id}',
                'Content-Type': 'application/x-sah-ws-4-call+json',
            }
        )
        response = request.json()

        if response.get('errors'):
            raise Exception(response['errors'])

        request.raise_for_status() # Might not be useful as observation showed the API always returns a 200 status code

        return response

    def _toggle_wifi(self, status):
        """
        Set the wifi to the given status.
        """
        self._perform_request({
            "service":"NMC.Wifi","method":"set","parameters":{
                "Enable": status,
                "Status": status
            }},

        )

    def disable_wifi(self):
        """
        Disables the wifi.
        """
        self._toggle_wifi(False)

    def enable_wifi(self):
        """
        Enables the wifi.
        """
        self._toggle_wifi(True)

    def wifi_enabled(self):
        """
        Returns True if the wifi is enabled, False otherwise.
        """
        response = self._perform_request({
            "service":"NMC.Wifi","method":"get","parameters":{}
        })
        return response['status']['Status'] and response['status']['Enable'] # No idea why both are needed, might as well use both

    def reboot(self):
        """
        Reboots the livebox.
        """
        self._perform_request({
            "service":"NMC","method":"reboot","parameters":{}
        })

    def _generate_typology(self):
        """
        This method is not used, but it's here for future uses.
        Generates a typology of the network, with all the devices connected to the all the interfaces.
        """
        res = self._perform_request({
            "service":"TopologyDiagnostics","method":"buildTopology","parameters":{"SendXmlFile": False}
        })
        children = res["status"][0]["Children"]
        lan_child = (child for child in children if child["Key"] == "lan").__next__()
        network_interfaces = lan_child["Children"]

        devices = {}
        for interface in network_interfaces:
            if "Children" not in interface:
                continue
            for device in interface["Children"]:
                devices[device["Key"]]={
                    "name": device["Name"],
                    "type": device["DeviceType"],
                }
        print(devices)
        return devices

    def _get_device_info(self, mac_address):
        """
        Gets a specific device's information.
        """
        res = self._perform_request({
            "service": f"Devices.Device.{mac_address}",
            "method":"get","parameters":{}
        })
        return res

    def is_device_connected(self, mac_address):
        """
        Returns True if the device is connected to the wifi, False otherwise.
        """
        return self._get_device_info(mac_address)["status"]["Active"]
