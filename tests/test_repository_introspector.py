# coding: utf-8

import tempfile
import unittest
from subprocess import call, check_output
from scrutinizer.ocular.repository_introspector import RepositoryIntrospector


class RepositoryIntrospectorTest(unittest.TestCase):
    def setUp(self):
        if not hasattr(tempfile, 'TemporaryDirectory'):
            self.skipTest("TemporaryDirectory() is not available.")

        self.repository_dir = tempfile.TemporaryDirectory()
        self.introspector = RepositoryIntrospector(self.repository_dir.name)
        call(['git', 'init'], cwd=self.repository_dir.name)

        f = open(self.repository_dir.name + '/foo', 'w')
        f.write("foobar\n")
        f.close()

        call(['git', 'add', 'foo'], cwd=self.repository_dir.name)
        call(['git', 'commit', '-m', '"Adds foo"'], cwd=self.repository_dir.name)
        self.first_revision = check_output(['git', 'rev-parse', 'HEAD'], cwd=self.repository_dir.name).strip()

        f = open(self.repository_dir.name + '/bar', 'w')
        f.write("BAAAARRRRRR\n")
        f.close()

        call(['git', 'add', 'bar'], cwd=self.repository_dir.name)
        call(['git', 'commit', '-m', '"Adds bar"'], cwd=self.repository_dir.name)
        self.second_revision = check_output(['git', 'rev-parse', 'HEAD'], cwd=self.repository_dir.name).strip()

        call(['git', 'remote', 'add', 'origin', 'git@github.com:scrutinizer-ci/ocular.py'], cwd=self.repository_dir.name)

    def tearDown(self):
        self.repository_dir.cleanup()

    def test_get_current_revision(self):
        self.assertEqual(self.second_revision, self.introspector.get_current_revision())

    def test_get_current_parents(self):
        self.assertEqual([self.first_revision], self.introspector.get_current_parents())

    def test_get_repository_name(self):
        self.assertEqual('g/scrutinizer-ci/ocular.py', self.introspector.get_repository_name())
