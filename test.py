#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
project = 'HSS/5G/citool'
url = "https://gerrit.ericsson.se/#/admin/projects/{}/access".format(project)
post_data = {}

r2 = requests.get("https://gerrit.ericsson.se/#/admin/projects/3pp/3pp_config/access".format(project))
print(r2.content)
# r = requests.post(url, data=post_data, headers={'Content-Type': 'application/json'})
# print(r.status_code)
# print(r.text)
