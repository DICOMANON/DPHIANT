
import requests
import json
orthancApi = requests.Session()
# orthancApi.headers.update({"Authorization": self.authorizationToken})
instanceId = "dd03786b-6cc667d1-a65fa0e9-34101126-6f82ca59"
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