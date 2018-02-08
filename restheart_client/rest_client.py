import os

import requests

# local connection hack fix
os.environ['no_proxy'] = '127.0.0.1,localhost'


class RESTAPIClient:
    def __init__(self, ip, port):
        """
        REST API client

        :param ip: IP of server
        :type ip: str
        :param port: port of server
        :type port: int
        """
        self.ip = ip
        self.port = port
        self.url = 'http://{}:{}'.format(ip, port)

    def get(self, path, headers):
        return requests.get(self.url + path, headers=headers)

    def post(self, path, headers, content):
        return requests.post(self.url + path, headers=headers, data=content)

    def put(self, path, headers, content):
        return requests.put(self.url + path, headers=headers, data=content)

    def delete(self, path, headers):
        return requests.delete(self.url + path, headers=headers)
