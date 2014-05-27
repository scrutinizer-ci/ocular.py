# coding: utf-8

import base64
import json
import requests


class Uploader:
    def __init__(self, api_url, repository, revision, parents=[], access_token=None):
        self.api_url = api_url
        self.repository = repository
        self.revision = revision
        self.parents = parents
        self.access_token = access_token

    def upload(self, data_format, data):
        json_data = json.dumps({
            'revision': self.revision,
            'parents': self.parents,
            'coverage': {
                'format': data_format,
                'data': base64.standard_b64encode(data.encode('utf-8')).decode('ascii')
            }
        })

        post_url = self.api_url + '/repositories/' + self.repository + '/data/code-coverage'
        if self.access_token is not None:
            post_url += '?access_token=' + self.access_token

        response = requests.post(
            url=post_url,
            headers={'Content-Type': 'application/json'},
            data=json_data
        )

        if response.status_code >= 300 or response.status_code < 200:
            raise UploadFailedException(response)


class UploadFailedException(Exception):
    def __init__(self, response):
        self.response = response