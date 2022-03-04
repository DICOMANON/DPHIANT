
import requests
import json
orthancApi = requests.Session()
# orthancApi.headers.update({"Authorization": self.authorizationToken})
instanceId = "b2f4e23c-9d5b3bfe-81474211-0e6af1a9-c976169e"
url = "http://localhost:8044/instances/" + instanceId + "/content/0010-0010"
# print(self.authorizationToken)
# page = orthancApi.get(url, headers = {"Authorization": self.authorizationToken})
page = orthancApi.get(url, auth=('demo', 'demo'))
print(page.text)

'''
    "0010-0010",
    "0010-0020",
    "0010-0030",
    "0010-0040",
'''