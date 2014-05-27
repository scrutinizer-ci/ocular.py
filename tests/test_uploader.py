# coding: utf-8

import unittest
from scrutinizer.ocular.uploader import Uploader, UploadFailedException


class UploaderTest(unittest.TestCase):
    def test_uploads_coverage(self):
        uploader = Uploader('https://scrutinizer-ci.com/api', 'g/schmittjoh/metadata', 'abcdef')
        uploader.upload('py-cc', 'abcdef')

    def test_raises_exception_when_upload_fails(self):
        uploader = Uploader('https://scrutinizer-ci.com/api', 'g/schmittjoh/metadabcata', 'abcdef')

        try:
            uploader.upload('py-cc', 'abcdef')
            self.fail("Exception was expected.")
        except UploadFailedException as e:
            self.assertEqual(404, e.response.status_code, e.response.text)

