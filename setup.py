from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        err_no = pytest.main(self.test_args)
        exit(err_no)

setup(
    name='scrutinizer-ocular',
    version='1.0.0',
    packages=['scrutinizer.ocular'],
    url='http://github.com/scrutinizer-ci/ocular.py',
    license='MIT',
    author='Scrutinizer',
    author_email='support@scrutinizer-ci.com',
    description='Reports Python code coverage data to scrutinizer-ci.com',
    entry_points={
        'console_scripts': [
            'ocular = scrutinizer.ocular.app:main',
        ],
    },
    install_requires=['coverage>=3.6', 'requests>=1.0.0', 'argparse>=1.0.0'],
    cmdclass={'test': PyTest},
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
