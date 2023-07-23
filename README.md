# Livebox Utils
Scripts that use the livebox undocumented API to perform operations on an Orange Livebox.

This will be used for home automation.

Configuration is handled via a *.env* file that requires:
- **LIVEBOX_IP**: Your livebox IP
- **LIVEBOX_PASSWORD**: Your livebox admin password
- **DEVICE_MAC_ADDRESS**: Your personnal device mac address that will be used in some scripts (e.g. disabling wifi when not at home)

Note: the email address might be prompted in the GUI but in reality, the *admin* username is used anyway.
