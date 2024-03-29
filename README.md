# textract-cli

[![PyPI](https://img.shields.io/pypi/v/textract-cli.svg)](https://pypi.org/project/textract-cli/)
[![Changelog](https://img.shields.io/github/v/release/simonw/textract-cli?include_prereleases&label=changelog)](https://github.com/simonw/textract-cli/releases)
[![Tests](https://github.com/simonw/textract-cli/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/textract-cli/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/textract-cli/blob/master/LICENSE)

CLI for running files through AWS Textract

## Installation

Install this tool using `pip`:
```bash
pip install textract-cli
```
## Usage

For help, run:
```bash
textract-cli --help
```
You can also use:
```bash
python -m textract_cli --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd textract-cli
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
