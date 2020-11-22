"""
Tests executable module
"""
import pytest
import argparse

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--smoke-test', action='store_true', help='Run Smoke Tests')
PARSER.add_argument('--keywords', default='test', help='Run tests with keyword')
PARSER.add_argument('--pdb', action='store_true', help='Enable pdb on first failure')
ARGS = PARSER.parse_args()


def main():
    test_folder = 'tests'

    # default pytest args, runs whole test in test_folder
    pytest_args = [test_folder, '-vs', '--junitxml=test.xml', '--cov=./app', '--cov-report=html']

    if ARGS.smoke_test:
        # to execute only smoke
        pytest_args.append('-m smoke')
    if ARGS.keywords:
        # to execute only test containing keyword
        pytest_args.append('-k ' + ARGS.keywords)
    if ARGS.pdb:
        # to enable debugger while testing on local
        pytest_args.append('--pdb')
    print(f"Running tests with following arguments {pytest_args}")
    pytest.main(pytest_args)


if __name__ == "__main__":
    main()