# coding: utf-8

import tempfile
import coverage
import os


class CoverageParser:
    def parse(self, coverage_file, config_file):
        coverage_data = coverage.coverage(data_file=coverage_file, config_file=config_file)
        coverage_data.load()

        xml_report_file = tempfile.NamedTemporaryFile()
        coverage_data.xml_report(outfile=xml_report_file.name)
        xml_report = open(xml_report_file.name).read()
        xml_report_file.close()

        return xml_report.replace(self.get_base_dir(), "{scrutinizer_project_base_path}")

    def get_base_dir(self):
        cur_dir = os.getcwd()

        while True:
            if os.path.isdir(cur_dir + "/.git"):
                return cur_dir

            cur_dir = os.path.dirname(cur_dir)
            if cur_dir == "":
                raise Exception("Repository base directory was not found.")