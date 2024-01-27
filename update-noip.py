#!/usr/bin/env python

import requests
import datetime
import os
from time import sleep
import re

def print_config(config_file_properties):
    for i in config_file_properties["required"]:
        print("'" + i + "': " + "'" + config_file_properties["required"][i] + "'")

def parse_config(config_string):
    config_key_values = {}
    for line_num, prop in enumerate(config_string.split("\n")):
        if re.match(r" *$", prop) or prop == "" or prop == "\n":
            continue
        prop = re.sub("\n", "", prop)
        key_prop = prop.split("=")[0]
        key_prop = re.sub(" ", "", key_prop)
        try:
            value_prop = prop.split("=")[1]
        except:
            print("Invalid syntax on line '" + str(line_num) + "'. Missing equals for key-value pair.")
            exit()
        value_prop = re.sub(" ", "", value_prop)
        config_key_values[key_prop] = value_prop
    return config_key_values

def define_config_vars(config_key_pairs):
    config_vars = {
        "required": {
            "email": "",
            "hostname": "",
            "username": "",
            "password": "",
            "ip_resolver": ""
            }
        }
    for prop in config_key_pairs:
        if prop == "email":
            config_vars["required"]["email"] = config_key_pairs[prop]
        elif prop == "hostname":
            config_vars["required"]["hostname"] = config_key_pairs[prop]
        elif prop == "username":
            config_vars["required"]["username"] = config_key_pairs[prop]
        elif prop == "password":
            config_vars["required"]["password"] = config_key_pairs[prop]
        elif prop == "ip-resolver":
            config_vars["required"]["ip_resolver"] = config_key_pairs[prop]
        else:
            print("Unknown value '" + prop + "'.")
            exit()
    return config_vars

def check_required(config_vars):
    for i in config_vars["required"]:
        if config_vars["required"][i] == "":
            print("Required key '" + i + "' is missing.")
            exit()



# Check if config file exists
try:
    with open("config", "r") as f:
        CONFIG_FILE = f.read();
except:
    print("No file called 'config' found in the current directory. Please create one.")
    exit()

# Parse each line of the config
config_key_values = parse_config(CONFIG_FILE)

# Variables to be used
config_vars = define_config_vars(config_key_values)

# Check if the minimum amount of variables are filled
check_required(config_vars)

header = {
        "User-Agent": "python-requests/" + requests.__version__ + " " + config_vars["required"]["email"]
}

ip_resolver = config_vars["required"]["ip_resolver"]
no_ip_host = config_vars["required"]["hostname"]
no_ip_user = config_vars["required"]["username"]  # DDNS Key Username, Email, or Account Username
no_ip_pass = config_vars["required"]["password"]  # DDNS Key Password, or Account Password
cred_format = no_ip_user + ":" + no_ip_pass

while True:
    setup = False
    curr_time = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
    try:
        curr_ip = str(requests.get(ip_resolver, headers = header).content.decode("UTF-8"))
        print("Current IP: " + curr_ip)
    except:
        log_msg = "\n[" + curr_time + "]: Error. Cannot resolve. Either DNS is configured incorrectly, there's no internet connectivity, or '" + ip_resolver + "' is down."
        with open("noip-log.txt", "a") as logs:
            logs.write(log_msg)
        print("Cannot connect to retrieve ip.")
        sleep(60)
        continue
    try:
        with open("noip-previous-ip.txt", "r") as old_ip:
            prev_ip = re.sub("\n", "", old_ip.read())
    except:
        prev_ip = ""
        setup = True
    if curr_ip != prev_ip:
        print("IP has changed.")
        with open("noip-previous-ip.txt", "w") as ip_log:
            ip_log.write(curr_ip)
        no_ip_url = "https://" + cred_format + "@dynupdate.no-ip.com/nic/update?hostname=" + no_ip_host + "&myip=" + curr_ip
        print("URL for GET Requests: " + no_ip_url)
        no_ip_response = re.sub("\n", "", str(requests.get(no_ip_url, headers = header).content.decode("UTF-8")))
        print(no_ip_response)
        # Check response code
        if no_ip_response.split(" ")[0] == "nochg" and not setup:
            log_msg = "\n[" + curr_time + "]: Warning. No change reported by No-IP but found IP has changed from local records. Current IP reported by No-IP is " + no_ip_response.split(" ")[1] + ". Current IP locally found is " + curr_ip + ". Check and see if No-IP is reporting the current IP correctly and check if the program is saving the IP to file correctly and that it is being read correctly."
            with open("noip-log.txt", "a") as logs:
                logs.write(log_msg)
            sleep(300)
        elif no_ip_response.split(" ")[0] == "nochg" and setup:
            log_msg = "\n[" + curr_time + "]: No change reported by No-IP. Current IP reported by No-IP is " + no_ip_response.split(" ")[1] + ". Current IP locally found is " + curr_ip + "."
            with open("noip-log.txt", "a") as logs:
                logs.write(log_msg)
            sleep(300)
        elif no_ip_response.split(" ")[0] == "good":
            log_msg = "\n[" + curr_time + "]: IP updated. Current IP was changed from " + prev_ip + " from recorded file to " + no_ip_response.split(" ")[1] + ". Current IP reported by system is " + curr_ip + "."
            with open("noip-log.txt", "a") as logs:
                logs.write(log_msg)
            sleep(900)
        elif no_ip_response.split(" ")[0] == "nohost":
            log_msg = "\n[" + curr_time + "]: Error. No host found. Check to make sure hostname is valid or that it has not expired."
            with open("noip-log.txt", "a") as logs:
                logs.write(log_msg)
            break
        elif no_ip_response.split(" ")[0] == "badauth":
            log_msg = "\n[" + curr_time + "]: Error. Wrong username/password. Check to make sure if account credentials/DDNS Keys have been changed. Check if email has changed."
            with open("noip-log.txt", "a") as logs:
                logs.write(log_msg)
            break
        elif no_ip_response.split(" ")[0] == "badagent":
            log_msg = "\n[" + curr_time + "]: Error. Client has been disabled due to bad user agent. Fix the User-Agent string before trying again."
            with open("noip-log.txt", "a") as logs:
                logs.write(log_msg)
            break
        elif no_ip_response.split(" ")[0] == "!donator":
            log_msg = "\n[" + curr_time + "]: Error. The GET request sent is requesting a premium feature. Change this program to accept features only from the free tier."
            with open("noip-log.txt", "a") as logs:
                logs.write(log_msg)
            break
        elif no_ip_response.split(" ")[0] == "abuse":
            log_msg = "\n[" + curr_time + "]: Error. The client is likely either blocked or the account is banned. Contact No-IP for further information."
            with open("noip-log.txt", "a") as logs:
                logs.write(log_msg)
            break
        elif no_ip_response.split(" ")[0] == "911":
            log_msg = "\n[" + curr_time + "]: Error. Something's wrong with No-IP. Check back later."
            with open("noip-log.txt", "a") as logs:
                logs.write(log_msg)
            break
        else:
            log_msg = "\n[" + curr_time + "]: Error. Unfamiliar response code. Testing is required. Check the response code given by No-IP. The response code is '" + no_ip_response + "'."
            with open("noip-log.txt", "a") as logs:
                logs.write(log_msg)
            break
    else:
        print("No change to IP")
        log_msg = "\n[" + curr_time + "]: No change. Current IP is " + curr_ip + "."
        with open("noip-log.txt", "a") as logs:
            logs.write(log_msg)
        sleep(300)
