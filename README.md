# viewserver-python-example

Example project demonstrating how to use `viewserver-python` to build
Python-driven ViewServer operators.

## Prerequisites

- Python 3.9+
- [GitHub CLI](https://cli.github.com) (`gh`) authenticated with access to
  `viewserver-rust/viewserver-core` (private repo)

## Setup

### Quick start (recommended)

```
quickstart.bat
```

This will create a virtual environment, install dependencies, download the
`viewserver-python` wheel from the private GitHub release using `gh`, and
run the interactive config wizard.

### Manual install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pandas pyarrow numpy

# Download wheel from private repo (requires gh auth)
gh release download python-v0.1.0-164c267 --repo viewserver-rust/viewserver-core --pattern "*win_amd64.whl" --dir .venv\wheels --clobber
pip install .venv\wheels\viewserver_python-*.whl

# Run config wizard
python setup_config.py
```

### Install from local wheel (development)

```bash
# Build viewserver-python from source (requires Rust toolchain)
cd ../viewserver-core3/viewserver-python
maturin build --release

# Install pure-Python deps, then the local wheel
cd ../viewserver-python-example
pip install pandas pyarrow numpy
pip install ../viewserver-core3/target/wheels/viewserver_python-*.whl
```

## Usage

Edit `config.json` to point at your ReportingEngine (or run `quickstart.bat`
to configure it interactively), then:

```bash
python -m viewserver_example.node --config config.json
```

### Run tests

```bash
pytest
```

## Project structure

```
viewserver-python-example/
├── quickstart.bat              # First-time setup script
├── setup_config.py             # Interactive config wizard
├── pyproject.toml              # Project dependencies
├── config.json                 # ViewServer node config (edit for your environment)
├── src/
│   └── viewserver_example/
│       ├── __init__.py
│       ├── node.py             # ViewServer node with Python operators
│       └── transforms.py       # Reusable transform functions
└── tests/
    └── test_transforms.py      # Unit tests for transforms
```

## How it works

The `viewserver-python` package is a native Rust extension (built with PyO3/maturin)
that embeds the ViewServer engine. It's distributed as a pre-built `.whl` file
attached to GitHub Releases — no Rust toolchain needed on the consumer machine.

The GitHub Actions workflow in the main repo builds the wheel, runs tests, and
creates a release with the wheel attached on every merge to `main`.
