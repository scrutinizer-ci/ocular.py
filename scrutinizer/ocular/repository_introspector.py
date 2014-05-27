# coding: utf-8

from subprocess import check_output
import re


class RepositoryIntrospector:
    def __init__(self, repository_dir):
        self.dir = repository_dir

    def get_current_revision(self):
        return check_output(['git', 'rev-parse', 'HEAD'], cwd=self.dir).strip()

    def get_current_parents(self):
        output = check_output(['git', 'log', '--pretty=%P', '-n1', 'HEAD'], cwd=self.dir).strip()

        if output == "":
            return []

        return output.split(b' ')

    def get_repository_name(self):
        output = check_output(['git', 'remote', '-v'], cwd=self.dir).decode('ascii')

        patterns = [
            '^origin\s+(?:git@|(?:git|https?)://)([^:/]+)(?:/|:)([^/]+)/([^/\s]+?)(?:\.git)?(?:\s|\n)',
            '^[^\s]+\s+(?:git@|(?:git|https?)://)([^:/]+)(?:/|:)([^/]+)/([^/\s]+?)(?:\.git)?(?:\s|\n)',
        ]

        for pattern in patterns:
            match = re.search(pattern, output, re.MULTILINE)
            if match is not None:
                return self.get_repository_type(match.group(1)) + "/" + match.group(2) + "/" + match.group(3)

        raise Exception("Could not determine repository. Please pass the '--repository' option.")

    def get_repository_type(self, host):
        if host == "github.com":
            return "g"
        elif host == "bitbucket.org":
            return "b"

        raise Exception("Unknown host " + host)