# coding: utf-8

import unittest
from scrutinizer.ocular.coverage_parser import CoverageParser
from scrutinizer.ocular.uploader import Uploader


class IntegrationTest(unittest.TestCase):
    def test_uploads_coverage(self):
        parser = CoverageParser()
        xml_data = parser.parse('tests/res/sample-coverage', None)
        uploader = Uploader('https://scrutinizer-ci.com/api', 'g/schmittjoh/metadata', 'abcdef')
        uploader.upload('py-cc', xml_data)
