# No-IP DUC in Python

This is a DUC (Dynamic Update Client) for No-IP implemented in Python. It makes use of No-IP's RESTful APIs that allow you to update a hostname from your account. It is simple enough where you can update your No-IP hostnames using Curl. This Python script is designed to be run as a daemon and keep watch whenever your IP changes. You can do that by creating a service using your init system (e.g. systemd, openrc, etc.).

*NOTE: Make sure this script isn't behind a VPN or proxy, or else the wrong IP address will be pushed to your No-IP account.*

## Setup

A config file is needed that's available in the same directory as the script. Mandatory fields are:

```
email = <YOUR EMAIL>
hostname = <YOUR NO-IP HOSTNAME/HOSTNAMES>
username = <YOUR USERNAME>
password = <YOUR PASSWORD>
ip-resolver = <PUBLIC IP RESOLVER>
```

An explanation of the config fields:

- `email` - An email address to use as part of the user agent when making GET requests to No-IP. This is in compliance to their guidelines when defining a user agent. The email with the user agent will also be used when retrieving your public IP from whatever website you choose. Use an email that can be used to contact you and that you are comfortable sharing.
- `hostname` - This is your hostname or hostnames (comma-separated field and no spaces when updating more than 1 hostname).
- `username` - This is the username for your account. You can use your email or the username you you made after the initial account setup.
- `password` - This is the password to your account.
- `ip-resolver` - This is a website that tells you what your public IP address is. It should return a basic webpage with just your IP address since the script, as of now, doesn't handle webpages with other elements in it. You can use a website like `http://ifconfig.me/ip`.

**IMPORTANT NOTE** for username/password credentials: It is recommended to use DDNS Keys instead of your account login credentials since the DDNS Keys are only used with updating your hostname. This makes these keys discardable and keeps your account dashboard from being accessed in the event where your DDNS Keys are compromised. You can setup your DDNS Keys in when viewing your list of active hostnames in your account dashboard before setting up this script. Make note of the password since it will only be shown *once*. Afterwards, use the DDNS Key credentials in-place of your account credentials for the `USERNAME` and `PASSWORD` field in the script.

Place this script in a folder. You will get two additional files after running it: one holds the public IP it has recorded. This is used to make sure that the script doesn't have to constantly send a request to No-IP when your IP doesn't change. The other file is a log to check if the script is running fine.
