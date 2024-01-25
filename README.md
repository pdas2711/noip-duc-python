---
geometry: margin=1in
---

# No-IP DUC in Python

This is a DUC (Dynamic Update Client) for No-IP implemented in Python. It makes use of No-IP's RESTful APIs that allow you to update a hostname from your account. It is simple enough where you can update your No-IP hostnames using Curl. This Python script is designed to be run as a daemon and keep watch whenever your IP changes. You can do that by creating a service using your init system (e.g. systemd, openrc, etc.).

*NOTE: Make sure this script isn't behind a VPN or firewall, or else the wrong IP address will be pushed to your No-IP account.*

## Setup

A couple strings need to be edited near the beginning of the script. These are:

- `USER_AGENT_CONTACT` - An email address to use as part of the user agent when making GET requests to No-IP. This is in compliance to their guidelines when defining a user agent.
- `HOSTNAME` - This is your hostname or hostnames (comma-separated field and no spaces when updating more than 1 hostname).
- `USERNAME` - This is the username for your account. You can use your email or the username you you made after the initial account setup.
- `PASSWORD` - This is the password to your account.

**IMPORTANT NOTE** for username/password credentials: It is recommended to use DDNS Keys instead of your account login credentials since the DDNS Keys are only used with updating your hostname. This makes these keys discardable and keeps your account dashboard from being accessed in the event where your DDNS Keys are compromised. You can setup your DDNS Keys in when viewing your list of active hostnames in your account dashboard before setting up this script. Make note of the password since it will only be shown *once*. Afterwards, use the DDNS Key credentials in-place of your account credentials for the `USERNAME` and `PASSWORD` field in the script.
