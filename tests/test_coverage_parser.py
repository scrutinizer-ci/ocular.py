# coding: utf-8

import unittest
from scrutinizer.ocular.coverage_parser import CoverageParser


class CoverageParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = CoverageParser()

    def test_parse_coverage(self):
        xml_data = self.parser.parse('tests/res/sample-coverage', None)
        self.assertNotEqual('', xml_data)
        self.assertGreater(0, xml_data.find('{scrutinizer_project_base_path}'))
