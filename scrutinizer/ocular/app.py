# coding: utf-8

import argparse
import os
from scrutinizer.ocular.coverage_parser import CoverageParser
from scrutinizer.ocular.repository_introspector import RepositoryIntrospector
from scrutinizer.ocular.uploader import Uploader, UploadFailedException


def main():
    App().run()

class App:
    def __init__(self):
        self.introspector = RepositoryIntrospector(os.getcwd)

    def run(self):
        args = self.parse_args()

        parser = CoverageParser()

        repository_name = self.parse_repository_name(args.repository)
        revision = self.parse_revision(args.revision)
        uploader = Uploader(
            api_url=args.api_url,
            repository=repository_name,
            revision=revision,
            parents=self.parse_parents(args.parents),
            access_token=args.access_token
        )

        xml_data = parser.parse(args.data_file, args.config_file)

        try:
            print("Uploading code coverage for '" + repository_name + "' and revision '" + revision + "'... ")
            uploader.upload(
                data_format='py-cc',
                data=xml_data
            )
            print("Done!\n")
        except UploadFailedException as e:
            print("Oops, an error occurred:\n" + e.response.text)
            exit(1)

    def parse_parents(self, arg_parents):
        if arg_parents is not None:
            return arg_parents.split(b',')

        return self.introspector.get_current_parents()

    def parse_revision(self, arg_revision):
        if arg_revision is not None:
            return arg_revision

        return self.introspector.get_current_revision()

    def parse_repository_name(self, arg_repository):
        if arg_repository is not None:
            return arg_repository

        return self.introspector.get_repository_name()

    def validate_args(self, args):
        if not os.path.isfile(args.data_file):
            print("Error: The coverage data file '" + args.data_file + "' does not exist.")
            exit(1)

        if args.config_file is not None and not os.path.isfile(args.config_file):
            print("Error: The config file '" + args.config_file + "' does not exist.")
            exit(1)

        if os.path.isfile(".coveragerc"):
            args.config_file = ".coveragerc"

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Uploads code coverage information')
        parser.add_argument('--data-file', type=str, help='The coverage data file', default='.coverage')
        parser.add_argument('--config-file', type=str, default=None, help='The coverage config file')
        parser.add_argument('--api-url', default='https://scrutinizer-ci.com/api', type=str)
        parser.add_argument('--access-token', default=None, type=str)
        parser.add_argument('--repository', default=None, type=str)
        parser.add_argument('--revision', default=None, type=str)
        parser.add_argument('--parents', default=None, type=str)
        parser.add_argument('--format', default='py-cc', type=str)

        args = parser.parse_args()
        self.validate_args(args)

        return args
